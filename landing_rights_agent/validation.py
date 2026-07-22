from __future__ import annotations

import re


class GeneratedFileError(RuntimeError):
    """Raised when generated Markdown does not satisfy repository rules."""


def strip_markdown_fence(text: str) -> str:
    value = text.strip()
    match = re.fullmatch(r"```(?:markdown|md)?\s*\n(.*)\n```", value, re.DOTALL)
    return match.group(1).strip() if match else value


def validate_case_markdown(content: str, *, number: str) -> list[str]:
    errors: list[str] = []
    if not content.startswith("---\n"):
        errors.append("缺少 YAML front matter")
    if "review_status: draft" not in content and "review_status: machine_generated" not in content:
        errors.append("review_status 必须是 draft 或 machine_generated")
    if not re.search(r"^#\s+\S", content, re.MULTILINE):
        errors.append("缺少中文一级标题")
    if "## 1. 文件用途" not in content and number != "00":
        errors.append("缺少“文件用途”章节")
    if "结论摘要" not in content and number not in {"08", "09", "10"}:
        errors.append("缺少“结论摘要”章节")
    if number != "10" and not re.search(r"^## .*?(官方来源|资料来源)", content, re.MULTILINE):
        errors.append("缺少官方来源或资料来源章节")
    if "相关文件" not in content:
        errors.append("缺少“相关文件”章节")
    if len(content) < 600:
        errors.append("正文过短，可能是空骨架")
    return errors


def require_valid_case_markdown(content: str, *, number: str, filename: str) -> None:
    errors = validate_case_markdown(content, number=number)
    if errors:
        raise GeneratedFileError(f"{filename} 校验失败：" + "；".join(errors))
