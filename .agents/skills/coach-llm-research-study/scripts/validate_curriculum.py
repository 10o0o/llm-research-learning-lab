#!/usr/bin/env python3
"""Validate CURRICULUM.md without third-party Python dependencies."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CURRICULUM = REPO_ROOT / "CURRICULUM.md"

COMPETENCY_HEADER = (
    "ID",
    "학습 성과",
    "목표 깊이",
    "선수 ID",
    "요구 근거",
    "자료 연결",
    "자료 충족도",
    "공백 처리",
    "비고",
)
SOURCE_HEADER = (
    "Source ID",
    "정확한 경로",
    "자료 형식",
    "SHA-256",
    "무결성",
    "감사 상태",
    "감사일",
    "비고",
)

REQUIRED_SECTIONS = (
    "## 1. 목적과 비목적",
    "## 2. ID, 깊이, 자료 충족도 범례",
    "## 3. 공통 핵심 역량",
    "## 4. 선택 전문 트랙",
    "## 5. 현재 강의자료 Registry",
    "## 6. 감사 중 발견된 주요 오류와 공백",
    "## 7. 갱신 규칙",
)

CORE_RANGES = {
    "MATH": 4,
    "PROB": 3,
    "STAT": 2,
    "ML": 5,
    "DL": 7,
    "NLP": 2,
    "LM": 2,
    "TRF": 3,
    "LLM": 4,
    "EVAL": 3,
    "SYS": 3,
    "RES": 3,
}
TRACK_RANGES = {"MOD": 4, "SYS": 4, "EVAL": 4, "DATA": 4}
EXPECTED_CORE_IDS = {
    f"CC-{area}-{number:02d}"
    for area, last in CORE_RANGES.items()
    for number in range(1, last + 1)
}
EXPECTED_TRACK_IDS = {
    f"TR-{area}-{number:02d}"
    for area, last in TRACK_RANGES.items()
    for number in range(1, last + 1)
}
EXPECTED_COMPETENCY_IDS = EXPECTED_CORE_IDS | EXPECTED_TRACK_IDS

COURSES = {
    "KBM": (
        "kant-basic-math",
        (
            "01-01", "01-02", "01-03", "01-04",
            "02-01", "02-02", "02-03",
            "03-01", "03-02", "03-03",
            "04-01", "04-02", "04-03",
            "05-01", "05-02", "06-01", "06-02", "07-01", "07-02",
        ),
    ),
    "KAM": (
        "kant-advanced-machine-learning",
        (
            "01-01", "01-02", "02-01", "02-02", "02-03",
            "03-01", "03-02", "04-01", "04-02", "05-01", "05-02",
        ),
    ),
    "KDL": (
        "kant-deep-learning-basics",
        (
            "01-00", "01-01", "01-02", "01-03", "01-04",
            "02-01", "02-02", "02-03", "02-04",
            "03-01", "03-02", "03-03", "03-04", "03-05",
            "04-01", "04-02", "04-03", "04-04",
            "05-01", "05-02", "05-03", "05-04",
            "06-01", "06-02", "06-03", "06-04", "06-05",
            "07-01", "07-02", "07-03", "07-04", "07-05",
        ),
    ),
}
EXPECTED_SOURCE_IDS = {
    f"SRC-{course}-{lesson}"
    for course, (_, lessons) in COURSES.items()
    for lesson in lessons
}

ALLOWED_DEPTHS = {"D1", "D2", "D3"}
ALLOWED_EVIDENCE = {
    "explain", "calculate", "shape", "implement",
    "debug", "interpret", "design", "transfer",
}
ALLOWED_RELATIONS = {"primary", "supporting", "context"}
ALLOWED_COVERAGE = {"미감사", "충분", "부분", "없음", "판정보류"}
ALLOWED_GAP_ACTIONS = {
    "그대로 사용", "수업 내 보충", "별도 자료 확보",
    "원본 복구 후 재감사", "트랙 선택 시 확보",
}
ALLOWED_FORMATS = {"PDF 페이지 보존형 Markdown", "HTML 토글 펼침 Markdown", "PDF"}
ALLOWED_INTEGRITY = {"complete", "limited", "blocked", "unverified"}
ALLOWED_AUDIT_STATUS = {"complete", "blocked", "pending"}
FORBIDDEN_PROGRESS_FIELDS = {
    "완료", "완료 여부", "점수", "진도", "진도율", "학습 날짜", "학습일",
    "mastery", "mastery 체크박스", "숙련도",
}

COMPETENCY_ID_RE = re.compile(r"(?:CC-[A-Z]+-\d{2}|TR-[A-Z]+-\d{2})\Z")
SOURCE_ID_RE = re.compile(r"SRC-(KBM|KAM|KDL)-(\d{2}-\d{2})\Z")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    code: str
    message: str

    def render(self) -> str:
        return f"ERROR {self.path}:{self.line} [{self.code}] {self.message}"


@dataclass(frozen=True)
class TableRow:
    line: int
    cells: tuple[str, ...]


@dataclass
class Competency:
    identifier: str
    line: int
    depth: str
    prerequisites: list[str]
    evidence: list[str]
    relations: dict[str, list[str]]
    coverage: str
    gap_action: str


@dataclass
class Source:
    identifier: str
    line: int
    relative_path: str
    material_format: str
    digest: str
    integrity: str
    audit_status: str
    audit_date: str
    note: str


def _display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path)


def _unwrap_code(cell: str) -> str:
    value = cell.strip()
    if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        return value[1:-1].strip()
    return value


def _split_table_row(line: str) -> tuple[str, ...] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return tuple(cell.strip() for cell in stripped[1:-1].split("|"))


def _is_separator(cells: tuple[str, ...] | None, width: int) -> bool:
    return bool(
        cells
        and len(cells) == width
        and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)
    )


def _extract_tables(
    lines: list[str],
    header: tuple[str, ...],
    document_path: str,
    findings: list[Finding],
) -> tuple[list[TableRow], int]:
    rows: list[TableRow] = []
    occurrences = 0
    index = 0
    while index < len(lines):
        cells = _split_table_row(lines[index])
        if cells != header:
            index += 1
            continue
        occurrences += 1
        if index + 1 >= len(lines) or not _is_separator(
            _split_table_row(lines[index + 1]), len(header)
        ):
            findings.append(Finding(
                document_path, index + 1, "TABLE_SEPARATOR",
                f"{header[0]} table must have a Markdown separator row",
            ))
            index += 1
            continue
        cursor = index + 2
        while cursor < len(lines) and lines[cursor].lstrip().startswith("|"):
            row_cells = _split_table_row(lines[cursor])
            if row_cells is None or len(row_cells) != len(header):
                findings.append(Finding(
                    document_path, cursor + 1, "TABLE_WIDTH",
                    f"{header[0]} table row has {len(row_cells or ())} cells; expected {len(header)}",
                ))
            elif not _is_separator(row_cells, len(header)):
                rows.append(TableRow(cursor + 1, row_cells))
            cursor += 1
        index = cursor
    return rows, occurrences


def _parse_prerequisites(cell: str) -> list[str]:
    if cell.strip() in {"", "—"}:
        return []
    return [_unwrap_code(item) for item in cell.split(",") if item.strip()]


def _parse_evidence(cell: str) -> list[str]:
    return [_unwrap_code(item) for item in cell.split(",") if item.strip()]


def _parse_relations(
    cell: str,
    line: int,
    document_path: str,
    findings: list[Finding],
) -> dict[str, list[str]]:
    relations: dict[str, list[str]] = {}
    if cell.strip() in {"", "—"}:
        return relations
    for group in cell.split(";"):
        if ":" not in group:
            findings.append(Finding(
                document_path, line, "RELATION_SYNTAX",
                f"material relation group lacks ':': {group.strip()!r}",
            ))
            continue
        relation, identifiers = (part.strip() for part in group.split(":", 1))
        if relation not in ALLOWED_RELATIONS:
            findings.append(Finding(
                document_path, line, "RELATION_ENUM",
                f"unsupported material relation {relation!r}",
            ))
            continue
        if relation in relations:
            findings.append(Finding(
                document_path, line, "RELATION_DUPLICATE",
                f"material relation {relation!r} appears more than once",
            ))
        values = [_unwrap_code(item) for item in identifiers.split(",") if item.strip()]
        if not values:
            findings.append(Finding(
                document_path, line, "RELATION_EMPTY",
                f"material relation {relation!r} has no source IDs",
            ))
        relations.setdefault(relation, []).extend(values)
    return relations


def _validate_document_shape(
    lines: list[str], document_path: str, findings: list[Finding]
) -> None:
    if "<!-- curriculum-schema: 1 -->" not in lines:
        findings.append(Finding(
            document_path, 1, "SCHEMA_VERSION", "missing curriculum schema marker version 1",
        ))

    positions: list[int] = []
    for heading in REQUIRED_SECTIONS:
        matches = [index for index, line in enumerate(lines) if line == heading]
        if len(matches) != 1:
            findings.append(Finding(
                document_path, 1, "SECTION_LAYOUT",
                f"required heading must appear exactly once: {heading!r}",
            ))
        else:
            positions.append(matches[0])
    if len(positions) == len(REQUIRED_SECTIONS) and positions != sorted(positions):
        findings.append(Finding(
            document_path, 1, "SECTION_ORDER", "required sections are out of order",
        ))

    for index in range(len(lines) - 1):
        cells = _split_table_row(lines[index])
        next_cells = _split_table_row(lines[index + 1])
        if not cells or not _is_separator(next_cells, len(cells)):
            continue
        for cell in cells:
            normalized = _unwrap_code(cell).strip().lower()
            if normalized in FORBIDDEN_PROGRESS_FIELDS:
                findings.append(Finding(
                    document_path, index + 1, "PROGRESS_FIELD",
                    f"learner progress field is forbidden in curriculum tables: {cell!r}",
                ))


def _parse_competencies(
    rows: list[TableRow], document_path: str, findings: list[Finding]
) -> list[Competency]:
    competencies: list[Competency] = []
    for row in rows:
        identifier = _unwrap_code(row.cells[0])
        depth = _unwrap_code(row.cells[2])
        prerequisites = _parse_prerequisites(row.cells[3])
        evidence = _parse_evidence(row.cells[4])
        relations = _parse_relations(row.cells[5], row.line, document_path, findings)
        coverage = _unwrap_code(row.cells[6])
        gap_action = _unwrap_code(row.cells[7])
        competencies.append(Competency(
            identifier, row.line, depth, prerequisites, evidence,
            relations, coverage, gap_action,
        ))
    return competencies


def _parse_sources(
    rows: list[TableRow], document_path: str, findings: list[Finding]
) -> list[Source]:
    sources: list[Source] = []
    for row in rows:
        values = [_unwrap_code(cell) for cell in row.cells]
        sources.append(Source(
            identifier=values[0],
            line=row.line,
            relative_path=values[1],
            material_format=values[2],
            digest=values[3],
            integrity=values[4],
            audit_status=values[5],
            audit_date=values[6],
            note=values[7],
        ))
    return sources


def _duplicate_values(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def _validate_competencies(
    competencies: list[Competency],
    sources: list[Source],
    document_path: str,
    findings: list[Finding],
) -> None:
    identifiers = [item.identifier for item in competencies]
    line_by_id = {item.identifier: item.line for item in competencies}
    for duplicate in _duplicate_values(identifiers):
        findings.append(Finding(
            document_path, line_by_id[duplicate], "COMPETENCY_DUPLICATE",
            f"duplicate competency ID {duplicate}",
        ))

    actual_ids = set(identifiers)
    for missing in sorted(EXPECTED_COMPETENCY_IDS - actual_ids):
        findings.append(Finding(
            document_path, 1, "COMPETENCY_MISSING", f"missing required competency ID {missing}",
        ))
    for unexpected in sorted(actual_ids - EXPECTED_COMPETENCY_IDS):
        findings.append(Finding(
            document_path, line_by_id[unexpected], "COMPETENCY_UNEXPECTED",
            f"unexpected competency ID {unexpected}",
        ))

    source_by_id = {source.identifier: source for source in sources}
    for item in competencies:
        if not COMPETENCY_ID_RE.fullmatch(item.identifier):
            findings.append(Finding(
                document_path, item.line, "COMPETENCY_ID", f"invalid competency ID {item.identifier!r}",
            ))
        if item.depth not in ALLOWED_DEPTHS:
            findings.append(Finding(
                document_path, item.line, "DEPTH_ENUM", f"unsupported depth {item.depth!r}",
            ))
        if item.identifier.startswith("TR-") and item.depth != "D3":
            findings.append(Finding(
                document_path, item.line, "TRACK_DEPTH", "every optional track must target D3",
            ))
        if not item.evidence:
            findings.append(Finding(
                document_path, item.line, "EVIDENCE_EMPTY", "at least one evidence token is required",
            ))
        for token in item.evidence:
            if token not in ALLOWED_EVIDENCE:
                findings.append(Finding(
                    document_path, item.line, "EVIDENCE_ENUM",
                    f"unsupported evidence token {token!r}",
                ))
        if len(item.evidence) != len(set(item.evidence)):
            findings.append(Finding(
                document_path, item.line, "EVIDENCE_DUPLICATE", "evidence tokens must be unique",
            ))
        for prerequisite in item.prerequisites:
            if not COMPETENCY_ID_RE.fullmatch(prerequisite):
                findings.append(Finding(
                    document_path, item.line, "PREREQUISITE_ID",
                    f"invalid prerequisite ID {prerequisite!r}",
                ))
            elif prerequisite not in actual_ids:
                findings.append(Finding(
                    document_path, item.line, "PREREQUISITE_MISSING",
                    f"unknown prerequisite ID {prerequisite}",
                ))
        if len(item.prerequisites) != len(set(item.prerequisites)):
            findings.append(Finding(
                document_path, item.line, "PREREQUISITE_DUPLICATE",
                "prerequisite IDs must be unique",
            ))
        if item.coverage not in ALLOWED_COVERAGE:
            findings.append(Finding(
                document_path, item.line, "COVERAGE_ENUM",
                f"unsupported material coverage {item.coverage!r}",
            ))
        if item.gap_action not in ALLOWED_GAP_ACTIONS:
            findings.append(Finding(
                document_path, item.line, "GAP_ACTION_ENUM",
                f"unsupported gap action {item.gap_action!r}",
            ))

        linked = [
            source_id
            for source_ids in item.relations.values()
            for source_id in source_ids
        ]
        for source_id in linked:
            if not SOURCE_ID_RE.fullmatch(source_id):
                findings.append(Finding(
                    document_path, item.line, "SOURCE_LINK_ID",
                    f"invalid linked source ID {source_id!r}",
                ))
            elif source_id not in source_by_id:
                findings.append(Finding(
                    document_path, item.line, "SOURCE_LINK_MISSING",
                    f"linked source is absent from registry: {source_id}",
                ))
        if len(linked) != len(set(linked)):
            findings.append(Finding(
                document_path, item.line, "SOURCE_LINK_DUPLICATE",
                "a source may appear only once in one competency mapping",
            ))

        direct = item.relations.get("primary", []) + item.relations.get("supporting", [])
        if item.coverage == "충분" and not direct:
            findings.append(Finding(
                document_path, item.line, "SUFFICIENT_WITHOUT_DIRECT_SOURCE",
                "coverage '충분' requires at least one primary or supporting source",
            ))
        if item.coverage in {"부분", "없음", "판정보류"} and item.gap_action == "그대로 사용":
            findings.append(Finding(
                document_path, item.line, "GAP_ACTION_REQUIRED",
                f"coverage {item.coverage!r} requires an actual gap treatment",
            ))
        if item.coverage == "없음" and direct:
            findings.append(Finding(
                document_path, item.line, "NONE_WITH_DIRECT_SOURCE",
                "coverage '없음' cannot have a primary or supporting source; use '부분'",
            ))
        if item.coverage == "판정보류" and item.gap_action != "원본 복구 후 재감사":
            findings.append(Finding(
                document_path, item.line, "DEFERRED_WITHOUT_RECOVERY",
                "coverage '판정보류' requires '원본 복구 후 재감사'",
            ))
        if item.coverage in {"충분", "부분"}:
            for source_id in direct:
                source = source_by_id.get(source_id)
                if source and source.audit_status != "complete":
                    findings.append(Finding(
                        document_path, item.line, "UNAUDITED_COVERAGE_SOURCE",
                        f"{item.coverage} coverage links non-complete source {source_id}",
                    ))
            if item.coverage == "충분" and direct and not any(
                source_by_id.get(source_id)
                and source_by_id[source_id].integrity == "complete"
                for source_id in direct
            ):
                findings.append(Finding(
                    document_path, item.line, "SUFFICIENT_ONLY_LIMITED",
                    "coverage '충분' needs at least one complete-integrity direct source",
                ))

    graph = {
        item.identifier: [p for p in item.prerequisites if p in actual_ids]
        for item in competencies
    }
    state: dict[str, int] = {}
    stack: list[str] = []
    reported_cycles: set[tuple[str, ...]] = set()

    def visit(identifier: str) -> None:
        state[identifier] = 1
        stack.append(identifier)
        for prerequisite in graph.get(identifier, []):
            if state.get(prerequisite, 0) == 0:
                visit(prerequisite)
            elif state.get(prerequisite) == 1:
                start = stack.index(prerequisite)
                cycle = tuple(stack[start:] + [prerequisite])
                if cycle not in reported_cycles:
                    reported_cycles.add(cycle)
                    findings.append(Finding(
                        document_path, line_by_id.get(identifier, 1), "PREREQUISITE_CYCLE",
                        "prerequisite cycle: " + " -> ".join(cycle),
                    ))
        stack.pop()
        state[identifier] = 2

    for identifier in graph:
        if state.get(identifier, 0) == 0:
            visit(identifier)


def _validate_sources(
    sources: list[Source], document_path: str, findings: list[Finding]
) -> None:
    identifiers = [source.identifier for source in sources]
    line_by_id = {source.identifier: source.line for source in sources}
    for duplicate in _duplicate_values(identifiers):
        findings.append(Finding(
            document_path, line_by_id[duplicate], "SOURCE_DUPLICATE",
            f"duplicate source ID {duplicate}",
        ))
    actual_ids = set(identifiers)
    for missing in sorted(EXPECTED_SOURCE_IDS - actual_ids):
        findings.append(Finding(
            document_path, 1, "SOURCE_MISSING", f"missing required source ID {missing}",
        ))
    for unexpected in sorted(actual_ids - EXPECTED_SOURCE_IDS):
        findings.append(Finding(
            document_path, line_by_id[unexpected], "SOURCE_UNEXPECTED",
            f"unexpected source ID {unexpected}",
        ))
    expected_source_count = len(EXPECTED_SOURCE_IDS)
    if len(sources) != expected_source_count:
        findings.append(Finding(
            document_path, 1, "SOURCE_COUNT",
            f"registry has {len(sources)} rows; expected {expected_source_count}",
        ))

    paths = [source.relative_path for source in sources]
    for duplicate in _duplicate_values(paths):
        source = next(item for item in sources if item.relative_path == duplicate)
        findings.append(Finding(
            document_path, source.line, "SOURCE_PATH_DUPLICATE",
            f"source path is registered more than once: {duplicate}",
        ))

    for source in sources:
        match = SOURCE_ID_RE.fullmatch(source.identifier)
        if not match:
            findings.append(Finding(
                document_path, source.line, "SOURCE_ID", f"invalid source ID {source.identifier!r}",
            ))
        else:
            course, lesson = match.groups()
            course_dir = COURSES[course][0]
            expected_prefix = f"materials/private/{course_dir}/"
            filename = Path(source.relative_path).name
            if not source.relative_path.startswith(expected_prefix) or not filename.startswith(lesson + "_"):
                findings.append(Finding(
                    document_path, source.line, "SOURCE_PATH_ID_MISMATCH",
                    f"path does not match {source.identifier}: {source.relative_path}",
                ))
        path_object = Path(source.relative_path)
        if path_object.is_absolute() or ".." in path_object.parts or "course-provided-practice" in path_object.parts:
            findings.append(Finding(
                document_path, source.line, "SOURCE_PATH_SCOPE",
                f"source path must be a safe course-relative lesson path: {source.relative_path}",
            ))
        if source.material_format not in ALLOWED_FORMATS:
            findings.append(Finding(
                document_path, source.line, "SOURCE_FORMAT_ENUM",
                f"unsupported source format {source.material_format!r}",
            ))
        if source.material_format == "PDF" and path_object.suffix.lower() != ".pdf":
            findings.append(Finding(
                document_path, source.line, "SOURCE_FORMAT_SUFFIX", "PDF format requires a .pdf path",
            ))
        if source.material_format.endswith("Markdown") and path_object.suffix.lower() != ".md":
            findings.append(Finding(
                document_path, source.line, "SOURCE_FORMAT_SUFFIX", "Markdown format requires a .md path",
            ))
        if not SHA256_RE.fullmatch(source.digest):
            findings.append(Finding(
                document_path, source.line, "SOURCE_HASH", "SHA-256 must be 64 lowercase hex characters",
            ))
        if source.integrity not in ALLOWED_INTEGRITY:
            findings.append(Finding(
                document_path, source.line, "INTEGRITY_ENUM",
                f"unsupported integrity value {source.integrity!r}",
            ))
        if source.audit_status not in ALLOWED_AUDIT_STATUS:
            findings.append(Finding(
                document_path, source.line, "AUDIT_STATUS_ENUM",
                f"unsupported audit status {source.audit_status!r}",
            ))
        if source.audit_status == "complete" and source.integrity == "unverified":
            findings.append(Finding(
                document_path, source.line, "COMPLETE_UNVERIFIED",
                "complete audit cannot have unverified integrity",
            ))
        if source.audit_status == "blocked" and not source.note.strip():
            findings.append(Finding(
                document_path, source.line, "BLOCKED_WITHOUT_NOTE",
                "blocked source requires a reason in 비고",
            ))
        try:
            dt.date.fromisoformat(source.audit_date)
        except ValueError:
            findings.append(Finding(
                document_path, source.line, "AUDIT_DATE", f"invalid ISO audit date {source.audit_date!r}",
            ))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _extract_index_lessons(index_path: Path) -> list[str]:
    text = index_path.read_text(encoding="utf-8")
    try:
        lesson_section = text.split("## 강의 자료", 1)[1]
    except IndexError:
        return []
    lesson_section = re.split(r"^## ", lesson_section, maxsplit=1, flags=re.MULTILINE)[0]
    return re.findall(r"^\| `([^`]+)` \|", lesson_section, flags=re.MULTILINE)


def _local_link_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1:target.index(">")]
    else:
        target = re.split(r"\s+[\"']", target, maxsplit=1)[0]
    target = unquote(target.replace("\\(", "(").replace("\\)", ")"))
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    return parsed.path


def _check_asset_signature(path: Path) -> str | None:
    data = path.read_bytes()
    if not data:
        return "asset is empty"
    suffix = path.suffix.lower()
    if suffix == ".webp" and not (len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP"):
        return "invalid WebP signature"
    if suffix == ".png" and not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "invalid PNG signature"
    if suffix in {".jpg", ".jpeg"} and not (data.startswith(b"\xff\xd8") and data.endswith(b"\xff\xd9")):
        return "invalid JPEG signature"
    if suffix == ".svg":
        try:
            root = ElementTree.fromstring(data)
        except ElementTree.ParseError as exc:
            return f"invalid SVG XML: {exc}"
        if not root.tag.endswith("svg"):
            return "SVG root element is not <svg>"
    return None


def _course_for_index(
    course_index: Path,
    repo_root: Path,
) -> tuple[str, str, tuple[str, ...]] | None:
    try:
        relative = course_index.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return None
    for course, (directory, expected_lessons) in COURSES.items():
        expected = f"materials/private/{directory}/INDEX.md"
        if relative == expected:
            return course, directory, expected_lessons
    return None


def _strict_source_checks(
    sources: list[Source],
    repo_root: Path,
    findings: list[Finding],
    *,
    course_index: Path | None = None,
) -> None:
    root = repo_root.resolve()
    selected_course = None
    if course_index is not None:
        selected_course = _course_for_index(course_index, repo_root)
        if selected_course is None:
            findings.append(Finding(
                _display_path(course_index, repo_root),
                1,
                "INDEX_SCOPE",
                "--course-index must name a configured course INDEX.md",
            ))
            return
    selected_directory = selected_course[1] if selected_course else None
    scoped_sources = [
        source
        for source in sources
        if selected_directory is None
        or source.relative_path.startswith(f"materials/private/{selected_directory}/")
    ]
    registered_paths: set[str] = set()
    for source in scoped_sources:
        source_path = repo_root / source.relative_path
        display = source.relative_path
        if source.audit_status != "complete":
            findings.append(Finding(
                display,
                1,
                "SOURCE_AUDIT_INCOMPLETE",
                f"registered source audit status is {source.audit_status!r}; expected 'complete'",
            ))
        try:
            resolved = source_path.resolve(strict=True)
        except FileNotFoundError:
            findings.append(Finding(display, 1, "SOURCE_FILE_MISSING", "registered source does not exist"))
            continue
        try:
            resolved.relative_to(root)
        except ValueError:
            findings.append(Finding(display, 1, "SOURCE_FILE_SCOPE", "resolved source escapes repository root"))
            continue
        if not resolved.is_file():
            findings.append(Finding(display, 1, "SOURCE_NOT_FILE", "registered source is not a regular file"))
            continue
        registered_paths.add(source.relative_path)
        actual_digest = sha256_file(resolved)
        if actual_digest != source.digest:
            findings.append(Finding(
                display, 1, "SOURCE_HASH_STALE",
                f"registry SHA-256 {source.digest} does not match file {actual_digest}",
            ))
        data = resolved.read_bytes()
        if source.material_format == "PDF":
            if not data.startswith(b"%PDF-") or b"%%EOF" not in data[-4096:]:
                findings.append(Finding(display, 1, "PDF_STRUCTURE", "file lacks a valid PDF header or EOF marker"))
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            findings.append(Finding(display, 1, "MARKDOWN_ENCODING", f"source is not UTF-8: {exc}"))
            continue
        in_fence = False
        for line_number, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in MARKDOWN_LINK_RE.finditer(line):
                local = _local_link_target(match.group(1))
                if local is None:
                    continue
                linked_path = resolved.parent / local
                try:
                    linked_resolved = linked_path.resolve(strict=True)
                except FileNotFoundError:
                    findings.append(Finding(
                        display, line_number, "INTERNAL_LINK_MISSING",
                        f"local link target does not exist: {local}",
                    ))
                    continue
                try:
                    linked_resolved.relative_to(root)
                except ValueError:
                    findings.append(Finding(
                        display, line_number, "INTERNAL_LINK_SCOPE",
                        f"local link target escapes repository: {local}",
                    ))
                    continue
                if match.group(0).startswith("!"):
                    problem = _check_asset_signature(linked_resolved)
                    if problem:
                        findings.append(Finding(
                            display, line_number, "ASSET_INTEGRITY", f"{local}: {problem}",
                        ))

    indexed_paths: set[str] = set()
    course_items = (
        [(selected_course[0], (selected_course[1], selected_course[2]))]
        if selected_course
        else list(COURSES.items())
    )
    for course, (directory, expected_lessons) in course_items:
        index_path = repo_root / "materials" / "private" / directory / "INDEX.md"
        display = str(index_path.relative_to(repo_root))
        if not index_path.is_file():
            findings.append(Finding(display, 1, "INDEX_MISSING", f"course index for {course} is missing"))
            continue
        filenames = _extract_index_lessons(index_path)
        if len(filenames) != len(expected_lessons):
            findings.append(Finding(
                display, 1, "INDEX_COUNT",
                f"강의 자료 table has {len(filenames)} rows; expected {len(expected_lessons)}",
            ))
        for duplicate in _duplicate_values(filenames):
            findings.append(Finding(display, 1, "INDEX_DUPLICATE", f"duplicate lesson path {duplicate}"))
        actual_lessons = {filename[:5] for filename in filenames}
        expected_lesson_set = set(expected_lessons)
        if actual_lessons != expected_lesson_set:
            missing = sorted(expected_lesson_set - actual_lessons)
            extra = sorted(actual_lessons - expected_lesson_set)
            findings.append(Finding(
                display, 1, "INDEX_LESSON_IDS",
                f"lesson IDs differ; missing={missing}, extra={extra}",
            ))
        for filename in filenames:
            if "/" in filename or "\\" in filename or filename.startswith("course-provided-practice"):
                findings.append(Finding(
                    display, 1, "INDEX_SCOPE", f"강의 자료 contains an out-of-scope path: {filename}",
                ))
            indexed_paths.add(f"materials/private/{directory}/{filename}")

    for missing in sorted(indexed_paths - registered_paths):
        findings.append(Finding(missing, 1, "INDEX_NOT_REGISTERED", "indexed lesson is absent from registry"))
    for extra in sorted(registered_paths - indexed_paths):
        findings.append(Finding(extra, 1, "REGISTRY_NOT_INDEXED", "registered source is absent from course index"))


def validate_course_index_freshness(
    curriculum_path: Path,
    course_index: Path,
    *,
    repo_root: Path = REPO_ROOT,
) -> list[Finding]:
    """Validate one configured course INDEX against registry rows and source bytes."""
    path = curriculum_path.resolve()
    document_path = _display_path(path, repo_root)
    findings: list[Finding] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return [Finding(document_path, 1, "CURRICULUM_MISSING", "curriculum document does not exist")]
    except UnicodeDecodeError as exc:
        return [Finding(document_path, 1, "CURRICULUM_ENCODING", f"document is not UTF-8: {exc}")]

    source_rows, source_tables = _extract_tables(
        lines, SOURCE_HEADER, document_path, findings,
    )
    if source_tables != 1:
        findings.append(Finding(
            document_path,
            1,
            "SOURCE_TABLE_COUNT",
            f"found {source_tables} source registry tables; expected 1",
        ))
        return findings
    sources = _parse_sources(source_rows, document_path, findings)
    _strict_source_checks(
        sources,
        repo_root,
        findings,
        course_index=course_index,
    )
    return findings


def validate_curriculum(
    curriculum_path: Path = DEFAULT_CURRICULUM,
    *,
    strict_sources: bool = False,
    course_index: Path | None = None,
    repo_root: Path = REPO_ROOT,
) -> list[Finding]:
    path = curriculum_path.resolve()
    document_path = _display_path(path, repo_root)
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [Finding(document_path, 1, "CURRICULUM_MISSING", "curriculum document does not exist")]
    except UnicodeDecodeError as exc:
        return [Finding(document_path, 1, "CURRICULUM_ENCODING", f"document is not UTF-8: {exc}")]
    lines = text.splitlines()
    _validate_document_shape(lines, document_path, findings)

    competency_rows, competency_tables = _extract_tables(
        lines, COMPETENCY_HEADER, document_path, findings,
    )
    source_rows, source_tables = _extract_tables(
        lines, SOURCE_HEADER, document_path, findings,
    )
    if competency_tables != 2:
        findings.append(Finding(
            document_path, 1, "COMPETENCY_TABLE_COUNT",
            f"found {competency_tables} competency tables; expected 2",
        ))
    if source_tables != 1:
        findings.append(Finding(
            document_path, 1, "SOURCE_TABLE_COUNT",
            f"found {source_tables} source registry tables; expected 1",
        ))

    competencies = _parse_competencies(competency_rows, document_path, findings)
    sources = _parse_sources(source_rows, document_path, findings)
    _validate_sources(sources, document_path, findings)
    _validate_competencies(competencies, sources, document_path, findings)
    if strict_sources:
        _strict_source_checks(
            sources,
            repo_root,
            findings,
            course_index=course_index,
        )
    return findings


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate CURRICULUM.md structure and optional private source integrity.",
    )
    parser.add_argument(
        "path", nargs="?", type=Path, default=DEFAULT_CURRICULUM,
        help="curriculum Markdown path (default: repository CURRICULUM.md)",
    )
    parser.add_argument(
        "--strict-sources", action="store_true",
        help="also check private files, SHA-256, course index parity, and local links",
    )
    parser.add_argument(
        "--course-index", type=Path,
        help="with --strict-sources, restrict byte and parity checks to one configured course INDEX.md",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.course_index is not None and not args.strict_sources:
        parser.error("--course-index requires --strict-sources")
    try:
        findings = validate_curriculum(
            args.path,
            strict_sources=args.strict_sources,
            course_index=args.course_index,
        )
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        print(f"ERROR {args.path}:1 [VALIDATOR_INTERNAL] {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    if findings:
        for finding in findings:
            print(finding.render(), file=sys.stderr)
        return 1
    mode = "strict source and structure" if args.strict_sources else "structure"
    print(f"OK {args.path}: {mode} validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
