#!/usr/bin/env python3
"""Print validated TIL input without mutating the draft or active handoff."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[3]
COACH_SCRIPTS = REPO_ROOT / ".agents/skills/coach-llm-research-study/scripts"
for directory in (SCRIPT_DIR, COACH_SCRIPTS):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from strip_lesson_evidence_markers import MARKER_FRAGMENT, MarkerError, strip_markers  # noqa: E402
from validate_lesson_handoff import validate_handoff  # noqa: E402


class PreflightError(Exception):
    pass


def _inside_repo(path: Path, repo_root: Path) -> Path:
    candidate = path if path.is_absolute() else repo_root / path
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(repo_root.resolve())
    except ValueError as error:
        raise PreflightError("draft path escapes the repository") from error
    return resolved


def prepare_til_input(
    draft: Path | str = Path("til/today.md"),
    *,
    repo_root: Path | str = REPO_ROOT,
    handoff: Path | str = Path("tmp/active-lesson-handoff.md"),
) -> str:
    """Return save input after read-only handoff and marker validation."""
    root = Path(repo_root).resolve()
    draft_path = _inside_repo(Path(draft), root)
    handoff_path = _inside_repo(Path(handoff), root)
    canonical = (root / "til/today.md").resolve(strict=False)

    try:
        draft_text = draft_path.read_bytes().decode("utf-8")
    except (OSError, UnicodeError) as error:
        raise PreflightError(f"cannot read draft: {error}") from error

    has_markers = MARKER_FRAGMENT in draft_text
    if draft_path != canonical:
        if has_markers:
            raise PreflightError("standalone draft contains lesson-evidence markers")
        return draft_text

    if handoff_path.is_file():
        report = validate_handoff(
            handoff_path,
            repo_root=root,
            til_ready=True,
            check_draft=True,
        )
        if not report.ok:
            rendered = "\n".join(error.rendered(handoff_path) for error in report.errors)
            raise PreflightError("active handoff is not TIL-ready\n" + rendered)
        try:
            return strip_markers(draft_text)
        except MarkerError as error:
            raise PreflightError(f"draft marker validation failed at line {error.line}: {error.message}") from error

    if has_markers:
        raise PreflightError("canonical draft contains lesson-evidence markers but no active handoff exists")
    return draft_text


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.exit(2, f"ERROR <cli>:1 [SCHEMA] {message}\n")


def _build_parser() -> argparse.ArgumentParser:
    parser = _ArgumentParser(description=__doc__)
    parser.add_argument(
        "draft",
        nargs="?",
        type=Path,
        default=Path("til/today.md"),
        help="repository-relative Markdown draft (default: til/today.md)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        prepared = prepare_til_input(args.draft)
    except PreflightError as error:
        print(f"ERROR {args.draft}:1 [TIL_PREFLIGHT] {error}", file=sys.stderr)
        return 1
    sys.stdout.write(prepared)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
