from __future__ import annotations

import re


class GeneratedFileError(RuntimeError):
    """Raised when generated Markdown does not satisfy repository rules."""


def strip_markdown_fence(text: str) -> str:
    value = text.strip()
    match = re.fullmatch(r"```(?:markdown|md)?\s*\n(.*)\n```", value, re.DOTALL)
    return match.group(1).strip() if match else value


def _numbered_h2_body(content: str, number: int) -> str:
    match = re.search(
        rf"^##\s+{number}\.\s+.*?\n(.*?)(?=^##\s+\d+\.\s+|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else ""


def validate_case_markdown(content: str, *, number: str) -> list[str]:
    errors: list[str] = []
    front_matter = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", content, re.DOTALL)
    if not front_matter:
        errors.append("缺少或未正确闭合 YAML front matter")
    else:
        yaml_text = front_matter.group(1)
        for field in (
            "country",
            "topic",
            "case_type",
            "source_document",
            "language",
            "review_status",
        ):
            if not re.search(rf"^{field}:\s*\S", yaml_text, re.MULTILINE):
                errors.append(f"YAML 缺少字段 {field}")
    if "review_status: draft" not in content and "review_status: machine_generated" not in content:
        errors.append("review_status 必须是 draft 或 machine_generated")
    if not re.search(r"^#\s+\S", content, re.MULTILINE):
        errors.append("缺少中文一级标题")
    if "## 1. 文件用途" not in content:
        errors.append("缺少“文件用途”章节")
    if "## 2. 结论摘要" not in content:
        errors.append("缺少“结论摘要”章节")
    for heading in (
        "### 2.1 已确认信息",
        "### 2.2 分析推断",
        "### 2.3 待确认事项",
        "## 8. 官方来源",
        "## 9. 相关文件",
    ):
        if heading not in content:
            errors.append(f"缺少“{heading.lstrip('# ')}”章节")

    numbered_sections = {
        int(match.group(1))
        for match in re.finditer(r"^##\s+(\d+)\.\s+\S", content, re.MULTILINE)
    }
    missing_sections = sorted(set(range(1, 10)) - numbered_sections)
    if missing_sections:
        errors.append(
            "缺少连续编号章节：" + "、".join(str(value) for value in missing_sections)
        )

    confirmed = re.search(
        r"^### 2\.1 已确认信息\s*\n(.*?)(?=^### 2\.2 分析推断)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    confirmed_items = (
        re.findall(r"^(?:[-*]|\d+\.)\s+.+$", confirmed.group(1), re.MULTILINE)
        if confirmed
        else []
    )
    if not confirmed_items:
        errors.append("“已确认信息”至少需要一条列表项")
    elif any("（依据：" not in item for item in confirmed_items):
        errors.append("每条“已确认信息”都必须标注“（依据：<source_id>）”")

    inferred = re.search(
        r"^### 2\.2 分析推断\s*\n(.*?)(?=^### 2\.3 待确认事项)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    inferred_items = (
        re.findall(r"^(?:[-*]|\d+\.)\s+.+$", inferred.group(1), re.MULTILINE)
        if inferred
        else []
    )
    if inferred_items and any("（推断依据：" not in item for item in inferred_items):
        errors.append("每条“分析推断”都必须标注“（推断依据：<source_id>）”")
    if len(inferred_items) > 2:
        errors.append("“分析推断”最多保留两条，避免超出证据自由扩写")

    for section_number in range(3, 8):
        body = _numbered_h2_body(content, section_number)
        invalid_lines: list[str] = []
        for line in body.splitlines():
            value = line.strip()
            if not value or value.startswith(("### ", "#### ")):
                continue
            if not re.match(r"^(?:[-*]|\d+\.)\s+", value):
                invalid_lines.append(value)
                continue
            if not any(
                marker in value
                for marker in ("（依据：", "（推断依据：", "待确认", "未在公开官方资料中确认")
            ):
                invalid_lines.append(value)
        if invalid_lines:
            errors.append(
                f"第 {section_number} 节必须使用逐条证据清单，"
                "每条标注依据、推断依据或待确认状态"
            )

    if not re.search(r"\[\[[^\]\n]+\]\]", content):
        errors.append("“相关文件”缺少 Obsidian 链接")
    if len(content) < 600:
        errors.append("正文过短，可能是空骨架")
    return errors


def require_valid_case_markdown(content: str, *, number: str, filename: str) -> None:
    errors = validate_case_markdown(content, number=number)
    if errors:
        raise GeneratedFileError(f"{filename} 校验失败：" + "；".join(errors))
