#!/usr/bin/env python3
"""Validate and remove internal lesson envelopes from a composed TIL draft."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path


OPEN_RE = re.compile(
    r"<!-- lesson-evidence:"
    r"(?P<lesson>[a-z0-9][a-z0-9-]{2,63}):"
    r"(?P<evidence>E[0-9]{3}):"
    r"(?P<sha256>[0-9a-f]{64}) -->"
)
CLOSE_RE = re.compile(
    r"<!-- /lesson-evidence:"
    r"(?P<lesson>[a-z0-9][a-z0-9-]{2,63}):"
    r"(?P<evidence>E[0-9]{3}) -->"
)
TIL_OPEN_RE = re.compile(
    r"<!-- lesson-til-item:"
    r"(?P<lesson>[a-z0-9][a-z0-9-]{2,63}):"
    r"(?P<item>D[0-9]{3}):"
    r"(?P<representation>learning|changed-understanding|remaining-question):"
    r"(?P<evidence>none|E[0-9]{3}(?:,E[0-9]{3})*):"
    r"(?P<sha256>[0-9a-f]{64}) -->"
)
TIL_CLOSE_RE = re.compile(
    r"<!-- /lesson-til-item:"
    r"(?P<lesson>[a-z0-9][a-z0-9-]{2,63}):"
    r"(?P<item>D[0-9]{3}) -->"
)
MARKER_FRAGMENTS = ("lesson-evidence:", "lesson-til-item:")


class MarkerError(Exception):
    def __init__(self, line: int, message: str) -> None:
        super().__init__(message)
        self.line = line
        self.message = message


def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def content_without_boundary_lf(body_with_boundary_lf: str) -> str:
    if not body_with_boundary_lf.endswith("\n"):
        raise ValueError("the closing marker must start on the line after learner content")
    return body_with_boundary_lf[:-1]


def contains_markers(text: str) -> bool:
    """Return whether text contains a supported internal lesson marker."""
    return any(fragment in text for fragment in MARKER_FRAGMENTS)


def strip_markers(text: str) -> str:
    if not contains_markers(text):
        return text

    normalized = normalize_lf(text)
    lines = normalized.splitlines(keepends=True)
    output: list[str] = []
    body: list[str] = []
    current: tuple[str, str, str, str, int] | None = None
    seen: set[tuple[str, str, str]] = set()

    for line_number, line in enumerate(lines, start=1):
        marker_line = line.removesuffix("\n")
        evidence_opening = OPEN_RE.fullmatch(marker_line)
        til_opening = TIL_OPEN_RE.fullmatch(marker_line)
        evidence_closing = CLOSE_RE.fullmatch(marker_line)
        til_closing = TIL_CLOSE_RE.fullmatch(marker_line)
        opening = evidence_opening or til_opening
        closing = evidence_closing or til_closing

        if current is None:
            if opening:
                kind = "evidence" if evidence_opening else "til-item"
                item_id = opening["evidence"] if evidence_opening else opening["item"]
                key = (kind, opening["lesson"], item_id)
                if key in seen:
                    raise MarkerError(line_number, f"duplicate {kind} envelope: {key[1]}:{key[2]}")
                seen.add(key)
                current = (
                    kind,
                    opening["lesson"],
                    item_id,
                    opening["sha256"],
                    line_number,
                )
                body = []
            elif closing:
                raise MarkerError(line_number, "closing marker has no matching opening marker")
            elif contains_markers(marker_line):
                raise MarkerError(line_number, "malformed lesson marker")
            else:
                output.append(line)
            continue

        kind, lesson_id, item_id, expected_hash, opening_line = current
        if opening:
            raise MarkerError(line_number, "nested lesson envelopes are not allowed")
        if closing:
            closing_kind = "evidence" if evidence_closing else "til-item"
            closing_id = closing["evidence"] if evidence_closing else closing["item"]
            if (closing_kind, closing["lesson"], closing_id) != (kind, lesson_id, item_id):
                raise MarkerError(
                    line_number,
                    "closing marker does not match "
                    f"{lesson_id}:{item_id} opened on line {opening_line}",
                )
            raw_body = "".join(body)
            try:
                learner_content = content_without_boundary_lf(raw_body)
            except ValueError as error:
                raise MarkerError(line_number, str(error)) from error
            actual_hash = hashlib.sha256(learner_content.encode("utf-8")).hexdigest()
            if actual_hash != expected_hash:
                raise MarkerError(
                    opening_line,
                    f"learner content SHA-256 mismatch: expected {expected_hash}, got {actual_hash}",
                )
            # The final LF in raw_body is the structural boundary before the
            # closing marker.  Keep it when removing the marker line so a
            # following paragraph cannot be concatenated with learner text.
            output.append(raw_body)
            current = None
            body = []
        elif contains_markers(marker_line):
            raise MarkerError(line_number, "malformed or nested lesson marker")
        else:
            body.append(line)

    if current is not None:
        _, lesson_id, item_id, _, opening_line = current
        raise MarkerError(
            opening_line,
            f"opening marker has no matching close: {lesson_id}:{item_id}",
        )

    return "".join(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Print a composed draft with validated internal lesson comments removed "
            "and visible content preserved."
        )
    )
    parser.add_argument("draft", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        text = args.draft.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"ERROR {args.draft}:1 [DRAFT_CONTENT] {error}", file=sys.stderr)
        return 1

    try:
        cleaned = strip_markers(text)
    except MarkerError as error:
        print(
            f"ERROR {args.draft}:{error.line} [DRAFT_MARKER] {error.message}",
            file=sys.stderr,
        )
        return 1

    sys.stdout.write(cleaned)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
