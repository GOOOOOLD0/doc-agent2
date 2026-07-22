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
    paths = [root / "AGENTS.md"]
    paths.extend(common_files(root))
    paths.extend(country_raw_files(root, country))
    paths.extend(country_case_files(root, country))
    return render_context(load_documents(root, paths))


def research_context(root: Path, country: str) -> str:
    brazil = root / "wiki" / "concepts" / "landing_rights" / "cases" / "brazil"
    paths = [root / "AGENTS.md"]
    paths.extend(common_files(root))
    paths.extend(
        [
            brazil / "00_brazil_case_index.md",
            brazil / "01_brazil_landing_overview.md",
            brazil / "09_brazil_reusable_experience.md",
        ]
    )
    paths.extend(country_raw_files(root, country))
    return render_context(load_documents(root, paths))


def build_context(root: Path, country: str) -> str:
    brazil = root / "wiki" / "concepts" / "landing_rights" / "cases" / "brazil"
    paths = [root / "AGENTS.md"]
    paths.extend(common_files(root))
    paths.extend(country_raw_files(root, country))
    paths.extend(country_case_files(root, country))
    paths.extend(_glob_files(brazil))
    return render_context(load_documents(root, paths, max_chars=650_000))


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
