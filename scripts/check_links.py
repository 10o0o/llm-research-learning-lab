#!/usr/bin/env python3
"""Check local inline Markdown links and heading anchors; no network or packages."""

import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

FENCE = re.compile(r"(?ms)^ {0,3}(`{3,}|~{3,})[^\n]*\n.*?^ {0,3}\1[^\n]*$")
LINK = re.compile(r'!?\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\s)]+))(?:\s+"[^"]*")?\s*\)')
HEADING = re.compile(r"(?m)^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$")


def readable_text(path):
    return FENCE.sub("", path.read_text(encoding="utf-8"))


def anchors(path):
    counts = Counter()
    result = set()
    for title in HEADING.findall(readable_text(path)):
        title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", title)
        slug = re.sub(r"[^\w\s-]", "", title.lower()).strip()
        slug = re.sub(r"\s", "-", slug)
        suffix = f"-{counts[slug]}" if counts[slug] else ""
        counts[slug] += 1
        result.add(slug + suffix)
    return result


def check(root):
    errors, checked = [], 0
    pages = sorted(p for p in root.rglob("*.md") if ".git" not in p.relative_to(root).parts)
    for page in pages:
        for match in LINK.finditer(readable_text(page)):
            target = match.group(1) or match.group(2)
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            checked += 1
            path = unquote(url.path)
            destination = (root / path.lstrip("/") if path.startswith("/") else page.parent / path).resolve() if path else page.resolve()
            label = f"{page.relative_to(root)} -> {target}"
            if not destination.is_relative_to(root):
                errors.append(f"{label}: outside repository")
            elif not destination.exists():
                errors.append(f"{label}: missing target")
            elif url.fragment and destination.is_file() and destination.suffix.lower() == ".md":
                if unquote(url.fragment) not in anchors(destination):
                    errors.append(f"{label}: missing heading")
    return pages, checked, errors


if __name__ == "__main__":
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    pages, checked, errors = check(root)
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Checked {len(pages)} Markdown files and {checked} local links; {len(errors)} errors.")
    sys.exit(bool(errors))
