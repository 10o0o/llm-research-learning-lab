#!/usr/bin/env python3
"""Validate this repository's canonical knowledge Markdown format."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path
from urllib.parse import unquote


CANONICAL_HEADINGS = (
    "핵심 요약",
    "개념 정리",
    "예제 또는 적용",
    "주의점",
    "관련 기록",
)
REQUIRED_HEADINGS = CANONICAL_HEADINGS[:2]
DATE_IN_NAME_RE = re.compile(r"(?:^|[-_])\d{4}-\d{2}-\d{2}(?:[-_]|$)")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
PROHIBITED_MACRO_RE = re.compile(
    r"\\(?:operatorname|DeclareMathOperator|newcommand|renewcommand|def|require)\b"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate finalized knowledge notes or knowledge/template.md."
    )
    parser.add_argument("paths", nargs="+", type=Path)
    return parser.parse_args()


def scalar_value(line: str) -> str:
    return line.split(":", maxsplit=1)[1].strip().strip('"').strip("'")


def parse_frontmatter(path: Path, lines: list[str], is_template: bool) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not lines or lines[0].strip() != "---":
        return {}, [f"{path}: file must start with YAML frontmatter"]

    try:
        closing = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}, [f"{path}: YAML frontmatter is not closed"]

    frontmatter = lines[1:closing]
    values: dict[str, str] = {}
    tags: list[str] = []
    in_tags = False
    for line_number, line in enumerate(frontmatter, start=2):
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r"^(title|updated):\s*", line):
            key = line.split(":", maxsplit=1)[0]
            values[key] = scalar_value(line)
            in_tags = False
        elif re.match(r"^tags:\s*$", line):
            values["tags"] = "present"
            in_tags = True
        elif in_tags and re.match(r"^\s+-\s+\S", line):
            tags.append(re.sub(r"^\s+-\s+", "", line).strip())
        else:
            errors.append(f"{path}:{line_number}: unsupported frontmatter line")

    for field in ("title", "updated", "tags"):
        if field not in values:
            errors.append(f"{path}: missing frontmatter field: {field}")

    if "title" in values and not values["title"]:
        errors.append(f"{path}: title cannot be empty")
    if "updated" in values and not is_template:
        try:
            dt.date.fromisoformat(values["updated"])
        except ValueError:
            errors.append(f"{path}: updated must be a valid YYYY-MM-DD date")
    if not tags:
        errors.append(f"{path}: tags must contain at least one item")

    values["closing_line"] = str(closing + 1)
    return values, errors


def visible_lines(lines: list[str]) -> tuple[list[tuple[int, str]], list[str]]:
    visible: list[tuple[int, str]] = []
    errors: list[str] = []
    in_fence = False
    opening_line = 0
    frontmatter_closed = False

    for line_number, line in enumerate(lines, start=1):
        if line_number == 1 and line.strip() == "---":
            continue
        if not frontmatter_closed:
            if line.strip() == "---":
                frontmatter_closed = True
            continue
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


def check_path(path: Path, is_template: bool) -> list[str]:
    if is_template:
        return []
    parts = path.resolve().parts
    indices = [index for index, part in enumerate(parts) if part == "knowledge"]
    if not indices:
        return [f"{path}: expected a file under knowledge/<area>/"]
    relative = parts[indices[-1] + 1 :]
    errors: list[str] = []
    if len(relative) < 2:
        errors.append(f"{path}: expected path knowledge/<area>/<concept>.md")
    if path.suffix.lower() != ".md":
        errors.append(f"{path}: expected a Markdown file")
    if DATE_IN_NAME_RE.search(path.stem):
        errors.append(f"{path}: knowledge filenames must not contain a study date")
    return errors


def check_headings(
    path: Path,
    lines: list[str],
    visible: list[tuple[int, str]],
    title: str,
    is_template: bool,
) -> list[str]:
    errors: list[str] = []
    top = [(number, line[2:].strip()) for number, line in visible if re.match(r"^#\s+\S", line)]
    if len(top) != 1:
        errors.append(f"{path}: expected exactly one top-level heading, found {len(top)}")
    elif top[0][1] != title:
        errors.append(f"{path}:{top[0][0]}: top-level heading must match frontmatter title")

    headings = [
        (number, match.group(1).strip())
        for number, line in visible
        if (match := re.match(r"^##(?!#)\s+(.+?)\s*$", line))
    ]
    names = [name for _, name in headings]
    for name in names:
        if name not in CANONICAL_HEADINGS:
            errors.append(f"{path}: unknown level-two heading: {name}")
    for name in CANONICAL_HEADINGS:
        if names.count(name) > 1:
            errors.append(f"{path}: duplicate level-two heading: {name}")
    required = CANONICAL_HEADINGS if is_template else REQUIRED_HEADINGS
    for name in required:
        if name not in names:
            errors.append(f"{path}: missing required section: {name}")
    recognized = [name for name in names if name in CANONICAL_HEADINGS]
    expected = [name for name in CANONICAL_HEADINGS if name in recognized]
    if recognized != expected:
        errors.append(f"{path}: level-two sections are not in canonical order")

    if not is_template:
        for index, (line_number, name) in enumerate(headings):
            next_line = headings[index + 1][0] if index + 1 < len(headings) else len(lines) + 1
            body = [
                line.strip()
                for line in lines[line_number: next_line - 1]
                if line.strip() and not line.lstrip().startswith("<!--")
            ]
            if not body:
                errors.append(f"{path}:{line_number}: section is empty: {name}")
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


def repository_root(path: Path) -> Path | None:
    resolved = path.resolve(strict=False)
    for ancestor in resolved.parents:
        if ancestor.name == "knowledge":
            return ancestor.parent
    return None


def is_within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
    except ValueError:
        return False
    return True


def check_links(path: Path, visible: list[tuple[int, str]]) -> list[str]:
    errors: list[str] = []
    resolved_path = path.resolve(strict=False)
    root = repository_root(path)
    private_materials = (
        (root / "materials" / "private").resolve(strict=False)
        if root is not None
        else None
    )
    for line_number, line in visible:
        for raw_target in extract_link_targets(line):
            target = normalize_link_target(raw_target)
            if not target or target.startswith(("#", "http://", "https://", "mailto:", "data:")):
                continue
            resolved_target = (resolved_path.parent / target).resolve(strict=False)
            if root is not None and not is_within(resolved_target, root):
                errors.append(
                    f"{path}:{line_number}: relative link target is outside repository: {target}"
                )
                continue
            if (
                private_materials is not None
                and is_within(resolved_target, private_materials)
            ):
                errors.append(
                    f"{path}:{line_number}: relative link target is in private materials: {target}"
                )
                continue
            if not resolved_target.exists():
                errors.append(f"{path}:{line_number}: relative link target does not exist: {target}")
    return errors


def check_math(path: Path, visible: list[tuple[int, str]]) -> list[str]:
    errors: list[str] = []
    block_open = False
    block_line = 0
    for line_number, line in visible:
        if PROHIBITED_MACRO_RE.search(line):
            errors.append(f"{path}:{line_number}: prohibited math macro")
        if any(delimiter in line for delimiter in (r"\(", r"\)", r"\[", r"\]")):
            errors.append(f"{path}:{line_number}: use $...$ or $$...$$ for math")
        index = 0
        inline_dollars = 0
        while index < len(line):
            if line.startswith("$$", index) and (index == 0 or line[index - 1] != "\\"):
                block_open = not block_open
                block_line = line_number if block_open else block_line
                index += 2
                continue
            if line[index] == "$" and (index == 0 or line[index - 1] != "\\") and not block_open:
                inline_dollars += 1
            index += 1
        if inline_dollars % 2:
            errors.append(f"{path}:{line_number}: unbalanced inline math delimiter")
    if block_open:
        errors.append(f"{path}:{block_line}: unclosed block math delimiter")
    return errors


def validate_file(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path}: path does not exist"]
    if not path.is_file():
        return [f"{path}: pass a Markdown file, not a directory"]
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"{path}: file is not valid UTF-8"]

    lines = text.splitlines()
    is_template = path.resolve().name == "template.md" and path.resolve().parent.name == "knowledge"
    values, errors = parse_frontmatter(path, lines, is_template)
    visible, fence_errors = visible_lines(lines)
    errors.extend(f"{path}:{message}" for message in fence_errors)
    errors.extend(check_path(path, is_template))
    if "title" in values:
        errors.extend(check_headings(path, lines, visible, values["title"], is_template))
    errors.extend(check_links(path, visible))
    errors.extend(check_math(path, visible))

    if not text.endswith("\n"):
        errors.append(f"{path}: missing final newline")
    if not is_template and any(token in text for token in ("YYYY-MM-DD", "개념 이름", "<!--", "-->")):
        errors.append(f"{path}: template placeholder remains in finalized note")
    return errors


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    files = sorted(set(args.paths), key=lambda item: str(item))
    for path in files:
        errors.extend(validate_file(path))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Validated {len(files)} knowledge Markdown file(s): OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
