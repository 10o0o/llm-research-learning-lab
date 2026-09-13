from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/validate_knowledge.py"
SPEC = importlib.util.spec_from_file_location("validate_knowledge_under_test", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


def _write_note(repo: Path, body: str) -> tuple[Path, int]:
    note = repo / "knowledge" / "area" / "concept.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        'title: "Fixture concept"',
        "updated: 2026-09-14",
        "tags:",
        "  - fixture",
        "---",
        "",
        "# Fixture concept",
        "",
        "## 핵심 요약",
        "",
        "A stable summary.",
        "",
        "## 개념 정리",
        "",
        body,
        "",
    ]
    note.write_text("\n".join(lines), encoding="utf-8")
    return note, lines.index(body) + 1


@pytest.mark.parametrize(
    ("target", "source_exists"),
    [
        ("../../materials/private/source.md", True),
        ("../../materials/private/missing.md", False),
    ],
)
def test_private_material_relative_links_are_rejected_regardless_of_existence(
    tmp_path: Path, target: str, source_exists: bool
) -> None:
    repo = tmp_path / "repo"
    private_dir = repo / "materials" / "private"
    private_dir.mkdir(parents=True)
    if source_exists:
        (private_dir / "source.md").write_text("private", encoding="utf-8")

    note, line_number = _write_note(repo, f"- [Source]({target})")
    errors = validator.validate_file(note)

    assert any(
        f"{note}:{line_number}:" in error and "private materials" in error
        for error in errors
    )
    assert not any("relative link target does not exist" in error for error in errors)


@pytest.mark.parametrize(
    "target",
    [
        "../../materials/%70rivate/missing.md",
        "%2e%2e/%2e%2e/materials/private/missing.md",
        "../../knowledge/area/../../materials/private/missing.md",
    ],
)
def test_private_link_scope_is_checked_after_url_and_path_normalization(
    tmp_path: Path, target: str
) -> None:
    repo = tmp_path / "repo"
    note, line_number = _write_note(repo, f"- [Source]({target})")
    errors = validator.validate_file(note)

    assert any(
        f"{note}:{line_number}:" in error and "private materials" in error
        for error in errors
    )


@pytest.mark.parametrize(
    ("target", "outside_exists"),
    [
        ("../../../outside.md", True),
        ("../../../missing-outside.md", False),
    ],
)
def test_relative_links_outside_repository_are_rejected_regardless_of_existence(
    tmp_path: Path, target: str, outside_exists: bool
) -> None:
    repo = tmp_path / "repo"
    if outside_exists:
        (tmp_path / "outside.md").write_text("outside", encoding="utf-8")

    note, line_number = _write_note(repo, f"- [Outside]({target})")
    errors = validator.validate_file(note)

    assert any(
        f"{note}:{line_number}:" in error and "outside repository" in error
        for error in errors
    )
    assert not any("relative link target does not exist" in error for error in errors)


def test_symlink_targets_are_classified_by_their_resolved_location(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    private_source = repo / "materials" / "private" / "source.md"
    private_source.parent.mkdir(parents=True)
    private_source.write_text("private", encoding="utf-8")
    aliases = repo / "practice"
    aliases.mkdir(parents=True)
    (aliases / "private-alias.md").symlink_to(private_source)
    (aliases / "outside-alias.md").symlink_to(tmp_path / "missing-outside.md")

    private_note, private_line = _write_note(
        repo, "- [Alias](../../practice/private-alias.md)"
    )
    outside_note = private_note.with_name("outside-alias.md")
    outside_note.write_text(
        private_note.read_text(encoding="utf-8").replace(
            "../../practice/private-alias.md", "../../practice/outside-alias.md"
        ),
        encoding="utf-8",
    )
    outside_line = private_line

    private_errors = validator.validate_file(private_note)
    outside_errors = validator.validate_file(outside_note)

    assert any(
        f"{private_note}:{private_line}:" in error and "private materials" in error
        for error in private_errors
    )
    assert any(
        f"{outside_note}:{outside_line}:" in error and "outside repository" in error
        for error in outside_errors
    )


def test_public_links_plain_bibliography_http_urls_inline_math_and_metadata_pass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = tmp_path / "repo"
    public_target = repo / "practice" / "reference.md"
    public_target.parent.mkdir(parents=True)
    public_target.write_text("public", encoding="utf-8")
    body = (
        "- [Public](../../practice/reference.md) · [HTTP](http://example.com/source) "
        "· [HTTPS](https://example.com/source) · Source: Linear Algebra, Chapter 3 "
        "(private material) · "
        "inline math $x^2$"
    )
    note, _ = _write_note(repo, body)
    original = note.read_bytes()
    assert not (repo / "materials" / "private").exists()

    monkeypatch.setattr(sys, "argv", [str(SCRIPT), str(note)])
    assert validator.main() == 0
    assert "Validated 1 knowledge Markdown file(s): OK" in capsys.readouterr().out
    assert note.read_bytes() == original
