from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


COUNTRY_SLUG_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")


class KnowledgeBaseError(RuntimeError):
    """Raised when required knowledge-base material is missing or invalid."""


@dataclass(frozen=True)
class ContextDocument:
    path: Path
    content: str


CASE_RETRIEVAL_TERMS: dict[str, tuple[str, ...]] = {
    "00": (
        "卫星通信网络",
        "第 9.10",
        "频率许可",
        "设备合格",
        "地球站",
        "投资法",
    ),
    "01": (
        "卫星通信网络",
        "许可组合",
        "遴选",
        "频率许可",
        "设备合格",
        "地球站",
    ),
    "02": (
        "外国",
        "本地主体",
        "境外法人",
        "投资",
        "市场准入",
        "第 7.1",
        "MSS",
        "NTN",
    ),
    "03": (
        "卫星通信网络",
        "服务特别许可",
        "服务授权",
        "集体利益服务",
        "服务通知",
        "第 9.10",
        "遴选",
        "通信法",
        "许可法",
        "资费",
        "service authorization",
        "Mosaico",
        "SCM",
        "SMP",
    ),
    "04": (
        "无线电频率",
        "无线电波法",
        "频段",
        "第 9.8",
        "ITU",
        "国际组织",
        "干扰",
        "协调",
        "国家频率划分表",
    ),
    "05": (
        "设备",
        "合格证",
        "认证",
        "EMC",
        "RF",
        "测试报告",
    ),
    "06": (
        "地球站",
        "网关",
        "站点",
        "土地",
        "坐标",
        "覆盖",
        "发射机",
        "TT&C",
    ),
    "07": (
        "费用",
        "收费",
        "费率",
        "权利费",
        "服务费",
        "频段使用费",
    ),
    "08": (
        "法律",
        "法规",
        "决议",
        "许可法",
        "通信法",
        "无线电波法",
        "投资法",
        "收费规则",
        "第 37/2022",
    ),
    "09": (
        "限制",
        "待确认",
        "MSS",
        "NTN",
        "外国",
        "频率",
        "设备",
        "地球站",
        "费用",
    ),
    "10": (
        "核心结论",
        "双许可",
        "待确认",
        "卫星开发权",
        "服务授权",
        "协调",
        "设备认证",
        "homologation",
        "地球站",
        "费用",
        "MSS",
        "NTN",
        "频率许可",
        "卫星通信网络",
    ),
}


CASE_NOTE_LIMITS = {
    "00": 9,
    "01": 7,
    "02": 6,
    "03": 6,
    "04": 7,
    "05": 4,
    "06": 5,
    "07": 5,
    "08": 11,
    "09": 8,
    "10": 11,
}


CASE_REQUIRED_NOTE_STEMS = {
    "01": (
        "br-res-748-2021",
        "br-anatel-satellite-rights-page",
        "br-res-720-2020",
        "br-res-777-2025",
        "br-anatel-collective-services",
        "br-anatel-product-certification",
        "br-anatel-earth-station-licensing",
    ),
    "02": (
        "br-res-748-2021",
        "br-act-9526-2021",
        "br-anatel-satellite-rights-page",
        "br-anatel-satellite-rights-manual-2023",
    ),
    "03": (
        "br-anatel-collective-services",
        "br-res-720-2020",
        "br-res-777-2025",
        "br-res-748-2021",
    ),
    "04": (
        "mn-legal-radio-waves-law",
        "br-res-748-2021",
        "br-anatel-satellite-rights-page",
        "br-anatel-satellite-rights-manual-2023",
        "br-act-9523-2021",
        "br-act-9426-2021",
    ),
    "05": (
        "br-res-715-2019",
        "br-anatel-product-certification",
        "br-anatel-ocd-list",
    ),
    "06": (
        "br-res-719-2020",
        "br-anatel-earth-station-licensing",
        "br-anatel-satellite-rights-page",
    ),
    "07": (
        "mn-legal-radio-frequency-fee-rule",
        "br-res-748-2021",
        "br-anatel-satellite-rights-page",
        "br-anatel-collective-services",
        "br-law-5070-1966",
    ),
    "08": ("mn-legal-radio-frequency-fee-rule",),
    "10": (
        "br-res-748-2021",
        "br-act-9526-2021",
        "br-anatel-satellite-rights-page",
        "br-anatel-satellite-rights-manual-2023",
        "br-res-720-2020",
        "br-res-777-2025",
        "br-anatel-collective-services",
        "br-anatel-product-certification",
        "br-anatel-ocd-list",
        "br-anatel-earth-station-licensing",
        "br-law-5070-1966",
    ),
}


def validate_country_slug(country: str) -> str:
    normalized = country.strip().lower().replace("-", "_").replace(" ", "_")
    if not COUNTRY_SLUG_RE.fullmatch(normalized):
        raise KnowledgeBaseError(
            "国家参数必须使用英文小写 slug，例如 mongolia、thailand、south_africa。"
        )
    return normalized


def ensure_repo_root(root: Path) -> Path:
    root = root.expanduser().resolve()
    required = (root / "AGENTS.md", root / "wiki" / "concepts" / "landing_rights")
    if not all(path.exists() for path in required):
        raise KnowledgeBaseError(
            f"{root} 不是有效项目根目录：缺少 AGENTS.md 或 landing_rights Wiki。"
        )
    return root


def _existing_files(paths: Iterable[Path]) -> list[Path]:
    result: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        if path.is_file() and path not in seen:
            result.append(path)
            seen.add(path)
    return result


def _glob_files(directory: Path, pattern: str = "*.md") -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted(path for path in directory.glob(pattern) if path.is_file())


def _rank_paths(
    paths: Sequence[Path],
    terms: Sequence[str],
    *,
    limit: int,
) -> list[Path]:
    ranked: list[tuple[int, str, Path]] = []
    normalized_terms = tuple(term.casefold() for term in terms if term.strip())
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace").casefold()
        name = path.stem.casefold()
        score = 0
        for term in normalized_terms:
            if term in name:
                score += 12
            occurrences = min(text.count(term), 8)
            score += occurrences
            if term in text[:3000]:
                score += 3
        ranked.append((score, path.name, path))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    positive = [path for score, _, path in ranked if score > 0]
    return positive[:limit]


def _ensure_required_notes(
    selected: Sequence[Path],
    available: Sequence[Path],
    required_stems: Sequence[str],
    *,
    limit: int,
) -> list[Path]:
    by_stem = {path.stem: path for path in available}
    required_paths: list[Path] = []
    for stem in required_stems:
        required = by_stem.get(stem)
        if required is not None and required not in required_paths:
            required_paths.append(required)
    ranked_paths = [path for path in selected if path not in required_paths]
    return (required_paths + ranked_paths)[:limit]


def _source_note_files(root: Path, country: str) -> list[Path]:
    notes_dir = root / "wiki" / "raw" / "landing_rights" / country / "source_notes"
    return [
        path
        for path in _glob_files(notes_dir)
        if path.name != "source_notes_index.md"
    ]


def _source_notes_index(root: Path, country: str) -> Path:
    return (
        root
        / "wiki"
        / "raw"
        / "landing_rights"
        / country
        / "source_notes"
        / "source_notes_index.md"
    )


def _inventory(root: Path, country: str) -> Path:
    return root / "wiki" / "raw" / "landing_rights" / country / "source_inventory.md"


def _build_common_files(root: Path) -> list[Path]:
    common = root / "wiki" / "concepts" / "landing_rights" / "common"
    return [
        common / "country_landing_rights_sop.md",
        common / "source_priority_rules.md",
        common / "open_questions_template.md",
    ]


def _brazil_structure_file(root: Path, number: str) -> Path | None:
    brazil = root / "wiki" / "concepts" / "landing_rights" / "cases" / "brazil"
    matches = _glob_files(brazil, f"{number}_brazil_*.md")
    return matches[0] if matches else None


def _structure_document(root: Path, path: Path) -> ContextDocument:
    text = path.read_text(encoding="utf-8", errors="replace")
    front_matter = re.match(r"\A---\s*\n(.*?)\n---", text, re.DOTALL)
    yaml_keys: list[str] = []
    if front_matter:
        yaml_keys = re.findall(r"^([a-z_]+):", front_matter.group(1), re.MULTILINE)
    headings = re.findall(r"^(#{1,4}\s+.+)$", text, re.MULTILINE)
    content = [
        "[仅作 Markdown 结构样板，不得复述其中的巴西事实、法规或结论]",
        "YAML 字段：" + ", ".join(yaml_keys),
        "章节结构：",
        *headings,
    ]
    return ContextDocument(path=path.relative_to(root), content="\n".join(content))


def _markdown_h2_section(text: str, number: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(number)}\.\s+.*?\n(.*?)(?=^##\s+|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(0).strip() if match else ""


def _compact_source_note_document(root: Path, path: Path) -> ContextDocument:
    text = path.read_text(encoding="utf-8", errors="replace")
    metadata: list[str] = [f"source_id: {path.stem}"]
    for key in ("source_name", "source_url", "source_agency", "source_type"):
        match = re.search(rf"^{key}:\s*(.+)$", text, re.MULTILINE)
        if match:
            metadata.append(f"{key}: {match.group(1).strip()}")
    sections = [
        section
        for number in ("2", "4", "5")
        if (section := _markdown_h2_section(text, number))
    ]
    if not sections:
        sections = [text[:4000]]
    content = "\n".join(
        [
            "[目标国官方来源证据包；法规名称、条款号与结论不得交叉归属]",
            *metadata,
            *sections,
        ]
    )
    return ContextDocument(path=path.relative_to(root), content=content)


def load_documents(
    root: Path,
    paths: Sequence[Path],
    *,
    max_chars: int = 400_000,
    per_file_max_chars: int = 100_000,
) -> list[ContextDocument]:
    documents: list[ContextDocument] = []
    used = 0
    for path in _existing_files(paths):
        text = path.read_text(encoding="utf-8", errors="replace")
        if len(text) > per_file_max_chars:
            text = text[:per_file_max_chars] + "\n\n[文件内容因长度限制被截断]\n"
        remaining = max_chars - used
        if remaining <= 0:
            break
        if len(text) > remaining:
            text = text[:remaining] + "\n\n[上下文因总长度限制被截断]\n"
        documents.append(ContextDocument(path=path.relative_to(root), content=text))
        used += len(text)
    return documents


def render_context(documents: Sequence[ContextDocument]) -> str:
    if not documents:
        return "[本地知识库没有找到可用文件]"
    sections = []
    for document in documents:
        sections.append(
            f"\n===== FILE: {document.path.as_posix()} =====\n{document.content.strip()}\n"
        )
    return "".join(sections).strip()


def common_files(root: Path) -> list[Path]:
    common = root / "wiki" / "concepts" / "landing_rights" / "common"
    preferred = [
        "country_landing_rights_sop.md",
        "license_type_overview.md",
        "information_extraction_checklist.md",
        "source_priority_rules.md",
        "open_questions_template.md",
        "md_file_format_rules.md",
        "source_inventory_template.md",
        "source_note_template.md",
    ]
    return [common / name for name in preferred]


def country_case_files(root: Path, country: str) -> list[Path]:
    directory = root / "wiki" / "concepts" / "landing_rights" / "cases" / country
    return _glob_files(directory)


def country_raw_files(root: Path, country: str) -> list[Path]:
    raw = root / "wiki" / "raw" / "landing_rights" / country
    paths = [raw / "source_inventory.md"]
    paths.extend(_glob_files(raw / "source_notes"))
    return paths


def answer_context(root: Path, country: str) -> str:
    return answer_context_for_question(root, country, "卫星落地许可")


def answer_context_for_question(root: Path, country: str, question: str) -> str:
    terms = _terms_for_question(question)
    cases = country_case_files(root, country)
    preferred_cases = [
        path
        for path in cases
        if path.name.startswith(("00_", "10_"))
    ]
    selected_cases = _rank_paths(cases, terms, limit=4)
    notes = _rank_paths(_source_note_files(root, country), terms, limit=5)
    paths = _build_common_files(root)[:2]
    paths.extend([_inventory(root, country), _source_notes_index(root, country)])
    paths.extend(notes)
    paths.extend(preferred_cases)
    paths.extend(selected_cases)
    return render_context(load_documents(root, paths, max_chars=180_000))


def research_context(root: Path, country: str, question: str = "") -> str:
    brazil = root / "wiki" / "concepts" / "landing_rights" / "cases" / "brazil"
    common = root / "wiki" / "concepts" / "landing_rights" / "common"
    paths = [
        common / "country_landing_rights_sop.md",
        common / "information_extraction_checklist.md",
        common / "source_priority_rules.md",
        common / "source_inventory_template.md",
        common / "source_note_template.md",
    ]
    paths.extend(
        [
            brazil / "00_brazil_case_index.md",
            brazil / "01_brazil_landing_overview.md",
            brazil / "09_brazil_reusable_experience.md",
        ]
    )
    paths.extend([_inventory(root, country), _source_notes_index(root, country)])
    paths.extend(
        _rank_paths(
            _source_note_files(root, country),
            _terms_for_question(question),
            limit=5,
        )
    )
    return render_context(load_documents(root, paths, max_chars=220_000))


def _terms_for_question(question: str) -> tuple[str, ...]:
    value = question.casefold()
    matched: list[str] = []
    for terms in CASE_RETRIEVAL_TERMS.values():
        if any(term.casefold() in value for term in terms):
            matched.extend(terms)
    if not matched:
        matched.extend(CASE_RETRIEVAL_TERMS["01"])
    return tuple(dict.fromkeys(matched))


def build_file_documents(
    root: Path,
    country: str,
    *,
    number: str,
) -> list[ContextDocument]:
    number = number.zfill(2)
    if number not in CASE_RETRIEVAL_TERMS:
        raise KnowledgeBaseError(f"未知案例文件编号：{number}")
    available_notes = _source_note_files(root, country)
    notes = _rank_paths(
        available_notes,
        CASE_RETRIEVAL_TERMS[number],
        limit=CASE_NOTE_LIMITS[number],
    )
    notes = _ensure_required_notes(
        notes,
        available_notes,
        CASE_REQUIRED_NOTE_STEMS.get(number, ()),
        limit=CASE_NOTE_LIMITS[number],
    )
    paths = _build_common_files(root)
    if number == "00":
        paths.extend([_inventory(root, country), _source_notes_index(root, country)])
    elif number == "08":
        paths.append(_inventory(root, country))
    documents: list[ContextDocument] = []
    brazil_file = _brazil_structure_file(root, number)
    if brazil_file is not None:
        documents.append(_structure_document(root, brazil_file))
    documents.extend(
        load_documents(
            root,
            paths,
            max_chars=80_000,
            per_file_max_chars=30_000,
        )
    )
    documents.extend(
        _compact_source_note_document(root, path) for path in reversed(notes)
    )
    return documents


def build_file_context(root: Path, country: str, *, number: str) -> str:
    return render_context(build_file_documents(root, country, number=number))


def require_source_notes(root: Path, country: str, minimum: int = 3) -> list[Path]:
    raw = root / "wiki" / "raw" / "landing_rights" / country
    inventory = raw / "source_inventory.md"
    notes = [
        path
        for path in _glob_files(raw / "source_notes")
        if path.name != "source_notes_index.md"
    ]
    if not inventory.exists() or len(notes) < minimum:
        raise KnowledgeBaseError(
            f"{country} 的证据层不足：需要 source_inventory.md 和至少 {minimum} 个 "
            "source notes。请先运行 research 并人工核验、抓取官方来源。"
        )
    return notes
