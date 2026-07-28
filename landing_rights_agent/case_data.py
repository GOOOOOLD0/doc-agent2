from __future__ import annotations

import json
import re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Mapping, Sequence

from .knowledge import ContextDocument
from .validation import GeneratedFileError


EVIDENCE_ITEM_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "source_id": {"type": "string"},
        "evidence_quote": {"type": "string"},
    },
    "required": ["text", "source_id", "evidence_quote"],
    "additionalProperties": False,
}


SECTION_ITEM_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "status": {
            "type": "string",
            "enum": ["confirmed", "pending"],
        },
        "text": {"type": "string"},
        "source_id": {"type": "string"},
        "evidence_quote": {"type": "string"},
    },
    "required": ["status", "text", "source_id", "evidence_quote"],
    "additionalProperties": False,
}


CASE_DATA_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "purpose": {"type": "string"},
        "confirmed": {
            "type": "array",
            "items": EVIDENCE_ITEM_SCHEMA,
        },
        "inferences": {
            "type": "array",
            "maxItems": 0,
            "items": EVIDENCE_ITEM_SCHEMA,
        },
        "pending": {
            "type": "array",
            "items": {"type": "string"},
        },
        "sections": {
            "type": "array",
            "minItems": 5,
            "maxItems": 5,
            "items": {
                "type": "object",
                "properties": {
                    "number": {"type": "integer", "enum": [3, 4, 5, 6, 7]},
                    "heading": {"type": "string"},
                    "items": {
                        "type": "array",
                        "items": SECTION_ITEM_SCHEMA,
                    },
                },
                "required": ["number", "heading", "items"],
                "additionalProperties": False,
            },
        },
        "sources": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "label": {"type": "string"},
                    "url": {"type": "string"},
                },
                "required": ["label", "url"],
                "additionalProperties": False,
            },
        },
        "related_files": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": [
        "title",
        "purpose",
        "confirmed",
        "inferences",
        "pending",
        "sections",
        "sources",
        "related_files",
    ],
    "additionalProperties": False,
}


@dataclass(frozen=True)
class EvidenceItem:
    text: str
    source_id: str
    evidence_quote: str


@dataclass(frozen=True)
class SectionItem:
    status: str
    text: str
    source_id: str = ""
    evidence_quote: str = ""


@dataclass(frozen=True)
class CaseSection:
    number: int
    heading: str
    items: tuple[SectionItem, ...]


@dataclass(frozen=True)
class SourceLink:
    label: str
    url: str


@dataclass(frozen=True)
class CaseData:
    title: str
    purpose: str
    confirmed: tuple[EvidenceItem, ...]
    inferences: tuple[EvidenceItem, ...]
    pending: tuple[str, ...]
    sections: tuple[CaseSection, ...]
    sources: tuple[SourceLink, ...]
    related_files: tuple[str, ...]


def constrain_machine_case_data(
    data: CaseData,
    *,
    documents: Sequence[ContextDocument] | None = None,
) -> CaseData:
    source_tokens: set[str] | None = None
    if documents is not None:
        source_text = "\n".join(
            document.content
            for document in documents
            if "/source_notes/" in f"/{document.path.as_posix()}"
        )
        source_tokens = set(
            re.findall(
                r"\b[A-Z][A-Z0-9/&-]{1,}\b|\d+(?:\.\d+)*",
                source_text,
            )
        )

    def pending_is_supported(text: str) -> bool:
        if source_tokens is None:
            return True
        pending_tokens = set(
            re.findall(r"\b[A-Z][A-Z0-9/&-]{1,}\b|\d+(?:\.\d+)*", text)
        )
        return pending_tokens <= source_tokens

    sections: list[CaseSection] = []
    for section in data.sections:
        safe_items = tuple(
            item
            for item in section.items
            if item.status == "confirmed"
            or (
                item.status == "pending"
                and pending_is_supported(item.text)
            )
        )
        if not safe_items:
            safe_items = (
                SectionItem(
                    status="pending",
                    text="本节尚无可直接引用的官方来源原文，需人工复核。",
                ),
            )
        sections.append(replace(section, items=safe_items))
    return replace(
        data,
        inferences=(),
        pending=tuple(
            item for item in data.pending if pending_is_supported(item)
        ),
        sections=tuple(sections),
    )


def _required_string(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GeneratedFileError(f"结构化案例字段 {field} 必须是非空字符串")
    return value.strip()


def _required_list(value: Any, *, field: str) -> list[Any]:
    if not isinstance(value, list):
        raise GeneratedFileError(f"结构化案例字段 {field} 必须是数组")
    return value


def _parse_evidence_item(value: Any, *, field: str) -> EvidenceItem:
    if not isinstance(value, Mapping):
        raise GeneratedFileError(f"{field} 中的条目必须是对象")
    source_id = _required_string(
        value.get("source_id"), field=f"{field}.source_id"
    )
    evidence_quote = _required_string(
        value.get("evidence_quote"), field=f"{field}.evidence_quote"
    )
    text = str(value.get("text") or "").strip() or evidence_quote
    return EvidenceItem(
        text=text,
        source_id=source_id,
        evidence_quote=evidence_quote,
    )


def parse_case_data(raw: str) -> CaseData:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise GeneratedFileError(f"模型没有返回合法 JSON：{exc}") from exc
    if not isinstance(value, Mapping):
        raise GeneratedFileError("模型返回的 JSON 顶层必须是对象")

    confirmed = tuple(
        _parse_evidence_item(item, field="confirmed")
        for item in _required_list(value.get("confirmed"), field="confirmed")
    )
    inferences = tuple(
        _parse_evidence_item(item, field="inferences")
        for item in _required_list(value.get("inferences"), field="inferences")
    )
    sections: list[CaseSection] = []
    for raw_section in _required_list(value.get("sections"), field="sections"):
        if not isinstance(raw_section, Mapping):
            raise GeneratedFileError("sections 中的条目必须是对象")
        section_number = raw_section.get("number")
        if not isinstance(section_number, int):
            raise GeneratedFileError("sections.number 必须是整数")
        items: list[SectionItem] = []
        for raw_item in _required_list(
            raw_section.get("items"), field=f"sections.{section_number}.items"
        ):
            if not isinstance(raw_item, Mapping):
                raise GeneratedFileError("sections.items 中的条目必须是对象")
            status = _required_string(
                raw_item.get("status"), field="sections.items.status"
            )
            if status not in {"confirmed", "inference", "pending"}:
                raise GeneratedFileError(f"未知条目状态：{status}")
            source_id = str(raw_item.get("source_id") or "").strip()
            evidence_quote = str(
                raw_item.get("evidence_quote") or ""
            ).strip()
            text = str(raw_item.get("text") or "").strip()
            if status == "pending" and not text:
                text = "本节尚无可直接引用的官方来源原文，需人工复核。"
            elif status != "pending" and not text:
                text = evidence_quote
            if not text:
                raise GeneratedFileError(
                    "结构化案例字段 sections.items.text 必须是非空字符串"
                )
            items.append(
                SectionItem(
                    status=status,
                    text=text,
                    source_id=source_id,
                    evidence_quote=evidence_quote,
                )
            )
        sections.append(
            CaseSection(
                number=section_number,
                heading=_required_string(
                    raw_section.get("heading"), field="sections.heading"
                ),
                items=tuple(items),
            )
        )

    sources: list[SourceLink] = []
    for raw_source in _required_list(value.get("sources"), field="sources"):
        if not isinstance(raw_source, Mapping):
            raise GeneratedFileError("sources 中的条目必须是对象")
        sources.append(
            SourceLink(
                label=_required_string(raw_source.get("label"), field="sources.label"),
                url=_required_string(raw_source.get("url"), field="sources.url"),
            )
        )

    return CaseData(
        title=_required_string(value.get("title"), field="title"),
        purpose=_required_string(value.get("purpose"), field="purpose"),
        confirmed=confirmed,
        inferences=inferences,
        pending=tuple(
            str(item).strip()
            for item in _required_list(value.get("pending"), field="pending")
            if isinstance(item, str) and item.strip()
        ),
        sections=tuple(sections),
        sources=tuple(sources),
        related_files=tuple(
            _required_string(item, field="related_files")
            for item in _required_list(
                value.get("related_files"), field="related_files"
            )
        ),
    )


def _normalize_evidence(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _canonical_evidence(value: str) -> str:
    normalized = _normalize_evidence(value).casefold()
    return "".join(
        character
        for character in normalized
        if character.isalnum() or character in {".", "/", "-", "_"}
    )


def _evidence_quote_in_source(quote: str, source: str) -> bool:
    canonical_quote = _canonical_evidence(quote)
    lines = [
        _canonical_evidence(line)
        for line in source.splitlines()
        if line.strip()
    ]
    candidates = list(lines)
    candidates.extend(
        first + second
        for first, second in zip(lines, lines[1:])
    )
    return any(canonical_quote in candidate for candidate in candidates)


def _source_note_map(
    documents: Sequence[ContextDocument],
) -> dict[str, str]:
    return {
        document.path.stem: document.content
        for document in documents
        if "/source_notes/" in f"/{document.path.as_posix()}"
    }


def _validate_evidence_item(
    item: EvidenceItem | SectionItem,
    *,
    source_notes: Mapping[str, str],
    field: str,
) -> None:
    source = source_notes.get(item.source_id)
    if source is None:
        raise GeneratedFileError(
            f"{field} 引用了未提供的 source_id：{item.source_id}"
        )
    quote = _normalize_evidence(item.evidence_quote)
    if len(quote) < 8:
        raise GeneratedFileError(f"{field} 的 evidence_quote 过短")
    if not _evidence_quote_in_source(quote, source):
        raise GeneratedFileError(
            f"{field} 的 evidence_quote 不是 source note 中的连续原文"
        )

def validate_case_data(
    data: CaseData,
    *,
    documents: Sequence[ContextDocument],
    allowed_related_files: Sequence[str],
) -> None:
    source_notes = _source_note_map(documents)
    if not source_notes:
        raise GeneratedFileError("结构化案例没有可用 source notes")
    if not data.confirmed:
        raise GeneratedFileError("结构化案例至少需要一条已确认信息")
    if data.inferences:
        raise GeneratedFileError(
            "机器生成案例暂不接受自由推断；inferences 必须为空数组"
        )
    for index, item in enumerate(data.confirmed):
        _validate_evidence_item(
            item,
            source_notes=source_notes,
            field=f"confirmed[{index}]",
        )

    section_numbers = [section.number for section in data.sections]
    if section_numbers != [3, 4, 5, 6, 7]:
        raise GeneratedFileError("sections 必须按顺序且仅包含 3、4、5、6、7")
    for section in data.sections:
        if not section.items:
            raise GeneratedFileError(f"第 {section.number} 节不得为空")
        for index, item in enumerate(section.items):
            if item.status == "pending":
                continue
            if item.status != "confirmed":
                raise GeneratedFileError(
                    f"第 {section.number} 节只能包含 confirmed 或 pending 条目"
                )
            _validate_evidence_item(
                item,
                source_notes=source_notes,
                field=f"sections[{section.number}].items[{index}]",
            )

    all_source_text = "\n".join(source_notes.values())
    all_source_tokens = set(
        re.findall(
            r"\b[A-Z][A-Z0-9/&-]{1,}\b|\d+(?:\.\d+)*",
            all_source_text,
        )
    )
    for index, item in enumerate(data.pending):
        pending_tokens = set(
            re.findall(r"\b[A-Z][A-Z0-9/&-]{1,}\b|\d+(?:\.\d+)*", item)
        )
        unknown_tokens = sorted(pending_tokens - all_source_tokens)
        if unknown_tokens:
            raise GeneratedFileError(
                f"pending[{index}] 出现全部 source notes 均未包含的缩写或数字："
                f"{', '.join(unknown_tokens[:5])}"
            )

    allowed_urls = {
        match
        for source in source_notes.values()
        for match in re.findall(r"https?://[^\s<>\]\)）】。，；、]+", source)
    }
    for source in data.sources:
        if source.url not in allowed_urls:
            raise GeneratedFileError(f"官方来源 URL 未出现在 source notes：{source.url}")

    allowed_related = set(allowed_related_files)
    unknown_related = sorted(set(data.related_files) - allowed_related)
    if unknown_related:
        raise GeneratedFileError(
            "相关文件出现未知文件名：" + ", ".join(unknown_related[:5])
        )


def _render_evidence_item(item: EvidenceItem, *, inference: bool = False) -> str:
    marker = "推断依据" if inference else "依据"
    return f"- {item.evidence_quote}（{marker}：{item.source_id}）"


def render_case_markdown(
    data: CaseData,
    *,
    country: str,
    topic: str,
    purpose: str | None = None,
) -> str:
    lines = [
        "---",
        f"country: {country.replace('_', ' ').title()}",
        f"topic: {topic}",
        "case_type: structured_case",
        f"source_document: {country}_official_source_notes",
        "language: zh-CN",
        "review_status: machine_generated",
        "---",
        "",
        f"# {data.title}",
        "",
        "## 1. 文件用途",
        "",
        purpose or data.purpose,
        "",
        "## 2. 结论摘要",
        "",
        "### 2.1 已确认信息",
        "",
        *(_render_evidence_item(item) for item in data.confirmed),
        "",
        "### 2.2 分析推断",
        "",
    ]
    lines.append("未在公开官方资料中确认可安全形成的额外推断。")
    lines.extend(["", "### 2.3 待确认事项", ""])
    lines.extend(f"- {item}" for item in data.pending)

    for section in data.sections:
        lines.extend(["", f"## {section.number}. {section.heading}", ""])
        for item in section.items:
            if item.status == "confirmed":
                lines.append(
                    f"- {item.evidence_quote}（依据：{item.source_id}）"
                )
            else:
                lines.append(f"- 待确认：{item.text}")

    lines.extend(["", "## 8. 官方来源", ""])
    lines.extend(f"- [{source.label}]({source.url})" for source in data.sources)
    lines.extend(["", "## 9. 相关文件", ""])
    lines.extend(
        f"- [[{Path(filename).stem}]]" for filename in data.related_files
    )
    return "\n".join(lines).rstrip() + "\n"
