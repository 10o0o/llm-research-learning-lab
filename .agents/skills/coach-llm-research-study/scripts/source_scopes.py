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
    "Included units",
    "Boundary units",
    "Note",
)
SCOPE_ID_RE = re.compile(r"SCOPE-([A-Z][A-Z0-9-]*)-(\d{2})\Z")
SOURCE_ID_RE = re.compile(r"SRC-([A-Z][A-Z0-9-]*-\d{2}-\d{2})\Z")
PDF_FRAGMENT_RE = re.compile(r"page-(\d+)(?:--(\d+))?(?:: .+)?\Z", re.IGNORECASE)
UNIT_ANCHOR_RE = re.compile(r"(?P<label>.+?)\s*\[(?P<location>[^\[\]]+)\]\Z")


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
    included_units: tuple[str, ...]
    boundary_units: tuple[str, ...]
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
    return [cell.strip().replace(r"\|", "|") for cell in re.split(r"(?<!\\)\|", stripped[1:-1])]


def _is_separator(cells: list[str] | None, width: int) -> bool:
    return bool(
        cells
        and len(cells) == width
        and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)
    )


def split_units(raw: str) -> tuple[str, ...]:
    if raw == "none":
        return ()
    return tuple(item.strip() for item in raw.split(";") if item.strip())


def unit_location(unit: str) -> str | None:
    match = UNIT_ANCHOR_RE.fullmatch(unit.strip())
    if match is None or not match.group("label").strip():
        return None
    return match.group("location").strip()


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
        included = split_units(raw_included)
        boundary = split_units(raw_boundary)
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
        if not scope.included_units:
            findings.append(ScopeFinding(scope.line, "INDEX_SCOPE_VALUE", "Scope requires one or more Included units", affected))
        if not scope.note or scope.note == "none":
            findings.append(ScopeFinding(scope.line, "INDEX_SCOPE_VALUE", "Scope Note must be concrete", affected))
        included_locations = [unit_location(unit) for unit in scope.included_units]
        boundary_locations = [unit_location(unit) for unit in scope.boundary_units]
        for label, units, locations in (
            ("Included", scope.included_units, included_locations),
            ("Boundary", scope.boundary_units, boundary_locations),
        ):
            if len(units) != len(set(units)):
                findings.append(ScopeFinding(scope.line, "INDEX_SCOPE_DUPLICATE", f"{label} units contain duplicates", affected))
            for unit, location in zip(units, locations, strict=True):
                if location is None:
                    findings.append(ScopeFinding(scope.line, "INDEX_SCOPE_UNIT", f"{label} unit needs a concrete title and one [source locator] anchor: {unit}", affected))
                    continue
                if location_path(location) != source_path:
                    findings.append(ScopeFinding(scope.line, "INDEX_SCOPE_LOCATION", f"{label} unit anchor must point to {source_path}: {location}", affected))
                    continue
                if not source_location_exists(repo_root, location):
                    findings.append(ScopeFinding(scope.line, "INDEX_SCOPE_LOCATION", f"{label} unit anchor is absent or out of range: {location}", affected))
        valid_included = [location for location in included_locations if location is not None]
        valid_boundary = [location for location in boundary_locations if location is not None]
        overlap = [
            f"{included} <> {boundary}"
            for included in valid_included
            for boundary in valid_boundary
            if locations_overlap(included, boundary)
        ]
        if overlap:
            findings.append(ScopeFinding(scope.line, "INDEX_SCOPE_OVERLAP", "Included units and Boundary units must not overlap: " + ", ".join(sorted(overlap)), affected))
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
        if count is None:
            return False
        start = int(match.group(1))
        end = int(match.group(2) or start)
        return 1 <= start <= end <= count
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


def _pdf_page_range(location: str) -> tuple[int, int] | None:
    match = PDF_FRAGMENT_RE.fullmatch(_location_fragment(location))
    if match is None:
        return None
    start = int(match.group(1))
    return start, int(match.group(2) or start)


def locations_overlap(left: str, right: str) -> bool:
    if location_path(left) != location_path(right):
        return False
    left_pages = _pdf_page_range(left)
    right_pages = _pdf_page_range(right)
    if left_pages is not None and right_pages is not None:
        return max(left_pages[0], right_pages[0]) <= min(left_pages[1], right_pages[1])
    return _location_fragment(left) == _location_fragment(right)


def _location_is_covered_by_unit(location: str, unit: str) -> bool:
    anchor = unit_location(unit)
    if anchor is None or location_path(anchor) != location_path(location):
        return False
    location_pages = _pdf_page_range(location)
    anchor_pages = _pdf_page_range(anchor)
    if location_pages is not None and anchor_pages is not None:
        return anchor_pages[0] <= location_pages[0] and location_pages[1] <= anchor_pages[1]
    return _location_fragment(anchor) == _location_fragment(location)


def location_is_included(location: str, scope: CourseScope) -> bool:
    path = location_path(location)
    if path is None:
        return False
    return any(_location_is_covered_by_unit(location, included) for included in scope.included_units)


def location_is_boundary(location: str, scope: CourseScope) -> bool:
    path = location_path(location)
    if path is None:
        return False
    return any(_location_is_covered_by_unit(location, boundary) for boundary in scope.boundary_units)
