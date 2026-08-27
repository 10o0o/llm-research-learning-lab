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


SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from pdf_utils import pdf_page_count as _pdf_page_count  # noqa: E402


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
REGISTRY_SUMMARY_HEADER = (
    "과정 수",
    "Source 수",
    "Markdown 자산",
    "Raster",
    "SVG",
    "기타 자산",
    "PDF 페이지",
    "Limited source",
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
SOURCE_ID_RE = re.compile(
    r"SRC-([A-Z0-9]+(?:-[A-Z0-9]+)*)-(\d{2}-\d{2})\Z"
)
SOURCE_NAMESPACE_RE = re.compile(r"[A-Z0-9]+(?:-[A-Z0-9]+)*\Z")
LESSON_FILENAME_RE = re.compile(r"(\d{2}-\d{2})_.+\Z")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
RASTER_SUFFIXES = {
    ".avif", ".bmp", ".gif", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp",
}


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    code: str
    message: str
    affected_source_paths: tuple[str, ...] = ()

    def render(self) -> str:
        return f"ERROR {self.path}:{self.line} [{self.code}] {self.message}"


@dataclass
class LessonSliceFreshness:
    errors: list[Finding]
    warnings: list[Finding]


@dataclass(frozen=True)
class TableRow:
    line: int
    cells: tuple[str, ...]


@dataclass(frozen=True)
class IndexLesson:
    filename: str
    line: int


@dataclass(frozen=True)
class RegistrySummary:
    courses: int
    sources: int
    markdown_assets: int
    raster_assets: int
    svg_assets: int
    other_assets: int
    pdf_pages: int
    limited_sources: int


@dataclass(frozen=True)
class CurriculumTargetSnapshot:
    depth: str
    prerequisites: tuple[str, ...]
    required_evidence: tuple[str, ...]
    coverage: str
    gap_action: str
    line: int
    direct_source_ids: tuple[str, ...]
    direct_source_paths: frozenset[str]


@dataclass(frozen=True)
class CurriculumSnapshot:
    targets: dict[str, CurriculumTargetSnapshot]
    source_paths_by_id: dict[str, tuple[str, ...]]
    source_ids_by_path: dict[str, tuple[str, ...]]


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


def curriculum_snapshot_from_text(text: str) -> CurriculumSnapshot:
    """Return target/source relations without requiring private source bytes."""
    lines = text.splitlines()
    ignored_findings: list[Finding] = []
    competency_rows, _ = _extract_tables(
        lines, COMPETENCY_HEADER, "CURRICULUM.md", ignored_findings,
    )
    source_rows, _ = _extract_tables(
        lines, SOURCE_HEADER, "CURRICULUM.md", ignored_findings,
    )
    competencies = _parse_competencies(
        competency_rows, "CURRICULUM.md", ignored_findings,
    )
    sources = _parse_sources(source_rows, "CURRICULUM.md", ignored_findings)

    paths_by_id: dict[str, list[str]] = {}
    ids_by_path: dict[str, list[str]] = {}
    for source in sources:
        paths_by_id.setdefault(source.identifier, []).append(source.relative_path)
        ids_by_path.setdefault(source.relative_path, []).append(source.identifier)

    targets: dict[str, CurriculumTargetSnapshot] = {}
    for competency in competencies:
        direct_ids = tuple(
            competency.relations.get("primary", [])
            + competency.relations.get("supporting", [])
        )
        direct_paths = frozenset(
            path
            for source_id in direct_ids
            for path in paths_by_id.get(source_id, [])
        )
        targets[competency.identifier] = CurriculumTargetSnapshot(
            depth=competency.depth,
            prerequisites=tuple(competency.prerequisites),
            required_evidence=tuple(competency.evidence),
            coverage=competency.coverage,
            gap_action=competency.gap_action,
            line=competency.line,
            direct_source_ids=direct_ids,
            direct_source_paths=direct_paths,
        )

    return CurriculumSnapshot(
        targets=targets,
        source_paths_by_id={
            source_id: tuple(paths) for source_id, paths in paths_by_id.items()
        },
        source_ids_by_path={
            path: tuple(source_ids) for path, source_ids in ids_by_path.items()
        },
    )


def _parse_registry_summary(
    rows: list[TableRow],
    occurrences: int,
    document_path: str,
    findings: list[Finding],
) -> RegistrySummary | None:
    if occurrences != 1:
        findings.append(Finding(
            document_path,
            1,
            "REGISTRY_SUMMARY_COUNT",
            f"found {occurrences} registry summary tables; expected 1",
        ))
        return None
    if len(rows) != 1:
        findings.append(Finding(
            document_path,
            rows[0].line if rows else 1,
            "REGISTRY_SUMMARY_COUNT",
            f"registry summary must contain exactly one data row; found {len(rows)}",
        ))
        return None
    row = rows[0]
    values: list[int] = []
    for label, cell in zip(REGISTRY_SUMMARY_HEADER, row.cells, strict=True):
        value = _unwrap_code(cell)
        if not re.fullmatch(r"\d+", value):
            findings.append(Finding(
                document_path,
                row.line,
                "REGISTRY_SUMMARY_VALUE",
                f"{label} must be a non-negative integer; got {value!r}",
            ))
            return None
        values.append(int(value))
    summary = RegistrySummary(*values)
    classified_assets = (
        summary.raster_assets + summary.svg_assets + summary.other_assets
    )
    if summary.markdown_assets != classified_assets:
        findings.append(Finding(
            document_path,
            row.line,
            "REGISTRY_SUMMARY_VALUE",
            "Markdown 자산 must equal Raster + SVG + 기타 자산",
        ))
    return summary


def _registry_structure_summary(sources: list[Source]) -> RegistrySummary:
    return RegistrySummary(
        courses=len({
            directory
            for source in sources
            if (directory := _source_course_directory(source)) is not None
        }),
        sources=len(sources),
        markdown_assets=0,
        raster_assets=0,
        svg_assets=0,
        other_assets=0,
        pdf_pages=0,
        limited_sources=sum(source.integrity == "limited" for source in sources),
    )


def _validate_registry_structure_summary(
    declared: RegistrySummary | None,
    sources: list[Source],
    document_path: str,
    findings: list[Finding],
) -> None:
    if declared is None:
        return
    actual = _registry_structure_summary(sources)
    expected = (actual.courses, actual.sources, actual.limited_sources)
    recorded = (declared.courses, declared.sources, declared.limited_sources)
    if recorded != expected:
        findings.append(Finding(
            document_path,
            1,
            "REGISTRY_SUMMARY_MISMATCH",
            "registry summary courses/sources/limited values "
            f"{recorded} do not match registry-derived values {expected}",
        ))


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
    def add_source_finding(source: Source, code: str, message: str) -> None:
        findings.append(Finding(
            document_path,
            source.line,
            code,
            message,
            (source.relative_path,),
        ))

    identifiers = [source.identifier for source in sources]
    for duplicate in _duplicate_values(identifiers):
        duplicate_sources = [
            source for source in sources if source.identifier == duplicate
        ]
        findings.append(Finding(
            document_path, duplicate_sources[1].line, "SOURCE_DUPLICATE",
            f"duplicate source ID {duplicate}",
            tuple(source.relative_path for source in duplicate_sources),
        ))
    paths = [source.relative_path for source in sources]
    for duplicate in _duplicate_values(paths):
        duplicate_sources = [
            source for source in sources if source.relative_path == duplicate
        ]
        findings.append(Finding(
            document_path, duplicate_sources[1].line, "SOURCE_PATH_DUPLICATE",
            f"source path is registered more than once: {duplicate}",
            (duplicate,),
        ))

    for source in sources:
        match = SOURCE_ID_RE.fullmatch(source.identifier)
        if not match:
            add_source_finding(source, "SOURCE_ID", f"invalid source ID {source.identifier!r}")
        else:
            _, lesson = match.groups()
            filename = Path(source.relative_path).name
            if not filename.startswith(lesson + "_"):
                add_source_finding(
                    source,
                    "SOURCE_PATH_ID_MISMATCH",
                    f"path does not match {source.identifier}: {source.relative_path}",
                )
        path_object = Path(source.relative_path)
        path_parts = path_object.parts
        if (
            path_object.is_absolute()
            or "\\" in source.relative_path
            or ".." in path_parts
            or len(path_parts) != 4
            or path_parts[:2] != ("materials", "private")
            or path_parts[2] in {"", ".", ".."}
            or path_parts[3] == "INDEX.md"
            or "course-provided-practice" in path_parts
        ):
            add_source_finding(
                source,
                "SOURCE_PATH_SCOPE",
                "source path must be a direct, safe lesson file under "
                f"materials/private/<course>/: {source.relative_path}",
            )
        if source.material_format not in ALLOWED_FORMATS:
            add_source_finding(
                source, "SOURCE_FORMAT_ENUM", f"unsupported source format {source.material_format!r}"
            )
        if source.material_format == "PDF" and path_object.suffix.lower() != ".pdf":
            add_source_finding(source, "SOURCE_FORMAT_SUFFIX", "PDF format requires a .pdf path")
        if source.material_format.endswith("Markdown") and path_object.suffix.lower() != ".md":
            add_source_finding(
                source, "SOURCE_FORMAT_SUFFIX", "Markdown format requires a .md path"
            )
        if not SHA256_RE.fullmatch(source.digest):
            add_source_finding(
                source, "SOURCE_HASH", "SHA-256 must be 64 lowercase hex characters"
            )
        if source.integrity not in ALLOWED_INTEGRITY:
            add_source_finding(
                source, "INTEGRITY_ENUM", f"unsupported integrity value {source.integrity!r}"
            )
        if source.audit_status not in ALLOWED_AUDIT_STATUS:
            add_source_finding(
                source, "AUDIT_STATUS_ENUM", f"unsupported audit status {source.audit_status!r}"
            )
        if source.audit_status == "complete" and source.integrity == "unverified":
            add_source_finding(
                source, "COMPLETE_UNVERIFIED", "complete audit cannot have unverified integrity"
            )
        if source.audit_status == "blocked" and not source.note.strip():
            add_source_finding(
                source, "BLOCKED_WITHOUT_NOTE", "blocked source requires a reason in 비고"
            )
        try:
            dt.date.fromisoformat(source.audit_date)
        except ValueError:
            add_source_finding(
                source, "AUDIT_DATE", f"invalid ISO audit date {source.audit_date!r}"
            )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _extract_index_lessons(index_path: Path) -> list[IndexLesson]:
    text = index_path.read_text(encoding="utf-8")
    try:
        lesson_section = text.split("## 강의 자료", 1)[1]
    except IndexError:
        return []
    section_start = text.index("## 강의 자료") + len("## 강의 자료")
    lesson_section = re.split(
        r"^## ", lesson_section, maxsplit=1, flags=re.MULTILINE,
    )[0]
    start_line = text.count("\n", 0, section_start)
    lessons: list[IndexLesson] = []
    for offset, line in enumerate(lesson_section.splitlines(), start=1):
        match = re.match(r"^\| `([^`]+)` \|", line)
        if match:
            lessons.append(IndexLesson(match.group(1), start_line + offset))
    return lessons


def _index_namespace(
    index_path: Path,
    repo_root: Path,
) -> tuple[str | None, list[Finding]]:
    display = _display_path(index_path, repo_root)
    try:
        lines = index_path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return None, [Finding(display, 1, "INDEX_MISSING", "course index is missing")]
    except UnicodeDecodeError as exc:
        return None, [Finding(
            display, 1, "INDEX_NAMESPACE_FORMAT", f"course index is not UTF-8: {exc}",
        )]
    matches = [
        (line_no, match.group(1).strip())
        for line_no, line in enumerate(lines, start=1)
        if (match := re.fullmatch(r"- source_namespace:\s*(.*?)\s*", line)) is not None
    ]
    if len(matches) != 1:
        return None, [Finding(
            display,
            matches[0][0] if matches else 1,
            "INDEX_NAMESPACE_COUNT",
            f"course INDEX must declare source_namespace exactly once; found {len(matches)}",
        )]
    line_no, namespace = matches[0]
    if SOURCE_NAMESPACE_RE.fullmatch(namespace) is None:
        return None, [Finding(
            display,
            line_no,
            "INDEX_NAMESPACE_FORMAT",
            f"invalid source_namespace {namespace!r}",
        )]
    return namespace, []


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


def _private_registry_summary(
    sources: list[Source],
    repo_root: Path,
) -> tuple[RegistrySummary | None, list[str]]:
    root = repo_root.resolve()
    assets: set[Path] = set()
    pdf_pages = 0
    unreadable: list[str] = []
    for source in sources:
        source_path = repo_root / source.relative_path
        try:
            resolved = source_path.resolve(strict=True)
            resolved.relative_to(root)
        except (FileNotFoundError, ValueError):
            unreadable.append(source.relative_path)
            continue
        if not resolved.is_file():
            unreadable.append(source.relative_path)
            continue
        if source.material_format == "PDF":
            page_count = _pdf_page_count(resolved)
            if page_count is None:
                unreadable.append(source.relative_path)
            else:
                pdf_pages += page_count
            continue
        if not source.material_format.endswith("Markdown"):
            continue
        try:
            text = resolved.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            unreadable.append(source.relative_path)
            continue
        in_fence = False
        for line in text.splitlines():
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in MARKDOWN_LINK_RE.finditer(line):
                if not match.group(0).startswith("!"):
                    continue
                local = _local_link_target(match.group(1))
                if local is None:
                    continue
                try:
                    linked = (resolved.parent / local).resolve(strict=True)
                    linked.relative_to(root)
                except (FileNotFoundError, ValueError):
                    unreadable.append(f"{source.relative_path} -> {local}")
                    continue
                if not linked.is_file():
                    unreadable.append(f"{source.relative_path} -> {local}")
                    continue
                assets.add(linked)

    if unreadable:
        return None, sorted(set(unreadable))
    raster = sum(path.suffix.lower() in RASTER_SUFFIXES for path in assets)
    svg = sum(path.suffix.lower() == ".svg" for path in assets)
    structure = _registry_structure_summary(sources)
    return RegistrySummary(
        courses=structure.courses,
        sources=structure.sources,
        markdown_assets=len(assets),
        raster_assets=raster,
        svg_assets=svg,
        other_assets=len(assets) - raster - svg,
        pdf_pages=pdf_pages,
        limited_sources=structure.limited_sources,
    ), []


def _validate_private_registry_summary(
    declared: RegistrySummary | None,
    sources: list[Source],
    repo_root: Path,
    document_path: str,
    findings: list[Finding],
) -> None:
    if declared is None:
        return
    actual, unreadable = _private_registry_summary(sources, repo_root)
    if actual is None:
        findings.append(Finding(
            document_path,
            1,
            "REGISTRY_SUMMARY_UNREADABLE",
            "cannot compute registry summary from: " + ", ".join(unreadable),
        ))
        return
    if actual != declared:
        findings.append(Finding(
            document_path,
            1,
            "REGISTRY_SUMMARY_MISMATCH",
            f"declared registry summary {declared} does not match private sources {actual}",
        ))


def _course_directory_for_index(
    course_index: Path,
    repo_root: Path,
) -> str | None:
    try:
        relative = course_index.resolve(strict=False).relative_to(repo_root.resolve())
    except ValueError:
        return None
    parts = relative.parts
    if (
        len(parts) != 4
        or parts[:2] != ("materials", "private")
        or parts[2] in {"", ".", ".."}
        or parts[3] != "INDEX.md"
    ):
        return None
    return parts[2]


def _source_course_directory(source: Source) -> str | None:
    parts = Path(source.relative_path).parts
    if len(parts) == 4 and parts[:2] == ("materials", "private"):
        return parts[2]
    return None


def _discover_course_directories(repo_root: Path) -> set[str]:
    private_root = repo_root / "materials" / "private"
    if not private_root.is_dir():
        return set()
    return {
        index_path.parent.name
        for index_path in private_root.glob("*/INDEX.md")
        if index_path.is_file()
    }


def _strict_source_checks(
    sources: list[Source],
    repo_root: Path,
    findings: list[Finding],
    *,
    course_index: Path | None = None,
) -> None:
    root = repo_root.resolve()
    selected_directory = None
    if course_index is not None:
        selected_directory = _course_directory_for_index(course_index, repo_root)
        if selected_directory is None:
            findings.append(Finding(
                _display_path(course_index, repo_root),
                1,
                "INDEX_SCOPE",
                "--course-index must name materials/private/<course>/INDEX.md",
            ))
            return
    registered_directories = {
        directory
        for source in sources
        if (directory := _source_course_directory(source)) is not None
    }
    discovered_directories = _discover_course_directories(repo_root)
    namespace_directories = registered_directories | discovered_directories
    namespace_by_directory: dict[str, str] = {}
    for directory in sorted(namespace_directories):
        index_path = repo_root / "materials" / "private" / directory / "INDEX.md"
        if not index_path.is_file():
            continue
        namespace, namespace_findings = _index_namespace(index_path, repo_root)
        if selected_directory is None or directory == selected_directory:
            findings.extend(namespace_findings)
        if namespace is not None:
            namespace_by_directory[directory] = namespace

    directories_by_namespace: dict[str, list[str]] = {}
    for directory, namespace in namespace_by_directory.items():
        directories_by_namespace.setdefault(namespace, []).append(directory)
    for namespace, directories in sorted(directories_by_namespace.items()):
        if len(directories) < 2:
            continue
        affected_paths = tuple(
            source.relative_path
            for source in sources
            if _source_course_directory(source) in directories
        )
        report_directories = (
            directories
            if selected_directory is None
            else [selected_directory] if selected_directory in directories else []
        )
        for directory in report_directories:
            index_path = repo_root / "materials" / "private" / directory / "INDEX.md"
            findings.append(Finding(
                _display_path(index_path, repo_root),
                1,
                "INDEX_NAMESPACE_COLLISION",
                f"source_namespace {namespace} is declared by multiple course directories: "
                + ", ".join(directories),
                affected_paths,
            ))

    scoped_sources = [
        source
        for source in sources
        if selected_directory is None
        or _source_course_directory(source) == selected_directory
    ]
    registered_paths: set[str] = set()
    for source in scoped_sources:
        source_path = repo_root / source.relative_path
        display = source.relative_path
        registered_paths.add(source.relative_path)
        directory = _source_course_directory(source)
        namespace_match = SOURCE_ID_RE.fullmatch(source.identifier)
        expected_namespace = (
            namespace_by_directory.get(directory) if directory is not None else None
        )
        if (
            namespace_match is not None
            and expected_namespace is not None
            and namespace_match.group(1) != expected_namespace
        ):
            findings.append(Finding(
                display,
                1,
                "SOURCE_NAMESPACE_MISMATCH",
                f"source ID namespace {namespace_match.group(1)} does not match "
                f"course INDEX namespace {expected_namespace}",
                (source.relative_path,),
            ))
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
    course_directories = (
        {selected_directory}
        if selected_directory is not None
        else registered_directories | discovered_directories
    )
    for directory in sorted(course_directories):
        index_path = repo_root / "materials" / "private" / directory / "INDEX.md"
        display = str(index_path.relative_to(repo_root))
        if not index_path.is_file():
            findings.append(Finding(display, 1, "INDEX_MISSING", "course index is missing"))
            continue
        lessons = _extract_index_lessons(index_path)
        filenames = [lesson.filename for lesson in lessons]
        for duplicate in _duplicate_values(filenames):
            duplicate_rows = [lesson for lesson in lessons if lesson.filename == duplicate]
            affected = f"materials/private/{directory}/{duplicate}"
            for duplicate_row in duplicate_rows[1:]:
                findings.append(Finding(
                    display,
                    duplicate_row.line,
                    "INDEX_DUPLICATE",
                    f"duplicate lesson path {duplicate}",
                    (affected,),
                ))
        for lesson in lessons:
            filename = lesson.filename
            if "/" in filename or "\\" in filename or filename.startswith("course-provided-practice"):
                findings.append(Finding(
                    display,
                    lesson.line,
                    "INDEX_SCOPE",
                    f"강의 자료 contains an out-of-scope path: {filename}",
                ))
                continue
            if not LESSON_FILENAME_RE.fullmatch(filename):
                findings.append(Finding(
                    display, lesson.line, "INDEX_LESSON_ID",
                    f"강의 자료 filename must start with NN-NN_: {filename}",
                ))
                continue
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
    """Validate one private course INDEX against registry rows and source bytes."""
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


def validate_lesson_slice_freshness(
    curriculum_path: Path,
    course_index: Path,
    selected_source_paths: set[str] | list[str] | tuple[str, ...],
    *,
    repo_root: Path = REPO_ROOT,
) -> LessonSliceFreshness:
    """Validate selected lesson sources while downgrading unrelated course drift."""
    selected = set(selected_source_paths)
    errors: list[Finding] = []
    warnings: list[Finding] = []
    whole_course = validate_course_index_freshness(
        curriculum_path,
        course_index,
        repo_root=repo_root,
    )
    critical_codes = {
        "CURRICULUM_MISSING",
        "CURRICULUM_ENCODING",
        "SOURCE_TABLE_COUNT",
        "INDEX_SCOPE",
        "INDEX_MISSING",
        "INDEX_NAMESPACE_COUNT",
        "INDEX_NAMESPACE_FORMAT",
        "INDEX_NAMESPACE_COLLISION",
    }
    for finding in whole_course:
        affects_selected = bool(selected.intersection(finding.affected_source_paths))
        target = (
            errors
            if finding.path in selected or affects_selected or finding.code in critical_codes
            else warnings
        )
        target.append(finding)

    directory = _course_directory_for_index(course_index, repo_root)
    if directory is None:
        return LessonSliceFreshness(errors, warnings)
    if not selected:
        errors.append(Finding(
            _display_path(course_index, repo_root),
            1,
            "LESSON_SLICE_EMPTY",
            "lesson slice requires at least one selected primary source",
        ))
        return LessonSliceFreshness(errors, warnings)

    path = curriculum_path.resolve()
    document_path = _display_path(path, repo_root)
    parse_findings: list[Finding] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (FileNotFoundError, UnicodeDecodeError):
        return LessonSliceFreshness(_deduplicate_findings(errors), _deduplicate_findings(warnings))
    source_rows, source_tables = _extract_tables(
        lines, SOURCE_HEADER, document_path, parse_findings,
    )
    if source_tables != 1:
        return LessonSliceFreshness(_deduplicate_findings(errors), _deduplicate_findings(warnings))
    sources = _parse_sources(source_rows, document_path, parse_findings)
    structural_findings: list[Finding] = []
    _validate_sources(sources, document_path, structural_findings)
    for finding in parse_findings + structural_findings:
        affects_selected = bool(selected.intersection(finding.affected_source_paths))
        target = errors if finding.path in selected or affects_selected else warnings
        target.append(finding)

    source_by_path = {source.relative_path: source for source in sources}
    index_path = repo_root / "materials" / "private" / directory / "INDEX.md"
    indexed_filenames = (
        {lesson.filename for lesson in _extract_index_lessons(index_path)}
        if index_path.is_file()
        else set()
    )
    for selected_path in sorted(selected):
        parts = Path(selected_path).parts
        if (
            len(parts) != 4
            or parts[:2] != ("materials", "private")
            or parts[2] != directory
        ):
            errors.append(Finding(
                selected_path,
                1,
                "LESSON_SLICE_SCOPE",
                f"selected source does not belong to {course_index.as_posix()}",
            ))
            continue
        if selected_path not in source_by_path:
            errors.append(Finding(
                selected_path,
                1,
                "LESSON_SLICE_REGISTRY",
                "selected source is absent from the Curriculum registry",
            ))
        if parts[-1] not in indexed_filenames:
            errors.append(Finding(
                selected_path,
                1,
                "LESSON_SLICE_INDEX",
                "selected source is absent from the course INDEX 강의 자료 table",
            ))

    return LessonSliceFreshness(
        _deduplicate_findings(errors),
        _deduplicate_findings(warnings),
    )


def _deduplicate_findings(findings: list[Finding]) -> list[Finding]:
    unique: list[Finding] = []
    seen: set[tuple[str, int, str, str]] = set()
    for finding in findings:
        key = (finding.path, finding.line, finding.code, finding.message)
        if key not in seen:
            seen.add(key)
            unique.append(finding)
    return unique


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
    summary_rows, summary_tables = _extract_tables(
        lines, REGISTRY_SUMMARY_HEADER, document_path, findings,
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
    registry_summary = _parse_registry_summary(
        summary_rows, summary_tables, document_path, findings,
    )
    _validate_sources(sources, document_path, findings)
    _validate_competencies(competencies, sources, document_path, findings)
    _validate_registry_structure_summary(
        registry_summary, sources, document_path, findings,
    )
    if strict_sources:
        _strict_source_checks(
            sources,
            repo_root,
            findings,
            course_index=course_index,
        )
        if course_index is None:
            _validate_private_registry_summary(
                registry_summary,
                sources,
                repo_root,
                document_path,
                findings,
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
        help="with --strict-sources, restrict byte and parity checks to one materials/private/<course>/INDEX.md",
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
