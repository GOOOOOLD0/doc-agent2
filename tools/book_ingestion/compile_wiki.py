"""
compile_wiki.py

第四步：根据 Source Notes 生成正式 Wiki 知识页面，并更新索引。

读取 source_notes/ 目录中的所有 Source Notes，结合结构信息，
为每个 note 生成对应的 Concept Page（概念页面），输出到 wiki/concepts/<topic>/
目录。同时更新 wiki/index.md 和 wiki/log.md。

严格遵循：
- document.yaml.output.concepts_dir（优先）→ 默认 wiki/concepts/<topic>/
- document.yaml 的 version, language, document_type 等元信息
- document.yaml.output 各输出目录配置（优先于 profile.output）
- wiki/SCHEMA.md 的 Concept Page 结构和写作约定

复用：
- scripts/regulation_wiki/generate_wiki_pages.py 的页面生成逻辑
- scripts/regulation_wiki/build_index.py 的索引构建逻辑

用法:
    python compile_wiki.py <document.yaml路径> [--nodes 1,2,3]
"""

import sys
import json
import re
import argparse
import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

import yaml


def resolve_profile_path(doc_config: dict, doc_yaml_dir: Path) -> Path:
    profile_str = doc_config.get("profile", "")
    candidate = doc_yaml_dir / profile_str
    if candidate.exists():
        return candidate
    project_root = doc_yaml_dir.parent.parent.parent.parent
    candidate = project_root / profile_str
    if candidate.exists():
        return candidate
    raise FileNotFoundError(f"无法找到 profile 文件: {profile_str}")


def find_node_by_id(structure: dict, node_id: str) -> Optional[dict]:
    for node in structure.get("all_nodes", []):
        aid = node.get("article_id")
        if aid and str(aid) == node_id:
            return node
    return None


def parse_source_note_frontmatter(source_note_text: str) -> dict:
    """从 Source Note 的 YAML frontmatter 中提取元信息。"""
    m = re.match(r"^---\n(.*?)\n---", source_note_text, re.DOTALL)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def generate_concept_page(
    node: dict,
    source_note_text: str,
    chunk_text: str,
    doc_config: dict,
    profile: dict,
    position_type: str,
    topic: str,
    notes_info: List[dict],
    concepts_dir: Path,
) -> str:
    """
    生成符合 SCHEMA.md Concept Page 规范的 Wiki 页面。
    - 元信息来自 document.yaml
    - 摘要来自 source note（LLM 生成）
    - 核心内容来自 cleaned chunk 文件
    """
    node_id = node.get("article_id") or node.get("title", "unknown")
    node_title = node.get("title", "")

    # 严格从 document.yaml 读取元信息
    doc_title = doc_config.get("title", "")
    doc_type = doc_config.get("document_type", "")
    doc_version = doc_config.get("version", "")
    doc_id = doc_config.get("doc_id", "")
    language = doc_config.get("language", "zh-CN")
    today = datetime.date.today().isoformat()

    unit = "页" if position_type == "page" else "段落"
    start_pos = node.get("position", "?")
    end_pos = node.get("end_position", "?")
    source_location = f"第{start_pos}{unit} 至 第{end_pos}{unit}"

    # 从 source note 中提取各部分内容
    # 摘要（build_source_notes 使用"## 一句话总结"）
    summary_match = re.search(
        r"## (?:摘要|一句话总结)\s*\n+(.+?)(?=\n## |\Z)",
        source_note_text, re.DOTALL
    )
    summary = summary_match.group(1).strip() if summary_match else "(待生成)"

    # 核心内容 — 从 chunk 文件读取（不再从 source note）
    # 清理 chunk 中的 frontmatter
    core_content = chunk_text.strip() if chunk_text else "(待补充)"
    # 去掉 YAML frontmatter
    if core_content.startswith("---"):
        parts = core_content.split("---", 2)
        if len(parts) >= 3:
            core_content = parts[2].strip()
    # 截断超长内容
    if len(core_content) > 8000:
        core_content = core_content[:8000] + "..."

    # 款级结构
    clauses_match = re.search(
        r"## 款级结构\s*\n+(.+?)(?=\n## |\Z)",
        source_note_text, re.DOTALL
    )
    clause_section = clauses_match.group(1).strip() if clauses_match else ""

    # 关键条款/关键观点
    key_points_match = re.search(
        r"## 关键条款 / 关键观点\s*\n+(.+?)(?=\n## |\Z)",
        source_note_text, re.DOTALL
    )
    key_points = key_points_match.group(1).strip() if key_points_match else ""

    # 涉及概念
    concepts_match = re.search(
        r"## 涉及概念\s*\n+(.+?)(?=\n## |\Z)",
        source_note_text, re.DOTALL
    )
    related_concepts = concepts_match.group(1).strip() if concepts_match else ""

    # 待核查问题
    issues_match = re.search(
        r"## 待核查问题\s*\n+(.+?)(?=\n## |\Z)",
        source_note_text, re.DOTALL
    )
    verification_issues = issues_match.group(1).strip() if issues_match else ""

    # 构建标签
    tags = [doc_type]
    if topic:
        tags.append(topic)
    tags = [t for t in tags if t]

    # 构建其他概念页面的 wikilinks
    related_links = []
    for ni in notes_info:
        other_id = ni.get("node_id", "")
        other_title = ni.get("title", "")
        if other_id and str(other_id) != str(node_id):
            # 新版 node_id 格式为 article_NN 或 article_NN_section_NN，直接用作链接
            display = other_title if other_title else other_id
            related_links.append(f"- [[concepts/{topic}/{other_id}|{display}]]")
    related_text = "\n".join(related_links[:10]) if related_links else ""
    if len(related_links) > 10:
        related_text += f"\n- ... 及其他 {len(related_links) - 10} 条"

    lines = []
    # YAML frontmatter（严格遵循 SCHEMA.md 规范）
    lines.append("---")
    lines.append(f"title: {node_title}")
    lines.append(f"created: {today}")
    lines.append(f"updated: {today}")
    lines.append("type: concept")
    lines.append(f"tags: [{', '.join(tags)}]")
    lines.append(f"sources: [raw/{topic}/{doc_id}/source_notes/{node_id}.md]")
    lines.append("confidence: low")
    lines.append("---")
    lines.append("")

    # 正文
    lines.append(f"# {node_title}\n")

    # 概念定义（SCHEMA.md Concept Page 必须项）
    lines.append("## 概念定义\n")
    lines.append(f"来源于《{doc_title}》（{doc_version}）{source_location}。")
    lines.append("")
    lines.append(summary)
    lines.append("")

    # 核心内容
    lines.append("## 核心内容\n")
    if clause_section:
        lines.append(clause_section)
        lines.append("")
    core_preview = core_content[:3000] + ("..." if len(core_content) > 3000 else "")
    lines.append(core_preview)
    lines.append("")

    # 关键条款/关键观点
    lines.append("## 关键条款 / 关键观点\n")
    lines.append(key_points if key_points and "(待补充)" not in key_points else "（待补充）")
    lines.append("")

    # 涉及概念
    lines.append("## 涉及概念\n")
    lines.append(related_concepts if related_concepts and "(待补充)" not in related_concepts else "（待补充）")
    lines.append("")

    # 相关文档（SCHEMA.md Concept Page 要求）
    lines.append("## 相关文档\n")
    if related_text:
        lines.append("### 本文档内的其他条款\n")
        lines.append(related_text)
    lines.append("")

    # 争议或待核查问题（SCHEMA.md Concept Page 要求）
    lines.append("## 争议或待核查问题\n")
    lines.append(verification_issues if verification_issues and "(待补充)" not in verification_issues else "（待补充：由语义加工阶段填充实际核查项）")
    lines.append("")

    # 来源标记（SCHEMA.md provenance marker）
    lines.append(f"^[raw/{topic}/{doc_id}/source_notes/{node_id}.md]")
    lines.append("")

    result = "\n".join(lines)
    # 在 wiki 生成阶段注入交叉引用（chunks 阶段不做）
    # 受 profile.preserve.cross_references 控制
    preserve = profile.get("preserve", {})
    if preserve.get("cross_references", True):
        result = inject_crossrefs(result, topic, concepts_dir, node_id)
    return result


def roman_to_int(r: str) -> int:
    """Convert Roman numeral string to integer (I→1, VIII→8, etc.)."""
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    prev = 0
    for ch in reversed(r.upper()):
        v = values[ch]
        result += -v if v < prev else v
        prev = v
    return result


def inject_crossrefs(text: str, topic: str, concepts_dir: Path, current_node_id: str) -> str:
    """在 wiki 生成阶段注入交叉引用 wikilink。

    将纯文本引用（第N条、附录N、WRC-NN、第N.M款、第N条第X节）转为 [[...]] wikilink。
    新增模式会校验目标 .md 文件确实存在才注入链接；对当前 article 的自引用跳过。
    chunks 阶段不做此操作——保持 chunks 文本纯净。
    """
    # 提取当前 article 编号，用于跳过自引用
    cur_article = ""
    m = re.match(r"article_(\d+[A-Z]?)", current_node_id)
    if m:
        cur_article = m.group(1)

    def _exists(article_num: str, section_num=None):
        """检查目标 concept page 是否已存在。"""
        if section_num is not None:
            return (concepts_dir / f"article_{article_num}_section_{section_num:02d}.md").exists()
        return (concepts_dir / f"article_{article_num}.md").exists()

    # --- 嵌套款号：第N.M.X款 → article_N（必须优先于简单款号，避免部分匹配）---
    def _clause_nested(m):
        a = m.group(1)
        if a == cur_article or not _exists(a):
            return m.group(0)
        return f"[[concepts/{topic}/article_{a}|{m.group(0)}]]"
    text = re.sub(
        r'(?<!\[\[)第(\d+[A-Z]?)\.(\d+[A-Z]?)\.(\d+[A-Z]?)款(?!\||\])',
        _clause_nested, text,
    )

    # --- 简单款号：第N.M款 → article_N ---
    def _clause_simple(m):
        a = m.group(1)
        if a == cur_article or not _exists(a):
            return m.group(0)
        return f"[[concepts/{topic}/article_{a}|{m.group(0)}]]"
    text = re.sub(
        r'(?<!\[\[)第(\d+[A-Z]?)\.(\d+[A-Z]?)款(?!\||\])',
        _clause_simple, text,
    )

    # --- 条+节引用：第N条第X节 → article_N_section_XX（罗马数字转阿拉伯）---
    def _article_section(m):
        a = m.group(1)
        sn = roman_to_int(m.group(2))
        if a == cur_article or not _exists(a, sn):
            return m.group(0)
        return f"[[concepts/{topic}/article_{a}_section_{sn:02d}|{m.group(0)}]]"
    text = re.sub(
        r'(?<!\[\[)第(\d+[A-Z]?)条第\s*([IVXLCDM]+)\s*节(?!\||\])',
        _article_section, text,
    )

    # --- 原有模式（保持不变）---

    # Article references: 第N条 → [[concepts/<topic>/article_N|第N条]]
    text = re.sub(
        r'(?<!\[\[)第(\d+[A-Z]?)条(?!\||\])',
        f'[[concepts/{topic}/article_\\1|第\\1条]]',
        text,
    )
    # Appendix references
    text = re.sub(
        r'(?<!\[\[)附录(\d+[A-Z]?)(?!\||\])',
        f'[[concepts/{topic}/appendix_\\1|附录\\1]]',
        text,
    )
    # WRC references
    text = re.sub(
        r'(?<!\[\[)WRC-(\d{2})(?!\||\])',
        f'[[concepts/{topic}/wrc-\\1|WRC-\\1]]',
        text,
    )
    return text


def update_wiki_index(
    topic: str,
    doc_config: dict,
    pages_info: List[dict],
    wiki_root: Path,
) -> None:
    """
    更新 wiki/index.md（幂等操作）。
    将新生成的概念页面添加为新的 ### 节。
    """
    index_path = wiki_root / "index.md"
    if not index_path.exists():
        print("警告: wiki/index.md 不存在，跳过索引更新")
        return

    existing = index_path.read_text(encoding="utf-8")
    doc_title = doc_config.get("title", doc_config.get("doc_id", ""))
    doc_id = doc_config.get("doc_id", "")

    # 生成新节
    new_section_lines = [f"\n### {doc_title}\n"]
    for pi in pages_info:
        node_id = pi.get("node_id", "")
        title = pi.get("title", "")
        link = f"concepts/{topic}/{node_id}"
        display = title if title else node_id
        new_section_lines.append(f"- [[{link}|{display}]] — {doc_config.get('document_type', '')} 概念页面。")

    new_section = "\n".join(new_section_lines) + "\n"

    # 幂等：检查是否已存在该节
    section_marker = f"### {doc_title}"
    if section_marker in existing:
        # 移除旧节后重新插入
        pattern = rf"\n### {re.escape(doc_title)}\s*\n(?:(?:- \[\[.*?\]\].*?\n)*)"
        existing = re.sub(pattern, "", existing)

    # 在 ## Concepts 段后插入
    insert_pos = existing.find("## Concepts")
    if insert_pos != -1:
        next_section = existing.find("\n###", insert_pos + len("## Concepts"))
        if next_section != -1:
            existing = existing[:next_section] + new_section + existing[next_section:]
        else:
            existing = existing.rstrip() + "\n" + new_section
    else:
        existing = existing.rstrip() + "\n" + new_section

    # 更新日期
    today = datetime.date.today().isoformat()
    existing = re.sub(
        r"> Last updated: \d{4}-\d{2}-\d{2}",
        f"> Last updated: {today}",
        existing,
    )

    index_path.write_text(existing, encoding="utf-8")
    print(f"已更新 wiki/index.md")


def update_wiki_log(
    topic: str,
    doc_config: dict,
    pages_info: List[dict],
    wiki_root: Path,
) -> None:
    """
    追加操作记录到 wiki/log.md。
    严格按照 SKILL.md 的规则：每次重要操作都应追加记录到 log.md。
    """
    log_path = wiki_root / "log.md"
    today = datetime.date.today().isoformat()
    doc_id = doc_config.get("doc_id", "")
    doc_title = doc_config.get("title", "")
    doc_version = doc_config.get("version", "")

    entry_parts = [
        f"\n## [{today}] ingest | {doc_title}",
        f"- Source: raw/{topic}/{doc_id}/",
        f"- Target: concepts/{topic}/",
        f"- Pages: {len(pages_info)} 个概念页面",
    ]
    if doc_version:
        entry_parts.append(f"- Version: {doc_version}")
    entry_parts.append(f"- Summary: 由 compile_wiki.py 自动生成 {len(pages_info)} 个 Wiki 概念页面。")

    entry = "\n".join(entry_parts) + "\n"

    if log_path.exists():
        existing = log_path.read_text(encoding="utf-8")
        log_path.write_text(existing.rstrip() + "\n" + entry)
    else:
        log_path.write_text(f"# Wiki Log\n\n{entry}")

    print(f"已更新 wiki/log.md")


def generate_toc_index(
    structure: dict,
    topic: str,
    pages_info: List[dict],
    doc_config: dict,
    concepts_dir: Path,
) -> None:
    """
    生成目录索引（toc_index.md）。
    复用 build_index.py 的逻辑，同时使用 document.yaml 的 title 作为标题。
    """
    index_dir = concepts_dir / "index"
    index_dir.mkdir(parents=True, exist_ok=True)

    done_ids = {pi.get("node_id") for pi in pages_info}
    # 也收集原始 article_id（如 "1"）以兼容旧版
    done_raw_ids = set()
    for nid in done_ids:
        m = re.match(r"article_(\d+)", nid)
        if m:
            done_raw_ids.add(m.group(1))
    total = 0
    done = 0
    doc_title = doc_config.get("title", topic)

    lines = [
        f"# {doc_title} 目录索引\n",
        "> 自动生成，状态如实反映当前进度。\n",
    ]

    for node in structure.get("all_nodes", []):
        indent = "  " * node.get("depth", 0)
        if node.get("type") == "chapter":
            lines.append(f"\n{indent}## {node['title']}")
        elif node.get("type") == "article":
            total += 1
            aid = node.get("article_id")
            # 新版命名: article_NN.md，旧版命名: NN.md
            new_style = f"article_{str(aid):0>2}.md"
            old_style = concepts_dir / f"{aid}.md"
            new_style_exists = (concepts_dir / new_style).exists()
            if aid and (aid in done_ids or aid in done_raw_ids or (concepts_dir / f"article_{str(aid):0>2}").exists() or old_style.exists()):
                done += 1
                link_file = f"article_{str(aid):0>2}" if (concepts_dir / new_style).exists() else str(aid)
                lines.append(f"{indent}- [{node['title']}](../{link_file}.md)")
            else:
                lines.append(f"{indent}- {node['title']} `[未处理]`")

    lines.insert(2, f"\n> 处理进度: {done}/{total} 条已生成 wiki 页面。\n")

    (index_dir / "toc_index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"toc_index.md 完成，进度 {done}/{total}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc_yaml_path", help="document.yaml 路径")
    ap.add_argument("--nodes", default=None, help="只处理指定节点ID，逗号分隔")
    args = ap.parse_args()

    doc_yaml_path = Path(args.doc_yaml_path).resolve()
    if not doc_yaml_path.exists():
        print(f"文件不存在: {doc_yaml_path}")
        sys.exit(1)

    with open(doc_yaml_path, "r", encoding="utf-8") as f:
        doc_config = yaml.safe_load(f)
    doc_yaml_dir = doc_yaml_path.parent

    # 解析 profile
    profile_path = resolve_profile_path(doc_config, doc_yaml_dir)
    with open(profile_path, "r", encoding="utf-8") as f:
        profile = yaml.safe_load(f)

    # 确定目录：document.yaml.output 优先，profile.output 回退
    doc_output = doc_config.get("output", {})
    profile_output = profile.get("output", {})

    parsed_dir_name = doc_output.get("parsed_dir") or profile_output.get("parsed_dir", "parsed")
    parsed_dir = doc_yaml_dir / parsed_dir_name
    source_notes_dir_name = doc_output.get("source_notes_dir") or profile_output.get("source_notes_dir", "source_notes")
    source_notes_dir = doc_yaml_dir / source_notes_dir_name

    topic = doc_config.get("topic", "")

    # 确定 concepts 输出目录
    # 优先使用 document.yaml.output.concepts_dir，
    # 否则使用 profile.output.concepts_dir，
    # 否则默认 wiki/concepts/<topic>/
    concepts_dir_raw = doc_output.get("concepts_dir") or profile_output.get("concepts_dir")
    if concepts_dir_raw:
        # 如果是相对路径（如 "wiki/concepts/radio_rules"），相对于项目根目录
        if not Path(concepts_dir_raw).is_absolute():
            project_root = doc_yaml_dir.parent.parent.parent.parent
            concepts_dir = project_root / concepts_dir_raw
        else:
            concepts_dir = Path(concepts_dir_raw)
    else:
        # 默认：wiki/concepts/<topic>/
        project_root = doc_yaml_dir.parent.parent.parent.parent
        wiki_root = project_root / "wiki"
        concepts_dir = wiki_root / "concepts" / topic
    concepts_dir.mkdir(parents=True, exist_ok=True)

    # wiki 根目录
    doc_yaml_dir_resolved = doc_yaml_path.parent.resolve()
    project_root = doc_yaml_dir_resolved.parent.parent.parent.parent
    wiki_root = project_root / "wiki"

    structure_path = parsed_dir / "structure.json"
    if not structure_path.exists():
        print(f"未找到 {structure_path}，请先运行 parse_book.py")
        sys.exit(1)

    with open(structure_path, "r", encoding="utf-8") as f:
        structure = json.load(f)
    position_type = structure.get("position_type", "page")

    # 获取所有 source notes（支持新旧命名: article_NN.md / article_NN_section_NN.md）
    source_notes = {}
    for md_path in sorted(source_notes_dir.glob("*.md")):
        if md_path.name == "source_notes_index.md":
            continue
        node_id = md_path.stem
        source_notes[node_id] = md_path.read_text(encoding="utf-8")

    if args.nodes:
        wanted = set(args.nodes.split(","))
        def _matches_wanted(node_id: str) -> bool:
            if node_id in wanted:
                return True
            m = re.match(r"article_(\d+)", node_id)
            if m:
                article_num = m.group(1).lstrip("0") or "0"
                return article_num in wanted
            return node_id in wanted
        source_notes = {k: v for k, v in source_notes.items() if _matches_wanted(k)}

    ns_list = list(source_notes.items())
    notes_info = []
    for k, _ in ns_list:
        # 支持 section 级别 node_id：article_NN_section_NN
        n = find_node_by_id(structure, k)
        if not n:
            sec_m = re.match(r"article_(\d+)_section_(\d+)", k)
            art_m = re.match(r"article_(\d+)", k)
            if sec_m:
                pn = find_node_by_id(structure, sec_m.group(1))
                if pn:
                    n = dict(pn)
                    n["title"] = f"{pn.get('title', '')} — 第{sec_m.group(2)}节"
                    n["article_id"] = k
            elif art_m:
                pn = find_node_by_id(structure, art_m.group(1))
                if pn:
                    n = dict(pn)
        if n:
            notes_info.append({
                "node_id": n.get("article_id", k),
                "title": n.get("title", f"节点 {k}"),
            })
        else:
            notes_info.append({"node_id": k, "title": f"节点 {k}"})

    total_pages = 0

    for node_id, note_text in ns_list:
        # 从 source note 的 "## 源文件" 节提取 chunk 路径
        chunk_rel_path = ""
        cm = re.search(
            r"## 源文件\s*\n.*?`([^`]+)`",
            note_text
        )
        if cm:
            chunk_rel_path = cm.group(1)
        # 读取 chunk 文件内容
        chunk_text = ""
        if chunk_rel_path:
            chunk_path = doc_yaml_dir / chunk_rel_path
            if chunk_path.exists():
                chunk_text = chunk_path.read_text(encoding="utf-8")
        node = find_node_by_id(structure, node_id)
        if node is None:
            # 尝试 section 级别 node_id
            sec_m = re.match(r"article_(\d+)_section_(\d+)", node_id)
            art_m = re.match(r"article_(\d+)", node_id)
            if sec_m:
                pn = find_node_by_id(structure, sec_m.group(1))
                if pn:
                    node = dict(pn)
                    node["title"] = f"{pn.get('title', '')} — 第{sec_m.group(2)}节"
                    node["article_id"] = node_id
            elif art_m:
                pn = find_node_by_id(structure, art_m.group(1))
                if pn:
                    node = dict(pn)

        if node is None:
            node = {
                "title": f"节点 {node_id}",
                "article_id": node_id,
                "type": "unknown",
                "position": "?",
                "end_position": "?",
            }

        page_content = generate_concept_page(
            node, note_text, chunk_text, doc_config, profile, position_type, topic, notes_info, concepts_dir
        )

        out_path = concepts_dir / f"{node_id}.md"
        out_path.write_text(page_content, encoding="utf-8")
        total_pages += 1
        print(f"Wiki 页面: 第{node_id}条 -> {out_path}")

    # 更新 wiki/index.md
    update_wiki_index(topic, doc_config, notes_info, wiki_root)

    # 更新 wiki/log.md
    update_wiki_log(topic, doc_config, notes_info, wiki_root)

    # 生成 toc_index.md
    generate_toc_index(structure, topic, notes_info, doc_config, concepts_dir)

    # 追加解析记录
    parse_notes_path = parsed_dir / "parse_notes.md"
    if parse_notes_path.exists():
        existing = parse_notes_path.read_text(encoding="utf-8")
    else:
        existing = ""

    notes_section = (
        "\n\n## compile_wiki.py 追加记录\n\n"
        f"- 共生成 {total_pages} 个 Wiki 概念页面\n"
        f"- 输出目录: {concepts_dir}\n"
        f"- 已更新 wiki/index.md 和 wiki/log.md\n"
        f"- 来源文档: {doc_config.get('title', 'N/A')} (version: {doc_config.get('version', 'N/A')})\n"
    )
    (parsed_dir / "parse_notes.md").write_text(existing + notes_section, encoding="utf-8")

    print(f"\n完成。共生成 {total_pages} 个 Wiki 概念页面")
    print(f"输出目录: {concepts_dir}")
    print(f"全局索引和日志已更新")


if __name__ == "__main__":
    main()