from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


CASE_FILES = {
    "01": "landing_overview",
    "02": "foreign_satellite_rights",
    "03": "service_authorization",
    "04": "frequency_coordination",
    "05": "equipment_certification",
    "06": "station_licensing",
    "07": "fee_list",
    "08": "regulations",
    "09": "reusable_experience",
}

MATRIX_FIELDS = (
    "状态",
    "结论",
    "依据",
    "能够支持",
    "不能支持",
    "边界与风险",
    "目标文件",
    "待确认",
)

MATRIX_STATUSES = {"已确认", "分析推断", "待确认"}
PLACEHOLDER_RE = re.compile(
    r"\{\{[^}]+\}\}|<country>|<source_id>|\b(?:TODO|TBD|FIXME)\b",
    re.IGNORECASE,
)
LINE_PREFIX_RE = re.compile(r"^[0-9]+\|(?:[0-9]+\|)?", re.MULTILINE)
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


@dataclass
class EvidenceItem:
    evidence_id: str
    title: str
    fields: dict[str, str]
    source_ids: set[str]
    target_files: set[str]


@dataclass
class ValidationReport:
    scope: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metrics: dict[str, object] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors

    def merge(self, other: "ValidationReport") -> None:
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.metrics.update(other.metrics)


def find_project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "wiki").is_dir() and (
            (candidate / "AGENT.md").is_file()
            or (candidate / "AGENTS.md").is_file()
        ):
            return candidate
    raise FileNotFoundError("未找到同时包含 wiki/ 和 AGENT.md/AGENTS.md 的项目根目录")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str, list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, text, ["文件第一行必须严格为 ---"]

    lines = text.splitlines()
    try:
        closing = lines.index("---", 1)
    except ValueError:
        return {}, text, ["YAML frontmatter 缺少结束分隔符 ---"]

    metadata: dict[str, str] = {}
    for number, line in enumerate(lines[1:closing], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$", line)
        if not match:
            errors.append(f"frontmatter 第 {number} 行不是简单的 key: value 字段")
            continue
        value = match.group(2).strip().strip("\"'")
        metadata[match.group(1)] = value

    body = "\n".join(lines[closing + 1 :])
    return metadata, body, errors


def extract_wikilinks(text: str) -> set[str]:
    targets: set[str] = set()
    for raw in WIKILINK_RE.findall(text):
        target = raw.split("|", 1)[0].split("#", 1)[0].strip()
        if target:
            targets.add(Path(target).stem)
    return targets


def markdown_stems(wiki_root: Path) -> set[str]:
    return {path.stem for path in wiki_root.rglob("*.md")}


def common_markdown_checks(
    path: Path,
    text: str,
    report: ValidationReport,
    *,
    required_metadata: Iterable[str],
) -> tuple[dict[str, str], str]:
    metadata, body, frontmatter_errors = parse_frontmatter(text)
    report.errors.extend(f"{path.name}: {error}" for error in frontmatter_errors)

    for key in required_metadata:
        if not metadata.get(key):
            report.errors.append(f"{path.name}: frontmatter 缺少非空字段 {key}")

    h1_headings = re.findall(r"^# [^#].+$", body, re.MULTILINE)
    if len(h1_headings) != 1:
        report.errors.append(
            f"{path.name}: 必须且只能包含一个一级标题，当前为 {len(h1_headings)} 个"
        )

    placeholder = PLACEHOLDER_RE.search(text)
    if placeholder:
        report.errors.append(
            f"{path.name}: 存在模板占位符或未完成标记 {placeholder.group(0)!r}"
        )

    if LINE_PREFIX_RE.search(text):
        report.errors.append(f"{path.name}: 存在禁止的行号前缀")

    trailing_lines = [
        str(number)
        for number, line in enumerate(text.splitlines(), start=1)
        if line != line.rstrip()
    ]
    if trailing_lines:
        report.errors.append(
            f"{path.name}: 第 {', '.join(trailing_lines[:8])} 行存在行尾空白"
        )

    return metadata, body


def validate_wikilinks(
    path: Path,
    text: str,
    wiki_root: Path,
    report: ValidationReport,
) -> set[str]:
    links = extract_wikilinks(text)
    known = markdown_stems(wiki_root)
    missing = sorted(links - known)
    for target in missing:
        report.errors.append(f"{path.name}: Obsidian 链接目标不存在 [[{target}]]")
    return links


def parse_inventory(inventory_path: Path) -> dict[str, str]:
    sources: dict[str, str] = {}
    if not inventory_path.is_file():
        return sources

    for line in read_text(inventory_path).splitlines():
        source_match = re.search(r"source_id:\s*`([^`]+)`", line)
        if not source_match:
            continue
        url_match = re.search(r"https?://[^|\s]+", line)
        sources[source_match.group(1)] = url_match.group(0) if url_match else ""
    return sources


def _heading_blocks(text: str, prefix: str) -> list[tuple[str, str, str]]:
    headings = list(HEADING_RE.finditer(text))
    blocks: list[tuple[str, str, str]] = []
    pattern = re.compile(rf"^({re.escape(prefix)}-\d{{3}})[｜|]\s*(.+)$")

    for index, heading in enumerate(headings):
        if heading.group(1) != "###":
            continue
        match = pattern.match(heading.group(2))
        if not match:
            continue
        end = len(text)
        for following in headings[index + 1 :]:
            if len(following.group(1)) <= 3:
                end = following.start()
                break
        blocks.append((match.group(1), match.group(2), text[heading.end() : end]))
    return blocks


def _extract_field(block: str, name: str) -> tuple[str, int]:
    marker = re.compile(rf"^\*\*{re.escape(name)}\*\*\s*$", re.MULTILINE)
    matches = list(marker.finditer(block))
    if not matches:
        return "", 0
    start = matches[0].end()
    next_marker = re.search(r"^\*\*[^*]+\*\*\s*$", block[start:], re.MULTILINE)
    end = start + next_marker.start() if next_marker else len(block)
    return block[start:end].strip(), len(matches)


def parse_evidence_items(text: str) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    for evidence_id, title, block in _heading_blocks(text, "E"):
        fields = {name: _extract_field(block, name)[0] for name in MATRIX_FIELDS}
        source_ids = extract_wikilinks(fields["依据"])
        target_files = set(
            re.findall(r"`(0[1-9]_[a-z0-9_]+\.md)`", fields["目标文件"])
        )
        items.append(
            EvidenceItem(
                evidence_id=evidence_id,
                title=title,
                fields=fields,
                source_ids=source_ids,
                target_files=target_files,
            )
        )
    return items


def _metadata_count(text: str, label: str) -> int | None:
    match = re.search(
        rf"^-\s+\*\*{re.escape(label)}\*\*[：:]\s*`?(\d+)`?\s*$",
        text,
        re.MULTILINE,
    )
    return int(match.group(1)) if match else None


def _validate_sequential_ids(
    ids: list[str], prefix: str, report: ValidationReport
) -> None:
    expected = [f"{prefix}-{number:03d}" for number in range(1, len(ids) + 1)]
    if ids != expected:
        report.errors.append(
            f"{report.scope}: {prefix} 编号必须从 {prefix}-001 连续递增；"
            f"当前为 {', '.join(ids) or '空'}"
        )


def validate_evidence_matrix(root: Path, country: str) -> ValidationReport:
    country = country.lower()
    raw_root = root / "wiki" / "raw" / "landing_rights" / country
    matrix_path = raw_root / "evidence_matrix.md"
    inventory_path = raw_root / "source_inventory.md"
    notes_root = raw_root / "source_notes"
    report = ValidationReport(scope=f"{country} Evidence Matrix")

    if not matrix_path.is_file():
        report.errors.append(f"Evidence Matrix 不存在：{matrix_path}")
        return report
    if not inventory_path.is_file():
        report.errors.append(f"Source Inventory 不存在：{inventory_path}")
    if not notes_root.is_dir():
        report.errors.append(f"Source Notes 目录不存在：{notes_root}")
        return report

    text = read_text(matrix_path)
    metadata, _ = common_markdown_checks(
        matrix_path,
        text,
        report,
        required_metadata=(
            "country",
            "topic",
            "doc_type",
            "language",
            "review_status",
            "last_reviewed",
        ),
    )
    if metadata.get("topic") != "landing_rights":
        report.errors.append("evidence_matrix.md: topic 必须是 landing_rights")
    if metadata.get("doc_type") != "evidence_matrix":
        report.errors.append("evidence_matrix.md: doc_type 必须是 evidence_matrix")
    if metadata.get("country", "").lower() != country:
        report.errors.append(
            f"evidence_matrix.md: country 应与目录名 {country} 一致"
        )

    validate_wikilinks(matrix_path, text, root / "wiki", report)
    note_paths = sorted(
        path
        for path in notes_root.glob("*.md")
        if path.name != "source_notes_index.md"
    )
    note_ids = {path.stem for path in note_paths}
    inventory = parse_inventory(inventory_path)
    inventory_ids = set(inventory)

    for source_id in sorted(note_ids - inventory_ids):
        report.errors.append(
            f"evidence_matrix.md: Source Note 未登记到 Source Inventory：{source_id}"
        )
    for source_id in sorted(inventory_ids - note_ids):
        report.errors.append(
            f"evidence_matrix.md: Source Inventory 来源缺少 Source Note：{source_id}"
        )

    items = parse_evidence_items(text)
    if not items:
        report.errors.append("evidence_matrix.md: 至少需要一个 E-xxx 证据项")
        return report

    h2 = _section_headings(text, 2)
    required_sections = (
        r"^1\.\s*资料概览$",
        r"^2\.\s*证据项$",
        r"^3\.\s*冲突、版本与翻译问题$",
        r"^4\.\s*案例覆盖状态$",
        r"^5\.\s*关键证据缺口$",
        r"^6\.\s*生成前检查$",
    )
    for pattern in required_sections:
        if not _has_heading(h2, pattern):
            report.errors.append(
                f"evidence_matrix.md: 缺少规范要求的二级章节 /{pattern}/"
            )

    _validate_sequential_ids(
        [item.evidence_id for item in items], "E", report
    )
    expected_target_re = re.compile(
        rf"^0[1-9]_{re.escape(country)}_[a-z0-9_]+\.md$"
    )
    for item in items:
        block_match = next(
            (
                block
                for evidence_id, _, block in _heading_blocks(text, "E")
                if evidence_id == item.evidence_id
            ),
            "",
        )
        for field_name in MATRIX_FIELDS:
            value, count = _extract_field(block_match, field_name)
            if count != 1:
                report.errors.append(
                    f"{item.evidence_id}: 字段 {field_name} 必须且只能出现一次"
                )
            elif not value:
                report.errors.append(
                    f"{item.evidence_id}: 字段 {field_name} 不能为空"
                )

        status = item.fields["状态"].strip().strip("`")
        if status not in MATRIX_STATUSES:
            report.errors.append(
                f"{item.evidence_id}: 状态必须是 已确认、分析推断 或 待确认"
            )
        if not item.source_ids:
            report.errors.append(f"{item.evidence_id}: 依据中缺少 Source Note 链接")
        for source_id in sorted(item.source_ids - note_ids):
            report.errors.append(
                f"{item.evidence_id}: 依据链接不是现有 Source Note：{source_id}"
            )
        if not item.target_files:
            report.errors.append(f"{item.evidence_id}: 目标文件不能为空")
        for target in sorted(item.target_files):
            if not expected_target_re.match(target):
                report.errors.append(
                    f"{item.evidence_id}: 目标文件名不符合 01-09 国家案例规则：{target}"
                )

    status_counts = {
        status: sum(
            item.fields["状态"].strip().strip("`") == status for item in items
        )
        for status in MATRIX_STATUSES
    }
    count_labels = {
        "已读取 Source Notes": len(note_ids),
        "已确认结论": status_counts["已确认"],
        "分析推断": status_counts["分析推断"],
        "待确认事项": status_counts["待确认"],
    }

    unused_section_match = re.search(
        r"^### 未使用的 Source Notes\s*$([\s\S]*?)(?=^## 2\.)",
        text,
        re.MULTILINE,
    )
    unused_ids = (
        extract_wikilinks(unused_section_match.group(1))
        if unused_section_match
        else set()
    )
    used_ids = set().union(*(item.source_ids for item in items))
    for _, _, block in _heading_blocks(text, "C"):
        used_ids.update(extract_wikilinks(block))

    unknown_unused = unused_ids - note_ids
    for source_id in sorted(unknown_unused):
        report.errors.append(
            f"evidence_matrix.md: 未使用列表引用未知 Source Note：{source_id}"
        )
    duplicated = used_ids & unused_ids
    for source_id in sorted(duplicated):
        report.errors.append(
            f"evidence_matrix.md: Source Note 同时列为已使用和未使用：{source_id}"
        )
    unaccounted = note_ids - used_ids - unused_ids
    for source_id in sorted(unaccounted):
        report.errors.append(
            f"evidence_matrix.md: Source Note 未被证据使用且未说明未使用原因：{source_id}"
        )

    count_labels["未使用 Source Notes"] = len(unused_ids)
    for label, actual in count_labels.items():
        recorded = _metadata_count(text, label)
        if recorded is None:
            report.errors.append(f"evidence_matrix.md: 资料概览缺少 {label} 计数")
        elif recorded != actual:
            report.errors.append(
                f"evidence_matrix.md: {label} 记录为 {recorded}，实际为 {actual}"
            )

    conflict_ids = [
        conflict_id for conflict_id, _, _ in _heading_blocks(text, "C")
    ]
    if conflict_ids:
        _validate_sequential_ids(conflict_ids, "C", report)

    coverage_match = re.search(
        r"^## 4\. 案例覆盖状态\s*$([\s\S]*?)(?=^## 5\.)",
        text,
        re.MULTILINE,
    )
    if not coverage_match:
        report.errors.append("evidence_matrix.md: 缺少 ## 4. 案例覆盖状态")
    else:
        known_evidence = {item.evidence_id for item in items}
        coverage_ids = set(re.findall(r"\bE-\d{3}\b", coverage_match.group(1)))
        for evidence_id in sorted(coverage_ids - known_evidence):
            report.errors.append(
                f"evidence_matrix.md: 案例覆盖状态引用未知证据 {evidence_id}"
            )
        mapped_ids = {
            item.evidence_id for item in items if item.target_files
        }
        missing_coverage = mapped_ids - coverage_ids
        if missing_coverage:
            report.warnings.append(
                "案例覆盖状态未显式列出以下已映射证据："
                + "、".join(sorted(missing_coverage))
            )

    report.metrics.update(
        {
            "source_notes": len(note_ids),
            "inventory_sources": len(inventory_ids),
            "evidence_items": len(items),
            "confirmed": status_counts["已确认"],
            "inferences": status_counts["分析推断"],
            "pending": status_counts["待确认"],
            "unused_source_notes": len(unused_ids),
            "conflicts": len(conflict_ids),
        }
    )
    return report


def _section_headings(body: str, level: int) -> list[str]:
    marker = "#" * level
    return [
        match.group(1).strip()
        for match in re.finditer(
            rf"^{re.escape(marker)}\s+(.+?)\s*$", body, re.MULTILINE
        )
    ]


def _validate_nonempty_h2_sections(
    path: Path, body: str, report: ValidationReport
) -> None:
    headings = list(re.finditer(r"^##\s+(.+?)\s*$", body, re.MULTILINE))
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(body)
        content = body[heading.end() : end]
        meaningful = [
            line
            for line in content.splitlines()
            if line.strip() and not re.match(r"^#{3,6}\s+", line)
        ]
        if not meaningful:
            report.errors.append(
                f"{path.name}: 章节“{heading.group(1)}”没有正文内容"
            )


def _has_heading(headings: Iterable[str], pattern: str) -> bool:
    matcher = re.compile(pattern)
    return any(matcher.search(heading) for heading in headings)


def _case_expected_evidence(
    matrix_text: str, case_name: str
) -> list[EvidenceItem]:
    return [
        item
        for item in parse_evidence_items(matrix_text)
        if case_name in item.target_files
    ]


def validate_cases(
    root: Path,
    country: str,
    files: Iterable[str] | None = None,
) -> ValidationReport:
    country = country.lower()
    selected = list(files or CASE_FILES)
    report = ValidationReport(scope=f"{country} cases")
    invalid = [number for number in selected if number not in CASE_FILES]
    if invalid:
        report.errors.append(
            "未知案例编号：" + "、".join(invalid) + "；只支持 01-09"
        )
        return report

    cases_root = (
        root / "wiki" / "concepts" / "landing_rights" / "cases" / country
    )
    raw_root = root / "wiki" / "raw" / "landing_rights" / country
    matrix_path = raw_root / "evidence_matrix.md"
    inventory_path = raw_root / "source_inventory.md"
    note_ids = {
        path.stem
        for path in (raw_root / "source_notes").glob("*.md")
        if path.name != "source_notes_index.md"
    }
    inventory = parse_inventory(inventory_path)
    matrix_text = read_text(matrix_path) if matrix_path.is_file() else ""
    if not matrix_text:
        report.errors.append(f"无法校验案例证据：Evidence Matrix 不存在 {matrix_path}")

    total_expected = 0
    total_traced = 0
    validated = 0

    for number in selected:
        filename = f"{number}_{country}_{CASE_FILES[number]}.md"
        path = cases_root / filename
        if not path.is_file():
            report.errors.append(f"正式案例文件不存在：{path}")
            continue

        validated += 1
        text = read_text(path)
        metadata, body = common_markdown_checks(
            path,
            text,
            report,
            required_metadata=(
                "country",
                "topic",
                "case_type",
                "language",
                "review_status",
                "last_reviewed",
            ),
        )
        if metadata.get("country", "").lower() != country:
            report.errors.append(f"{filename}: country 应与目录名 {country} 一致")
        if metadata.get("review_status") not in {"draft", "human_reviewed"}:
            report.errors.append(
                f"{filename}: review_status 只能是 draft 或 human_reviewed"
            )

        links = validate_wikilinks(path, text, root / "wiki", report)
        _validate_nonempty_h2_sections(path, body, report)
        h2 = _section_headings(body, 2)
        h3 = _section_headings(body, 3)

        if number in {f"{value:02d}" for value in range(1, 8)}:
            required_h2 = (
                r"^1\.\s*文件用途$",
                r"^2\.\s*结论摘要$",
                r"官方来源",
                r"相关文件",
            )
            required_h3 = (
                r"^2\.1\s*已确认信息$",
                r"^2\.2\s*分析推断$",
                r"^2\.3\s*待确认事项$",
            )
            for pattern in required_h2:
                if not _has_heading(h2, pattern):
                    report.errors.append(
                        f"{filename}: 缺少规范要求的二级章节 /{pattern}/"
                    )
            for pattern in required_h3:
                if not _has_heading(h3, pattern):
                    report.errors.append(
                        f"{filename}: 缺少结论分区 /{pattern}/"
                    )
        elif number == "08":
            required = (
                r"^1\.\s*文件用途$",
                r"^2\.\s*结论摘要$",
                r"^3\.\s*核心法律和规则$",
                r"^4\.\s*监管机构申请和说明页面$",
                r"^5\.\s*法规层级和主题映射$",
                r"^6\.\s*版本、翻译和修订风险$",
                r"^7\.\s*仍需补充的官方文件$",
                r"^8\.\s*相关文件$",
            )
            for pattern in required:
                if not _has_heading(h2, pattern):
                    report.errors.append(
                        f"{filename}: 缺少法规文件专用章节 /{pattern}/"
                    )
            for pattern in (
                r"^2\.1\s*已确认信息$",
                r"^2\.2\s*分析推断$",
                r"^2\.3\s*待确认事项$",
            ):
                if not _has_heading(h3, pattern):
                    report.errors.append(
                        f"{filename}: 缺少结论分区 /{pattern}/"
                    )
            if text.count("| ---") < 2:
                report.errors.append(
                    f"{filename}: 第 3、4 节应包含核心法规表和监管页面表"
                )
        else:
            if len(h2) < 5:
                report.errors.append(
                    f"{filename}: 可复用经验文件至少需要 5 个二级章节"
                )
            for phrase in ("官方来源", "相关文件"):
                if not _has_heading(h2, phrase):
                    report.errors.append(
                        f"{filename}: 缺少包含“{phrase}”的章节"
                    )
            recommended = (
                "可复用",
                "官方来源",
                "许可边界",
                "版本",
                "不可迁移",
            )
            missing_recommended = [
                phrase
                for phrase in recommended
                if not any(phrase in heading for heading in h2)
            ]
            if missing_recommended:
                report.warnings.append(
                    f"{filename}: 建议结构尚未显式覆盖："
                    + "、".join(missing_recommended)
                )

        expected = (
            _case_expected_evidence(matrix_text, filename)
            if matrix_text
            else []
        )
        total_expected += len(expected)
        explicit_ids = set(re.findall(r"\bE-\d{3}\b", text))
        case_source_ids = links & note_ids
        missing_trace: list[str] = []
        for item in expected:
            source_traced = bool(item.source_ids & case_source_ids)
            if not source_traced:
                source_traced = any(
                    inventory.get(source_id)
                    and inventory[source_id] in text
                    for source_id in item.source_ids
                )
            if item.evidence_id in explicit_ids or source_traced:
                total_traced += 1
            else:
                missing_trace.append(item.evidence_id)

        if missing_trace:
            report.errors.append(
                f"{filename}: 未找到以下映射证据的 Evidence ID 或官方来源回链："
                + "、".join(missing_trace)
            )
        if expected and not explicit_ids:
            report.warnings.append(
                f"{filename}: 未显式记录 Evidence ID；当前仅以 Source Note/URL 回链近似检查证据采用情况"
            )

    report.metrics.update(
        {
            "requested_files": len(selected),
            "validated_files": validated,
            "expected_evidence_items": total_expected,
            "traced_evidence_items": total_traced,
        }
    )
    return report


def format_report(report: ValidationReport) -> str:
    status = "PASS" if report.ok else "FAIL"
    lines = [f"[{status}] {report.scope}"]
    if report.metrics:
        metrics = "，".join(
            f"{key}={value}" for key, value in report.metrics.items()
        )
        lines.append(f"指标：{metrics}")
    if report.errors:
        lines.append("错误：")
        lines.extend(f"- {error}" for error in report.errors)
    if report.warnings:
        lines.append("警告：")
        lines.extend(f"- {warning}" for warning in report.warnings)
    if report.ok and not report.warnings:
        lines.append("未发现结构、证据登记或内部链接问题。")
    return "\n".join(lines)
