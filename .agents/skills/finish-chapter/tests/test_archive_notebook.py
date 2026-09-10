from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/archive_notebook.py"
spec = importlib.util.spec_from_file_location("chapter_archive", SCRIPT)
assert spec and spec.loader
archive_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(archive_module)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@pytest.fixture
def saved(tmp_path):
    source = tmp_path / "main.ipynb"
    target = tmp_path / "practice" / "chapter.ipynb"
    notebook = {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {"kernelspec": {"name": "python3"}, "learner": "보존"},
        "cells": [{
            "id": "original-cell", "cell_type": "code", "metadata": {"collapsed": False},
            "source": ["if broken:``\n"], "execution_count": 7,
            "outputs": [{"output_type": "stream", "name": "stdout", "text": ["old output\n"]}],
        }],
    }
    raw = json.dumps(notebook, ensure_ascii=False, indent=1).encode() + b"\n"
    source.write_bytes(raw)
    return source, target, raw, notebook


def test_exact_snapshot_and_reset_preserve_metadata_and_original_output(saved):
    source, target, raw, notebook = saved
    assert archive_module.archive_notebook(source, target, digest(raw)) == "archived"
    assert source.read_bytes() == target.read_bytes() == raw
    assert archive_module.archive_notebook(source, target, digest(raw)) == "already_archived"
    assert archive_module.archive_notebook(source, target, digest(raw), reset=True) == "reset"
    blank = json.loads(source.read_bytes())
    assert blank["metadata"] == notebook["metadata"]
    assert blank["nbformat"] == notebook["nbformat"]
    assert len(blank["cells"]) == 1
    assert blank["cells"][0]["cell_type"] == "code"
    assert blank["cells"][0]["source"] == []
    assert blank["cells"][0]["outputs"] == []
    assert blank["cells"][0]["execution_count"] is None
    assert target.read_bytes() == raw


def test_conflicting_archive_is_never_overwritten(saved):
    source, target, raw, _ = saved
    target.parent.mkdir()
    target.write_bytes(b"previous chapter")
    with pytest.raises(ValueError, match="different"):
        archive_module.archive_notebook(source, target, digest(raw))
    assert source.read_bytes() == raw
    assert target.read_bytes() == b"previous chapter"


@pytest.mark.parametrize("bad", [b"not json", b"[]", b'{"cells": []}',
    b'{"nbformat":4,"nbformat_minor":5,"metadata":{},"cells":[{"cell_type":"code","source":17}]}'])
def test_invalid_notebook_cannot_be_archived_or_reset(saved, bad):
    source, target, _, _ = saved
    source.write_bytes(bad)
    with pytest.raises(ValueError):
        archive_module.archive_notebook(source, target, digest(bad))
    assert source.read_bytes() == bad
    assert not target.exists()


def test_source_changed_since_inspection_prevents_reset(saved):
    source, target, raw, _ = saved
    archive_module.archive_notebook(source, target, digest(raw))
    changed = raw + b" "
    source.write_bytes(changed)
    with pytest.raises(ValueError, match="changed"):
        archive_module.archive_notebook(source, target, digest(raw), reset=True)
    assert source.read_bytes() == changed
    assert target.read_bytes() == raw


def test_reset_requires_existing_exact_archive(saved):
    source, target, raw, _ = saved
    with pytest.raises(ValueError, match="archive"):
        archive_module.archive_notebook(source, target, digest(raw), reset=True)
    target.parent.mkdir()
    target.write_bytes(raw + b" ")
    with pytest.raises(ValueError, match="archive"):
        archive_module.archive_notebook(source, target, digest(raw), reset=True)
    assert source.read_bytes() == raw


def test_rerun_after_reset_cannot_replace_archive_with_empty_notebook(saved):
    source, target, raw, _ = saved
    archive_module.archive_notebook(source, target, digest(raw))
    archive_module.archive_notebook(source, target, digest(raw), reset=True)
    empty = source.read_bytes()
    assert archive_module.archive_notebook(source, target, digest(raw), reset=True) == "already_reset"
    assert archive_module.archive_notebook(source, target, digest(empty)) == "empty_source"
    assert archive_module.archive_notebook(source, target.with_name("empty.ipynb"), digest(empty)) == "empty_source"
    assert not target.with_name("empty.ipynb").exists()
    assert target.read_bytes() == raw
    assert source.read_bytes() == empty


def test_failed_archive_write_preserves_source(saved, monkeypatch):
    source, target, raw, _ = saved
    def fail(*args, **kwargs):
        raise OSError("disk full")
    monkeypatch.setattr(archive_module.os, "link", fail)
    with pytest.raises(OSError):
        archive_module.archive_notebook(source, target, digest(raw))
    assert source.read_bytes() == raw
    assert not target.exists()
    assert list(target.parent.iterdir()) == []


def test_failed_reset_preserves_source_and_archive(saved, monkeypatch):
    source, target, raw, _ = saved
    archive_module.archive_notebook(source, target, digest(raw))
    def fail(*args, **kwargs):
        raise OSError("write failed")
    monkeypatch.setattr(archive_module.os, "replace", fail)
    with pytest.raises(OSError):
        archive_module.archive_notebook(source, target, digest(raw), reset=True)
    assert source.read_bytes() == target.read_bytes() == raw


def test_same_path_or_symlink_is_rejected(saved):
    source, target, raw, _ = saved
    with pytest.raises(ValueError):
        archive_module.archive_notebook(source, source, digest(raw))
    target.parent.mkdir()
    target.symlink_to(source)
    with pytest.raises(ValueError):
        archive_module.archive_notebook(source, target, digest(raw), reset=True)
    assert source.read_bytes() == raw


def test_edit_during_reset_preparation_is_preserved(saved, monkeypatch):
    source, target, raw, _ = saved
    archive_module.archive_notebook(source, target, digest(raw))
    original = archive_module._blank_bytes
    changed = raw + b"\n"
    def concurrent_edit(notebook):
        source.write_bytes(changed)
        return original(notebook)
    monkeypatch.setattr(archive_module, "_blank_bytes", concurrent_edit)
    with pytest.raises(ValueError, match="changed"):
        archive_module.archive_notebook(source, target, digest(raw), reset=True)
    assert source.read_bytes() == changed
    assert target.read_bytes() == raw
