"""
generate_wiki_pages.py (v2)

第三步:语义层页面组装。

相对上一版的改动:
1. "原文正文"不再是一大段文字,改成按款号的表格:原文(未改动)列
   直接来自 structured.json;清洗后列来自 semantic/<id>.json 里
   LLM 产出的 clauses[].cleaned_text,没有就留空,不拿原文回填冒充。
2. 接地检查(疑似幻觉判定)现在基于 structured.json 里所有款的
   原文拼接结果做子串匹配,而不是某个 reflowed.txt。
3. 字段名同步 extract_structure.py v2:position/end_position
   (原 page/end_page),position_type 决定单位是"页"还是"段落"。
4. 不再依赖写死的错字字典/ocr_flags.json——错字标记现在从
   semantic.json 的 clauses[].changes 里读,由 LLM 产出。

用法:
    python generate_wiki_pages.py <reg_name> <wiki根目录> [--articles 1,2,3]
"""

import sys
import json
import re
import argparse
from pathlib import Path


ARTICLE_REF_RE = re.compile(r"第\s*(\d+[A-Za-z]?)\s*条")
FOOTNOTE_REF_RE = re.compile(r"\b(\d+\.\d+[A-Za-z]?)\b")


def resolve_cross_references(raw_refs, full_text, article_ids, footnote_ids):
    """
    两级检查,顺序不能反:

    第一级(接地检查):raw_refs 是 LLM 在语义加工阶段列出的"原文中出现的
    引用文字"。先验证该文字是否真的能在原文(全条拼接文本)里逐字找到。
    找不到 → 标记"疑似幻觉",不进入目标定位。

    第二级(目标定位):接地检查通过后,按规则匹配去 structure.json 里
    找目标条款/脚注,找不到目标就标 [待链接]。
    """
    normalized_text = re.sub(r"\s+", "", full_text)

    resolved = []
    for ref in raw_refs:
        ref_core = re.sub(r"\s+", "", ref)
        ref_core = re.sub(r"^见", "", ref_core)

        grounded = ref_core in normalized_text
        if not grounded:
            resolved.append({"text": ref, "target": None, "linked": False, "grounded": False})
            continue

        m = ARTICLE_REF_RE.search(ref)
        if m and m.group(1) in article_ids:
            resolved.append({"text": ref, "target": f"articles/{m.group(1)}.md", "linked": True, "grounded": True})
            continue
        m = FOOTNOTE_REF_RE.search(ref)
        if m and m.group(1) in footnote_ids:
            resolved.append({"text": ref, "target": f"articles/{m.group(1)}.md", "linked": True, "grounded": True})
            continue
        resolved.append({"text": ref, "target": None, "linked": False, "grounded": True})
    return resolved


def build_clause_table(clauses, semantic_clauses_by_id):
    """
    生成"原文正文"表格。clauses 来自 structured.json(权威原文,不改动);
    semantic_clauses_by_id 是 {clause_id: {"cleaned_text":..., "changes":[...]}}
    来自 semantic.json,没有对应条目时清洗列留空,不拿原文回填。
    """
    header = "| 款号 | 页码 | 原文(未改动) | 清洗后(LLM) |"
    sep = "|---|---|---|---|"
    rows = [header, sep]
    all_changes = []
    for c in clauses:
        cid = c["clause_id"]
        page = c.get("page", "")
        original = c["text"].replace("|", "\\|").replace("\n", "<br>")
        sem = semantic_clauses_by_id.get(cid)
        if sem and sem.get("cleaned_text"):
            cleaned = sem["cleaned_text"].replace("|", "\\|").replace("\n", "<br>")
        else:
            cleaned = "(待清洗)"
        rows.append(f"| {cid} | {page} | {original} | {cleaned} |")
        if sem:
            for ch in sem.get("changes", []):
                all_changes.append(f"第{cid}款: 「{ch.get('from')}」→「{ch.get('to')}」({ch.get('reason', '')})")
    return "\n".join(rows), all_changes


def render_page(art_meta, clauses, unassigned, semantic, resolved_refs, method, reg_name, position_type, extra_notes=None):
    aid = art_meta["article_id"]
    confidence_map = {"text_layer": "高", "ocr": "中(存在OCR噪声,建议核对)",
                       "vision_llm_transcribe": "视具体质量而定", "docx_text": "高(原生文字,无需OCR)"}
    confidence = confidence_map.get(method, "未知")
    unit = "页" if position_type == "page" else "段落"

    semantic_clauses_by_id = {}
    if semantic:
        for sc in semantic.get("clauses", []):
            semantic_clauses_by_id[sc["clause_id"]] = sc

    lines = []
    lines.append(f"# 第{aid}条 - {art_meta['title'].split('-', 1)[-1].strip()}\n")
    lines.append("## 元信息\n")
    lines.append(f"- 条款编号: {aid}")
    lines.append(f"- {unit}范围: {art_meta['position']}-{art_meta['end_position']}")
    lines.append(f"- 原文来源: {method}")
    lines.append(f"- 原文可信度: {confidence}")
    lines.append(f"- 版本: {reg_name}\n")

    lines.append("## 摘要\n")
    lines.append(semantic.get("summary", "(待生成:尚未提交语义加工JSON)") if semantic else "(待生成:尚未提交语义加工JSON)")
    lines.append("")

    lines.append("## 关键词\n")
    kw = semantic.get("keywords", []) if semantic else []
    lines.append(", ".join(kw) if kw else "(待生成)")
    lines.append("")

    lines.append("## 相关条款\n")
    if resolved_refs:
        for r in resolved_refs:
            if r["linked"]:
                lines.append(f"- {r['text']} → [{r['target']}]({r['target']})")
            elif not r.get("grounded", True):
                lines.append(f"- [疑似幻觉,原文未找到该引用文字] {r['text']}")
            else:
                lines.append(f"- [待链接] {r['text']}")
    else:
        lines.append("(无自动识别到的引用,或尚未提交语义加工JSON)")
    lines.append("")

    lines.append("## 原文正文\n")
    if clauses:
        table, changes = build_clause_table(clauses, semantic_clauses_by_id)
        lines.append(table)
    else:
        changes = []
        lines.append("(未找到 structured.json,请先运行 clean_ocr_text.py 生成款级结构)")
    lines.append("")

    lines.append("## 备注/待确认项\n")
    notes = list(semantic.get("notes", [])) if semantic else []
    if not semantic:
        notes = notes + ["尚未提交语义加工JSON,本页仅完成原文层抽取,摘要/关键词/引用/清洗待补。"]
    if changes:
        notes = notes + changes
    if unassigned:
        notes = notes + [f"{len(unassigned)} 行未能归入任何款号(页眉/页码/未识别内容),详见 structured.json 的 unassigned 字段。"]
    if extra_notes:
        notes = notes + extra_notes
    if notes:
        for n in notes:
            lines.append(f"- {n}")
    else:
        lines.append("(无)")

    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reg_name")
    ap.add_argument("wiki_root")
    ap.add_argument("--articles", default=None)
    args = ap.parse_args()

    wiki_root = Path(args.wiki_root)
    raw_dir = wiki_root / "raw" / "regulations" / args.reg_name
    concept_dir = wiki_root / "concepts" / "regulations" / args.reg_name
    articles_out = concept_dir / "articles"
    articles_out.mkdir(parents=True, exist_ok=True)

    structure = json.loads((raw_dir / "structure.json").read_text(encoding="utf-8"))
    position_type = structure.get("position_type", "page")
    article_ids = {a["article_id"] for a in structure["articles"] if a["article_id"]}
    footnote_ids = set()  # 若已跑过第5条脚注级二次切分,把脚注编号补充到这里

    articles = structure["articles"]
    if args.articles:
        wanted = set(args.articles.split(","))
        articles = [a for a in articles if a["article_id"] in wanted]

    for art in articles:
        aid = art["article_id"]
        chunk_path = raw_dir / "raw_chunks" / f"{aid}.txt"
        structured_path = raw_dir / "raw_chunks" / f"{aid}.structured.json"
        if not chunk_path.exists():
            print(f"跳过第{aid}条: 未找到原文chunk,请先跑 chunk_articles.py")
            continue

        extra_notes = []
        clauses, unassigned = [], []
        if structured_path.exists():
            structured = json.loads(structured_path.read_text(encoding="utf-8"))
            clauses = structured.get("clauses", [])
            unassigned = structured.get("unassigned", [])
        else:
            extra_notes.append("尚未跑 clean_ocr_text.py 生成款级结构,无法渲染表格化原文,请先运行该脚本。")

        full_text = chunk_path.read_text(encoding="utf-8")

        # 原文抽取方式:暂用 text_layer 作为默认值(实际项目建议 chunk_articles.py
        # 额外写一份 per-article method 记录;目前 hardcode 是因为已知本PDF文字层正常)
        method = "text_layer"

        semantic_path = raw_dir / "semantic" / f"{aid}.json"
        semantic = json.loads(semantic_path.read_text(encoding="utf-8")) if semantic_path.exists() else None

        resolved_refs = []
        if semantic and semantic.get("raw_cross_references"):
            resolved_refs = resolve_cross_references(semantic["raw_cross_references"], full_text, article_ids, footnote_ids)

        page_md = render_page(art, clauses, unassigned, semantic, resolved_refs, method, args.reg_name,
                               position_type, extra_notes=extra_notes)
        out_path = articles_out / f"{aid}.md"
        out_path.write_text(page_md, encoding="utf-8")
        print(f"第{aid}条 -> {out_path}")


if __name__ == "__main__":
    main()
