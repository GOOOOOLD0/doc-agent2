"""
extract_structure.py (v2)

第一步:结构层提取,规则驱动,不靠 LLM 猜层级。

改动点(相对上一版):
1. PDF 侧统一改用 fitz(PyMuPDF)的 get_toc(),不再用 pypdf——
   减少库依赖种类,行为更可预测,书签页码本身就是1-indexed,不用
   再额外处理 destination 解析。
2. 新增 docx 支持:不依赖 Word 的"标题样式"(很多文档标题只是加粗
   普通段落,没有正经用 Heading 样式),而是复用和 PDF 书签同一套
   正则规则,直接扫描每个段落的文字判断是不是"章"或"条"标题,
   保证 PDF/DOCX 走同一套分类逻辑,行为一致。
3. structure.json 里新增 position_type 字段(page / paragraph_index),
   下游脚本(chunk_articles.py)按这个字段决定怎么去取内容区间。

用法:
    python extract_structure.py <文档路径,支持.pdf/.docx> <reg_name> <wiki根目录>
"""

import sys
import json
import re
from pathlib import Path


def classify_node(title: str) -> str:
    """规则匹配,不用 LLM:判断是"章"还是"条"。PDF/DOCX共用同一套规则。"""
    if re.match(r"^第\s*[一二三四五六七八九十百]+\s*章", title):
        return "chapter"
    if re.match(r"^第\s*\d+[A-Za-z]?\s*条", title):
        return "article"
    return "other"


def extract_article_id(title: str):
    m = re.match(r"^第\s*(\d+[A-Za-z]?)\s*条", title)
    return m.group(1) if m else None


def extract_from_pdf(path: str, notes: list):
    import fitz
    doc = fitz.open(path)
    toc = doc.get_toc(simple=True)  # [[level, title, page(1-indexed)], ...]
    if not toc:
        notes.append("PDF 未检测到书签/大纲(TOC),无法自动提取结构,需人工核对目录后手动补 structure.json。")
        return [], "page", None

    flat = []
    for level, title, page in toc:
        flat.append({"title": title.strip(), "depth": level - 1, "position": page})
    return flat, "page", doc.page_count


def extract_from_docx(path: str, notes: list):
    import docx
    document = docx.Document(path)
    flat = []
    depth_by_type = {"chapter": 0, "article": 1}
    for idx, para in enumerate(document.paragraphs):
        text = para.text.strip()
        if not text:
            continue
        node_type = classify_node(text)
        if node_type == "other":
            continue
        flat.append({"title": text, "depth": depth_by_type.get(node_type, 1), "position": idx})

    if not flat:
        notes.append(
            "docx 中未通过规则(章/条标题正则)扫描到任何标题段落,"
            "可能该文档标题格式不符合'第X章'/'第X条'的写法,需人工核对后手动补 structure.json。"
        )
    return flat, "paragraph_index", len(document.paragraphs)


def build_structure(flat_items, position_type: str, doc_length):
    for i, node in enumerate(flat_items):
        node["type"] = classify_node(node["title"])
        node["article_id"] = extract_article_id(node["title"]) if node["type"] == "article" else None
        next_position = None
        for j in range(i + 1, len(flat_items)):
            next_position = flat_items[j]["position"]
            break
        if position_type == "page":
            node["end_position"] = (next_position - 1) if next_position else doc_length
        else:  # paragraph_index:区间是左闭右开,end给"下一个标题段落的前一段"
            node["end_position"] = (next_position - 1) if next_position else (doc_length - 1)

    chapters = [n for n in flat_items if n["type"] == "chapter"]
    articles = [n for n in flat_items if n["type"] == "article"]
    return {"position_type": position_type, "all_nodes": flat_items, "chapters": chapters, "articles": articles}


def render_structure_md(structure, reg_name, position_type):
    unit = "页" if position_type == "page" else "段落"
    lines = [f"# {reg_name} 结构树\n", "> 本文件由 extract_structure.py 自动生成,不做人工改写。\n",
             f"> 位置单位: {unit}(position_type = {position_type})\n"]
    for node in structure["all_nodes"]:
        indent = "  " * node["depth"]
        pos_info = f"({unit} {node['position']}-{node['end_position']})"
        marker = {"chapter": "##", "article": "-", "other": "-"}[node["type"]]
        if node["type"] == "chapter":
            lines.append(f"\n{indent}{marker} {node['title']} {pos_info}")
        else:
            lines.append(f"{indent}{marker} {node['title']} {pos_info}")
    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) != 4:
        print("用法: python extract_structure.py <文档路径(.pdf/.docx)> <reg_name> <wiki根目录>")
        sys.exit(1)

    doc_path, reg_name, wiki_root = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    raw_dir = wiki_root / "raw" / "regulations" / reg_name
    raw_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(doc_path).suffix.lower()
    notes = []

    if ext == ".pdf":
        flat_items, position_type, doc_length = extract_from_pdf(doc_path, notes)
    elif ext == ".docx":
        flat_items, position_type, doc_length = extract_from_docx(doc_path, notes)
    else:
        print(f"暂不支持的文件类型: {ext}(目前支持 .pdf / .docx)")
        sys.exit(1)

    structure = build_structure(flat_items, position_type, doc_length)

    notes.append(f"共识别到 {len(structure['chapters'])} 个章、{len(structure['articles'])} 个条。"
                 f"(来源文件类型: {ext}, 位置单位: {'页' if position_type == 'page' else '段落'})")

    (raw_dir / "structure.json").write_text(
        json.dumps(structure, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (raw_dir / "structure.md").write_text(render_structure_md(structure, reg_name, position_type), encoding="utf-8")

    notes_md = f"# {reg_name} 解析记录\n\n" + "\n".join(f"- {n}" for n in notes) + "\n"
    (raw_dir / "parse_notes.md").write_text(notes_md, encoding="utf-8")

    print(f"完成。章: {len(structure['chapters'])}, 条: {len(structure['articles'])}, 位置单位: {position_type}")
    print(f"输出目录: {raw_dir}")


if __name__ == "__main__":
    main()
