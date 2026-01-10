#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, urldefrag


SKIP_SCHEMES = {"http", "https", "mailto", "tel", "sms", "data", "javascript"}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[tuple[str, int]] = []  # (url, line)

    def handle_starttag(self, tag, attrs):
        # Check common link-bearing attributes
        for (k, v) in attrs:
            if not v:
                continue
            k = k.lower()
            if k in {"href", "src"}:
                self.refs.append((v.strip(), self.getpos()[0]))


def is_external_or_special(u: str) -> bool:
    if u.startswith("#"):
        return True
    parsed = urlparse(u)
    if parsed.scheme and parsed.scheme.lower() in SKIP_SCHEMES:
        return True
    return False


def resolve_local_target(raw: str, html_file: Path, repo_root: Path) -> Path | None:
    # Remove fragment (#...) and keep path only (ignore query too)
    nofrag, _ = urldefrag(raw)
    noquery = nofrag.split("?", 1)[0].strip()

    if not noquery or is_external_or_special(noquery):
        return None

    # Root-relative: /assets/x -> repo_root/assets/x
    if noquery.startswith("/"):
        rel = noquery.lstrip("/")
        return (repo_root / rel).resolve()

    # Relative to current HTML file directory
    return (html_file.parent / noquery).resolve()


def exists_target(p: Path) -> bool:
    if p.is_file():
        return True
    # If linking to a directory, treat as directory index.html
    if p.is_dir():
        return (p / "index.html").is_file()
    return False


def scan_html_file(html_file: Path, repo_root: Path) -> list[str]:
    issues: list[str] = []

    text = html_file.read_text(encoding="utf-8", errors="replace")
    parser = LinkParser()
    parser.feed(text)

    for raw, line in parser.refs:
        target = resolve_local_target(raw, html_file, repo_root)
        if target is None:
            continue

        # Only enforce targets inside the repo for local checks
        try:
            target.relative_to(repo_root.resolve())
        except Exception:
            # Points outside repo; skip
            continue

        if not exists_target(target):
            issues.append(f"{html_file.relative_to(repo_root)}:{line} -> broken local link: {raw}")

    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Check broken local links in HTML files.")
    ap.add_argument("--root", default=".", help="Repo root (default: .)")
    args = ap.parse_args()

    repo_root = Path(args.root).resolve()
    html_files = list(repo_root.rglob("*.html"))

    if not html_files:
        print("No .html files found.")
        return 0

    all_issues: list[str] = []
    for f in html_files:
        all_issues.extend(scan_html_file(f, repo_root))

    if all_issues:
        print("❌ Broken local links found:\n")
        for issue in all_issues:
            print(f"- {issue}")
        return 1

    print(f"✅ No broken local links found across {len(html_files)} HTML file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
