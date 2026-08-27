"""Shared, parser-backed PDF inspection helpers."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


def _pypdf_page_count(path: Path) -> int | None:
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    try:
        page_count = len(PdfReader(str(path), strict=False).pages)
    except Exception:  # pypdf exposes several parser and encryption errors.
        return None
    return page_count if page_count > 0 else None


def _pdfinfo_page_count(path: Path) -> int | None:
    try:
        completed = subprocess.run(
            ["pdfinfo", str(path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0:
        return None
    match = re.search(r"^Pages:\s+(\d+)\s*$", completed.stdout, re.MULTILINE)
    if match is None:
        return None
    page_count = int(match.group(1))
    return page_count if page_count > 0 else None


def pdf_page_count(path: Path) -> int | None:
    """Return a trustworthy positive page count or None when unreadable."""
    return _pypdf_page_count(path) or _pdfinfo_page_count(path)
