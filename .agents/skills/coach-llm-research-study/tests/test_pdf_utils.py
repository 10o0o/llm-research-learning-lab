from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

from pypdf import PdfWriter


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/pdf_utils.py"
SPEC = importlib.util.spec_from_file_location("pdf_utils_under_test", SCRIPT)
assert SPEC and SPEC.loader
pdf_utils = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = pdf_utils
SPEC.loader.exec_module(pdf_utils)


def _write_pdf(path: Path, pages: int) -> None:
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=72, height=72)
    with path.open("wb") as stream:
        writer.write(stream)


def test_parser_counts_multiple_pages_and_ignores_raw_page_decoys(tmp_path: Path) -> None:
    path = tmp_path / "two-pages.pdf"
    _write_pdf(path, 2)
    path.write_bytes(path.read_bytes() + b"\n% decoy /Type /Page /Type /Page\n")
    assert len(re.findall(rb"/Type\s*/Page(?!s)\b", path.read_bytes())) != 2
    assert pdf_utils.pdf_page_count(path) == 2


def test_pdfinfo_is_the_only_fallback_after_pypdf_failure(
    tmp_path: Path, monkeypatch
) -> None:
    path = tmp_path / "fallback.pdf"
    path.write_bytes(b"not parsed by pypdf")
    monkeypatch.setattr(pdf_utils, "_pypdf_page_count", lambda _path: None)
    monkeypatch.setattr(
        pdf_utils.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(
            returncode=0,
            stdout="Pages:          7\n",
        ),
    )
    assert pdf_utils.pdf_page_count(path) == 7


def test_unreadable_pdf_returns_none(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / "broken.pdf"
    path.write_bytes(b"/Type /Page /Type /Page")
    monkeypatch.setattr(pdf_utils, "_pypdf_page_count", lambda _path: None)
    monkeypatch.setattr(
        pdf_utils.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=1, stdout=""),
    )
    assert pdf_utils.pdf_page_count(path) is None


def test_pdfinfo_timeout_is_unreadable(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / "timeout.pdf"
    path.write_bytes(b"broken")
    monkeypatch.setattr(pdf_utils, "_pypdf_page_count", lambda _path: None)

    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired("pdfinfo", 30)

    monkeypatch.setattr(pdf_utils.subprocess, "run", timeout)
    assert pdf_utils.pdf_page_count(path) is None
