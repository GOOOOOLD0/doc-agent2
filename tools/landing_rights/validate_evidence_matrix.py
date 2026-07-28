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
    validate_evidence_matrix,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="校验卫星落地许可 Evidence Matrix。"
    )
    parser.add_argument("--country", required=True, help="英文小写国家目录名")
    parser.add_argument("--root", type=Path, help="项目根目录，默认自动查找")
    args = parser.parse_args()

    root = args.root.resolve() if args.root else find_project_root()
    report = validate_evidence_matrix(root, args.country)
    print(format_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
