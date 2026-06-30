#!/usr/bin/env python3
"""Download and compare monitored regulatory source pages."""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import html.parser
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


SKIP_TAGS = {"script", "style", "noscript", "svg", "nav", "header", "footer", "form"}
BLOCK_TAGS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "br",
    "dd",
    "div",
    "dl",
    "dt",
    "fieldset",
    "figcaption",
    "figure",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "li",
    "main",
    "ol",
    "p",
    "pre",
    "section",
    "table",
    "td",
    "th",
    "tr",
    "ul",
}


class TextExtractor(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.capture_depth = 0
        self.in_title = False
        self.title_parts: list[str] = []
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs_dict = {key.lower(): value for key, value in attrs if value is not None}
        if tag == "title":
            self.in_title = True
            return

        if self.capture_depth:
            self.capture_depth += 1
        elif tag == "div" and attrs_dict.get("id") == "content":
            self.capture_depth = 1
        else:
            return

        if tag in SKIP_TAGS:
            self.skip_depth += 1
            return
        if tag in BLOCK_TAGS and self.skip_depth == 0:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
            return

        if not self.capture_depth:
            return

        if tag in SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
        if tag in BLOCK_TAGS and self.skip_depth == 0:
            self.parts.append("\n")
        self.capture_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
            return
        if self.skip_depth or not self.capture_depth:
            return
        self.parts.append(data)

    @property
    def title(self) -> str:
        return normalize_spaces(" ".join(self.title_parts))

    @property
    def text(self) -> str:
        return "\n".join(normalize_lines("".join(self.parts)))


def normalize_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ").replace("\ufeff", "")).strip()


def normalize_lines(value: str) -> list[str]:
    value = value.replace("\xa0", " ").replace("\ufeff", "")
    raw_lines = re.split(r"[\r\n]+", value)
    lines = [normalize_spaces(line) for line in raw_lines]
    return [line for line in lines if line and not re.fullmatch(r"Acessos:\s*\d+", line)]


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_config(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    sources = data.get("sources")
    if not isinstance(sources, list):
        raise ValueError(f"{path} does not contain a sources list")
    return sources


def should_process(source: dict[str, Any], args: argparse.Namespace) -> tuple[bool, str]:
    if args.source_id and source.get("source_id") not in args.source_id:
        return False, "not requested"
    if source.get("capture_method") == "archive_only" and not args.include_archive:
        return False, "archive only"
    if not args.include_unmonitored and not source.get("monitor"):
        return False, "monitor disabled"
    url = source.get("url")
    if not isinstance(url, str) or not url.startswith(("http://", "https://")):
        return False, "missing url"
    if source.get("source_format") != "html":
        return False, f"unsupported format: {source.get('source_format')}"
    return True, ""


def download(url: str, timeout: int) -> tuple[bytes, str]:
    if shutil.which("curl"):
        return download_with_curl(url, timeout)
    return download_with_urllib(url, timeout)


def download_with_curl(url: str, timeout: int) -> tuple[bytes, str]:
    command = [
        "curl",
        "-L",
        "--fail",
        "--silent",
        "--show-error",
        "--max-time",
        str(timeout),
        "--user-agent",
        "spacesail-regulatory-monitor/0.1 (+local research)",
        url,
    ]
    completed = subprocess.run(command, check=False, capture_output=True)
    if completed.returncode:
        stderr = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(stderr or f"curl exited with {completed.returncode}")
    return completed.stdout, "utf-8"


def download_with_urllib(url: str, timeout: int) -> tuple[bytes, str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "spacesail-regulatory-monitor/0.1 (+local research)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read(), charset


def normalize_html(raw: bytes, charset: str, source: dict[str, Any], fetched_at: str) -> tuple[str, str]:
    html_text = raw.decode(charset, errors="replace")
    extractor = TextExtractor()
    extractor.feed(html_text)
    extractor.close()
    title = extractor.title
    header = [
        f"source_id: {source['source_id']}",
        f"country: {source.get('country', '')}",
        f"norm: {source.get('norm', '')}",
        f"url: {source.get('url', '')}",
        f"title: {title}",
        "",
    ]
    return title, "\n".join(header) + extractor.text + "\n"


def latest_snapshot(root: Path, run_date: str) -> Path | None:
    snapshot_root = root / "snapshots"
    if not snapshot_root.exists():
        return None
    candidates: list[Path] = []
    for child in snapshot_root.iterdir():
        normalized = child / "normalized.txt"
        if child.is_dir() and child.name != run_date and normalized.exists():
            candidates.append(normalized)
    if not candidates:
        return None
    return sorted(candidates, key=lambda p: p.parent.name)[-1]


def diff_summary(old: str, new: str) -> tuple[str, str]:
    old_lines = old.splitlines()
    new_lines = new.splitlines()
    diff = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile="previous",
            tofile="current",
            lineterm="",
            n=2,
        )
    )
    added = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
    removed = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))
    excerpt = "\n".join(diff[:80])
    return f"{added} added lines, {removed} removed lines", excerpt


def write_check_log(
    root: Path,
    source: dict[str, Any],
    status: str,
    fetched_at: str,
    normalized_hash: str | None,
    compared_to: str | None,
    summary: str | None = None,
    excerpt: str | None = None,
    error: str | None = None,
) -> None:
    root.mkdir(parents=True, exist_ok=True)
    log_path = root / "checks.md"
    lines = [
        f"## {fetched_at}",
        "",
        f"- source_id: `{source['source_id']}`",
        f"- norm: {source.get('norm', '')}",
        f"- status: `{status}`",
        f"- url: {source.get('url', '')}",
    ]
    if normalized_hash:
        lines.append(f"- normalized_sha256: `{normalized_hash}`")
    if compared_to:
        lines.append(f"- compared_to: `{compared_to}`")
    if summary:
        lines.append(f"- diff_summary: {summary}")
    if error:
        lines.append(f"- error: {error}")
    if excerpt:
        lines.extend(["", "```diff", excerpt, "```"])
    lines.append("")
    with log_path.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines))


def process_source(source: dict[str, Any], args: argparse.Namespace) -> tuple[str, str]:
    run_date = args.date
    fetched_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    source_root = args.output_dir / source["country"] / source["source_id"]
    snapshot_dir = source_root / "snapshots" / run_date
    original_path = snapshot_dir / "original.html"
    normalized_path = snapshot_dir / "normalized.txt"
    metadata_path = snapshot_dir / "metadata.json"

    raw, charset = download(source["url"], args.timeout)
    title, normalized = normalize_html(raw, charset, source, fetched_at)
    normalized_hash = sha256_text(normalized)

    previous_path = latest_snapshot(source_root, run_date)
    if previous_path:
        previous_text = previous_path.read_text(encoding="utf-8")
        compared_to = str(previous_path)
    elif normalized_path.exists():
        previous_text = normalized_path.read_text(encoding="utf-8")
        compared_to = str(normalized_path)
    else:
        previous_text = None
        compared_to = None

    if previous_text is None:
        status = "baseline-created"
        summary = None
        excerpt = None
    elif previous_text == normalized:
        status = "no-update"
        summary = None
        excerpt = None
    else:
        status = "updated"
        summary, excerpt = diff_summary(previous_text, normalized)

    if not args.dry_run:
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        original_path.write_bytes(raw)
        normalized_path.write_text(normalized, encoding="utf-8")
        metadata = {
            "source_id": source["source_id"],
            "country": source["country"],
            "norm": source.get("norm"),
            "url": source.get("url"),
            "fetched_at": fetched_at,
            "title": title,
            "charset": charset,
            "source_format": source.get("source_format"),
            "capture_method": source.get("capture_method"),
            "normalized_sha256": normalized_hash,
            "status": status,
            "compared_to": compared_to,
        }
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_check_log(source_root, source, status, fetched_at, normalized_hash, compared_to, summary, excerpt)

    return source["source_id"], status


def build_parser() -> argparse.ArgumentParser:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=root / "regulatory_sources" / "sources.json")
    parser.add_argument("--output-dir", type=Path, default=root / "sources")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--source-id", action="append", help="Process only this source_id. Can be repeated.")
    parser.add_argument("--limit", type=int, help="Process at most N eligible sources.")
    parser.add_argument("--include-archive", action="store_true", help="Also process archive_only sources.")
    parser.add_argument("--include-unmonitored", action="store_true", help="Also process monitor=false sources with valid URLs.")
    parser.add_argument("--dry-run", action="store_true", help="Download and compare without writing snapshots or logs.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    sources = read_config(args.config)
    eligible: list[dict[str, Any]] = []
    skipped: list[tuple[str, str]] = []

    for source in sources:
        ok, reason = should_process(source, args)
        if ok:
            eligible.append(source)
        else:
            skipped.append((source.get("source_id", "<unknown>"), reason))

    if args.limit is not None:
        eligible = eligible[: args.limit]

    errors = 0
    for source in eligible:
        try:
            source_id, status = process_source(source, args)
            print(f"{source_id}: {status}")
        except (OSError, urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as exc:
            errors += 1
            source_id = source.get("source_id", "<unknown>")
            print(f"{source_id}: error: {exc}", file=sys.stderr)
            if not args.dry_run:
                fetched_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
                source_root = args.output_dir / source.get("country", "unknown") / source_id
                write_check_log(source_root, source, "error", fetched_at, None, None, error=str(exc))

    print(f"processed: {len(eligible)}")
    print(f"skipped: {len(skipped)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
