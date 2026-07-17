"""
chunk_articles.py (v2)

第二步:原始层文字抽取 + 条款级切块。

相对上一版的改动:

1. 修正"大面积空白误判"问题:
   旧版直接用 cjk字符数/文本总长度 算比例,但 fitz 抽取中文时经常在
   两个汉字中间插入空格(字体字宽/间距导致,不代表原文真的有空格),
   这会把分母(总长度)显著抬高,导致比例被稀释,原本能正常读取的页
   也被误判成"文字层不可靠"送去 OCR。同时,含大面积版式空白、正文
   很少的页(比如章节扉页),因为有效字符样本数太小,单纯看比例波动
   很大,也容易被误判。
   现在改成两步判断:
     a) 先去掉空白字符再算比例(比例更真实);
     b) 有效字符数太少(默认<20)时,不基于比例做判断——这类页本来
        内容就少,直接采用抽取结果,不强行 OCR。
   只有"有一定文字量、但去空白后CJK比例仍然很低"才判定为文字层损坏。

2. 抽取到的文字统一做"字符间空格归一化":只去掉两个中文字符之间的
   空格(fitz/OCR的排版噪声),不动其他任何字符,不影响英文单词间的
   空格、数字和单位之间的空格等真实需要保留空格的地方。

3. 新增 docx 分支:docx 是原生文字格式,直接按段落取文字,不存在
   "文字层可信度"问题,不会走 OCR,method 统一记为 "docx_text"。

用法:
    python chunk_articles.py <文档路径> <reg_name> <wiki根目录> [--articles 1,2,3]
"""

import sys
import json
import re
import argparse
from pathlib import Path


CJK_RE = re.compile(r"[\u4e00-\u9fff]")
INTER_CJK_SPACE_RE = re.compile(r"(?<=[\u4e00-\u9fff])[ \t]+(?=[\u4e00-\u9fff])")

MIN_MEANINGFUL_CHARS = 20  # 有效字符(去空白后)少于这个数,不基于比例判断,直接采用抽取结果
CJK_RATIO_THRESHOLD = 0.05


def normalize_inter_cjk_spaces(text: str) -> str:
    """
    只删除"中文字符-空格-中文字符"里的空格,其余空格(英文单词间、
    数字单位间、标点后)一律保留,不做任何其他改动。
    """
    prev = None
    cur = text
    # 连续多个中文字符间可能有多处空格,循环到不再变化为止
    while prev != cur:
        prev = cur
        cur = INTER_CJK_SPACE_RE.sub("", cur)
    return cur


def cjk_ratio_after_strip(text: str):
    """返回 (去空白后的有效字符数, CJK占比)。"""
    stripped = re.sub(r"\s+", "", text)
    if not stripped:
        return 0, 0.0
    cjk = len(CJK_RE.findall(stripped))
    return len(stripped), cjk / len(stripped)


def extract_page_text_pdf(doc, page_index: int, ocr_lang: str, tessdata_dir: str, notes: list):
    """
    先试 fitz 文字层;仅当"有效字符数足够多,但CJK占比仍然很低"时才走OCR。
    返回 (text, method)。
    """
    page = doc[page_index]
    text = page.get_text()
    meaningful_len, ratio = cjk_ratio_after_strip(text)

    if meaningful_len < MIN_MEANINGFUL_CHARS:
        # 内容本来就少(比如扉页、大面积空白页),不强行OCR,直接采用fitz结果
        return normalize_inter_cjk_spaces(text), "text_layer"

    if ratio >= CJK_RATIO_THRESHOLD:
        return normalize_inter_cjk_spaces(text), "text_layer"

    # 有效字符量够,但CJK占比仍然很低 -> 判定文字层确实损坏,走OCR
    notes.append(
        f"第 {page_index + 1} 页:有效字符数 {meaningful_len},去空白后CJK占比 {ratio:.1%},"
        f"低于阈值 {CJK_RATIO_THRESHOLD:.0%},判定文字层损坏,已切换为 OCR。"
    )
    import fitz  # 延迟导入,避免未用到OCR分支时也强制要求相关依赖
    import pytesseract
    from PIL import Image
    import io
    import os

    pix = page.get_pixmap(dpi=300)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    os.environ["TESSDATA_PREFIX"] = tessdata_dir
    ocr_text = pytesseract.image_to_string(img, lang=ocr_lang)
    return normalize_inter_cjk_spaces(ocr_text), "ocr"


def extract_range_docx(document, start_idx: int, end_idx: int) -> str:
    paras = document.paragraphs[start_idx:end_idx + 1]
    text = "\n".join(p.text for p in paras)
    return normalize_inter_cjk_spaces(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc_path")
    ap.add_argument("reg_name")
    ap.add_argument("wiki_root")
    ap.add_argument("--articles", default=None, help="只处理指定条款号,逗号分隔;不填则处理全部")
    ap.add_argument("--ocr-lang", default="chi_sim")
    ap.add_argument("--tessdata-dir", default="/home/claude/tessdata")
    args = ap.parse_args()

    wiki_root = Path(args.wiki_root)
    raw_dir = wiki_root / "raw" / "regulations" / args.reg_name
    structure_path = raw_dir / "structure.json"
    if not structure_path.exists():
        print(f"未找到 {structure_path},请先运行 extract_structure.py")
        sys.exit(1)

    structure = json.loads(structure_path.read_text(encoding="utf-8"))
    position_type = structure.get("position_type", "page")
    articles = structure["articles"]

    if args.articles:
        wanted = set(args.articles.split(","))
        articles = [a for a in articles if a["article_id"] in wanted]

    chunks_dir = raw_dir / "raw_chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(args.doc_path).suffix.lower()
    notes = []

    if ext == ".pdf":
        import fitz
        doc = fitz.open(args.doc_path)
        for art in articles:
            aid = art["article_id"]
            start, end = art["position"], art["end_position"]
            if start is None or end is None:
                notes.append(f"第{aid}条位置信息缺失,跳过自动切块,需人工处理。")
                continue
            span = end - start + 1
            methods_used = set()
            parts = []
            for p in range(start - 1, end):
                text, method = extract_page_text_pdf(doc, p, args.ocr_lang, args.tessdata_dir, notes)
                methods_used.add(method)
                parts.append(f"--- page {p + 1} ---")
                parts.append(text)
            full_text = "\n".join(parts)
            out_path = chunks_dir / f"{aid}.txt"
            out_path.write_text(full_text, encoding="utf-8")
            if span > 15:
                notes.append(f"第{aid}条跨 {span} 页,超过单条款常规篇幅,建议做款级二次切分。")
            print(f"第{aid}条 ({start}-{end}页, {span}页, 方式:{'/'.join(methods_used)}) -> {out_path}")

    elif ext == ".docx":
        import docx
        document = docx.Document(args.doc_path)
        for art in articles:
            aid = art["article_id"]
            start, end = art["position"], art["end_position"]
            if start is None or end is None:
                notes.append(f"第{aid}条位置信息缺失,跳过自动切块,需人工处理。")
                continue
            full_text = extract_range_docx(document, start, end)
            out_path = chunks_dir / f"{aid}.txt"
            out_path.write_text(full_text, encoding="utf-8")
            print(f"第{aid}条 (段落{start}-{end}, 方式:docx_text) -> {out_path}")

    else:
        print(f"暂不支持的文件类型: {ext}")
        sys.exit(1)

    notes_path = raw_dir / "parse_notes.md"
    existing = notes_path.read_text(encoding="utf-8") if notes_path.exists() else ""
    with_new = existing + "\n\n## chunk_articles.py 追加记录\n\n" + ("\n".join(f"- {n}" for n in notes) if notes else "- 无异常") + "\n"
    notes_path.write_text(with_new, encoding="utf-8")

    print(f"\n完成。原文切块输出目录: {chunks_dir}")
    print(f"解析记录已追加到: {notes_path}")


if __name__ == "__main__":
    main()
