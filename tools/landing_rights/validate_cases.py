#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.landing_rights.validation import (  # noqa: E402
    find_project_root,
    format_report,
    validate_cases,
)


def parse_files(value: str) -> list[str]:
    return [item.strip().zfill(2) for item in value.split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="校验卫星落地许可正式 01-09 案例。"
    )
    parser.add_argument("--country", required=True, help="英文小写国家目录名")
    parser.add_argument(
        "--files",
        type=parse_files,
        help="仅校验指定编号，例如 04 或 01,04,08",
    )
    parser.add_argument("--root", type=Path, help="项目根目录，默认自动查找")
    args = parser.parse_args()

    root = args.root.resolve() if args.root else find_project_root()
    report = validate_cases(root, args.country, args.files)
    print(format_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
