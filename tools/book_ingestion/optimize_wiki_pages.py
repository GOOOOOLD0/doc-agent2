"""
optimize_wiki_pages.py

第六步（可选）：优化 Wiki 概念页面。

注意：mechanical-clean 和 LLM 精修已前移到 Step 3（chunk 清洗阶段），
对 chunks/ 目录执行。本工具主要保留 --rebuild-core 功能：
将 compile_wiki.py 生成的截断概念页面替换为从 chunks 合并的完整文本。

【--rebuild-core】
从 chunks 目录读取原始文本合并后写入概念页面的 ## 核心内容 节。
解决 compile_wiki.py 可能截断超长内容的问题。

【--mechanical-clean】（已弃用，但代码保留）
原用于概念页面清洗的逻辑，现已移至 chunk 清洗阶段（Step 3）。
如确需对概念页面重跑，仍可使用。

用法:
    uv run python tools/book_ingestion/optimize_wiki_pages.py <doc.yaml> --nodes 1,2,3 --rebuild-core
"""

import sys
import re
import argparse
import shutil
from pathlib import Path
from typing import List, Tuple

import yaml


# ═══════════════════════════════════════════════════
# Python 机械层 — 确定性修复
# ═══════════════════════════════════════════════════

OCR_FIXES = [
    ('笫', '第'), ('GH2', 'GHz'), ('GHZ', 'GHz'), ('MHZ', 'MHz'), ('MIZ', 'MHz'),
    ('KZ', 'kHz'), ('kr', 'kHz'), ('O00', '000'), ('O0O', '000'),
    ('WRC-IS', 'WRC-15'), ('WRC-I9', 'WRC-19'),
    ('困际', '国际'), ('太会', '大会'), ('己下定义', '已下定义'),
    ('第工节', '第I节'), ('第皿节', '第IV节'), ('三织法', '组织法'),
    ('IU-尽', 'ITU-R'), ('ITU-尽', 'ITU-R'),
]

GARBAGE_SET = {'人', '米', '米米', '卜', 'eSt', '豆', '•', '●', '○', '◎', '※', '~', '…', '"', "'", 'C', 'G', '('}
GARBAGE_RE = re.compile(
    r'^(---\s*page\s*\d+\s*---'
    r'|RRI\d*|RR\d+[-–]\d+|RR\d+\s+\d+|RRI[Ll]'
    r'|第[一二三四五六七八九十]+章\s*[−–—\-]\s*\S*$'  # "第一章 − 术语..." 整行删除（含U+2212，章和−间可能有空格）
    r'|[−–—\-]\s*\d+\s*[−–—\-]$'                  # "– 7 –" 独立页码行
    r')$'
)

CLAUSE_PAT = re.compile(r'^(\d+\.?\d*[A-Za-z]?)(?:\s+(.*))?$')
SECTION_PAT = re.compile(r'^第([IVXLCDM]+)节\s*[-–—]\s*(.*)')
CLS_PAT = re.compile(r'^\d+\.?\d*[A-Za-z]?\s')  # match clause-start line


def mechanical_clean(text: str, article_id: str, topic: str,
                     existing_pages: set, inject_wikilinks: bool = True) -> Tuple[str, dict]:
    """Python 机械清洗：确定性操作，不依赖 LLM。返回 (clean_text, stats)。

    inject_wikilinks=False 时跳过 Pass 5（交叉引用 wikilink 注入），
    用于 chunk 阶段清洗。chunk 保留 PDF 原文，wikilink 注入延迟到 wiki 页面阶段。"""
    stats = {"dedup": 0, "garbage": 0, "ocr_fix": 0, "xref": 0, "junk": 0}

    lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')

    # ── Pass 1: 垃圾行过滤 ──
    ok = []
    for l in lines:
        s = l.strip()
        if not s:
            continue
        if s in GARBAGE_SET:
            stats["garbage"] += 1
            continue
        if GARBAGE_RE.match(s):
            stats["garbage"] += 1
            continue
        if re.match(r'^\d{1,3}$', s):
            stats["garbage"] += 1
            continue
        ok.append(s)

    # ── Pass 2: OCR 错字修正 ──
    for old, new in OCR_FIXES:
        ok = [s.replace(old, new) for s in ok]
    ok = [re.sub(r'\s+', ' ', s.replace('\u3000', ' ')).strip() for s in ok]
    ok = [s for s in ok if s]
    stats["ocr_fix"] = 1

    # ── Pass 3: 去重 ──
    dedup = []
    seen = {}
    for s in ok:
        m = CLAUSE_PAT.match(s)
        if m:
            num = m.group(1)
            rest = (m.group(2) or '').strip()
            if num in seen and rest[:60] == seen[num][:60]:
                stats["dedup"] += 1
                continue
            seen[num] = rest
        dedup.append(s)

    # ── Pass 4: 条款分组 + 残行合并 + 行末垃圾清理 ──
    out = []
    cur, buf = None, []

    def flush():
        nonlocal cur, buf, out
        if cur is None:
            return
        t = re.sub(r'\s+', ' ', ' '.join(buf)).strip()
        # 行末垃圾清理（节标题/页码/章节名/下划线/Unicode）
        old_len = len(t)
        t = re.sub(r'\s+第[IVXLCDM]+节\s*[-–—]\s*\S.*$', '', t)
        t = re.sub(r'\s+\d{1,3}\s+第[一二三四五六七八九十]+章\S*$', '', t)
        t = re.sub(r'\s+第[一二三四五六七八九十]+章\s*[−–—\-]?\s*\S*$', '', t)  # 章名残留（可能有或没有分隔符）
        t = re.sub(r'\s*[−–—\-]\s*\d{1,3}\s*[−–—\-]\s*$', '', t)  # " – 7 –" 行内
        t = re.sub(r'_{4,}', '', t)
        t = re.sub(r'[\uf000-\uf8ff\u2000-\u2fff\ufff0-\uffff]', '', t)
        t = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])', '', t)
        if len(t) < old_len:
            stats["junk"] += 1
        t = t.strip()
        if t:
            out.append(f"{cur} {t}")
        cur, buf = None, []

    for s in dedup:
        sm = SECTION_PAT.match(s)
        if sm:
            flush()
            out.append(f"第{sm.group(1)}节 - {sm.group(2).strip()}")
            continue
        m = CLAUSE_PAT.match(s)
        if m:
            flush()
            cur = m.group(1)
            r2 = (m.group(2) or '').strip()
            if r2:
                buf.append(r2)
        else:
            if cur is not None:
                buf.append(s)
            else:
                out.append(s)
    flush()

    core = '\n'.join(out)

    # ── Pass 5: 交叉引用 wikilink 注入（正则，无语义依赖）──
    # 仅在 inject_wikilinks=True（wiki 页面阶段）时执行
    if inject_wikilinks:
        # 第N条 → wikilink（跳过自我引用）
        # 从 article_id 提取条号用于自我引用判断（article_1_section_03 → 1）
        self_article_num = None
        m_self = re.match(r"article_(\d+)", article_id)
        if m_self:
            self_article_num = m_self.group(1).lstrip("0") or "0"

        def article_link(m):
            n = m.group(1)
            if n == self_article_num:
                return m.group(0)
            return f"[[concepts/{topic}/article_{n}|第{n}条]]"

        core = re.sub(r'(?<!\[\[)(?<!\|)第(\d+[A-Za-z]?)条(?!\])', article_link, core)
        # 附录N → wikilink
        core = re.sub(r'(?<!\[\[)(?<!\|)附录(\d+)(?!\])',
                      lambda m: f"[[concepts/{topic}/appendix-{m.group(1)}|附录{m.group(1)}]]", core)
        # 第N章 → wikilink
        core = re.sub(
            r'(?<!\[\[)(?<!\|)第(\s*[一二三四五六七八九十]+\s*)章(?!\])',
            lambda m: f"[[concepts/{topic}/chapter-{m.group(1).strip()}|第{m.group(1).strip()}章]]",
            core
        )
        # 第N.M款 → wikilink
        core = re.sub(r'(?<!\[\[)(?<!\|)第(\d+)\.(\d+[A-Za-z]?)款(?!\])',
                      lambda m: f"[[concepts/{topic}/article_{m.group(1)}#clause-{m.group(1)}.{m.group(2)}|第{m.group(1)}.{m.group(2)}款]]",
                      core)
        # WRC-NN → wikilink
        core = re.sub(r'(?<!\[\[)(?<!\|)WRC[-–](\d+)(?!\])',
                      lambda m: f"[[concepts/{topic}/wrc-{m.group(1)}|WRC-{m.group(1)}]]", core)

        xref_before = len(re.findall(r'\[\[concepts/', core))
        stats["xref"] = xref_before

        # ── Pass 5b: 修正旧格式 wikilink（{topic}/N → {topic}/article_N）──
        core = re.sub(
            r'\[\[concepts/' + re.escape(topic) + r'/(\d+[A-Za-z]?)([\]\|])',
            r'[[concepts/' + topic + r'/article_\1\2',
            core
        )
        # 款号链接同样修正: /N#clause → /article_N#clause
        core = re.sub(
            r'\[\[concepts/' + re.escape(topic) + r'/(\d+)#clause-',
            r'[[concepts/' + topic + r'/article_\1#clause-',
            core
        )

    # ── Pass 6: 段落间距 ──
    result = []
    prev = False
    for l in core.split('\n'):
        is_c = bool(CLS_PAT.match(l))
        if is_c and prev:
            result.append('')
        result.append(l)
        prev = is_c

    return '\n'.join(result), stats


# ═══════════════════════════════════════════════════
# 公共函数
# ═══════════════════════════════════════════════════

def load_config(doc_yaml_path: Path) -> tuple:
    with open(doc_yaml_path, "r", encoding="utf-8") as f:
        doc_config = yaml.safe_load(f)
    doc_yaml_dir = doc_yaml_path.parent
    profile_str = doc_config.get("profile", "")
    profile_path = doc_yaml_dir / profile_str
    if not profile_path.exists():
        project_root = doc_yaml_dir.parent.parent.parent.parent
        profile_path = project_root / profile_str
    if not profile_path.exists():
        raise FileNotFoundError(f"profile 文件不存在: {profile_path}")
    with open(profile_path, "r", encoding="utf-8") as f:
        profile = yaml.safe_load(f)
    return doc_config, profile, doc_yaml_dir


def merge_chunk_parts(chunks_dir: Path, article_id: str) -> str:
    """从 chunks 目录合并文章全文。支持新旧两种目录结构。"""
    # 新版: chunks/article_NN/article.md + article.part*.md
    article_dir = chunks_dir / f"article_{article_id:0>2}"
    if article_dir.is_dir():
        part_files = sorted(article_dir.glob("article.part*.md"))
        if part_files:
            texts = [pf.read_text(encoding="utf-8") for pf in part_files]
            return "\n".join(texts)
        main_file = article_dir / "article.md"
        if main_file.exists():
            return main_file.read_text(encoding="utf-8")

    # 旧版兼容: chunks/{id}.txt + {id}.part*.txt
    part_files = sorted(chunks_dir.glob(f"{article_id}.part*.txt"))
    if part_files:
        texts = [pf.read_text(encoding="utf-8") for pf in part_files]
        return "\n".join(texts)
    main_file = chunks_dir / f"{article_id}.txt"
    if main_file.exists():
        return main_file.read_text(encoding="utf-8")
    return ""


def get_existing_pages(concepts_dir: Path) -> set:
    existing = set()
    if not concepts_dir.exists():
        return existing
    for f in concepts_dir.glob("*.md"):
        if "index" not in f.stem:
            existing.add(f.stem)
    return existing


# ═══════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════

def _matches_wanted(node_id: str, wanted: set) -> bool:
    """兼容新旧 node_id 格式: "1" 匹配 "article_01" 或 "article_01_section_03"。"""
    if node_id in wanted:
        return True
    m = re.match(r"article_(\d+)", node_id)
    if m:
        article_num = m.group(1).lstrip("0") or "0"
        return article_num in wanted
    return node_id in wanted


def main():
    ap = argparse.ArgumentParser(description="优化 Wiki 概念页面 — 双层架构")
    ap.add_argument("doc_yaml_path", help="document.yaml 路径")
    ap.add_argument("--nodes", default=None, help="只处理指定节点ID，逗号分隔")
    ap.add_argument("--no-backup", action="store_true", help="不创建备份")
    ap.add_argument("--rebuild-core", action="store_true",
                    help="从 chunks 重建核心内容（覆盖 compile_wiki 的截断）")
    ap.add_argument("--mechanical-clean", action="store_true",
                    help="Python 机械层清洗（去重/OCR/行末垃圾/交叉引用/间距）+ 备份")
    args = ap.parse_args()

    doc_yaml_path = Path(args.doc_yaml_path).resolve()
    doc_config, profile, doc_yaml_dir = load_config(doc_yaml_path)

    topic = doc_config.get("topic", "")
    doc_output = doc_config.get("output", {})
    profile_output = profile.get("output", {})
    chunks_dir_name = doc_output.get("chunks_dir") or profile_output.get("chunks_dir", "chunks")
    chunks_dir = doc_yaml_dir / chunks_dir_name

    concepts_dir_raw = doc_output.get("concepts_dir") or profile_output.get("concepts_dir")
    if concepts_dir_raw:
        concepts_dir = Path(concepts_dir_raw)
        if not concepts_dir.is_absolute():
            project_root = doc_yaml_dir.parent.parent.parent.parent
            concepts_dir = (project_root / concepts_dir_raw).resolve()
    else:
        project_root = doc_yaml_dir.parent.parent.parent.parent
        concepts_dir = (project_root / "wiki" / "concepts" / topic).resolve()

    if not concepts_dir.exists():
        print(f"概念页面目录不存在: {concepts_dir}")
        sys.exit(1)

    # 确定目标文件
    if args.nodes:
        wanted = set(args.nodes.split(","))
        md_files = sorted(f for f in concepts_dir.glob("*.md")
                          if _matches_wanted(f.stem, wanted) and "index" not in f.stem)
    else:
        md_files = sorted(f for f in concepts_dir.glob("*.md")
                          if "index" not in f.stem)

    if not md_files:
        print("没有找到要优化的 MD 文件")
        sys.exit(1)

    # ─── 备份 ───
    if not args.no_backup and (args.rebuild_core or args.mechanical_clean):
        backup_dir = doc_yaml_dir / "unoptimized"
        backup_dir.mkdir(parents=True, exist_ok=True)
        for f in md_files:
            shutil.copy2(f, backup_dir / f.name)
        print(f"已备份 {len(md_files)} 个文件到 {backup_dir}")

    # ─── --rebuild-core: 从 chunk 重建核心内容 ───
    if args.rebuild_core:
        for md_path in md_files:
            aid = md_path.stem
            # 从新版命名中提取原始 article_id: article_01_section_04 → 1, article_01 → 1
            raw_id = aid
            sec_m = re.match(r"article_(\d+)(?:_section_\d+)?", aid)
            if sec_m:
                raw_id = sec_m.group(1)
            full_text = merge_chunk_parts(chunks_dir, raw_id)
            if not full_text:
                print(f"  跳过 {aid}: 无 chunk 文件")
                continue
            page = md_path.read_text(encoding="utf-8")
            core_start = page.find("## 核心内容")
            key_start = page.find("## 关键条款 / 关键观点")
            if core_start == -1:
                print(f"  跳过 {aid}: 无核心内容节")
                continue
            before = page[:core_start]
            after = page[key_start:] if key_start >= 0 else ""
            core_marker = "## 核心内容\n\n<!-- RAW CHUNK — Python 机械层 + LLM 精修 -->\n\n"
            new_page = before + core_marker + full_text + "\n\n" + after
            md_path.write_text(new_page, encoding="utf-8")
            print(f"  重建核心内容: {md_path.name} ({len(full_text)} 原始字符)")

    # ─── --mechanical-clean: Python 机械清洗 ───
    if args.mechanical_clean:
        existing_pages = get_existing_pages(concepts_dir)
        total_stats = {"dedup": 0, "garbage": 0, "ocr_fix": 0, "xref": 0, "junk": 0}

        for md_path in md_files:
            aid = md_path.stem
            page = md_path.read_text(encoding="utf-8")

            # 找到核心内容节
            core_start = page.find("## 核心内容")
            key_start = page.find("## 关键条款 / 关键观点")
            if core_start == -1:
                continue
            before = page[:core_start]
            after = page[key_start:] if key_start >= 0 else ""

            # 提取原始文本（跳过 <!-- RAW CHUNK --> 标记）
            raw_search_start = core_start + len("## 核心内容")
            chunk_marker_end = page.find("-->", raw_search_start)
            text_start = (chunk_marker_end + 3) if chunk_marker_end >= 0 else raw_search_start
            raw_text = page[text_start:key_start].strip() if key_start >= 0 else page[text_start:].strip()

            if not raw_text:
                print(f"  跳过 {aid}: 核心内容为空")
                continue

            # 机械清洗
            cleaned, stats = mechanical_clean(raw_text, aid, topic, existing_pages)
            for k, v in stats.items():
                total_stats[k] += v

            # 重新组合页面
            new_page = before + "## 核心内容\n\n" + cleaned + "\n\n" + after
            new_page = new_page.replace('\r\n', '\n')
            # 去重 provenance 标记
            new_page = re.sub(r'(\^\[raw/[^\]]+\])\s*\n\s*\^\[raw/[^\]]+\]', r'\1', new_page)
            # 修正 after 段中的旧格式 wikilink（编译阶段生成的链接）
            new_page = re.sub(
                r'\[\[concepts/' + re.escape(topic) + r'/(\d+[A-Za-z]?)([\]\|])',
                r'[[concepts/' + topic + r'/article_\1\2',
                new_page
            )
            new_page = re.sub(
                r'\[\[concepts/' + re.escape(topic) + r'/(\d+)#clause-',
                r'[[concepts/' + topic + r'/article_\1#clause-',
                new_page
            )
            md_path.write_text(new_page, encoding="utf-8")

            clause_count = len(re.findall(r'^\d+\.\d+[A-Za-z]?\s', cleaned, re.MULTILINE))
            section_count = len(re.findall(r'^第[IVXLCDM]+节\s*[-–—]', cleaned, re.MULTILINE))
            print(f"  机械清洗: {md_path.name} → {clause_count}条款 {section_count}节")

        # 记录到 parse_notes.md
        notes_path = doc_yaml_dir / "parsed" / "parse_notes.md"
        parse_notes = notes_path.read_text(encoding="utf-8") if notes_path.exists() else ""
        preserve = profile.get("preserve", {})
        llm_items = [k for k in ("tables", "footnotes", "wrc_revision", "printed_page",
                                  "article_number", "clause_number", "cross_references")
                     if preserve.get(k, False)]

        section = (
            "## optimize_wiki_pages.py — Python 机械层\n\n"
            f"- 去重: {total_stats['dedup']} 行\n"
            f"- 垃圾行: {total_stats['garbage']} 行\n"
            f"- OCR 错字: {'是' if total_stats['ocr_fix'] else '否'}\n"
            f"- 行末垃圾: {total_stats['junk']} 处\n"
            f"- 交叉引用: {total_stats['xref']} 个链接\n"
            "\n### 待 LLM 精修\n\n"
            "Python 机械层已完成清洗（去重、垃圾行、OCR修正、条款合并、交叉引用）。\n"
            "**所有表格识别与重建由 LLM 全权负责：**\n"
            "1. **条款→定义表格**：将条款号+定义文本转为 `| 条款 | 定义 |` 表格（包括单条款）\n"
            "2. **内联表格重建**：检测合一条款中的内联结构化数据，重建为 Markdown 表格\n"
            "   - 频段划分表（频段序号+符号+频率范围+米制细分）\n"
            "   - 多语种术语对照表（中文+法文+英文+西班牙文+阿拉伯文+俄文）\n"
            "   - 任何其他 PDF 压平的结构化数据\n"
            "3. **残行修正**、**交叉引用审查**、**脚注归属**、**页码格式化**、**一致性检查**\n"
        )
        if llm_items:
            section += f"\npreserve 标记参考: {', '.join(llm_items)}\n"

        notes_path.write_text(parse_notes.rstrip() + "\n\n" + section, encoding="utf-8")
        print(f"\n机械层完成。详细记录 -> parse_notes.md")


if __name__ == "__main__":
    main()
