"""
build_source_notes.py

第三步：根据切分结果生成 Source Notes（原始文档页面）。

Source Note 是 wiki/SCHEMA.md 中定义的 Source Page，记录单篇文档片段的信息。
每块 chunk 生成一个 Source Note，包含：
- 文档元信息（严格来自 document.yaml 的 title, version, language 等）
- 来源位置（页码/段落，来自 structure.json）
- 一句话总结
- 核心内容
- 关键条款或关键观点
- 涉及概念
- 涉及机构
- 可能影响
- 待核查问题

严格遵循：
- document.yaml.output.source_notes_dir（优先）→ profile.output.source_notes_dir（回退）
- document.yaml 的 version, language, document_type 等元信息
- profile.preserve 决定是否保留页码等标记

输出到 source_notes/ 目录，文件名格式：{node_id}.md
同时生成 source_notes_index.md 汇总所有 Source Notes。

复用 SCHEMA.md 中定义的 Source Page 结构和 wiki 规范。

用法:
    python build_source_notes.py <document.yaml路径> [--nodes 1,2,3]
"""

import sys
import json
import re
import argparse
import datetime
from pathlib import Path
from typing import List, Dict, Optional

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
    """在结构树中查找指定ID的节点。"""
    for node in structure.get("all_nodes", []):
        aid = node.get("article_id")
        if aid and str(aid) == node_id:
            return node
    return None


def generate_source_note(
    node: dict,
    chunk_text: str,
    chunk_path: str,
    doc_config: dict,
    profile: dict,
    position_type: str,
    structured_data: Optional[dict] = None,
) -> str:
    """
    生成 Source Note（摘要页面）。
    
    新设计：Source Note = 基于 chunk 的灵活摘要。
    - frontmatter 从 chunk 文件的 YAML 读取（不重复 document.yaml）
    - 正文不复制 chunk 内容，仅保留 chunk 路径引用
    - 不生成与 frontmatter 重复的属性表格
    - frontmatter 精简：仅保留必要字段
    - 所有语义字段（关键条款、概念等）留空，由 LLM 在后续步骤填充
    """
    node_id = node.get("article_id") or node.get("title", "unknown")
    node_title = node.get("title", "")

    # 从 chunk frontmatter 提取元信息
    chunk_fm = parse_chunk_frontmatter(chunk_text) if chunk_text else {}
    
    # 构建 frontmatter（从 chunk fm 读取，回退到 document.yaml）
    fm_text = build_source_note_frontmatter(chunk_fm, node_title, doc_config)

    topic = doc_config.get("topic", "")
    doc_id = doc_config.get("doc_id", "")

    # 摘要占位 — 由 LLM 代理在后续步骤中生成
    summary = "(待LLM生成)"

    lines = [fm_text]

    # 正文
    lines.append(f"# {node_title}\n")

    # 一句话总结
    lines.append("## 一句话总结\n")
    lines.append(summary)
    lines.append("")

    # 源文件引用 — 指向清洗后的 chunk 文件
    lines.append("## 源文件\n")
    if chunk_path:
        lines.append(f"原始内容参见: `{chunk_path}`")
    lines.append("")

    # 关键条款 / 关键观点
    lines.append("## 关键条款 / 关键观点\n")
    lines.append("（待LLM生成）")
    lines.append("")

    # 涉及概念
    lines.append("## 涉及概念\n")
    lines.append("（待LLM生成）")
    lines.append("")

    # 涉及机构
    lines.append("## 涉及机构\n")
    lines.append("（待LLM生成）")
    lines.append("")

    # 可能影响
    lines.append("## 可能影响\n")
    lines.append("（待LLM生成）")
    lines.append("")

    # 待核查问题
    lines.append("## 待核查问题\n")
    lines.append("（待LLM生成）")
    lines.append("")

    # 来源标记
    lines.append(f"^[raw/{topic}/{doc_id}/source_notes/{node_id}.md]")
    lines.append("")

    return "\n".join(lines)


def generate_source_notes_index(
    doc_config: dict,
    notes_info: List[dict],
    source_notes_dir: Path,
) -> str:
    """生成 source_notes_index.md，汇总所有 Source Notes。"""
    doc_title = doc_config.get("title", doc_config.get("doc_id", ""))
    doc_id = doc_config.get("doc_id", "")

    lines = [
        f"# {doc_title} - Source Notes 索引\n",
        "> 由 build_source_notes.py 自动生成。",
        f"> 共 {len(notes_info)} 个 Source Note。\n",
    ]

    for ni in notes_info:
        node_id = ni.get("node_id", "")
        title = ni.get("title", "")
        lines.append(f"- [{title}]({node_id}.md)")

    return "\n".join(lines) + "\n"


def parse_chunk_frontmatter(chunk_text: str) -> dict:
    """从 chunk 文件的 YAML frontmatter 提取元信息。"""
    m = re.match(r"^---\n(.*?)\n---", chunk_text, re.DOTALL)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def build_source_note_frontmatter(fm: dict, node_title: str, doc_config: dict) -> str:
    """从精简 chunk frontmatter 生成 source note 的 YAML frontmatter。
    
    精简后的 chunk fm 只有: title, type, tags, source_doc, source_version,
    source_location, node_id, chunk_id。其他字段从 document.yaml 补全。
    """
    today = datetime.date.today().isoformat()
    topic = doc_config.get("topic", "")
    doc_id = doc_config.get("doc_id", "")
    source_file = doc_config.get("source_file", "")
    source_filename = Path(source_file).name if source_file else ""

    lines = [
        "---",
        f"title: {node_title}",
        f"created: {today}",
        f"updated: {today}",
        "type: source",
        f"tags: [{', '.join(fm.get('tags', []))}]",
        f"sources: [raw/{topic}/{doc_id}/source/{source_filename}]",
        "confidence: low",
        f"source_doc: {fm.get('source_doc', doc_config.get('title', ''))}",
    ]
    if fm.get("source_version"):
        lines.append(f"source_version: {fm.get('source_version')}")
    lines.append(f"source_location: {fm.get('source_location', '')}")
    node_id = fm.get("node_id", "")
    if node_id:
        lines.append(f"node_id: {node_id}")
    chunk_id = fm.get("chunk_id", "")
    if chunk_id:
        lines.append(f"chunk_id: {chunk_id}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)



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
    chunks_dir_name = doc_output.get("chunks_dir") or profile_output.get("chunks_dir", "chunks")
    chunks_dir = doc_yaml_dir / chunks_dir_name
    source_notes_dir_name = doc_output.get("source_notes_dir") or profile_output.get("source_notes_dir", "source_notes")
    source_notes_dir = doc_yaml_dir / source_notes_dir_name
    source_notes_dir.mkdir(parents=True, exist_ok=True)

    structure_path = parsed_dir / "structure.json"
    if not structure_path.exists():
        print(f"未找到 {structure_path}，请先运行 parse_book.py")
        sys.exit(1)

    with open(structure_path, "r", encoding="utf-8") as f:
        structure = json.load(f)
    position_type = structure.get("position_type", "page")

    # 读取 source_notes 配置（控制 note 生成行为）
    source_notes_config = profile.get("source_notes", {})
    one_note_per_chunk = source_notes_config.get("one_note_per_chunk", False)
    short_article_as_one_note = source_notes_config.get("short_article_as_one_note", False)
    section_as_one_note = source_notes_config.get("section_as_one_note", False)
    merge_fallback_parts = source_notes_config.get("merge_fallback_parts", True)
    tables_require_individual_note = source_notes_config.get("tables_require_individual_note", False)
    # NOTE: one_note_per_chunk=true 时每个 chunk 文件独立生成一个 Note，不走合并逻辑。
    # tables_require_individual_note 不在此处由 Python 检测表格——表格语义判断交给 LLM 代理
    # 在 source_notes 生成后按 skill 中的 prompt 决定是否拆分表格为独立 Note。

    # 获取所有切分后的 chunk 文件 — 新版目录结构: article_NN/*.md
    chunk_files = {}  # node_id -> [(path, section_num, is_section)]
    article_dirs = sorted(
        d for d in chunks_dir.iterdir() if d.is_dir() and d.name.startswith("article_")
    )

    if article_dirs:
        # 新版目录结构
        for ad in article_dirs:
            # 从 article_NN 目录名提取 node_id
            dir_name = ad.name  # article_01
            article_num_str = dir_name.replace("article_", "").lstrip("0") or "0"

            # 检查是否有节文件
            section_files = sorted(ad.glob("section_*.md"))
            section_parts = {}  # section_num -> [paths]
            for sf in section_files:
                m = re.match(r"section_(\d+)\.md$", sf.name)
                if m:
                    sn = int(m.group(1))
                    section_parts.setdefault(sn, []).append(sf)
            # 合并 part 文件
            for sf in sorted(ad.glob("section_*.part*.md")):
                m = re.match(r"section_(\d+)\.part(\d+)\.md$", sf.name)
                if m:
                    sn = int(m.group(1))
                    section_parts.setdefault(sn, []).append(sf)

            if one_note_per_chunk:
                # 严格按 chunk 文件一对一生成 Note（不合并）
                for chunk_file in sorted(ad.glob("*.md")):
                    stem = chunk_file.stem  # e.g. "section_02", "article"
                    if stem == "article":
                        # article.md 全文也单独一个 Note
                        node_id = f"article_{article_num_str}"
                        chunk_files[node_id] = [chunk_file]
                        # 但如果有 section 文件，article fulltext note 可能重复，
                        # 仍然生成，由 LLM 后续判断是否需要
                    elif re.match(r"^section_\\d+$", stem):
                        node_id = f"article_{article_num_str}_{stem}"
                        chunk_files[node_id] = [chunk_file]
                    elif re.match(r"^article\\.part\\d+$", stem):
                        node_id = f"article_{article_num_str}_{stem}"
                        chunk_files[node_id] = [chunk_file]
            elif section_files and section_as_one_note:
                # 每个节生成独立 Source Note
                for sn in sorted(section_parts):
                    paths = sorted(section_parts[sn])
                    node_id = f"article_{article_num_str}_section_{sn:02d}"
                    chunk_files[node_id] = paths
            elif short_article_as_one_note:
                # 整个 article 生成一个 Source Note
                article_file = ad / "article.md"
                parts = sorted(ad.glob("article.part*.md"))
                all_paths = ([article_file] if article_file.exists() else []) + parts
                if merge_fallback_parts and parts:
                    all_paths = [article_file] if article_file.exists() else parts
                node_id = f"article_{article_num_str}"
                chunk_files[node_id] = all_paths
    else:
        # 兼容旧版扁平结构
        for txt_path in sorted(chunks_dir.glob("*.txt")):
            if re.search(r"\.part\d+\.txt$", txt_path.name):
                base_name = re.sub(r"\.part\d+\.txt$", "", txt_path.name)
                if base_name not in chunk_files:
                    chunk_files[base_name] = []
                chunk_files[base_name].append(txt_path)
            else:
                node_id = txt_path.stem
                chunk_files[node_id] = [txt_path]

    if args.nodes:
        wanted = set(args.nodes.split(","))
        # 兼容新旧 node_id 格式: "1" 应匹配 "article_01", "article_01_section_03" 等
        def _matches_wanted(node_id: str) -> bool:
            if node_id in wanted:
                return True
            # 从 node_id 提取 article 编号: article_NN[_...] 或纯数字
            m = re.match(r"article_(\d+)", node_id)
            if m:
                article_num = m.group(1).lstrip("0") or "0"
                return article_num in wanted
            return node_id in wanted
        chunk_files = {k: v for k, v in chunk_files.items() if _matches_wanted(k)}

    notes_info = []
    total_notes = 0

    for node_id, txt_paths in chunk_files.items():
        # 合并所有 part 的文本
        combined_text = ""
        for tp in sorted(txt_paths):
            combined_text += tp.read_text(encoding="utf-8") + "\n"

        # 查找结构化数据（在第一个文件旁边）
        structured_data = None
        if txt_paths:
            primary = txt_paths[0]
            structured_path = primary.with_suffix(".structured.json")
            if structured_path.exists():
                with open(structured_path, "r", encoding="utf-8") as f:
                    structured_data = json.load(f)

        # 查找节点信息
        # 对于 section 级别的 node_id（如 article_01_section_04），提取 article 编号查找父节点
        node = None
        section_num = None
        sec_match = re.match(r"article_(\d+)_section_(\d+)", node_id)
        if sec_match:
            article_num = sec_match.group(1)
            section_num = int(sec_match.group(2))
            node = find_node_by_id(structure, article_num)
            if node:
                node = dict(node)
                node["title"] = f"{node.get('title', '')} — 第{section_num}节"
                node["article_id"] = node_id
        else:
            art_match = re.match(r"article_(\d+)", node_id)
            if art_match:
                article_num = art_match.group(1)
                node = find_node_by_id(structure, article_num)

        if node is None:
            node = {
                "title": f"节点 {node_id}",
                "article_id": node_id,
                "type": "unknown",
                "position": "?",
                "end_position": "?",
            }

        # 生成 Source Note
        # 确定 chunk 引用路径（相对于 document.yaml）
        chunk_rel_path = ""
        if txt_paths:
            primary = txt_paths[0]
            try:
                chunk_rel_path = str(primary.relative_to(doc_yaml_dir))
            except ValueError:
                chunk_rel_path = str(primary)
        note_content = generate_source_note(
            node, combined_text, chunk_rel_path,
            doc_config, profile, position_type, structured_data
        )

        out_path = source_notes_dir / f"{node_id}.md"
        out_path.write_text(note_content, encoding="utf-8")

        notes_info.append(
            {"node_id": node_id, "title": node.get("title", f"节点 {node_id}")}
        )
        total_notes += 1
        print(f"Source Note: {node_id} -> {out_path}")

    # 生成索引
    if notes_info:
        index_content = generate_source_notes_index(doc_config, notes_info, source_notes_dir)
        (source_notes_dir / "source_notes_index.md").write_text(
            index_content, encoding="utf-8"
        )
        print(f"索引: {source_notes_dir / 'source_notes_index.md'}")

    # 追加解析记录
    parse_notes_path = parsed_dir / "parse_notes.md"
    if parse_notes_path.exists():
        existing = parse_notes_path.read_text(encoding="utf-8")
    else:
        existing = ""

    notes_section = (
        "\n\n## build_source_notes.py 追加记录\n\n"
        f"- 共生成 {total_notes} 个 Source Note\n"
        f"- 输出目录: {source_notes_dir}\n"
        f"- 来源文档: {doc_config.get('title', 'N/A')} (version: {doc_config.get('version', 'N/A')})\n"
    )
    (parsed_dir / "parse_notes.md").write_text(existing + notes_section, encoding="utf-8")

    print(f"\n完成。共生成 {total_notes} 个 Source Note")
    print(f"输出目录: {source_notes_dir}")


if __name__ == "__main__":
    main()