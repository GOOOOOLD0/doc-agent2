"""
split_book.py

第二步：按章节/条款/小节切分文档文本。

读取 parsed/ 中的 structure.json，根据 profile 配置中的 split.hierarchy
和 split.preferred_level 进行切分。PDF 会采用文本抽取 + OCR 兜底策略；
DOCX 直接按段落取文字。

严格遵循配置字段：
- profile.split.hierarchy / preferred_level / max_chunk_tokens
- profile.split.fallback_chunk_tokens（用于 token 兜底切分）
- profile.split.overlap_tokens / overlap_only_for_fallback
- profile.special_articles（特殊条款的二次切分规则）
- profile.preserve（保留页号、脚注等标记）
- profile.patterns（款号等正则识别模式）

输出到 chunks/ 目录：
- {node_id}.txt（每个切分单元的原文）
- 对条款文本进一步做款级结构重组（如适用）

用法:
    python split_book.py <document.yaml路径> [--nodes 1,2,3]
"""

import sys
import json
import re
import argparse
import datetime
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any

import yaml


CJK_RE = re.compile(r"[\u4e00-\u9fff]")
INTER_CJK_SPACE_RE = re.compile(r"(?<=[\u4e00-\u9fff])[ \t]+(?=[\u4e00-\u9fff])")

MIN_MEANINGFUL_CHARS = 20
CJK_RATIO_THRESHOLD = 0.05

PAGE_MARK_RE = re.compile(r"^---\s*page\s*(\d+)\s*---$")
PAGE_NUMBER_RE = re.compile(r"^\d{1,4}$")

# ── 罗马数字 → 整数 ──
_ROMAN_MAP = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7,
              "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13,
              "XIV": 14, "XV": 15, "XVI": 16, "XVII": 17, "XVIII": 18,
              "XIX": 19, "XX": 20}


def roman_to_int(roman: str) -> int:
    """将大写罗马数字字符串转为整数，未知时返回 0。"""
    return _ROMAN_MAP.get(roman.upper().strip(), 0)


def normalize_inter_cjk_spaces(text: str) -> str:
    """只删除中文字符之间的空格，保留英文单词间的空格。"""
    prev = None
    cur = text
    while prev != cur:
        prev = cur
        cur = INTER_CJK_SPACE_RE.sub("", cur)
    return cur


def cjk_ratio_after_strip(text: str) -> Tuple[int, float]:
    """返回 (去空白后的有效字符数, CJK占比)。"""
    stripped = re.sub(r"\s+", "", text)
    if not stripped:
        return 0, 0.0
    cjk = len(CJK_RE.findall(stripped))
    return len(stripped), cjk / len(stripped)


_EASYOCR_READER = None

def get_easyocr_reader(ocr_lang: str) -> "easyocr.Reader":
    global _EASYOCR_READER
    if _EASYOCR_READER is None:
        import easyocr
        lang_map = {"chi_sim": "ch_sim", "chi_tra": "ch_tra", "eng": "en", "jpn": "ja", "kor": "ko"}
        easyocr_langs = [lang_map.get(ocr_lang, ocr_lang.split("_")[0]), "en"]
        _EASYOCR_READER = easyocr.Reader(easyocr_langs, gpu=False)
    return _EASYOCR_READER


def extract_page_text_pdf(
    doc, page_index: int, ocr_lang: str, tessdata_dir: str, notes: list
) -> Tuple[str, str]:
    """
    先尝试 fitz 文字层；仅当"有效字符数足够多，但CJK占比仍然很低"时才走OCR。
    返回 (text, method)。
    """
    page = doc[page_index]
    text = page.get_text()
    meaningful_len, ratio = cjk_ratio_after_strip(text)

    if meaningful_len < MIN_MEANINGFUL_CHARS:
        return normalize_inter_cjk_spaces(text), "text_layer"

    if ratio >= CJK_RATIO_THRESHOLD:
        return normalize_inter_cjk_spaces(text), "text_layer"

    notes.append(
        f"第 {page_index + 1} 页: 有效字符数 {meaningful_len}，去空白后CJK占比 {ratio:.1%}，"
        f"低于阈值 {CJK_RATIO_THRESHOLD:.0%}，判定文字层损坏，已切换为 OCR。"
    )

    import numpy as np
    from PIL import Image
    import io

    reader = get_easyocr_reader(ocr_lang)
    pix = page.get_pixmap(dpi=300)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    raw_results = reader.readtext(np.array(img), detail=0)
    ocr_text = "\n".join(raw_results)
    return normalize_inter_cjk_spaces(ocr_text), "ocr"


def extract_range_docx(document, start_idx: int, end_idx: int) -> str:
    """按段落索引范围提取 docx 文本。"""
    paras = document.paragraphs[start_idx : end_idx + 1]
    text = "\n".join(p.text for p in paras)
    return normalize_inter_cjk_spaces(text)


def reflow_clauses(
    raw_text: str, patterns: dict, heading_patterns: list
) -> Tuple[List[Dict], List[Dict]]:
    """
    按款号行重排文本。
    使用 profile.patterns 中定义的 clause pattern 做款号识别。
    返回 (clauses, unassigned)。
    """
    lines = raw_text.split("\n")
    clauses = []
    unassigned = []
    current_page = None
    current_clause = None
    current_buf = []

    # 编译款号正则（从 profile.patterns 读取）
    clause_pattern_str = patterns.get("clause", r"^\d+\.\d+[A-Za-z]?$")
    try:
        clause_re = re.compile(clause_pattern_str)
    except re.error:
        clause_re = re.compile(r"^\d+\.\d+[A-Za-z]?$")

    # 编译条款标题正则（从 profile.patterns + hierarchy 构建）
    heading_res = []
    for key in heading_patterns:
        p = patterns.get(key)
        if p:
            try:
                heading_res.append(re.compile(p))
            except re.error:
                pass

    def _is_heading(text: str) -> bool:
        for hr in heading_res:
            if hr.match(text):
                return True
        return False

    def flush():
        nonlocal current_clause, current_buf
        if current_clause is not None:
            text = "".join(current_buf).strip()
            clauses.append(
                {"clause_id": current_clause, "page": current_page, "text": text}
            )
        current_clause = None
        current_buf = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        pm = PAGE_MARK_RE.match(stripped)
        if pm:
            flush()
            current_page = int(pm.group(1))
            continue

        if _is_heading(stripped):
            flush()
            unassigned.append(
                {"page": current_page, "line": stripped, "note": "标题行，不计入款内容"}
            )
            continue

        if clause_re.match(stripped):
            flush()
            current_clause = stripped
            continue

        if PAGE_NUMBER_RE.match(stripped):
            unassigned.append(
                {"page": current_page, "line": stripped, "note": "疑似页码/页脚，已从款内容中排除"}
            )
            continue

        if current_clause is not None:
            if (
                current_buf
                and current_buf[-1]
                and current_buf[-1][-1].isascii()
                and stripped[0].isascii()
            ):
                current_buf.append(" " + stripped)
            else:
                current_buf.append(stripped)
        else:
            unassigned.append(
                {
                    "page": current_page,
                    "line": stripped,
                    "note": "未归入任何款号，可能是页眉或未识别到款号",
                }
            )

    flush()
    return clauses, unassigned


def estimate_tokens(text: str) -> int:
    """粗略估算 token 数量（字符数 * 1.3）。"""
    return int(len(text) * 1.3)


def split_by_tokens(
    text: str, max_tokens: int, overlap_tokens: int,
    prefer_structural: bool = True,
    no_split_inside_clause: bool = False,
    clause_pattern: str = "",
) -> List[str]:
    """
    纯 token 长度兜底切分。
    按 max_tokens 切割，overlap_tokens 指定重叠量。

    - prefer_structural: True 时优先在段落边界（空行）切分
    - no_split_inside_clause: True 时不在款号中间切断（用 clause_pattern 识别）
    """
    if estimate_tokens(text) <= max_tokens:
        return [text]

    # 编译 clause pattern
    clause_re = None
    if no_split_inside_clause and clause_pattern:
        try:
            clause_re = re.compile(clause_pattern)
        except re.error:
            pass

    chunks = []
    lines = text.split("\n")
    current = []
    current_tokens = 0
    target_overlap_lines = 0

    if overlap_tokens > 0:
        avg_tokens_per_line = sum(estimate_tokens(l) for l in lines[:50]) / max(50, len(lines[:50]))
        if avg_tokens_per_line > 0:
            target_overlap_lines = max(1, int(overlap_tokens / avg_tokens_per_line))

    for i, line in enumerate(lines):
        line_tokens = estimate_tokens(line)
        if current_tokens + line_tokens > max_tokens and current:
            # prefer_structural: 回退到最近的段落边界（空行）
            if prefer_structural:
                for j in range(len(current) - 1, max(len(current) - 10, 0), -1):
                    if current[j].strip() == "":
                        # 在空行处切分
                        chunk_lines = current[:j]
                        current = current[j + 1:]  # +1 跳过空行
                        current_tokens = sum(estimate_tokens(l) for l in current)
                        chunks.append("\n".join(chunk_lines))
                        break
                else:
                    # 没找到段落边界，照常切
                    chunks.append("\n".join(current))
                    if target_overlap_lines > 0:
                        overlap_count = min(target_overlap_lines, len(current))
                        current = current[-overlap_count:]
                        current_tokens = sum(estimate_tokens(l) for l in current)
                    else:
                        current = []
                        current_tokens = 0
            else:
                chunks.append("\n".join(current))
                if target_overlap_lines > 0:
                    overlap_count = min(target_overlap_lines, len(current))
                    current = current[-overlap_count:]
                    current_tokens = sum(estimate_tokens(l) for l in current)
                else:
                    current = []
                    current_tokens = 0

            # no_split_inside_clause: 检查新 chunk 起始是否在款号中间
            if no_split_inside_clause and clause_re and current:
                # 如果 current 的第一行不是款号起始，回退到上一个款号
                first_stripped = current[0].strip() if current else ""
                if not clause_re.match(first_stripped):
                    # 向前扫描上一个 chunk 的末尾，找到最近的款号行
                    last_chunk = chunks[-1].split("\n") if chunks else []
                    for j in range(len(last_chunk) - 1, -1, -1):
                        if clause_re.match(last_chunk[j].strip()):
                            # 从此款号行开始分离到 current
                            moved = last_chunk[j:]
                            chunks[-1] = "\n".join(last_chunk[:j])
                            current = moved + current
                            current_tokens = sum(estimate_tokens(l) for l in current)
                            break

        current.append(line)
        current_tokens += line_tokens

    if current:
        chunks.append("\n".join(current))

    return chunks


def determine_preferred_nodes(
    structure: dict, profile: dict
) -> Tuple[str, List[dict]]:
    """
    根据 profile.split.preferred_level 确定切分粒度。
    节点类型名称从 profile.split.hierarchy 中获取。
    返回 (level_name, nodes)。
    """
    split_config = profile.get("split", {})
    preferred = split_config.get("preferred_level", "article")

    # 直接匹配 structure 中的 key
    preferred_key = preferred + "s" if not preferred.endswith("s") else preferred
    nodes = structure.get(preferred_key, [])

    if not nodes:
        # 尝试用复数形式查找
        nodes = structure.get(preferred, [])

    if not nodes:
        # 回退：按 hierarchy 顺序找第一个有数据的层级
        hierarchy = split_config.get("hierarchy", ["chapter", "article"])
        for level in hierarchy:
            plural = level + "s" if not level.endswith("s") else level
            fallback = structure.get(plural, [])
            if fallback:
                return level, fallback

    return preferred, nodes


def get_node_id(node: dict) -> str:
    """从节点中提取标识符。"""
    aid = node.get("article_id")
    if aid:
        return str(aid)
    title = node.get("title", "unknown")
    safe = re.sub(r"[^\w\u4e00-\u9fff-]", "_", title)[:50]
    return safe


def apply_special_article_rules(
    node_id: str, full_text: str, node: dict, profile: dict, article_dir: Path, notes: list
) -> List[str]:
    """
    根据 profile.special_articles 中的配置对特定条款做二次切分。
    输出到 article_NN/ 目录下，节文件命名为 section_NN.md。
    返回生成的所有节文件 stem（不含路径和扩展名）。

    目录结构:
      chunks/article_NN/
        section_01.md    (第I节)
        section_02.md    (第II节)
        article.md       (全文，下游兼容)
    """
    special = profile.get("special_articles", {})
    # 支持 article_1 和 article_01 两种写法
    article_key = f"article_{node_id}"
    if article_key not in special:
        article_key_padded = f"article_{node_id:0>2}"
        if article_key_padded in special:
            article_key = article_key_padded
        else:
            return []

    rules = special[article_key]
    split_by = rules.get("split_by", [])
    if isinstance(split_by, str):
        split_by = [split_by]

    if not split_by:
        return []

    # ── 策略分发 ──
    # 支持的策略列表
    IMPLEMENTED = {"section", "general_rules", "allocation_tables", "footnotes", "table"}
    requested = set(split_by)
    implemented = requested & IMPLEMENTED
    unimplemented = requested - IMPLEMENTED
    if unimplemented:
        notes.append(
            f"特殊条款 {article_key}: split_by 中的 {unimplemented} 未识别，"
            f"已忽略。支持: {IMPLEMENTED}"
        )

    if not implemented:
        return []

    # 语义切分策略 (general_rules, allocation_tables, footnotes)
    has_semantic = bool({"general_rules", "allocation_tables", "footnotes"} & implemented)
    # 结构切分策略 (section, table)
    has_structural = bool({"section", "table"} & implemented)

    # ── 语义切分: 按内容类型分类 ──
    semantic_stems = []
    if has_semantic:
        semantic_stems = _split_by_semantic_category(
            full_text, implemented, article_dir, article_key, notes
        )

    # ── 结构切分: 按 section 标题切分 (+ 可选 table 检测) ──
    section_stems = []
    table_stems = []
    if "section" in implemented:
        section_stems, section_contents = _split_by_section(
            full_text, article_dir, profile, article_key, node_id,
            split_by, notes
        )
        # table 策略: 在每个 section 中检测表格并拆分
        if "table" in implemented and section_stems:
            table_stems = _split_tables_from_sections(
                section_contents, article_dir, article_key, notes
            )

    stems = semantic_stems + section_stems + table_stems

    return stems


def _split_by_section(
    full_text: str,
    article_dir: Path,
    profile: dict,
    article_key: str,
    node_id: str,
    split_by: list,
    notes: list,
) -> tuple:
    """按 section 标题切分文本，返回 (stems, [(sec_num, content), ...])。"""
    patterns = profile.get("patterns", {})
    section_pattern_str = patterns.get("section", r"^第\s*([IVXLCDM]+)\s*节")
    try:
        section_re = re.compile(section_pattern_str)
    except re.error:
        section_re = re.compile(r"^第\s*([IVXLCDM]+)\s*节")

    article_dir.mkdir(parents=True, exist_ok=True)

    sub_chunks = []
    lines = full_text.split("\n")
    current_lines = []
    current_section_num = 0

    for line in lines:
        stripped = line.strip()
        sm = section_re.match(stripped)
        if sm:
            if current_lines:
                sub_chunks.append((current_section_num, "\n".join(current_lines)))
                notes.append(
                    f"特殊条款 article_{node_id}: 在 '{stripped}' 处切分，"
                    f"规则: split_by={split_by}"
                )
            current_lines = [line]
            current_section_num = roman_to_int(sm.group(1))
        else:
            current_lines.append(line)

    if current_lines:
        sub_chunks.append((current_section_num, "\n".join(current_lines)))

    stems = []
    for sec_num, content in sub_chunks:
        sname = f"section_{sec_num:02d}"
        sp = article_dir / f"{sname}.md"
        sp.write_text(content, encoding="utf-8")
        stems.append(sname)
        notes.append(
            f"  特殊条款 {article_key}: 写入节文件 {sname}.md ({len(content)} 字符)"
        )

    if stems:
        full_path = article_dir / "article.md"
        full_path.write_text(full_text, encoding="utf-8")
        notes.append(
            f"  特殊条款 {article_key}: 同时写入全文 article.md ({len(full_text)} 字符)"
        )

    if sub_chunks and len(sub_chunks) > 1:
        notes.append(
            f"特殊条款 article_{node_id}: 按 {split_by} 切分为 {len(sub_chunks)} 个子块。"
        )

    return stems, sub_chunks


def _split_by_semantic_category(
    full_text: str,
    strategies: set,
    article_dir: Path,
    article_key: str,
    notes: list,
) -> list:
    """按内容语义分类切分: general_rules, allocation_tables, footnotes。"""
    article_dir.mkdir(parents=True, exist_ok=True)

    lines = full_text.split("\n")
    chunks = {"general_rules": [], "allocation_tables": [], "footnotes": []}
    current_category = "general_rules"
    consecutive_allocation_rows = 0  # 连续分配表行计数，用于防误切换

    # ── 判断某行是否像频率划分表行 ──
    def _looks_like_allocation_row(line: str) -> bool:
        """频率划分表行: 包含频率单位 + 业务/区域信息。"""
        bare = line.strip()
        if not bare or len(bare) < 8:
            return False
        has_freq = bool(re.search(r"(kHz|MHz|GHz|THz)", bare))
        has_region = bool(re.search(r"(1区|2区|3区|所有区|全部区|一区|二区|三区|第[一二三]区)", bare))
        has_service = bool(re.search(
            r"(固定|移动|广播|卫星|无线电|航空|水上|业余|射电|空间"
            r"|地对空|空对地|上行|下行|馈线|主要|次要|允许|禁止|划分)",
            bare
        ))
        score = sum([has_freq, has_region, has_service])
        return score >= 2

    # ── 判断某行是否像脚注行 ──
    def _looks_like_footnote(line: str) -> bool:
        """脚注行: 以编号开头且有较长解释文字，或显式标记。"""
        bare = line.strip()
        if not bare:
            return False
        # 脚注标记行: "注 1 – ..." 或 "脚注: ..."
        if re.match(r"^(注\s*\d+|脚注)[\s:：–—]", bare):
            return True
        # 编号行: 如 "5.XXX " 后跟大段解释文字（>60字符）
        if re.match(r"^\d+\.[A-Z]?\d+(?:\.\d+)?\s", bare):
            rest = bare[bare.index(" ") + 1:] if " " in bare else ""
            if len(rest) > 60 and not re.match(r"^第[IVXLCDM]+节", rest):
                return True
        return False

    for line in lines:
        stripped = line.strip()

        # 节标题 → 根据关键词决定类别
        if re.match(r"^第\s*[IVXLCDM]+\s*节", stripped):
            consecutive_allocation_rows = 0
            if re.search(r"(脚注|注\s*释|附注|footnote)", stripped, re.IGNORECASE):
                current_category = "footnotes"
            elif re.search(r"(表|频率划分|allocation|划分表|频段表)", stripped, re.IGNORECASE):
                current_category = "allocation_tables"
            else:
                current_category = "general_rules"
            chunks[current_category].append(line)
            continue

        # 显式脚注标记
        is_footnote = _looks_like_footnote(stripped)
        if is_footnote:
            consecutive_allocation_rows = 0
            current_category = "footnotes"
            chunks[current_category].append(line)
            continue

        # 分配表行检测（需连续 ≥2 行才切换，防止孤立的含频率数字的规则行误判）
        is_alloc_row = _looks_like_allocation_row(stripped)
        if is_alloc_row:
            consecutive_allocation_rows += 1
            if consecutive_allocation_rows >= 2 and current_category != "footnotes":
                current_category = "allocation_tables"
        else:
            consecutive_allocation_rows = 0
            # 如果当前在 allocation_tables 但遇到连续非表行，不再自动切回——
            # 保持 sticky（section 标题或脚注标记才会切换）

        chunks[current_category].append(line)

    # 写入文件
    stems = []
    for strategy in ("general_rules", "allocation_tables", "footnotes"):
        if strategy in strategies and chunks[strategy]:
            content = "\n".join(chunks[strategy]).strip()
            if not content:
                continue
            sname = f"semantic_{strategy}"
            sp = article_dir / f"{sname}.md"
            sp.write_text(content, encoding="utf-8")
            stems.append(sname)
            notes.append(
                f"  特殊条款 {article_key}: 语义切分 {strategy} → {sname}.md "
                f"({len(content)} 字符)"
            )

    # 全文保留
    if stems:
        full_path = article_dir / "article.md"
        full_path.write_text(full_text, encoding="utf-8")
        notes.append(
            f"  特殊条款 {article_key}: 同时写入全文 article.md ({len(full_text)} 字符)"
        )

    return stems


def _split_tables_from_sections(
    section_contents: list,
    article_dir: Path,
    article_key: str,
    notes: list,
) -> list:
    """在每个 section 中检测密集表格行并拆分为独立 table_N 文件。"""
    table_stems = []

    for sec_num, content in section_contents:
        lines = content.split("\n")
        table_blocks = []  # [(start_idx, end_idx), ...]
        in_table = False
        block_start = 0

        for i, line in enumerate(lines):
            stripped = line.strip()
            # 检测表格行: 数字占比 > 50% 且非纯空行
            if stripped:
                digit_ratio = sum(c.isdigit() or c in ".-+± " for c in stripped) / len(stripped)
                is_table_row = (
                    digit_ratio > 0.5
                    or bool(re.match(r"^[\s\d.\-+±±dBWmHzGMk]*$", stripped))
                )
            else:
                is_table_row = False

            if is_table_row and not in_table:
                in_table = True
                block_start = i
            elif not is_table_row and in_table:
                # 表格块至少 3 行
                if i - block_start >= 3:
                    table_blocks.append((block_start, i))
                in_table = False

        if in_table and len(lines) - block_start >= 3:
            table_blocks.append((block_start, len(lines)))

        if not table_blocks:
            continue

        # 写入表格文件
        for ti, (start, end) in enumerate(table_blocks, 1):
            table_text = "\n".join(lines[start:end]).strip()
            if len(table_text) < 50:
                continue
            tname = f"section_{sec_num:02d}_table_{ti}"
            tp = article_dir / f"{tname}.md"
            # 在表格文本末尾加来源标记
            footer = (
                f"\n\n---\n"
                f"*来源: 第{sec_num}节, 行{start+1}-{end}*"
            )
            tp.write_text(table_text + footer, encoding="utf-8")
            table_stems.append(tname)
            notes.append(
                f"  特殊条款 {article_key}: 表格拆分 section_{sec_num:02d} "
                f"→ {tname}.md (行{start+1}-{end}, {len(table_text)} 字符)"
            )

    return table_stems


def build_chunk_frontmatter(
    node: dict, doc_config: dict, position_type: str = "page",
    section_num: int = 0, extra_type: str = "", chunk_file_stem: str = ""
) -> str:
    """为 chunk 文件生成精简 YAML frontmatter。

    只保留必要字段：title, type, source_doc, source_version,
    source_location, node_id, chunk_id。冗余字段（created/updated/
    source_doc_id/source_type/source_file/source_language）已删除。
    """
    node_id = get_node_id(node)
    node_title = node.get("title", "")
    doc_title = doc_config.get("title", "")
    doc_version = doc_config.get("version", "")
    topic = doc_config.get("topic", "")

    unit = "页" if position_type == "page" else "段落"
    start_pos = node.get("position", "?")
    end_pos = node.get("end_position", "?")
    source_location = f"第{start_pos}{unit} 至 第{end_pos}{unit}"

    # Build chunk_id
    chunk_id = f"article_{node_id:0>2}"
    if section_num:
        chunk_id += f"_section_{section_num:02d}"
    if extra_type:
        chunk_id += f"_{extra_type}"

    # Build title
    title = node_title
    if section_num:
        title += f" — 第{section_num}节"

    tags = [doc_config.get("document_type", "")]
    if topic:
        tags.append(topic)
    tags = [t for t in tags if t]

    lines = [
        "---",
        f"title: {title}",
        "type: chunk",
        f"tags: [{', '.join(tags)}]",
        f"source_doc: {doc_title}",
    ]
    if doc_version:
        lines.append(f"source_version: {doc_version}")
    lines.append(f"source_location: {source_location}")
    lines.append(f"node_id: {node_id}")
    lines.append(f"chunk_id: {chunk_id}")
    lines.append("---")
    lines.append("")

    return "\n".join(lines)



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc_yaml_path", help="document.yaml 路径")
    ap.add_argument("--nodes", default=None, help="只处理指定节点ID，逗号分隔")
    ap.add_argument("--ocr-lang", default="chi_sim")
    ap.add_argument("--tessdata-dir", default=r"C:\Program Files\Tesseract-OCR\tessdata")
    args = ap.parse_args()

    doc_yaml_path = Path(args.doc_yaml_path).resolve()
    if not doc_yaml_path.exists():
        print(f"文件不存在: {doc_yaml_path}")
        sys.exit(1)

    with open(doc_yaml_path, "r", encoding="utf-8") as f:
        doc_config = yaml.safe_load(f)

    doc_yaml_dir = doc_yaml_path.parent

    # 解析 profile
    profile_path_str = doc_config.get("profile", "")
    profile_path = doc_yaml_dir / profile_path_str
    if not profile_path.exists():
        project_root = doc_yaml_dir.parent.parent.parent.parent
        profile_path = project_root / profile_path_str
    if not profile_path.exists():
        print(f"profile 文件不存在: {profile_path}")
        sys.exit(1)

    with open(profile_path, "r", encoding="utf-8") as f:
        profile = yaml.safe_load(f)

    # 从 profile 读取核心配置
    split_config = profile.get("split", {})
    patterns = profile.get("patterns", {})
    hierarchy = split_config.get("hierarchy", ["chapter", "article", "section"])
    preserve = profile.get("preserve", {})

    max_chunk_tokens = split_config.get("max_chunk_tokens", 5000)
    fallback_chunk_tokens = split_config.get("fallback_chunk_tokens", 2500)
    overlap_tokens = split_config.get("overlap_tokens", 150)
    overlap_only_for_fallback = split_config.get("overlap_only_for_fallback", False)
    prefer_structural = split_config.get("prefer_structural_boundaries", True)
    no_split_inside_clause = not split_config.get("allow_split_inside_clause", True)

    # 读取 structure.json
    doc_output = doc_config.get("output", {})
    profile_output = profile.get("output", {})
    parsed_dir_name = doc_output.get("parsed_dir") or profile_output.get("parsed_dir", "parsed")
    parsed_dir = doc_yaml_dir / parsed_dir_name
    structure_path = parsed_dir / "structure.json"

    if not structure_path.exists():
        print(f"未找到 {structure_path}，请先运行 parse_book.py")
        sys.exit(1)

    structure = json.loads(structure_path.read_text(encoding="utf-8"))

    # 确定切分目标节点
    level_name, nodes = determine_preferred_nodes(structure, profile)

    if args.nodes:
        wanted = set(args.nodes.split(","))
        nodes = [n for n in nodes if get_node_id(n) in wanted]

    if not nodes:
        print(f"没有找到可切分的节点（preferred_level={level_name}）")
        sys.exit(1)

    # 确定 chunks 输出目录
    chunks_dir_name = doc_output.get("chunks_dir") or profile_output.get("chunks_dir", "chunks")
    chunks_dir = doc_yaml_dir / chunks_dir_name
    chunks_dir.mkdir(parents=True, exist_ok=True)

    # 源文件路径
    source_file_rel = doc_config.get("source_file", "")
    source_path = doc_yaml_dir / source_file_rel
    ext = source_path.suffix.lower()

    notes = []
    methods_summary = {}

    if ext == ".pdf":
        import fitz

        doc = fitz.open(str(source_path))

        for node in nodes:
            node_id = get_node_id(node)
            start, end = node["position"], node.get("end_position")
            if start is None or end is None:
                notes.append(f"节点 {node_id} 位置信息缺失，跳过自动切块，需人工处理。")
                continue

            span = end - start + 1
            methods_used = set()
            parts = []
            page_preserve = preserve.get("pdf_page", False)
            page_label_preserve = preserve.get("page_label", False)

            for p in range(start - 1, end):
                text, method = extract_page_text_pdf(
                    doc, p, args.ocr_lang, args.tessdata_dir, notes
                )
                methods_used.add(method)
                parts.append(text)

            full_text = "\n".join(parts)

            # 创建按 article 分组的子目录
            article_dir_name = f"article_{node_id:0>2}"
            article_dir = chunks_dir / article_dir_name
            article_dir.mkdir(parents=True, exist_ok=True)

            # 应用 special_articles 规则（优先于 token 兜底）
            # 如果 special_articles 成功切分，不再走 token 兜底
            sa_stems = apply_special_article_rules(
                node_id, full_text, node, profile, article_dir, notes
            )
            was_section_split = bool(sa_stems)

            if was_section_split:
                # special_articles 已做了节级切分，检查各节是否需要进一步 token 兜底
                for stem in sa_stems:
                    sp = article_dir / f"{stem}.md"
                    if sp.exists():
                        stext = sp.read_text(encoding="utf-8")
                        if estimate_tokens(stext) > max_chunk_tokens:
                            sub = split_by_tokens(
                                stext, fallback_chunk_tokens,
                                overlap_tokens if overlap_only_for_fallback else 0,
                                prefer_structural=prefer_structural,
                                no_split_inside_clause=no_split_inside_clause,
                                clause_pattern=patterns.get("clause", ""),
                            )
                            if len(sub) > 1:
                                for i, sc in enumerate(sub):
                                    (article_dir / f"{stem}.part{i + 1}.md").write_text(sc, encoding="utf-8")
                                notes.append(
                                    f"  特殊条款 article_{node_id} 的子节 {stem} 超出 {max_chunk_tokens}，"
                                    f"已按 fallback_chunk_tokens ({fallback_chunk_tokens}) 兜底切分为 {len(sub)} 个部分"
                                )
                out_path = article_dir
                print(
                    f"{level_name} {node_id} ({start}-{end}页, {span}页, "
                    f"方式:{'/'.join(methods_used)}, "
                    f"token:{estimate_tokens(full_text)}/{max_chunk_tokens}, "
                    f"切分:按节({len(sa_stems)}节)) -> {out_path}"
                )
            else:
                # 未命中 special_articles → 原 token 兜底逻辑
                use_fallback = estimate_tokens(full_text) > max_chunk_tokens
                if use_fallback:
                    sub_chunks = split_by_tokens(
                        full_text, fallback_chunk_tokens,
                        overlap_tokens if overlap_only_for_fallback else 0,
                        prefer_structural=prefer_structural,
                        no_split_inside_clause=no_split_inside_clause,
                        clause_pattern=patterns.get("clause", ""),
                    )
                    if len(sub_chunks) > 1:
                        for i, sc in enumerate(sub_chunks):
                            (article_dir / f"article.part{i + 1}.md").write_text(sc, encoding="utf-8")
                        out_path = article_dir / "article.md"
                        out_path.write_text(sub_chunks[0], encoding="utf-8")
                        notes.append(
                            f"节点 {node_id} 超出 max_chunk_tokens ({max_chunk_tokens})，"
                            f"已按 fallback_chunk_tokens ({fallback_chunk_tokens}) 兜底切分为 {len(sub_chunks)} 个部分"
                        )
                    else:
                        out_path = article_dir / "article.md"
                        out_path.write_text(full_text, encoding="utf-8")
                else:
                    out_path = article_dir / "article.md"
                    out_path.write_text(full_text, encoding="utf-8")

                print(
                    f"{level_name} {node_id} ({start}-{end}页, {span}页, "
                    f"方式:{'/'.join(methods_used)}, "
                    f"token:{estimate_tokens(full_text)}/{max_chunk_tokens}) -> {out_path}"
                )

        doc.close()

    elif ext == ".docx":
        import docx

        document = docx.Document(str(source_path))

        for node in nodes:
            node_id = get_node_id(node)
            start, end = node["position"], node.get("end_position")
            if start is None or end is None:
                notes.append(f"节点 {node_id} 位置信息缺失，跳过自动切块，需人工处理。")
                continue

            full_text = extract_range_docx(document, start, end)

            # 创建按 article 分组的子目录
            article_dir_name = f"article_{node_id:0>2}"
            article_dir = chunks_dir / article_dir_name
            article_dir.mkdir(parents=True, exist_ok=True)

            # 检查是否需要按 token 兜底切分
            if estimate_tokens(full_text) > max_chunk_tokens:
                overlap_for_split = overlap_tokens if overlap_only_for_fallback else 0
                sub_chunks = split_by_tokens(
                    full_text, fallback_chunk_tokens, overlap_for_split,
                    prefer_structural=prefer_structural,
                    no_split_inside_clause=no_split_inside_clause,
                    clause_pattern=patterns.get("clause", ""),
                )
                if len(sub_chunks) > 1:
                    for i, sc in enumerate(sub_chunks):
                        sub_path = article_dir / f"article.part{i + 1}.md"
                        sub_path.write_text(sc, encoding="utf-8")
                    notes.append(
                        f"节点 {node_id} 超出 max_chunk_tokens ({max_chunk_tokens})，"
                        f"已按 fallback_chunk_tokens ({fallback_chunk_tokens}) 兜底切分"
                    )
                out_path = article_dir / "article.md"
                out_path.write_text(sub_chunks[0], encoding="utf-8")
            else:
                out_path = article_dir / "article.md"
                out_path.write_text(full_text, encoding="utf-8")

            methods_summary[node_id] = "docx_text"

            if not (estimate_tokens(full_text) > max_chunk_tokens):
                apply_special_article_rules(
                    node_id, full_text, node, profile, article_dir, notes
                )

            print(
                f"{level_name} {node_id} (段落{start}-{end}, 方式:docx_text, "
                f"token:{estimate_tokens(full_text)}/{max_chunk_tokens}) -> {out_path}"
            )

    else:
        print(f"暂不支持的文件类型: {ext}")
        sys.exit(1)

    # 对所有切分结果尝试做款级结构重组
    # 使用 profile.patterns 中的 clause 模式 + hierarchy 中的层级做标题识别
    # 扫描新的目录结构: article_NN/article.md 和 article_NN/section_NN.md
    clauses_count = 0
    article_dirs = sorted(d for d in chunks_dir.iterdir() if d.is_dir() and d.name.startswith("article_"))
    if not article_dirs:
        # 兼容旧版扁平结构
        article_dirs = [chunks_dir]

    for ad in article_dirs:
        for md_path in sorted(ad.glob("*.md")):
            if re.search(r"\.part\d+\.md$", md_path.name):
                continue

            raw_text = md_path.read_text(encoding="utf-8")
            clauses, unassigned = reflow_clauses(raw_text, patterns, hierarchy)

            if clauses:
                structured_path = md_path.with_suffix(".structured.json")
                structured_path.write_text(
                    json.dumps(
                        {"clauses": clauses, "unassigned": unassigned},
                        ensure_ascii=False,
                        indent=2,
                    ),
                    encoding="utf-8",
                )
                clauses_count += len(clauses)

    # 追加解析记录
    parse_notes_path = parsed_dir / "parse_notes.md"
    if parse_notes_path.exists():
        existing = parse_notes_path.read_text(encoding="utf-8")
    else:
        existing = ""

    split_section = (
        "\n\n## split_book.py 追加记录\n\n"
        + ("\n".join(f"- {n}" for n in notes) if notes else "- 无异常")
        + "\n"
    )
    (parsed_dir / "parse_notes.md").write_text(existing + split_section, encoding="utf-8")

    # ── 后处理：为所有 chunk 文件添加 frontmatter ──
    fm_added = 0
    article_dirs = sorted(
        d for d in chunks_dir.iterdir() if d.is_dir() and d.name.startswith("article_")
    )
    for ad in article_dirs:
        # 提取 article 编号
        article_num_str = ad.name.replace("article_", "").lstrip("0") or "0"
        article_num = int(article_num_str)
        # 查找对应 node
        node = None
        for n in nodes:
            if str(get_node_id(n)) == str(article_num):
                node = n
                break
        if node is None:
            continue

        for md_file in sorted(ad.glob("*.md")):
            stem = md_file.stem  # e.g. "section_01", "article", "article.part1"
            section_num = 0
            extra_type = ""

            if stem.startswith("section_"):
                # section_NN or section_NN.partN or section_NN_table_N
                parts = stem.split("_")
                try:
                    section_num = int(parts[1])
                except (ValueError, IndexError):
                    pass
                if "table" in stem:
                    extra_type = "table"
                    section_num = 0  # table 文件复用 section info 而非单独节号
                elif "part" in stem:
                    extra_type = "part"
            elif stem.startswith("semantic_"):
                extra_type = stem.replace("semantic_", "")
            elif stem.startswith("article.part"):
                extra_type = "part"
            elif stem == "article":
                pass  # 全文文件，section_num=0
            else:
                continue

            fm = build_chunk_frontmatter(
                node, doc_config, position_type=structure.get("position_type", "page"),
                section_num=section_num, extra_type=extra_type
            )
            existing_text = md_file.read_text(encoding="utf-8")
            # Skip if already has frontmatter
            if existing_text.startswith("---"):
                continue
            md_file.write_text(fm + existing_text, encoding="utf-8")
            fm_added += 1

    if fm_added:
        notes.append(f"已为 {fm_added} 个 chunk 文件添加 YAML frontmatter")

    # 汇总报告
    print(f"\n完成。切分层级: {level_name}，共 {len(nodes)} 个节点")
    print(f"原文切块输出目录: {chunks_dir}")
    if clauses_count:
        print(f"款级结构重组: {clauses_count} 款已识别 (使用 clause pattern: {patterns.get('clause', 'N/A')})")
    print(f"兜底切分配置: max={max_chunk_tokens}, fallback={fallback_chunk_tokens}, "
          f"overlap={overlap_tokens}, overlap_only_for_fallback={overlap_only_for_fallback}")


if __name__ == "__main__":
    main()