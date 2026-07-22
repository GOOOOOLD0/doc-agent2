from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from . import __version__
from .client import AgentAPIError, ResponsesClient
from .knowledge import KnowledgeBaseError, ensure_repo_root, validate_country_slug
from .validation import GeneratedFileError
from .workflows import build_country_cases, run_answer, run_research


def load_env_file(path: Path) -> None:
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="landing-rights-agent",
        description="独立运行的卫星落地许可研究 Agent",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="项目根目录，默认当前目录",
    )
    parser.add_argument("--model", help="模型 ID，默认读取环境变量")
    parser.add_argument(
        "--reasoning-effort",
        choices=("none", "low", "medium", "high", "xhigh", "max"),
        help="推理强度",
    )
    parser.add_argument("--timeout", type=int, default=180, help="API 超时秒数")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor", help="检查项目、配置和 API Key")

    answer = subparsers.add_parser("answer", help="基于知识库回答许可问题")
    answer.add_argument("--country", required=True, help="英文小写国家 slug")
    answer.add_argument("--question", required=True, help="要回答的问题")
    answer.add_argument("--web", action="store_true", help="同时检索最新官方网页")
    answer.add_argument("--output", type=Path, help="将回答保存到指定文件")

    research = subparsers.add_parser("research", help="检索新国家官方资料")
    research.add_argument("--country", required=True, help="英文小写国家 slug")
    research.add_argument("--question", help="可选研究重点")
    research.add_argument("--output", type=Path, help="将研究报告保存到指定文件")

    build = subparsers.add_parser("build-country", help="由 source notes 生成案例文件")
    build.add_argument("--country", required=True, help="英文小写国家 slug")
    build.add_argument(
        "--files",
        default="00,01,02,03,04,05,06,07,08,09,10",
        help="逗号分隔的文件编号",
    )
    build.add_argument(
        "--apply",
        action="store_true",
        help="通过全部校验后写入正式 Wiki；默认只生成预览",
    )
    build.add_argument("--preview-dir", type=Path, help="自定义预览根目录")
    return parser


def _client(args: argparse.Namespace) -> ResponsesClient:
    return ResponsesClient.from_env(
        model=args.model,
        reasoning_effort=args.reasoning_effort,
        timeout=args.timeout,
    )


def _write_or_print(text: str, output: Path | None) -> None:
    if output is None:
        print(text)
        return
    output = output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text.rstrip() + "\n", encoding="utf-8")
    print(f"已保存：{output}")


def _doctor(root: Path) -> int:
    print(f"项目根目录：{root}")
    print("知识库：正常")
    provider = os.environ.get("LANDING_RIGHTS_PROVIDER", "qwen").strip().lower()
    defaults = {
        "qwen": ("qwen3.6-flash", "DASHSCOPE_API_KEY"),
        "openai": ("gpt-5.6-terra", "OPENAI_API_KEY"),
    }
    if provider not in defaults:
        print(f"模型提供方：{provider}（不支持）")
        return 2
    default_model, key_name = defaults[provider]
    model = os.environ.get("LANDING_RIGHTS_MODEL", default_model)
    print(f"模型提供方：{provider}")
    print(f"模型：{model}")
    if os.environ.get(key_name, "").strip():
        print(f"{key_name}：已设置")
        return 0
    print(f"{key_name}：未设置（answer/research/build-country 暂不可调用模型）")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        root = ensure_repo_root(args.root)
        load_env_file(root / ".env")

        if args.command == "doctor":
            return _doctor(root)

        country = validate_country_slug(args.country)
        client = _client(args)
        if args.command == "answer":
            result = run_answer(
                client,
                root=root,
                country=country,
                question=args.question,
                web_search=args.web,
            )
            _write_or_print(result, args.output)
            return 0

        if args.command == "research":
            result = run_research(
                client,
                root=root,
                country=country,
                question=args.question,
            )
            _write_or_print(result, args.output)
            return 0

        if args.command == "build-country":
            numbers = [value.strip() for value in args.files.split(",") if value.strip()]
            preview_dir, files = build_country_cases(
                client,
                root=root,
                country=country,
                numbers=numbers,
                apply=args.apply,
                preview_root=args.preview_dir,
            )
            print(f"预览目录：{preview_dir}")
            print(f"已生成并校验：{len(files)} 个文件")
            if args.apply:
                print("已写入正式 Wiki。所有文件仍为 draft，必须人工复核。")
            else:
                print("未修改正式 Wiki；人工复核后可使用 --apply 重新生成并写入。")
            return 0

        parser.error("未知命令")
    except (AgentAPIError, KnowledgeBaseError, GeneratedFileError, ValueError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2
    return 0
