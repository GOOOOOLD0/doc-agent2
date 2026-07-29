"""
parse_book.py

第一步：解析原始书籍文件，提取文档结构。

读取 document.yaml 和对应的 profile 配置，解析 PDF/DOCX 文件结构，
生成 structure.json、structure.md 和 parse_notes.md，输出到 parsed/ 目录。

大量复用了 scripts/regulation_wiki/extract_structure.py 的核心逻辑，
适配了新的 document.yaml + profile 配置体系。

严格遵循配置：
- document.yaml 中的 source_file, output.*, version, language 等
- profile 中的 split.hierarchy, patterns, preserve.*, output.*

用法:
    python parse_book.py <document.yaml路径>
"""

import sys
import json
import re
from pathlib import Path
from typing import Tuple, Optional, List, Dict, Any

import yaml


def load_document_config(doc_yaml_path: Path) -> dict:
    """加载 document.yaml 配置。"""
    with open(doc_yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_profile(profile_path: Path) -> dict:
    """加载 profile 配置。"""
    with open(profile_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_from_pdf(path: str, notes: list) -> Tuple[List[Dict], str, Optional[int]]:
    """
    使用 PyMuPDF (fitz) 的 get_toc() 提取 PDF 书签/大纲结构。
    返回 (flat_items, position_type, doc_length)。
    """
    import fitz

    doc = fitz.open(path)
    toc = doc.get_toc(simple=True)  # [[level, title, page(1-indexed)], ...]
    if not toc:
        notes.append(
            "PDF 未检测到书签/大纲(TOC)，无法自动提取结构，需人工核对目录后手动补 structure.json。"
        )
        return [], "page", None

    flat = []
    for level, title, page in toc:
        flat.append({"title": title.strip(), "depth": level - 1, "position": page})
    return flat, "page", doc.page_count


def classify_node(title: str, patterns: dict, hierarchy: list) -> str:
    """
    规则驱动的节点分类，不依赖 LLM。
    严格按 profile.split.hierarchy 中定义的顺序，使用 profile.patterns 中的正则匹配层级。
    返回节点类型名称（hierarchy 中定义的值）。
    """
    for node_type in hierarchy:
        pattern = patterns.get(node_type)
        if pattern and re.match(pattern, title):
            return node_type
    return "other"


def extract_article_id(title: str, patterns: dict) -> Optional[str]:
    """从标题中提取条款/章编号。使用 profile.patterns 中的模式进行匹配。"""
    for key in ["article", "chapter", "section"]:
        pattern = patterns.get(key)
        if pattern:
            m = re.match(pattern, title)
            if m:
                # article and section patterns capture a group number
                if m.lastindex and m.lastindex >= 1:
                    return m.group(1)
                return m.group(0)
    return None


def extract_from_docx(
    path: str, notes: list, patterns: dict, hierarchy: list
) -> Tuple[List[Dict], str, Optional[int]]:
    """
    扫描 docx 每个段落判断是否为标题（复用 profile.patterns 中定义的正则规则），
    不依赖 Word 的"标题样式"。
    深度映射严格按 profile.split.hierarchy 的顺序。
    返回 (flat_items, position_type, doc_length)。
    """
    import docx

    document = docx.Document(path)
    flat = []

    # 按 profile.split.hierarchy 确定 depth 映射
    depth_by_type = {t: i for i, t in enumerate(hierarchy)}

    for idx, para in enumerate(document.paragraphs):
        text = para.text.strip()
        if not text:
            continue
        node_type = classify_node(text, patterns, hierarchy)
        if node_type == "other":
            continue
        depth = depth_by_type.get(node_type, len(hierarchy))
        flat.append(
            {
                "title": text,
                "depth": depth,
                "position": idx,
            }
        )

    if not flat:
        notes.append(
            "docx 中未通过规则扫描到任何标题段落，"
            "可能该文档标题格式不符合 profile.patterns 中的写法，需人工核对后手动补 structure.json。"
        )
    return flat, "paragraph_index", len(document.paragraphs)


def build_structure(
    flat_items: List[Dict],
    position_type: str,
    doc_length: Optional[int],
    patterns: dict,
    hierarchy: list,
) -> Dict[str, Any]:
    """
    构建完整结构：为每个节点计算 end_position 并归类。
    节点类型使用 hierarchy 中定义的值进行分类。
    """
    items = []
    for i, node in enumerate(flat_items):
        n = dict(node)
        n["type"] = classify_node(n["title"], patterns, hierarchy)
        n["article_id"] = extract_article_id(n["title"], patterns)

        # 计算 end_position
        next_position = None
        for j in range(i + 1, len(flat_items)):
            next_position = flat_items[j]["position"]
            break
        if position_type == "page":
            n["end_position"] = (next_position - 1) if next_position else doc_length
        else:  # paragraph_index: 区间左闭右开
            n["end_position"] = (
                (next_position - 1) if next_position else (doc_length - 1 if doc_length else None)
            )

        items.append(n)

    # 按类型分组（动态使用 hierarchy 中的类型名）
    grouped = {}
    for node in items:
        t = node["type"]
        if t not in grouped:
            grouped[t] = []
        grouped[t].append(node)

    result = {
        "position_type": position_type,
        "all_nodes": items,
        "chapters": grouped.get("chapter", []),
        "articles": grouped.get("article", []),
        "sections": grouped.get("section", []),
        "clauses": grouped.get("clause", []),
    }
    # 也保留所有其他类型的分组
    for t, nodes in grouped.items():
        if t not in result:
            result[t] = nodes

    return result


def render_structure_md(
    structure: Dict[str, Any], doc_config: dict, position_type: str
) -> str:
    """生成可读的结构树 Markdown 文件。"""
    title = doc_config.get("title", doc_config.get("doc_id", "Unknown"))
    unit = "页" if position_type == "page" else "段落"

    lines = [
        f"# {title} 结构树\n",
        "> 本文件由 parse_book.py 自动生成，不做人工改写。\n",
        f"> 位置单位: {unit} (position_type = {position_type})\n",
    ]

    marker_map = {"chapter": "##", "article": "-", "section": "-", "clause": "  -", "other": "-"}

    for node in structure["all_nodes"]:
        indent = "  " * node["depth"]
        pos_info = f"({unit} {node['position']}-{node.get('end_position', '?')})"
        marker = marker_map.get(node["type"], "-")
        if node["type"] == "chapter":
            lines.append(f"\n{indent}{marker} {node['title']} {pos_info}")
        else:
            lines.append(f"{indent}{marker} {node['title']} {pos_info}")

    return "\n".join(lines) + "\n"


def determine_profile_path(doc_config: dict, doc_yaml_dir: Path) -> Path:
    """
    解析 profile 路径。
    document.yaml 中 profile 字段是相对于项目根目录的路径。
    document.yaml 位于 wiki/raw/<topic>/<doc_id>/document.yaml，
    项目根目录是其上 4 级。
    """
    profile = doc_config.get("profile", "")
    # 尝试相对于 document.yaml 所在目录解析
    candidate = doc_yaml_dir / profile
    if candidate.exists():
        return candidate
    # 尝试相对于项目根目录（document.yaml 往上 4 级）
    project_root = doc_yaml_dir.parent.parent.parent.parent
    candidate = project_root / profile
    if candidate.exists():
        return candidate
    raise FileNotFoundError(f"无法找到 profile 文件: {profile}")


def main():
    if len(sys.argv) != 2:
        print("用法: python parse_book.py <document.yaml路径>")
        sys.exit(1)

    doc_yaml_path = Path(sys.argv[1]).resolve()
    if not doc_yaml_path.exists():
        print(f"文件不存在: {doc_yaml_path}")
        sys.exit(1)

    doc_config = load_document_config(doc_yaml_path)
    doc_yaml_dir = doc_yaml_path.parent

    # 解析 profile 路径并加载
    profile_path = determine_profile_path(doc_config, doc_yaml_dir)
    profile = load_profile(profile_path)

    # 从 profile 读取核心配置
    patterns = profile.get("patterns", {})
    hierarchy = profile.get("split", {}).get("hierarchy", ["chapter", "article", "section"])
    preserve = profile.get("preserve", {})

    # 确定源文件路径（相对于 document.yaml 所在目录）
    source_file_rel = doc_config.get("source_file", "")
    source_path = doc_yaml_dir / source_file_rel
    if not source_path.exists():
        print(f"源文件不存在: {source_path}")
        sys.exit(1)

    # 确定输出目录
    # document.yaml.output 是权威配置，profile.output 仅作为兜底默认值
    doc_output = doc_config.get("output", {})
    profile_output = profile.get("output", {})
    parsed_dir_name = doc_output.get("parsed_dir") or profile_output.get("parsed_dir", "parsed")
    parsed_dir = doc_yaml_dir / parsed_dir_name
    parsed_dir.mkdir(parents=True, exist_ok=True)

    # 提取
    ext = source_path.suffix.lower()
    notes = []
    doc_length = None

    if ext == ".pdf":
        flat_items, position_type, doc_length = extract_from_pdf(str(source_path), notes)
    elif ext == ".docx":
        flat_items, position_type, doc_length = extract_from_docx(
            str(source_path), notes, patterns, hierarchy
        )
    else:
        print(f"暂不支持的文件类型: {ext}（目前支持 .pdf / .docx）")
        sys.exit(1)

    structure = build_structure(flat_items, position_type, doc_length, patterns, hierarchy)

    # 附加上下文信息到 structure
    structure["doc_config"] = {
        "doc_id": doc_config.get("doc_id", ""),
        "title": doc_config.get("title", ""),
        "topic": doc_config.get("topic", ""),
        "document_type": doc_config.get("document_type", ""),
        "version": doc_config.get("version", ""),
        "language": doc_config.get("language", "zh-CN"),
        "page_count": doc_config.get("page_count", doc_length),
        "profile_name": profile.get("profile_name", ""),
    }
    structure["profile"] = {
        "hierarchy": hierarchy,
        "split": profile.get("split", {}),
        "patterns": patterns,
        "preserve": preserve,
        "special_articles": profile.get("special_articles", {}),
    }

    # 生成备注
    chapter_count = len(structure["chapters"])
    article_count = len(structure["articles"])
    section_count = len(structure["sections"])
    clause_count = len(structure.get("clauses", []))

    notes.append(
        f"共识别到 {chapter_count} 个章、{article_count} 个条、"
        f"{section_count} 个节、{clause_count} 个子条款。"
        f"（来源文件类型: {ext}，位置单位: {'页' if position_type == 'page' else '段落'}）"
    )
    notes.append(
        f"使用 profile: {profile.get('profile_name', 'N/A')}，"
        f"层级体系: {' > '.join(hierarchy)}"
    )
    if preserve:
        preserved_keys = [k for k, v in preserve.items() if v]
        notes.append(f"需要保留的元数据: {', '.join(preserved_keys)}")
        # 标记由 LLM 层处理的 preserve 项
        llm_deferred = [k for k in preserved_keys if k in ("tables", "footnotes", "wrc_revision", "printed_page", "article_number", "clause_number")]
        if llm_deferred:
            notes.append(f"以下 preserve 标记依赖 LLM 精修阶段处理: {', '.join(llm_deferred)}")

    # 写入输出文件
    (parsed_dir / "structure.json").write_text(
        json.dumps(structure, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    reg_name = doc_config.get("doc_id", doc_config.get("title", "Unknown"))
    (parsed_dir / "structure.md").write_text(
        render_structure_md(structure, doc_config, position_type), encoding="utf-8"
    )

    notes_md = f"# {reg_name} 解析记录\n\n" + "\n".join(f"- {n}" for n in notes) + "\n"
    (parsed_dir / "parse_notes.md").write_text(notes_md, encoding="utf-8")

    print(
        f"完成。章: {chapter_count}，条: {article_count}，"
        f"节: {section_count}，款: {clause_count}，"
        f"位置单位: {position_type}"
    )
    print(f"输出目录: {parsed_dir}")


if __name__ == "__main__":
    main()