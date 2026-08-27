#!/usr/bin/env python3
"""Validate this repository's canonical daily TIL Markdown format."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path
from urllib.parse import unquote


CANONICAL_HEADINGS = (
    "오늘의 학습",
    "배운 점",
    "남은 질문",
    "다음에 할 것",
    "관련 기록",
)
REQUIRED_HEADINGS = {"오늘의 학습"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
BOLD_BEFORE_KOREAN_RE = re.compile(r"\*\*(?!\s)(?:(?!\*\*).)+?\*\*(?=[가-힣])")
PROHIBITED_MACRO_RE = re.compile(
    r"\\(?:operatorname|DeclareMathOperator|newcommand|renewcommand|def|require)\b"
)
RELATED_TARGET_RE = re.compile(r"^- 관련 역량: `CC-[A-Z]+-\d{2}`$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a finalized daily TIL or til/template.md."
    )
    parser.add_argument("paths", nargs="+", type=Path)
    return parser.parse_args()


def collect_files(paths: list[Path]) -> tuple[list[Path], list[str]]:
    files: set[Path] = set()
    errors: list[str] = []
    for path in paths:
        if not path.exists():
            errors.append(f"{path}: path does not exist")
        elif path.is_dir():
            errors.append(f"{path}: pass a Markdown file, not a directory")
        elif path.suffix.lower() != ".md":
            errors.append(f"{path}: expected a Markdown file")
        else:
            files.add(path)
    return sorted(files, key=lambda item: str(item)), errors


def strip_fenced_and_inline_code(
    lines: list[str],
) -> tuple[list[tuple[int, str]], list[str]]:
    visible: list[tuple[int, str]] = []
    errors: list[str] = []
    in_fence = False
    opening_line = 0

    for line_number, line in enumerate(lines, start=1):
        if line.lstrip().startswith("```"):
            if not in_fence:
                in_fence = True
                opening_line = line_number
                if line.lstrip() == "```":
                    errors.append(
                        f"line {line_number}: opening code fence needs a language identifier"
                    )
            else:
                in_fence = False
            continue
        if not in_fence:
            visible.append((line_number, INLINE_CODE_RE.sub("", line)))

    if in_fence:
        errors.append(f"line {opening_line}: unclosed fenced code block")
    return visible, errors


def check_math_and_emphasis(path: Path, visible: list[tuple[int, str]]) -> list[str]:
    errors: list[str] = []
    block_math_open = False
    block_math_line = 0

    for line_number, line in visible:
        if PROHIBITED_MACRO_RE.search(line):
            errors.append(f"{path}:{line_number}: prohibited math macro")
        if any(delimiter in line for delimiter in (r"\(", r"\)", r"\[", r"\]")):
            errors.append(
                f"{path}:{line_number}: use $...$ or $$...$$ instead of escaped delimiters"
            )
        if BOLD_BEFORE_KOREAN_RE.search(line):
            errors.append(
                f"{path}:{line_number}: Korean text follows a closing bold marker directly"
            )

        index = 0
        inline_dollars = 0
        while index < len(line):
            if line.startswith("$$", index) and (index == 0 or line[index - 1] != "\\"):
                if not block_math_open:
                    block_math_line = line_number
                block_math_open = not block_math_open
                index += 2
                continue
            if (
                line[index] == "$"
                and (index == 0 or line[index - 1] != "\\")
                and not block_math_open
            ):
                inline_dollars += 1
            index += 1

        if inline_dollars % 2:
            errors.append(f"{path}:{line_number}: unbalanced inline math delimiter")

    if block_math_open:
        errors.append(f"{path}:{block_math_line}: unclosed block math delimiter")
    return errors


def normalize_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    elif " " in target:
        target = target.split(maxsplit=1)[0]
    return unquote(target.split("#", maxsplit=1)[0])


def extract_link_targets(line: str) -> list[str]:
    targets: list[str] = []
    cursor = 0
    while True:
        start = line.find("](", cursor)
        if start == -1:
            return targets

        index = start + 2
        depth = 1
        escaped = False
        while index < len(line):
            character = line[index]
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    targets.append(line[start + 2 : index])
                    cursor = index + 1
                    break
            index += 1
        else:
            return targets


def check_links(path: Path, visible: list[tuple[int, str]]) -> list[str]:
    errors: list[str] = []
    for line_number, line in visible:
        for raw_target in extract_link_targets(line):
            target = normalize_link_target(raw_target)
            if not target or target.startswith(
                ("#", "http://", "https://", "mailto:", "data:")
            ):
                continue
            destination = (path.parent / target).resolve()
            if not destination.exists():
                errors.append(
                    f"{path}:{line_number}: relative link target does not exist: {target}"
                )
    return errors


def date_from_target_path(path: Path) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    parts = path.resolve().parts
    candidates: list[tuple[str, str, str]] = []
    for index, part in enumerate(parts[:-3]):
        if part == "til":
            candidates.append(tuple(parts[index + 1 : index + 4]))

    if not candidates:
        return None, [f"{path}: expected path til/YYYY/MM/YYYY-MM-DD.md"]

    year, month, filename = candidates[-1]
    date_text = Path(filename).stem
    if not DATE_RE.fullmatch(date_text):
        return None, [f"{path}: filename must be YYYY-MM-DD.md"]

    try:
        parsed_date = dt.date.fromisoformat(date_text)
    except ValueError:
        return None, [f"{path}: filename contains an invalid calendar date"]

    if year != f"{parsed_date.year:04d}" or month != f"{parsed_date.month:02d}":
        errors.append(f"{path}: year/month directories do not match the filename date")
    return date_text, errors


def heading_schema(
    path: Path,
    lines: list[str],
    visible: list[tuple[int, str]],
    is_template: bool,
) -> list[str]:
    errors: list[str] = []
    top_headings = [
        (line_number, line[2:].strip())
        for line_number, line in visible
        if re.match(r"^#\s+\S", line)
    ]
    if len(top_headings) != 1:
        errors.append(
            f"{path}: expected exactly one top-level heading, found {len(top_headings)}"
        )

    expected_date = "YYYY-MM-DD" if is_template else None
    if not is_template:
        expected_date, path_errors = date_from_target_path(path)
        errors.extend(path_errors)

    if expected_date and top_headings:
        expected_title = expected_date
        if top_headings[0][1] != expected_title:
            errors.append(
                f"{path}:{top_headings[0][0]}: top-level heading must be '# {expected_title}'"
            )

    headings = [
        (line_number, match.group(1).strip())
        for line_number, line in visible
        if (match := re.match(r"^##(?!#)\s+(.+?)\s*$", line))
    ]
    names = [name for _, name in headings]
    unknown = [name for name in names if name not in CANONICAL_HEADINGS]
    for name in unknown:
        errors.append(f"{path}: unknown level-two heading: {name}")

    for name in CANONICAL_HEADINGS:
        if names.count(name) > 1:
            errors.append(f"{path}: duplicate level-two heading: {name}")

    required = set(CANONICAL_HEADINGS) if is_template else REQUIRED_HEADINGS
    for name in required:
        if name not in names:
            errors.append(f"{path}: missing required section: {name}")

    recognized = [name for name in names if name in CANONICAL_HEADINGS]
    expected_order = [name for name in CANONICAL_HEADINGS if name in recognized]
    if recognized != expected_order:
        errors.append(f"{path}: level-two sections are not in canonical order")

    if not is_template:
        if lines and lines[0].strip() != f"# {expected_date}":
            errors.append(f"{path}: the first line must be the date heading")
        if any("<!--" in line or "-->" in line for line in lines):
            errors.append(f"{path}: template comments remain in the finalized note")

        for index, (line_number, name) in enumerate(headings):
            next_line = headings[index + 1][0] if index + 1 < len(headings) else len(lines) + 1
            body = [
                line.strip()
                for line in lines[line_number: next_line - 1]
                if line.strip()
            ]
            if not body:
                errors.append(f"{path}:{line_number}: section is empty: {name}")

    return errors


def check_related_target_provenance(path: Path, lines: list[str]) -> list[str]:
    """Keep temporary-source target provenance exact and non-mastery-shaped."""
    errors: list[str] = []
    current_h2: str | None = None
    in_fence = False
    for line_number, line in enumerate(lines, start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        heading = re.fullmatch(r"##(?!#)\s+(.+?)\s*", line)
        if heading is not None:
            current_h2 = heading.group(1)
        if not line.strip().startswith("- 관련 역량:"):
            continue
        if current_h2 != "관련 기록":
            errors.append(
                f"{path}:{line_number}: related target provenance belongs under 관련 기록"
            )
        if RELATED_TARGET_RE.fullmatch(line.strip()) is None:
            errors.append(
                f"{path}:{line_number}: use exactly '- 관련 역량: `CC-...`'"
            )
    return errors


def validate_file(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"{path}: file is not valid UTF-8"]

    lines = text.splitlines()
    errors: list[str] = []
    if not text.endswith("\n"):
        errors.append(f"{path}: missing final newline")

    visible, fence_errors = strip_fenced_and_inline_code(lines)
    errors.extend(f"{path}:{message}" for message in fence_errors)
    errors.extend(check_math_and_emphasis(path, visible))
    errors.extend(check_links(path, visible))
    errors.extend(heading_schema(path, lines, visible, path.name == "template.md"))
    if path.name != "template.md":
        errors.extend(check_related_target_provenance(path, lines))
    return errors


def main() -> int:
    args = parse_args()
    files, errors = collect_files(args.paths)
    for path in files:
        errors.extend(validate_file(path))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} TIL Markdown file(s): OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
