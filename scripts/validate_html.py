#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RE_DOCTYPE = re.compile(r"^\s*<!doctype\s+html\s*>", re.IGNORECASE)
RE_LANG = re.compile(r"<html\b[^>]*\blang\s*=\s*['\"][^'\"]+['\"]", re.IGNORECASE)
RE_CHARSET = re.compile(r"<meta\b[^>]*\bcharset\s*=\s*['\"][^'\"]+['\"]", re.IGNORECASE)
RE_TITLE = re.compile(r"<title\b[^>]*>.*?</title>", re.IGNORECASE | re.DOTALL)


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")

    # Fail-fast errors (treat as errors, not warnings)
    if not RE_DOCTYPE.search(text):
        errors.append("Missing <!doctype html> (recommended; helps consistent rendering)")

    if "<html" not in text.lower():
        errors.append("Missing <html> tag")

    if "<head" not in text.lower():
        errors.append("Missing <head> tag")

    if "<body" not in text.lower():
        errors.append("Missing <body> tag")

    if not RE_CHARSET.search(text):
        errors.append("Missing <meta charset=\"utf-8\"> (recommended)")

    if not RE_TITLE.search(text):
        errors.append("Missing <title>…</title> (recommended; helps SEO + browser tab label)")

    if not RE_LANG.search(text):
        errors.append("Missing lang attribute on <html> (recommended; accessibility/SEO)")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Basic HTML validation (sanity checks).")
    parser.add_argument("paths", nargs="+", help="HTML file(s) to validate")
    args = parser.parse_args()

    any_errors = False
    for p in args.paths:
        path = Path(p)
        if not path.exists():
            print(f"ERROR: File not found: {path}")
            any_errors = True
            continue

        errs = validate_file(path)
        if errs:
            any_errors = True
            print(f"\n❌ {path}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"✅ {path} (basic checks passed)")

    return 1 if any_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
