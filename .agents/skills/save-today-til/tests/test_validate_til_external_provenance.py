from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/validate_til.py"
SPEC = importlib.util.spec_from_file_location("validate_til_provenance_under_test", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


def _note(tmp_path: Path, provenance: str, *, section: str = "관련 기록") -> Path:
    path = tmp_path / "til/2026/08/2026-08-27.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        "# 2026-08-27\n\n"
        "## 오늘의 학습\n\n학습자 설명\n\n"
        f"## {section}\n\n"
        "- [Official source](https://official.example/course)\n"
        f"{provenance}\n",
        encoding="utf-8",
    )
    return path


def test_related_target_provenance_accepts_exact_cc_form(tmp_path: Path) -> None:
    path = _note(tmp_path, "- 관련 역량: `CC-DL-01`")
    assert validator.validate_file(path) == []


def test_related_target_provenance_rejects_wrong_section_or_shape(tmp_path: Path) -> None:
    wrong_section = _note(tmp_path, "- 관련 역량: CC-DL-01", section="배운 점")
    errors = validator.validate_file(wrong_section)
    assert any("belongs under 관련 기록" in error for error in errors)
    assert any("use exactly" in error for error in errors)
