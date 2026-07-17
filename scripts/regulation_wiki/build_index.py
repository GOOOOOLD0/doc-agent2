"""
build_index.py

第四步:检索层索引。
- toc_index.md: 按 structure.json 的原文章节结构生成目录索引,
  只对已实际生成 wiki 页面(articles/<id>.md 存在)的条款给出链接,
  未生成的条款如实标注"未处理",不假装已完成。
- topic_index.md: 汇总所有已生成页面的关键词,按关键词聚合条款,
  没有语义JSON(因此没有关键词)的条款不出现在主题索引里,
  而不是用空关键词占位。

用法:
    python build_index.py <reg_name> <wiki根目录>
"""

import sys
import json
import argparse
import re
from pathlib import Path
from collections import defaultdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("reg_name")
    ap.add_argument("wiki_root")
    args = ap.parse_args()

    wiki_root = Path(args.wiki_root)
    raw_dir = wiki_root / "raw" / "regulations" / args.reg_name
    concept_dir = wiki_root / "concepts" / "regulations" / args.reg_name
    articles_dir = concept_dir / "articles"
    index_dir = concept_dir / "index"
    index_dir.mkdir(parents=True, exist_ok=True)

    structure = json.loads((raw_dir / "structure.json").read_text(encoding="utf-8"))

    # ---- toc_index.md ----
    lines = [f"# {args.reg_name} 目录索引\n", "> 自动生成,状态如实反映当前进度,不代表整份法规已处理完。\n"]
    done, total = 0, 0
    for node in structure["all_nodes"]:
        indent = "  " * node["depth"]
        if node["type"] == "chapter":
            lines.append(f"\n{indent}## {node['title']}")
        elif node["type"] == "article":
            total += 1
            aid = node["article_id"]
            page_file = articles_dir / f"{aid}.md"
            if page_file.exists():
                done += 1
                lines.append(f"{indent}- [{node['title']}](../articles/{aid}.md)")
            else:
                lines.append(f"{indent}- {node['title']} `[未处理]`")
    lines.insert(2, f"\n> 处理进度: {done}/{total} 条已生成 wiki 页面。\n")
    (index_dir / "toc_index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---- topic_index.md(按已生成页面的关键词聚合) ----
    topic_map = defaultdict(list)
    for page_file in sorted(articles_dir.glob("*.md")):
        text = page_file.read_text(encoding="utf-8")
        m = re.search(r"## 关键词\s*\n\n(.+)\n", text)
        if not m or m.group(1).strip() == "(待生成)":
            continue
        keywords = [k.strip() for k in m.group(1).split(",") if k.strip()]
        title_m = re.search(r"^# (.+)$", text, re.MULTILINE)
        title = title_m.group(1) if title_m else page_file.stem
        for kw in keywords:
            topic_map[kw].append((page_file.stem, title))

    topic_lines = [f"# {args.reg_name} 主题索引\n", "> 仅汇总已完成语义加工(有关键词)的条款,未生成关键词的条款不在此列。\n"]
    for kw in sorted(topic_map.keys()):
        topic_lines.append(f"\n## {kw}")
        for aid, title in topic_map[kw]:
            topic_lines.append(f"- [{title}](../articles/{aid}.md)")
    (index_dir / "topic_index.md").write_text("\n".join(topic_lines) + "\n", encoding="utf-8")

    print(f"toc_index.md 完成,进度 {done}/{total}")
    print(f"topic_index.md 完成,收录 {len(topic_map)} 个主题关键词")


if __name__ == "__main__":
    main()
