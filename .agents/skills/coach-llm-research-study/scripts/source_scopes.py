from __future__ import annotations

import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

from pdf_utils import pdf_page_count


SCOPE_HEADER = (
    "Scope ID",
    "Source ID",
    "Title",
    "Included locations",
    "Boundary context",
    "Note",
)
SCOPE_ID_RE = re.compile(r"SCOPE-([A-Z][A-Z0-9-]*)-(\d{2})\Z")
SOURCE_ID_RE = re.compile(r"SRC-([A-Z][A-Z0-9-]*-\d{2}-\d{2})\Z")
PDF_FRAGMENT_RE = re.compile(r"page-(\d+)(?:: .+)?\Z", re.IGNORECASE)


@dataclass(frozen=True)
class ScopeFinding:
    line: int
    code: str
    message: str
    affected_source_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class CourseScope:
    scope_id: str
    source_id: str
    title: str
    included_locations: tuple[str, ...]
    boundary_locations: tuple[str, ...]
    note: str
    line: int


class _VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.parts.append(data)


def _split_table_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def _is_separator(cells: list[str] | None, width: int) -> bool:
    return bool(
        cells
        and len(cells) == width
        and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)
    )


def split_locations(raw: str) -> tuple[str, ...]:
    if raw == "none":
        return ()
    return tuple(item.strip() for item in raw.split(";") if item.strip())


def location_path(location: str) -> str | None:
    if "#" not in location:
        return None
    raw_path, fragment = location.rsplit("#", 1)
    path = unquote(raw_path.strip())
    if not path or not fragment.strip() or "\\" in path:
        return None
    pure = PurePosixPath(path)
    if pure.is_absolute() or ".." in pure.parts:
        return None
    return pure.as_posix()


def _location_fragment(location: str) -> str:
    return _normalize_fragment(location.rsplit("#", 1)[1])


def _normalize_fragment(value: str) -> str:
    value = re.sub(r"^#{1,6}[ \t]+", "", value.strip())
    while True:
        previous = value
        value = re.sub(r"^>[ \t]*", "", value)
        value = re.sub(r"^(?:[-*+]|\d+[.)])[ \t]+", "", value)
        if value == previous:
            break
    value = value.strip("| ")
    value = value.replace("`", "").replace("**", "").replace("__", "")
    return re.sub(r"\s+", " ", value).strip()


def parse_course_scopes(index_path: Path) -> tuple[list[CourseScope], list[ScopeFinding]]:
    findings: list[ScopeFinding] = []
    try:
        text = index_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [], findings
    except UnicodeDecodeError as exc:
        return [], [ScopeFinding(1, "INDEX_SCOPE_ENCODING", f"course INDEX is not UTF-8: {exc}")]

    heading_matches = list(re.finditer(r"^## 학습 범위\s*$", text, re.MULTILINE))
    if not heading_matches:
        return [], findings
    if len(heading_matches) != 1:
        return [], [ScopeFinding(1, "INDEX_SCOPE_TABLE_COUNT", "학습 범위 heading must appear at most once")]

    section_start = heading_matches[0].end()
    next_heading = re.search(r"^## ", text[section_start:], re.MULTILINE)
    section_end = section_start + next_heading.start() if next_heading else len(text)
    section = text[section_start:section_end]
    rows = [
        (text.count("\n", 0, section_start + match.start()) + 1, match.group(0))
        for match in re.finditer(r"^\|.*\|\s*$", section, re.MULTILINE)
    ]
    if not rows:
        return [], [ScopeFinding(text.count("\n", 0, section_start) + 1, "INDEX_SCOPE_TABLE_COUNT", "학습 범위 requires one table")]

    header = _split_table_row(rows[0][1])
    if header != list(SCOPE_HEADER):
        return [], [ScopeFinding(rows[0][0], "INDEX_SCOPE_HEADER", "학습 범위 columns must be " + " | ".join(SCOPE_HEADER))]
    if len(rows) < 2 or not _is_separator(_split_table_row(rows[1][1]), len(SCOPE_HEADER)):
        return [], [ScopeFinding(rows[0][0], "INDEX_SCOPE_HEADER", "학습 범위 separator is invalid")]

    scopes: list[CourseScope] = []
    for line_no, line in rows[2:]:
        cells = _split_table_row(line)
        if cells is None or len(cells) != len(SCOPE_HEADER):
            findings.append(ScopeFinding(line_no, "INDEX_SCOPE_ROW", "학습 범위 row must have six cells"))
            continue
        scope_id, source_id, title, raw_included, raw_boundary, note = cells
        included = split_locations(raw_included)
        boundary = split_locations(raw_boundary)
        scopes.append(CourseScope(scope_id, source_id, title, included, boundary, note, line_no))
    return scopes, findings


def validate_course_scopes(
    index_path: Path,
    *,
    repo_root: Path,
    source_paths_by_id: dict[str, tuple[str, ...]],
) -> tuple[list[CourseScope], list[ScopeFinding]]:
    scopes, findings = parse_course_scopes(index_path)
    seen_ids: dict[str, str] = {}
    for scope in scopes:
        if scope.scope_id in seen_ids:
            findings.append(
                ScopeFinding(
                    scope.line,
                    "INDEX_SCOPE_DUPLICATE",
                    f"duplicate Scope ID: {scope.scope_id}",
                    tuple(sorted({seen_ids[scope.scope_id], scope.source_id})),
                )
            )
        seen_ids[scope.scope_id] = scope.source_id

        affected = (scope.source_id,)

        source_match = SOURCE_ID_RE.fullmatch(scope.source_id)
        scope_match = SCOPE_ID_RE.fullmatch(scope.scope_id)
        expected_prefix = source_match.group(1) if source_match else None
        if scope_match is None or expected_prefix is None or scope_match.group(1) != expected_prefix:
            findings.append(
                ScopeFinding(
                    scope.line,
                    "INDEX_SCOPE_ID",
                    f"Scope ID must be SCOPE-<SOURCE-ID without SRC->-NN for {scope.source_id}",
                    affected,
                )
            )
        paths = source_paths_by_id.get(scope.source_id, ())
        if len(paths) != 1:
            findings.append(ScopeFinding(scope.line, "INDEX_SCOPE_SOURCE", f"Scope source must resolve to exactly one registry path: {scope.source_id}", affected))
            continue
        source_path = paths[0]
        expected_course = index_path.parent.relative_to(repo_root).as_posix() + "/"
        if not source_path.startswith(expected_course):
            findings.append(ScopeFinding(scope.line, "INDEX_SCOPE_SOURCE", f"{scope.source_id} does not belong to this course INDEX", affected))
        if not scope.title or scope.title == "none":
            findings.append(ScopeFinding(scope.line, "INDEX_SCOPE_VALUE", "Scope Title must be concrete", affected))
        if not scope.included_locations:
            findings.append(ScopeFinding(scope.line, "INDEX_SCOPE_VALUE", "Scope requires one or more Included locations", affected))
        if not scope.note or scope.note == "none":
            findings.append(ScopeFinding(scope.line, "INDEX_SCOPE_VALUE", "Scope Note must be concrete", affected))
        overlap = set(scope.included_locations).intersection(scope.boundary_locations)
        if overlap:
            findings.append(ScopeFinding(scope.line, "INDEX_SCOPE_OVERLAP", "Included locations and Boundary context must not overlap: " + ", ".join(sorted(overlap)), affected))
        for label, locations in (("Included", scope.included_locations), ("Boundary", scope.boundary_locations)):
            if len(locations) != len(set(locations)):
                findings.append(ScopeFinding(scope.line, "INDEX_SCOPE_DUPLICATE", f"{label} locations contain duplicates", affected))
            for location in locations:
                if location_path(location) != source_path:
                    findings.append(ScopeFinding(scope.line, "INDEX_SCOPE_LOCATION", f"{label} location must point to {source_path}: {location}", affected))
                    continue
                if not source_location_exists(repo_root, location):
                    findings.append(ScopeFinding(scope.line, "INDEX_SCOPE_LOCATION", f"{label} location is absent or out of range: {location}", affected))
    return scopes, findings


def source_location_exists(repo_root: Path, location: str) -> bool:
    path = location_path(location)
    if path is None:
        return False
    root = repo_root.resolve()
    candidate = (root / path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    if not candidate.is_file():
        return False
    fragment = _location_fragment(location)
    if candidate.suffix.lower() == ".pdf":
        match = PDF_FRAGMENT_RE.fullmatch(fragment)
        if match is None:
            return False
        count = pdf_page_count(candidate)
        return count is not None and 1 <= int(match.group(1)) <= count
    try:
        text = candidate.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    if fragment.lower().startswith("text: "):
        excerpt = re.sub(r"\s+", " ", fragment[6:]).strip()
        if candidate.suffix.lower() in {".html", ".htm"}:
            parser = _VisibleTextParser()
            try:
                parser.feed(text)
            except Exception:
                return False
            text = " ".join(parser.parts)
        return bool(excerpt) and excerpt in re.sub(r"\s+", " ", text).strip()
    return any(_normalize_fragment(line) == fragment for line in text.splitlines())


def location_is_included(location: str, scope: CourseScope) -> bool:
    path = location_path(location)
    if path is None:
        return False
    fragment = _location_fragment(location)
    page_match = PDF_FRAGMENT_RE.fullmatch(fragment)
    if page_match is not None:
        page = int(page_match.group(1))
        for included in scope.included_locations:
            included_match = PDF_FRAGMENT_RE.fullmatch(_location_fragment(included))
            if location_path(included) == path and included_match is not None and int(included_match.group(1)) == page:
                return True
        return False
    return any(
        location_path(included) == path
        and _location_fragment(included) == fragment
        for included in scope.included_locations
    )


def location_is_boundary(location: str, scope: CourseScope) -> bool:
    path = location_path(location)
    if path is None:
        return False
    fragment = _location_fragment(location)
    page_match = PDF_FRAGMENT_RE.fullmatch(fragment)
    if page_match is not None:
        page = int(page_match.group(1))
        return any(
            location_path(boundary) == path
            and (match := PDF_FRAGMENT_RE.fullmatch(_location_fragment(boundary))) is not None
            and int(match.group(1)) == page
            for boundary in scope.boundary_locations
        )
    return any(
        location_path(boundary) == path
        and _location_fragment(boundary) == fragment
        for boundary in scope.boundary_locations
    )
