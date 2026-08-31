#!/usr/bin/env python3
"""Validate the ignored active-lesson handoff and session-capture state."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit


SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_curriculum import (  # noqa: E402
    curriculum_snapshot_from_text,
    validate_lesson_slice_freshness,
)
from target_graph import (  # noqa: E402
    parse_roadmap_endpoints,
    prerequisite_closure,
)
from pdf_utils import pdf_page_count as _pdf_page_count  # noqa: E402
from source_scopes import (  # noqa: E402
    CourseScope,
    location_is_boundary,
    location_is_included,
    locations_overlap,
    parse_course_scopes,
    split_units,
    unit_location,
)


SCHEMA_VERSION = "9"
STATUSES = {
    "preparing",
    "review_pending",
    "repair_pending",
    "active",
    "paused",
    "blocked",
    "completed",
}
MANIFEST_ROLES = {
    "primary",
    "external-primary",
    "external-asset",
    "asset",
    "course-index",
    "curriculum",
    "roadmap",
    "knowledge",
    "til",
    "practice",
}
REVIEW_VERDICTS = {"pending", "pass", "repair_required", "blocked"}
REVIEW_PHASES = {"none", "independent-slice", "targeted-recheck"}
REPAIR_FINDING_RE = re.compile(r"R\d{3}\Z")
BLOCKER_FINDING_RE = re.compile(r"B\d{3}\Z")
TRUE_BLOCKER_KINDS = {
    "source-integrity",
    "source-access",
    "irreducible-factual-ambiguity",
    "user-scope-decision",
}
SCOPE_KINDS = {"entire-source", "registered-slice", "ephemeral-slice"}
EVIDENCE_KINDS = {
    "explain_back",
    "calculation",
    "shape_prediction",
    "code_interpretation",
    "transfer",
    "limit",
}
EVIDENCE_VERDICTS = {"confirmed", "partial", "misconception", "unconfirmed"}
CAPTURE_STATES = {"pending", "captured", "not_eligible"}
CONCEPT_MARKERS = {"none", "[선수개념]", "[정정]", "[보충]"}
COVERAGE_MODES = {"full-source", "focused"}
OBJECTIVE_REQUIREMENTS = {"source-core", "required-added", "optional-added"}
OBJECTIVE_MARKERS = {"none", "prerequisite", "correction", "supplement"}
OBJECTIVE_TREATMENTS = {"full", "bridge", "deferred"}
GOAL_DISPOSITIONS = {"learning", "guidance", "source-gap"}
GUIDANCE_KINDS = {"orientation", "diagnostic", "reference"}
FINDING_TYPES = {
    "none",
    "correction",
    "underspecification",
    "prerequisite",
    "supplement",
    "intentional-deferral",
}
CHECK_POLICIES = {"adaptive", "none"}
SESSION_PROFILES = {"standard", "short", "custom"}
FLOW_MODES = {"day-full", "single-lesson"}
STEP_ROLES = {
    "motivation",
    "concept-model",
    "worked-example",
    "contrast-limit",
    "synthesis-transfer",
}
STANDARD_STEP_ROLES = (
    "motivation",
    "concept-model",
    "worked-example",
    "contrast-limit",
    "synthesis-transfer",
)
POSITION_ACTIONS = {"teach", "await-answer", "remediate", "complete"}
DELIVERY_STATES = {"pending", "delivered"}
DELIVERY_MODES = {"none", "full", "bridge"}
STEP_DELIVERY_STATES = {"pending", "delivered", "completed"}
SESSION_CONCEPT_STATES = {"confirmed", "uncertain", "deferred"}
CURRICULUM_COVERAGE = {"미감사", "충분", "부분", "없음", "판정보류"}
CURRICULUM_GAP_ACTIONS = {
    "그대로 사용",
    "수업 내 보충",
    "별도 자료 확보",
    "원본 복구 후 재감사",
    "트랙 선택 시 확보",
}
LESSON_TREATMENTS = {
    "source-only",
    "supplement-now",
    "resolved-external",
    "defer-gap",
    "defer-track",
}
PRIMARY_ROLES = {"primary", "external-primary"}
TARGET_SELECTION_MODES = {"planner", "user-named-target", "user-named-source"}
TARGET_STATES = {
    "START_TARGET",
    "CONTINUE_TARGET",
    "BRIDGE_PREREQUISITE",
    "NEED_DIAGNOSTIC",
    "NO_ACTIONABLE_TARGET",
}
ACTIONABLE_TARGET_STATES = {
    "START_TARGET",
    "CONTINUE_TARGET",
    "BRIDGE_PREREQUISITE",
}
EXTERNAL_RELATIONS = {"primary", "supporting"}
EVIDENCE_TOKENS = {
    "explain",
    "calculate",
    "shape",
    "implement",
    "debug",
    "interpret",
    "design",
    "transfer",
}
HASH_RE = re.compile(r"[0-9a-f]{64}\Z")
LESSON_ID_RE = re.compile(r"[a-z0-9][a-z0-9-]{2,63}\Z")
CYCLE_ID_RE = re.compile(r"[a-z0-9][a-z0-9-]{2,95}\Z")
AGENT_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/@-]{1,127}\Z")
CURRICULUM_ID_RE = re.compile(r"(?:CC|TR)-[A-Z]+-\d{2}\Z")

METADATA_KEYS = (
    "schema_version",
    "cycle_id",
    "lesson_id",
    "title",
    "status",
    "session_profile",
    "flow_mode",
    "study_date",
    "created_at",
    "updated_at",
    "author_id",
    "input_manifest_sha256",
    "contract_sha256",
)
CURRENT_POSITION_KEYS = (
    "last_completed_step",
    "current_step",
    "next_action",
    "target_objectives",
    "basis",
    "resume_note",
)
SESSION_PLAN_KEYS = ("session_goal", "exit_step", "exit_evidence_kind")
REVIEW_KEYS = (
    "initial_reviewer_id",
    "reviewer_id",
    "review_iteration",
    "review_phase",
    "recheck_of",
    "reviewed_at",
    "verdict",
    "reviewed_input_manifest_sha256",
    "reviewed_contract_sha256",
)
EVIDENCE_KEYS = (
    "concept_ids",
    "objective_ids",
    "kind",
    "provenance",
    "verdict",
    "capture_state",
    "captured_at",
    "content_sha256",
)
CONTRACT_HEADINGS = (
    "Objective",
    "Coverage Mode",
    "Curriculum Targets",
    "Target Decision",
    "Curriculum Treatment Map",
    "External Source Identity",
    "External Target Relation",
    "Learner Evidence Baseline",
    "Audited Findings",
    "Source Scope Map",
    "Source Coverage Index",
    "Declared Goal Alignment",
    "Guidance Map",
    "Observable Objective Map",
    "Concept Path",
    "Module Plan",
    "Session Plan",
    "Example Map",
    "Prepared Teaching Steps",
    "Deferred",
)


@dataclass
class ValidationError:
    line: int
    code: str
    message: str

    def rendered(self, path: Path) -> str:
        return f"ERROR {path.as_posix()}:{self.line} [{self.code}] {self.message}"

    def as_json(self) -> dict[str, Any]:
        return {"line": self.line, "code": self.code, "message": self.message}


@dataclass
class ValidationWarning:
    line: int
    code: str
    message: str

    def rendered(self, path: Path) -> str:
        return f"WARNING {path.as_posix()}:{self.line} [{self.code}] {self.message}"

    def as_json(self) -> dict[str, Any]:
        return {"line": self.line, "code": self.code, "message": self.message}


@dataclass
class ManifestEntry:
    item_id: str
    role: str
    path: str
    sha256: str
    line: int


@dataclass
class TargetDecision:
    selection_mode: str
    target_state: str
    primary_target: str
    bridge_target: str
    evidence_gap: list[str]
    completion_evidence: str
    endpoint: str
    why_now: str
    line: int


@dataclass
class ExternalSourceIdentity:
    primary_id: str
    provider: str
    course: str
    offering_or_edition: str
    artifact: str
    official_url: str
    final_url: str
    retrieved_at: str
    media_type: str
    scope: str
    receipt_path: str
    line: int


@dataclass
class ExternalTargetRelation:
    target_id: str
    primary_id: str
    relation: str
    objective_ids: list[str]
    audit_basis: str
    line: int


@dataclass
class SemanticReviewRecord:
    iteration: int
    values: dict[str, str]
    line: int


@dataclass
class Evidence:
    evidence_id: str
    values: dict[str, str]
    content: str
    assessment: str
    line: int
    capture_value_span: tuple[int, int]


@dataclass
class LearningCoverage:
    concept_id: str
    today_state: str
    evidence_ids: list[str]
    note: str
    line: int


@dataclass
class LessonModule:
    module_id: str
    topic: str
    concept_ids: list[str]
    source_locations: list[str]
    application_step: str
    expected_minutes: int
    line: int


@dataclass
class CurriculumTreatment:
    target_id: str
    coverage: str
    gap_action: str
    lesson_treatment: str
    objective_ids: list[str]
    note: str
    line: int


@dataclass
class SourceCoverage:
    primary_id: str
    goal_ids: list[str]
    objective_ids: list[str]
    guidance_ids: list[str]
    line: int


@dataclass
class LessonSourceScope:
    primary_id: str
    scope_kind: str
    scope_id: str
    included_units: tuple[str, ...]
    boundary_units: tuple[str, ...]
    outside_disposition: str
    registered_scope: CourseScope | None
    line: int


@dataclass
class DeclaredGoal:
    goal_id: str
    primary_id: str
    goal_location: str
    disposition: str
    linked_ids: list[str]
    body_support: list[str]
    reason: str
    line: int


@dataclass
class GuidanceItem:
    guidance_id: str
    kind: str
    source_location: str
    summary: str
    trigger: str
    line: int


@dataclass
class AuditedFinding:
    finding_id: str
    finding_type: str
    source_location: str
    linked_ids: list[str]
    note: str
    line: int


@dataclass
class Objective:
    objective_id: str
    requirement: str
    marker: str
    source_location: str
    outcome: str
    concept_id: str
    treatment: str
    teaching_move: str
    baseline_evidence: str
    line: int


@dataclass
class ObjectiveDelivery:
    objective_id: str
    state: str
    mode: str
    note: str
    line: int


@dataclass
class TeachingStepDelivery:
    step_id: str
    state: str
    note: str
    line: int


@dataclass
class LessonExample:
    example_id: str
    purpose: str
    fixture: str
    objective_ids: list[str]
    line: int


@dataclass
class TeachingStep:
    step_id: str
    step_role: str
    concept_ids: list[str]
    objective_ids: list[str]
    example_id: str
    delivery_outline: str
    tiny_example: str
    check_policy: str
    check_basis: str
    check_question: str
    line: int


@dataclass
class HandoffDocument:
    path: Path
    repo_root: Path
    text: str
    metadata: dict[str, str] = field(default_factory=dict)
    manifest: list[ManifestEntry] = field(default_factory=list)
    contract: str = ""
    coverage_mode: str = ""
    contract_concepts: list[str] = field(default_factory=list)
    source_coverage: dict[str, SourceCoverage] = field(default_factory=dict)
    lesson_source_scopes: dict[str, LessonSourceScope] = field(default_factory=dict)
    declared_goals: dict[str, DeclaredGoal] = field(default_factory=dict)
    guidance: dict[str, GuidanceItem] = field(default_factory=dict)
    findings: dict[str, AuditedFinding] = field(default_factory=dict)
    objectives: dict[str, Objective] = field(default_factory=dict)
    modules: dict[str, LessonModule] = field(default_factory=dict)
    session_plan: dict[str, str] = field(default_factory=dict)
    examples: dict[str, LessonExample] = field(default_factory=dict)
    teaching_steps: dict[str, TeachingStep] = field(default_factory=dict)
    curriculum_targets: list[str] = field(default_factory=list)
    curriculum_treatments: dict[str, CurriculumTreatment] = field(default_factory=dict)
    target_decision: TargetDecision | None = None
    external_identities: dict[str, ExternalSourceIdentity] = field(default_factory=dict)
    external_relations: dict[tuple[str, str], ExternalTargetRelation] = field(default_factory=dict)
    semantic_review: SemanticReviewRecord | None = None
    current_position: dict[str, str] = field(default_factory=dict)
    objective_delivery: dict[str, ObjectiveDelivery] = field(default_factory=dict)
    step_delivery: dict[str, TeachingStepDelivery] = field(default_factory=dict)
    evidence: dict[str, Evidence] = field(default_factory=dict)
    learning_coverage: dict[str, LearningCoverage] = field(default_factory=dict)
    computed_manifest_sha256: str = ""
    computed_contract_sha256: str = ""


@dataclass
class ValidationReport:
    path: Path
    ready_requested: bool
    capture_ready_requested: bool
    errors: list[ValidationError]
    document: HandoffDocument | None
    warnings: list[ValidationWarning] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    @property
    def exit_code(self) -> int:
        if not self.errors:
            return 0
        return 2 if any(error.code == "SCHEMA" for error in self.errors) else 1

    def as_json(self) -> dict[str, Any]:
        computed: dict[str, str] = {}
        if self.document is not None:
            computed = {
                "input_manifest_sha256": self.document.computed_manifest_sha256,
                "contract_sha256": self.document.computed_contract_sha256,
            }
        return {
            "ok": self.ok,
            "path": self.path.as_posix(),
            "ready": self.ready_requested and self.ok,
            "capture_ready": self.capture_ready_requested and self.ok,
            "workflow_action": _workflow_action(self.document),
            "computed": computed,
            "errors": [error.as_json() for error in self.errors],
            "warnings": [warning.as_json() for warning in self.warnings],
        }


def _workflow_action(doc: HandoffDocument | None) -> str:
    if doc is None:
        return "PREPARE_CONTRACT"
    status = doc.metadata.get("status")
    if status == "completed":
        return "CAPTURE_SESSION"
    if status == "paused":
        return "TEACH_OR_RESUME"
    if status == "blocked":
        return "RESOLVE_TRUE_BLOCKER"
    if status == "active":
        return "TEACH_OR_RESUME"
    if status == "preparing":
        return "PREPARE_CONTRACT"
    current = doc.semantic_review
    if current is None:
        return "REQUEST_INDEPENDENT_REVIEW"
    verdict = current.values.get("verdict")
    if verdict == "pass":
        return "ACTIVATE_LESSON"
    if verdict == "blocked":
        return "RESOLVE_TRUE_BLOCKER"
    if verdict == "repair_required":
        reviewed_current = (
            current.values.get("reviewed_input_manifest_sha256") == doc.computed_manifest_sha256
            and current.values.get("reviewed_contract_sha256") == doc.computed_contract_sha256
        )
        return "REPAIR_CONTRACT" if reviewed_current else "REQUEST_TARGETED_RECHECK"
    return "REQUEST_INDEPENDENT_REVIEW"


def can_mechanically_rebuild_same_lesson(
    doc: HandoffDocument,
    *,
    primary_target: str,
    primary_paths: set[str],
) -> bool:
    """Return whether an explicit start/resume request may replace this handoff.

    This is intentionally narrower than schema migration: the caller must
    already have established the intended target and source identity. Learner
    evidence or delivered objectives make the current handoff non-replaceable.
    """

    if doc.metadata.get("status") in {"blocked", "completed"}:
        return False
    if doc.target_decision is None or doc.target_decision.primary_target != primary_target:
        return False
    manifested_primary_paths = {
        entry.path for entry in doc.manifest if entry.role in PRIMARY_ROLES
    }
    if manifested_primary_paths != primary_paths:
        return False
    if doc.evidence:
        return False
    return all(item.state == "pending" for item in doc.objective_delivery.values())


def can_replace_with_new_lesson(
    doc: HandoffDocument,
    *,
    explicit_discard: bool = False,
) -> bool:
    """Return whether the current operational handoff may be retired.

    A finished lesson may be retired only after every confirmed evidence item
    has been captured into the daily-flow cursor. Any other replacement
    requires an explicit learner decision to discard the current session.
    """

    if explicit_discard:
        return True
    return doc.metadata.get("status") == "completed" and all(
        evidence.values.get("verdict") != "confirmed"
        or evidence.values.get("capture_state") == "captured"
        for evidence in doc.evidence.values()
    )


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _repo_root_from_script() -> Path:
    script = Path(__file__).resolve()
    for candidate in script.parents:
        if (candidate / ".git").exists() or (candidate / "AGENTS.md").is_file():
            return candidate.resolve()
    raise RuntimeError("could not locate repository root")


def _is_rfc3339(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _is_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value))


def _section_ranges(text: str, errors: list[ValidationError]) -> dict[str, tuple[int, int, int]]:
    expected = (
        "Metadata",
        "Input Manifest",
        "Semantic Review",
        "Current Position",
        "Objective Delivery",
        "Teaching Step Delivery",
        "Session Concept Coverage",
        "Learner Evidence",
    )
    headings = list(re.finditer(r"^## ([^\n]+)$", text, re.MULTILINE))
    found = [match.group(1) for match in headings]
    if found != list(expected):
        errors.append(
            ValidationError(
                1,
                "SCHEMA",
                "level-two headings must appear exactly once in this order: " + ", ".join(expected),
            )
        )
    ranges: dict[str, tuple[int, int, int]] = {}
    for index, match in enumerate(headings):
        name = match.group(1)
        if name not in expected or name in ranges:
            continue
        body_start = match.end()
        if text[body_start : body_start + 1] == "\n":
            body_start += 1
        body_end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        ranges[name] = (body_start, body_end, _line_number(text, match.start()))
    return ranges


def _parse_bullets(
    text: str,
    start: int,
    end: int,
    expected_keys: tuple[str, ...],
    errors: list[ValidationError],
    *,
    context: str,
) -> tuple[dict[str, str], dict[str, int], dict[str, tuple[int, int]]]:
    values: dict[str, str] = {}
    lines: dict[str, int] = {}
    spans: dict[str, tuple[int, int]] = {}
    region = text[start:end]
    for match in re.finditer(r"^- ([a-z0-9_]+):[ \t]*(.*)$", region, re.MULTILINE):
        key, value = match.group(1), match.group(2).strip()
        absolute = start + match.start()
        if key in values:
            errors.append(ValidationError(_line_number(text, absolute), "SCHEMA", f"duplicate {context} field: {key}"))
            continue
        values[key] = value
        lines[key] = _line_number(text, absolute)
        spans[key] = (start + match.start(2), start + match.end(2))
    missing = [key for key in expected_keys if key not in values]
    extra = [key for key in values if key not in expected_keys]
    if missing:
        errors.append(ValidationError(_line_number(text, start), "SCHEMA", f"missing {context} fields: {', '.join(missing)}"))
    if extra:
        errors.append(ValidationError(lines[extra[0]], "SCHEMA", f"unknown {context} fields: {', '.join(extra)}"))
    return values, lines, spans


def _safe_repo_path(raw: str, repo_root: Path) -> tuple[Path | None, str | None]:
    if not raw or raw.startswith("/") or "\\" in raw:
        return None, "path must be a non-empty POSIX repository-relative path"
    components = raw.split("/")
    if any(component in {"", ".", ".."} for component in components):
        return None, "path must not contain empty, '.' or '..' components"
    pure = PurePosixPath(raw)
    if pure.is_absolute() or pure.as_posix() != raw:
        return None, "path is not canonical POSIX repository-relative syntax"
    candidate = repo_root.joinpath(*pure.parts)
    try:
        resolved = candidate.resolve(strict=False)
        resolved.relative_to(repo_root.resolve())
    except (OSError, ValueError):
        return None, "path or symlink escapes the repository"
    return candidate, None


def _marker_body(
    text: str,
    start_marker: str,
    end_marker: str,
    errors: list[ValidationError],
    *,
    code: str = "SCHEMA",
) -> tuple[str, int, int] | None:
    start_matches = list(re.finditer(rf"^{re.escape(start_marker)}[ \t]*$", text, re.MULTILINE))
    end_matches = list(re.finditer(rf"^{re.escape(end_marker)}[ \t]*$", text, re.MULTILINE))
    if len(start_matches) != 1 or len(end_matches) != 1:
        errors.append(
            ValidationError(
                1,
                code,
                f"expected exactly one marker pair: {start_marker} ... {end_marker}",
            )
        )
        return None
    start_match, end_match = start_matches[0], end_matches[0]
    if start_match.end() >= end_match.start():
        errors.append(ValidationError(_line_number(text, start_match.start()), code, "marker order is invalid"))
        return None
    body_start = start_match.end()
    if text[body_start : body_start + 1] == "\n":
        body_start += 1
    body_end = end_match.start()
    if body_end > body_start and text[body_end - 1 : body_end] == "\n":
        body_end -= 1
    return text[body_start:body_end], body_start, body_end


def _parse_metadata(
    doc: HandoffDocument,
    section: tuple[int, int, int] | None,
    errors: list[ValidationError],
) -> dict[str, int]:
    if section is None:
        return {}
    start, end, _ = section
    values, lines, _ = _parse_bullets(text=doc.text, start=start, end=end, expected_keys=METADATA_KEYS, errors=errors, context="metadata")
    doc.metadata = values
    if values.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            ValidationError(
                lines.get("schema_version", 1),
                "SCHEMA",
                f"schema_version must be {SCHEMA_VERSION}; rebuild older handoffs from the current template",
            )
        )
    if "cycle_id" in values and not CYCLE_ID_RE.fullmatch(values["cycle_id"]):
        errors.append(ValidationError(lines["cycle_id"], "SCHEMA", "cycle_id has an invalid format"))
    if "lesson_id" in values and not LESSON_ID_RE.fullmatch(values["lesson_id"]):
        errors.append(ValidationError(lines["lesson_id"], "SCHEMA", "lesson_id has an invalid format"))
    if not values.get("title"):
        errors.append(ValidationError(lines.get("title", 1), "SCHEMA", "title must not be empty"))
    if values.get("status") not in STATUSES:
        errors.append(ValidationError(lines.get("status", 1), "SCHEMA", "status is not allowed"))
    if values.get("session_profile") not in SESSION_PROFILES:
        errors.append(ValidationError(lines.get("session_profile", 1), "SCHEMA", "session_profile must be standard, short, or custom"))
    if values.get("flow_mode") not in FLOW_MODES:
        errors.append(ValidationError(lines.get("flow_mode", 1), "SCHEMA", "flow_mode must be day-full or single-lesson"))
    if "study_date" in values and not _is_date(values["study_date"]):
        errors.append(ValidationError(lines["study_date"], "SCHEMA", "study_date must be YYYY-MM-DD"))
    for key in ("created_at", "updated_at"):
        if key in values and not _is_rfc3339(values[key]):
            errors.append(ValidationError(lines[key], "SCHEMA", f"{key} must be an RFC 3339 timestamp with a timezone"))
    if "author_id" in values and not AGENT_ID_RE.fullmatch(values["author_id"]):
        errors.append(ValidationError(lines["author_id"], "SCHEMA", "author_id has an invalid format"))
    for key in ("input_manifest_sha256", "contract_sha256"):
        if key in values and not HASH_RE.fullmatch(values[key]):
            errors.append(ValidationError(lines[key], "SCHEMA", f"{key} must be 64 lowercase hexadecimal characters"))
    return lines


def _split_table_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def _contract_table_rows(
    section: str,
    expected_header: list[str],
    doc: HandoffDocument,
    body_start: int,
    errors: list[ValidationError],
    *,
    context: str,
) -> list[tuple[list[str], int]]:
    lines = [(index, line) for index, line in enumerate(section.splitlines()) if line.strip()]
    base_line = _line_number(doc.text, body_start)
    if len(lines) < 3:
        errors.append(ValidationError(base_line, "SCHEMA", f"{context} must contain a header, separator, and rows"))
        return []
    header = _split_table_row(lines[0][1])
    separator = _split_table_row(lines[1][1])
    if header != expected_header:
        errors.append(
            ValidationError(
                base_line + lines[0][0],
                "SCHEMA",
                f"{context} columns must be " + " | ".join(expected_header),
            )
        )
    if separator is None or len(separator) != len(expected_header) or not all(
        re.fullmatch(r":?-{3,}:?", cell) for cell in separator
    ):
        errors.append(ValidationError(base_line + lines[1][0], "SCHEMA", f"{context} separator is invalid"))
    rows: list[tuple[list[str], int]] = []
    for index, line in lines[2:]:
        cells = _split_table_row(line)
        line_no = base_line + index
        if cells is None or len(cells) != len(expected_header):
            errors.append(
                ValidationError(
                    line_no,
                    "SCHEMA",
                    f"{context} row must have {len(expected_header)} cells",
                )
            )
            continue
        rows.append((cells, line_no))
    return rows


def _location_path(location: str) -> str | None:
    if "#" not in location:
        return None
    path, anchor = location.rsplit("#", 1)
    return path if path and anchor.strip() else None


def _normalize_location_fragment(value: str) -> str:
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


class _VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag.lower() in {"script", "style", "noscript", "template"}:
            self._ignored_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript", "template"} and self._ignored_depth:
            self._ignored_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self._ignored_depth:
            self.parts.append(data)


def _location_exists(location: str, repo_root: Path) -> bool:
    path = _location_path(location)
    if path is None:
        return False
    candidate, path_error = _safe_repo_path(path, repo_root)
    if path_error or candidate is None or not candidate.is_file():
        return False
    anchor = _normalize_location_fragment(location.rsplit("#", 1)[1])
    if candidate.suffix.lower() == ".pdf":
        match = re.fullmatch(r"page-(\d+)(?:--(\d+))?(?:: .+)?", anchor, re.IGNORECASE)
        if match is None:
            return False
        page_count = _pdf_page_count(candidate)
        if page_count is None:
            return False
        start = int(match.group(1))
        end = int(match.group(2) or start)
        return 1 <= start <= end <= page_count
    try:
        text = candidate.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    if not anchor:
        return False
    if anchor.lower().startswith("text: "):
        excerpt = _normalize_location_fragment(anchor[6:])
        if candidate.suffix.lower() in {".html", ".htm"}:
            parser = _VisibleTextParser()
            try:
                parser.feed(text)
            except Exception:
                return False
            candidate_text = " ".join(parser.parts)
        else:
            candidate_text = text
        normalized_text = re.sub(r"\s+", " ", candidate_text).strip()
        return bool(excerpt) and excerpt in normalized_text
    if CURRICULUM_ID_RE.fullmatch(anchor):
        return re.search(rf"(?<![A-Z0-9-]){re.escape(anchor)}(?![A-Z0-9-])", text) is not None
    return any(_normalize_location_fragment(line) == anchor for line in text.splitlines())


def _comma_ids(raw: str, pattern: str) -> list[str] | None:
    if raw == "none":
        return []
    values = [value.strip() for value in raw.split(",")]
    if not values or any(not re.fullmatch(pattern, value) for value in values):
        return None
    return values


def _mixed_ids(raw: str, prefixes: tuple[str, ...]) -> list[str] | None:
    if raw == "none":
        return []
    values = [value.strip() for value in raw.split(",")]
    pattern = r"(?:" + "|".join(re.escape(prefix) for prefix in prefixes) + r")\d{3,}"
    if not values or any(re.fullmatch(pattern, value) is None for value in values):
        return None
    return values


def _locations(raw: str) -> list[str]:
    return [] if raw == "none" else [item.strip() for item in raw.split(";") if item.strip()]


def _curriculum_target_rows(text: str) -> dict[str, tuple[str, str, int]]:
    """Return target -> (coverage, gap action, line) from competency tables."""
    snapshot = curriculum_snapshot_from_text(text)
    return {
        target_id: (target.coverage, target.gap_action, target.line)
        for target_id, target in snapshot.targets.items()
    }


def _parse_manifest(
    doc: HandoffDocument,
    section: tuple[int, int, int] | None,
    errors: list[ValidationError],
) -> None:
    if section is None:
        return
    start, end, _ = section
    contract_marker = doc.text.find("<!-- lesson-contract:start -->", start, end)
    if contract_marker != -1:
        end = contract_marker
    lines_with_ends = doc.text[start:end].splitlines(keepends=True)
    offsets: list[int] = []
    cursor = start
    for line in lines_with_ends:
        offsets.append(cursor)
        cursor += len(line)
    nonblank = [(index, line.rstrip("\n")) for index, line in enumerate(lines_with_ends) if line.strip()]
    if len(nonblank) < 3:
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "Input Manifest must contain a header, separator, and rows"))
        return
    header = _split_table_row(nonblank[0][1])
    separator = _split_table_row(nonblank[1][1])
    if header != ["ID", "Role", "Path", "SHA-256"]:
        errors.append(ValidationError(_line_number(doc.text, offsets[nonblank[0][0]]), "SCHEMA", "Input Manifest columns must be ID | Role | Path | SHA-256"))
    if separator is None or len(separator) != 4 or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
        errors.append(ValidationError(_line_number(doc.text, offsets[nonblank[1][0]]), "SCHEMA", "Input Manifest separator is invalid"))
    entries: list[ManifestEntry] = []
    for row_number, (line_index, line) in enumerate(nonblank[2:], start=1):
        row = _split_table_row(line)
        absolute = offsets[line_index]
        line_no = _line_number(doc.text, absolute)
        if row is None or len(row) != 4:
            errors.append(ValidationError(line_no, "SCHEMA", "manifest row must have four cells"))
            continue
        item_id, role, raw_path, sha256 = row
        expected_id = f"I{row_number:03d}"
        if item_id != expected_id:
            errors.append(ValidationError(line_no, "SCHEMA", f"manifest ID must be {expected_id}"))
        if role not in MANIFEST_ROLES:
            errors.append(ValidationError(line_no, "SCHEMA", f"unknown manifest role: {role}"))
        if not HASH_RE.fullmatch(sha256):
            errors.append(ValidationError(line_no, "SCHEMA", "manifest SHA-256 must be 64 lowercase hexadecimal characters"))
        entries.append(ManifestEntry(item_id, role, raw_path, sha256, line_no))
    doc.manifest = entries

    paths = [entry.path for entry in entries]
    duplicate_paths = sorted({path for path in paths if paths.count(path) > 1})
    if duplicate_paths:
        errors.append(ValidationError(entries[0].line if entries else 1, "PATH", "duplicate manifest paths: " + ", ".join(duplicate_paths)))
    if not any(entry.role in PRIMARY_ROLES for entry in entries):
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "manifest requires at least one local or external primary input"))
    if sum(entry.role == "curriculum" for entry in entries) != 1:
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "manifest requires exactly one curriculum input"))
    if sum(entry.role == "roadmap" for entry in entries) != 1:
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "manifest requires exactly one roadmap input"))
    for entry in entries:
        if entry.path in {
            "til/today.md",
            "tmp/active-learning-flow.json",
            "tmp/active-lesson-handoff.md",
        }:
            errors.append(
                ValidationError(
                    entry.line,
                    "PATH",
                    f"mutable operational state must not be a lesson manifest input: {entry.path}",
                )
            )
        if entry.role == "curriculum" and entry.path != "CURRICULUM.md":
            errors.append(ValidationError(entry.line, "PATH", "the curriculum manifest path must be exactly CURRICULUM.md"))
        if entry.role == "roadmap" and entry.path != "ROADMAP.md":
            errors.append(ValidationError(entry.line, "PATH", "the roadmap manifest path must be exactly ROADMAP.md"))
        if entry.role in {"external-primary", "external-asset"}:
            expected_prefix = f"tmp/active-lesson-sources/{doc.metadata.get('lesson_id', '')}/"
            if not entry.path.startswith(expected_prefix):
                errors.append(
                    ValidationError(
                        entry.line,
                        "PATH",
                        f"{entry.role} must be inside {expected_prefix}",
                    )
                )
            allowed_suffixes = (
                {".pdf", ".html", ".md", ".txt"}
                if entry.role == "external-primary"
                else {".png", ".jpg", ".webp", ".gif", ".svg"}
            )
            external_path = PurePosixPath(entry.path)
            if external_path.stem != entry.sha256 or external_path.suffix not in allowed_suffixes:
                errors.append(
                    ValidationError(
                        entry.line,
                        "PATH",
                        f"{entry.role} path must use its SHA-256 filename and an allowed media suffix",
                    )
                )

    manifested_indexes = {entry.path: entry for entry in entries if entry.role == "course-index"}
    required_indexes: set[str] = set()
    for entry in entries:
        if entry.role != "primary":
            continue
        parts = PurePosixPath(entry.path).parts
        if len(parts) >= 4 and parts[:2] == ("materials", "private"):
            index_path = PurePosixPath(*parts[:3], "INDEX.md").as_posix()
            required_indexes.add(index_path)
            if index_path not in manifested_indexes:
                errors.append(
                    ValidationError(
                        entry.line,
                        "CURRICULUM_FRESHNESS",
                        f"private-course primary requires its course-index manifest input: {index_path}",
                    )
                )
    for index_path, entry in manifested_indexes.items():
        if index_path not in required_indexes:
            errors.append(
                ValidationError(
                    entry.line,
                    "CURRICULUM_FRESHNESS",
                    f"course-index does not correspond to a private-course primary input: {index_path}",
                )
            )

    canonical_rows: list[str] = []
    for entry in entries:
        candidate, path_error = _safe_repo_path(entry.path, doc.repo_root)
        if path_error:
            errors.append(ValidationError(entry.line, "PATH", path_error))
            continue
        assert candidate is not None
        if not candidate.exists() or not candidate.is_file():
            errors.append(ValidationError(entry.line, "SOURCE_MISSING", f"manifest file does not exist: {entry.path}"))
            continue
        actual_hash = _sha256_bytes(candidate.read_bytes())
        if HASH_RE.fullmatch(entry.sha256) and actual_hash != entry.sha256:
            errors.append(ValidationError(entry.line, "SOURCE_HASH", f"hash mismatch for {entry.path}: expected {entry.sha256}, got {actual_hash}"))
        canonical_rows.append(f"{entry.role}\t{entry.path}\t{entry.sha256}\n")
    all_rows = [f"{entry.role}\t{entry.path}\t{entry.sha256}\n" for entry in entries]
    doc.computed_manifest_sha256 = _sha256_bytes("".join(sorted(all_rows)).encode("utf-8"))


def _contract_sections(contract: str) -> tuple[dict[str, str], list[tuple[str, int]]]:
    matches = list(re.finditer(r"^### ([^\n]+)$", contract, re.MULTILINE))
    sections: dict[str, str] = {}
    headings: list[tuple[str, int]] = []
    for index, match in enumerate(matches):
        name = match.group(1)
        body_start = match.end()
        if contract[body_start : body_start + 1] == "\n":
            body_start += 1
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(contract)
        sections[name] = contract[body_start:body_end].strip("\n")
        headings.append((name, match.start()))
    return sections, headings


def _parse_target_decision(
    doc: HandoffDocument,
    section: str,
    body_start: int,
    errors: list[ValidationError],
) -> None:
    expected = (
        "selection_mode",
        "target_state",
        "primary_target",
        "bridge_target",
        "evidence_gap",
        "completion_evidence",
        "endpoint",
        "why_now",
    )
    values: dict[str, str] = {}
    line_no = _line_number(doc.text, body_start)
    for line in section.splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"- ([a-z_]+):[ \t]*(.*)", line.strip())
        if match is None:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid Target Decision row: {line.strip()}"))
            continue
        key, value = match.groups()
        if key in values:
            errors.append(ValidationError(line_no, "SCHEMA", f"duplicate Target Decision field: {key}"))
        values[key] = value.strip()
    if tuple(values) != expected:
        errors.append(
            ValidationError(
                line_no,
                "SCHEMA",
                "Target Decision fields must appear exactly in order: " + ", ".join(expected),
            )
        )
        return

    selection_mode = values["selection_mode"]
    target_state = values["target_state"]
    primary_target = values["primary_target"]
    bridge_target = values["bridge_target"]
    evidence_gap = _comma_ids(values["evidence_gap"], r"(?:explain|calculate|shape|implement|debug|interpret|design|transfer)")
    if selection_mode not in TARGET_SELECTION_MODES:
        errors.append(ValidationError(line_no, "SCHEMA", f"invalid target selection mode: {selection_mode}"))
    if target_state not in TARGET_STATES:
        errors.append(ValidationError(line_no, "SCHEMA", f"invalid target state: {target_state}"))
    elif target_state not in ACTIONABLE_TARGET_STATES:
        errors.append(
            ValidationError(
                line_no,
                "TARGET_DECISION",
                "lesson handoff requires START_TARGET, CONTINUE_TARGET, or BRIDGE_PREREQUISITE; return diagnostic and no-action results to the planner",
            )
        )
    if not CURRICULUM_ID_RE.fullmatch(primary_target):
        errors.append(ValidationError(line_no, "SCHEMA", f"invalid primary target: {primary_target}"))
    if bridge_target != "none" and not CURRICULUM_ID_RE.fullmatch(bridge_target):
        errors.append(ValidationError(line_no, "SCHEMA", f"invalid bridge target: {bridge_target}"))
    if evidence_gap is None or len(evidence_gap) != len(set(evidence_gap)):
        errors.append(ValidationError(line_no, "SCHEMA", "evidence_gap must be none or unique evidence tokens"))
        evidence_gap = []
    for key in ("completion_evidence", "endpoint", "why_now"):
        if not values[key] or values[key] == "none":
            errors.append(ValidationError(line_no, "SCHEMA", f"Target Decision {key} must be concrete"))
    if target_state == "BRIDGE_PREREQUISITE" and bridge_target == "none":
        errors.append(ValidationError(line_no, "SCHEMA", "BRIDGE_PREREQUISITE requires bridge_target"))
    if target_state != "BRIDGE_PREREQUISITE" and bridge_target != "none":
        errors.append(ValidationError(line_no, "SCHEMA", "bridge_target requires BRIDGE_PREREQUISITE"))
    doc.target_decision = TargetDecision(
        selection_mode,
        target_state,
        primary_target,
        bridge_target,
        evidence_gap or [],
        values["completion_evidence"],
        values["endpoint"],
        values["why_now"],
        line_no,
    )


def _validate_target_endpoint_relation(
    doc: HandoffDocument,
    curriculum_snapshot: Any,
    errors: list[ValidationError],
) -> None:
    decision = doc.target_decision
    if decision is None:
        return
    if decision.endpoint == "user-directed":
        if decision.selection_mode == "planner":
            errors.append(
                ValidationError(
                    decision.line,
                    "TARGET_DECISION",
                    "planner selection requires an exact ordered ROADMAP endpoint, not user-directed",
                )
            )
        return

    roadmap_entry = next(
        (
            entry
            for entry in doc.manifest
            if entry.role == "roadmap" and entry.path == "ROADMAP.md"
        ),
        None,
    )
    if roadmap_entry is None:
        return
    roadmap_path, path_error = _safe_repo_path(roadmap_entry.path, doc.repo_root)
    if path_error is not None or roadmap_path is None or not roadmap_path.is_file():
        return
    try:
        endpoints = parse_roadmap_endpoints(roadmap_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as error:
        errors.append(
            ValidationError(
                roadmap_entry.line,
                "TARGET_DECISION",
                f"ROADMAP endpoint table is invalid: {error}",
            )
        )
        return
    endpoint_ids = {entry["target_id"] for entry in endpoints}
    if decision.endpoint not in endpoint_ids:
        errors.append(
            ValidationError(
                decision.line,
                "TARGET_DECISION",
                f"endpoint is not an ordered ROADMAP endpoint: {decision.endpoint}",
            )
        )
        return
    if decision.primary_target not in curriculum_snapshot.targets:
        return
    try:
        route = set(
            prerequisite_closure(decision.endpoint, curriculum_snapshot.targets)
        ) | {decision.endpoint}
    except ValueError as error:
        errors.append(
            ValidationError(
                decision.line,
                "TARGET_DECISION",
                f"cannot resolve endpoint route: {error}",
            )
        )
        return
    if decision.primary_target not in route:
        errors.append(
            ValidationError(
                decision.line,
                "TARGET_DECISION",
                f"primary_target {decision.primary_target} is outside endpoint route {decision.endpoint}",
            )
        )


def _parse_external_identities(
    doc: HandoffDocument,
    section: str,
    body_start: int,
    errors: list[ValidationError],
) -> None:
    rows = _contract_table_rows(
        section,
        [
            "Primary ID",
            "Provider",
            "Course",
            "Offering/Edition",
            "Artifact",
            "Official URL",
            "Final URL",
            "Retrieved at",
            "Media type",
            "Scope",
            "Receipt path",
        ],
        doc,
        body_start,
        errors,
        context="External Source Identity",
    )
    if len(rows) == 1 and rows[0][0] == ["none"] * 11:
        rows = []
    identities: dict[str, ExternalSourceIdentity] = {}
    for cells, line_no in rows:
        (
            primary_id,
            provider,
            course,
            offering,
            artifact,
            official_url,
            final_url,
            retrieved_at,
            media_type,
            scope,
            receipt_path,
        ) = cells
        if primary_id in identities:
            errors.append(ValidationError(line_no, "EXTERNAL_IDENTITY", f"duplicate external identity: {primary_id}"))
            continue
        entry = next((item for item in doc.manifest if item.item_id == primary_id), None)
        if entry is None or entry.role != "external-primary":
            errors.append(ValidationError(line_no, "EXTERNAL_IDENTITY", f"{primary_id} is not an external-primary manifest row"))
        for label, value in (
            ("Provider", provider),
            ("Course", course),
            ("Offering/Edition", offering),
            ("Artifact", artifact),
            ("Scope", scope),
        ):
            if not value or value == "none":
                errors.append(ValidationError(line_no, "EXTERNAL_IDENTITY", f"{label} must be concrete"))
        for label, value in (("Official URL", official_url), ("Final URL", final_url)):
            parsed = urlsplit(value)
            if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
                errors.append(ValidationError(line_no, "EXTERNAL_IDENTITY", f"{label} must be a public HTTPS URL without credentials"))
        if not _is_rfc3339(retrieved_at):
            errors.append(ValidationError(line_no, "EXTERNAL_IDENTITY", "Retrieved at must be RFC 3339"))
        if not media_type or media_type == "none":
            errors.append(ValidationError(line_no, "EXTERNAL_IDENTITY", "Media type must be concrete"))
        receipt, path_error = _safe_repo_path(receipt_path, doc.repo_root)
        if path_error or receipt is None:
            errors.append(ValidationError(line_no, "EXTERNAL_IDENTITY", f"invalid receipt path: {path_error}"))
        if entry is not None and entry.role == "external-primary":
            expected_receipt = (
                f"tmp/active-lesson-sources/{doc.metadata.get('lesson_id', '')}/"
                f"{entry.sha256}.receipt.json"
            )
            if receipt_path != expected_receipt:
                errors.append(
                    ValidationError(
                        line_no,
                        "EXTERNAL_IDENTITY",
                        f"Receipt path must be the content-addressed lesson receipt: {expected_receipt}",
                    )
                )
        identities[primary_id] = ExternalSourceIdentity(
            primary_id,
            provider,
            course,
            offering,
            artifact,
            official_url,
            final_url,
            retrieved_at,
            media_type,
            scope,
            receipt_path,
            line_no,
        )
    external_primary_ids = [
        entry.item_id for entry in doc.manifest if entry.role == "external-primary"
    ]
    if list(identities) != external_primary_ids:
        errors.append(
            ValidationError(
                _line_number(doc.text, body_start),
                "EXTERNAL_IDENTITY",
                "External Source Identity must contain one ordered row per external-primary input",
            )
        )
    doc.external_identities = identities


def _validate_external_receipts(
    doc: HandoffDocument,
    errors: list[ValidationError],
) -> None:
    manifest_by_id = {entry.item_id: entry for entry in doc.manifest}
    for primary_id, identity in doc.external_identities.items():
        entry = manifest_by_id.get(primary_id)
        if entry is None:
            continue
        receipt_path, path_error = _safe_repo_path(identity.receipt_path, doc.repo_root)
        if path_error or receipt_path is None or not receipt_path.is_file():
            errors.append(ValidationError(identity.line, "EXTERNAL_CACHE_MISSING", f"cache receipt is missing: {identity.receipt_path}"))
            continue
        try:
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            errors.append(ValidationError(identity.line, "EXTERNAL_CACHE_IDENTITY", f"cache receipt is unreadable: {identity.receipt_path}"))
            continue
        expected = {
            "status": "CACHED",
            "lesson_id": doc.metadata.get("lesson_id"),
            "kind": "primary",
            "original_url": identity.official_url,
            "final_url": identity.final_url,
            "media_type": identity.media_type,
            "retrieved_at": identity.retrieved_at,
            "sha256": entry.sha256,
            "path": entry.path,
            "receipt_path": identity.receipt_path,
        }
        mismatches = [key for key, value in expected.items() if receipt.get(key) != value]
        candidate = doc.repo_root / entry.path
        if candidate.is_file() and receipt.get("byte_count") != candidate.stat().st_size:
            mismatches.append("byte_count")
        if mismatches:
            errors.append(
                ValidationError(
                    identity.line,
                    "EXTERNAL_CACHE_IDENTITY",
                    f"cache receipt differs from handoff identity: {', '.join(sorted(set(mismatches)))}",
                )
            )

    for entry in (item for item in doc.manifest if item.role == "external-asset"):
        expected_receipt_path = (
            doc.repo_root
            / "tmp/active-lesson-sources"
            / str(doc.metadata.get("lesson_id", ""))
            / f"{entry.sha256}.receipt.json"
        )
        if not expected_receipt_path.is_file():
            errors.append(
                ValidationError(
                    entry.line,
                    "EXTERNAL_CACHE_MISSING",
                    f"external asset receipt is missing: {expected_receipt_path.relative_to(doc.repo_root).as_posix()}",
                )
            )
            continue
        try:
            receipt = json.loads(expected_receipt_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            errors.append(
                ValidationError(
                    entry.line,
                    "EXTERNAL_CACHE_IDENTITY",
                    "external asset receipt is unreadable",
                )
            )
            continue
        expected = {
            "status": "CACHED",
            "lesson_id": doc.metadata.get("lesson_id"),
            "kind": "asset",
            "sha256": entry.sha256,
            "path": entry.path,
            "receipt_path": expected_receipt_path.relative_to(doc.repo_root).as_posix(),
        }
        mismatches = [key for key, value in expected.items() if receipt.get(key) != value]
        for key in ("original_url", "final_url"):
            parsed = urlsplit(str(receipt.get(key, "")))
            if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
                mismatches.append(key)
        candidate = doc.repo_root / entry.path
        if candidate.is_file() and receipt.get("byte_count") != candidate.stat().st_size:
            mismatches.append("byte_count")
        if mismatches:
            errors.append(
                ValidationError(
                    entry.line,
                    "EXTERNAL_CACHE_IDENTITY",
                    "external asset receipt differs from the manifest: "
                    + ", ".join(sorted(set(mismatches))),
                )
            )


def _parse_external_relations(
    doc: HandoffDocument,
    section: str,
    body_start: int,
    errors: list[ValidationError],
) -> None:
    rows = _contract_table_rows(
        section,
        ["Target ID", "Primary ID", "Relation", "Objective IDs", "Audit basis"],
        doc,
        body_start,
        errors,
        context="External Target Relation",
    )
    if len(rows) == 1 and rows[0][0] == ["none"] * 5:
        rows = []
    relations: dict[tuple[str, str], ExternalTargetRelation] = {}
    manifest_by_id = {entry.item_id: entry for entry in doc.manifest}
    for cells, line_no in rows:
        target_id, primary_id, relation, raw_objectives, audit_basis = cells
        key = (target_id, primary_id)
        if key in relations:
            errors.append(ValidationError(line_no, "EXTERNAL_SOURCE_RELATION", f"duplicate external target relation: {target_id} / {primary_id}"))
            continue
        if target_id not in doc.curriculum_targets:
            errors.append(ValidationError(line_no, "EXTERNAL_SOURCE_RELATION", f"external relation target is not selected: {target_id}"))
        entry = manifest_by_id.get(primary_id)
        if entry is None or entry.role != "external-primary":
            errors.append(ValidationError(line_no, "EXTERNAL_SOURCE_RELATION", f"external relation primary is invalid: {primary_id}"))
        if relation not in EXTERNAL_RELATIONS:
            errors.append(ValidationError(line_no, "EXTERNAL_SOURCE_RELATION", f"invalid external relation: {relation}"))
        objective_ids = _comma_ids(raw_objectives, r"O\d{3,}")
        if objective_ids is None or not objective_ids or len(objective_ids) != len(set(objective_ids)):
            errors.append(ValidationError(line_no, "EXTERNAL_SOURCE_RELATION", "external relation requires unique Objective IDs"))
            objective_ids = []
        for objective_id in objective_ids:
            objective = doc.objectives.get(objective_id)
            if objective is None:
                errors.append(ValidationError(line_no, "EXTERNAL_SOURCE_RELATION", f"unknown external Objective ID: {objective_id}"))
                continue
            objective_path = _location_path(objective.source_location)
            if (
                objective.requirement != "source-core"
                or entry is None
                or objective_path != entry.path
            ):
                errors.append(
                    ValidationError(
                        line_no,
                        "EXTERNAL_SOURCE_RELATION",
                        f"{objective_id} must be source-core from {primary_id}",
                    )
                )
        if not audit_basis or audit_basis == "none":
            errors.append(ValidationError(line_no, "EXTERNAL_SOURCE_RELATION", "Audit basis must be concrete"))
        relations[key] = ExternalTargetRelation(
            target_id, primary_id, relation, objective_ids, audit_basis, line_no
        )
    doc.external_relations = relations


def _parse_source_scope_map(
    doc: HandoffDocument,
    section: str,
    body_start: int,
    errors: list[ValidationError],
) -> None:
    rows = _contract_table_rows(
        section,
        [
            "Primary ID",
            "Scope kind",
            "Scope ID",
            "Included units",
            "Boundary units",
            "Outside-scope disposition",
        ],
        doc,
        body_start,
        errors,
        context="Source Scope Map",
    )
    primary_entries = [entry for entry in doc.manifest if entry.role in PRIMARY_ROLES]
    primary_by_id = {entry.item_id: entry for entry in primary_entries}
    curriculum_entry = next(
        (entry for entry in doc.manifest if entry.role == "curriculum"), None
    )
    source_paths_by_id: dict[str, tuple[str, ...]] = {}
    if curriculum_entry is not None:
        curriculum_path, path_error = _safe_repo_path(curriculum_entry.path, doc.repo_root)
        if path_error is None and curriculum_path is not None and curriculum_path.is_file():
            try:
                source_paths_by_id = dict(
                    curriculum_snapshot_from_text(
                        curriculum_path.read_text(encoding="utf-8")
                    ).source_paths_by_id
                )
            except UnicodeDecodeError:
                pass

    scopes: dict[str, LessonSourceScope] = {}
    for cells, line_no in rows:
        (
            primary_id,
            scope_kind,
            scope_id,
            raw_included,
            raw_boundary,
            outside_disposition,
        ) = cells
        if primary_id in scopes:
            errors.append(ValidationError(line_no, "SCHEMA", f"duplicate Source Scope primary: {primary_id}"))
            continue
        primary = primary_by_id.get(primary_id)
        if primary is None:
            errors.append(ValidationError(line_no, "SCHEMA", f"Source Scope references an unknown primary ID: {primary_id}"))
            continue
        if scope_kind not in SCOPE_KINDS:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid scope kind: {scope_kind}"))
        included = split_units(raw_included)
        boundary = split_units(raw_boundary)
        registered_scope: CourseScope | None = None

        if scope_kind == "entire-source":
            if doc.coverage_mode != "full-source":
                errors.append(ValidationError(line_no, "LESSON_SCOPE", "entire-source is allowed only in full-source mode"))
            if scope_id != "none" or raw_included != "entire-source" or boundary or outside_disposition != "none":
                errors.append(ValidationError(line_no, "LESSON_SCOPE", "entire-source requires Scope ID none, Included units entire-source, Boundary units none, and disposition none"))
            included = ()
        else:
            if doc.coverage_mode != "focused":
                errors.append(ValidationError(line_no, "LESSON_SCOPE", f"{scope_kind} is allowed only in focused mode"))
            if not included:
                errors.append(ValidationError(line_no, "LESSON_SCOPE", f"{scope_kind} requires Included units"))
            if not outside_disposition or outside_disposition == "none":
                errors.append(ValidationError(line_no, "LESSON_SCOPE", "focused source scope requires one coarse outside-scope disposition"))
            included_anchors = [unit_location(unit) for unit in included]
            boundary_anchors = [unit_location(unit) for unit in boundary]
            overlap = [
                f"{included_anchor} <> {boundary_anchor}"
                for included_anchor in included_anchors
                if included_anchor is not None
                for boundary_anchor in boundary_anchors
                if boundary_anchor is not None and locations_overlap(included_anchor, boundary_anchor)
            ]
            if overlap:
                errors.append(ValidationError(line_no, "LESSON_SCOPE", "Included units and Boundary units overlap: " + ", ".join(sorted(overlap))))
            for unit, location in zip(included + boundary, included_anchors + boundary_anchors, strict=True):
                if location is None:
                    errors.append(ValidationError(line_no, "LESSON_SCOPE", f"scope unit needs a concrete title and one [source locator] anchor: {unit}"))
                    continue
                if _location_path(location) != primary.path:
                    errors.append(ValidationError(line_no, "LESSON_SCOPE", f"scope unit anchor must point to {primary.path}: {location}"))
                elif not _location_exists(location, doc.repo_root):
                    errors.append(ValidationError(line_no, "SOURCE_LOCATION", f"scope unit anchor is absent: {location}"))

        if scope_kind == "registered-slice":
            if primary.role != "primary" or scope_id == "none":
                errors.append(ValidationError(line_no, "LESSON_SCOPE", "registered-slice requires a local primary and concrete Scope ID"))
            parts = PurePosixPath(primary.path).parts
            expected_index = (
                f"materials/private/{parts[2]}/INDEX.md"
                if len(parts) == 4 and parts[:2] == ("materials", "private")
                else None
            )
            index_entry = next(
                (entry for entry in doc.manifest if entry.role == "course-index" and entry.path == expected_index),
                None,
            )
            if index_entry is None:
                errors.append(ValidationError(line_no, "LESSON_SCOPE", "registered-slice requires the matching course INDEX manifest input"))
            else:
                index_path, path_error = _safe_repo_path(index_entry.path, doc.repo_root)
                if path_error is None and index_path is not None and index_path.is_file():
                    parsed_scopes, scope_findings = parse_course_scopes(index_path)
                    for finding in scope_findings:
                        errors.append(ValidationError(finding.line, finding.code, finding.message))
                    matches = [scope for scope in parsed_scopes if scope.scope_id == scope_id]
                    if len(matches) != 1:
                        errors.append(ValidationError(line_no, "LESSON_SCOPE", f"registered Scope ID must occur exactly once in the course INDEX: {scope_id}"))
                    else:
                        registered_scope = matches[0]
                        if source_paths_by_id.get(registered_scope.source_id, ()) != (primary.path,):
                            errors.append(ValidationError(line_no, "LESSON_SCOPE", f"registered scope {scope_id} does not resolve to {primary.path}"))
                        if included != registered_scope.included_units or boundary != registered_scope.boundary_units:
                            errors.append(ValidationError(line_no, "LESSON_SCOPE", f"registered scope {scope_id} units must exactly match the course INDEX row"))
        elif scope_kind == "ephemeral-slice":
            if scope_id != "none":
                errors.append(ValidationError(line_no, "LESSON_SCOPE", "ephemeral-slice must use Scope ID none"))

        scopes[primary_id] = LessonSourceScope(
            primary_id,
            scope_kind,
            scope_id,
            included,
            boundary,
            outside_disposition,
            registered_scope,
            line_no,
        )
    doc.lesson_source_scopes = scopes
    if list(scopes) != [entry.item_id for entry in primary_entries]:
        errors.append(ValidationError(_line_number(doc.text, body_start), "LESSON_SCOPE", "Source Scope Map must contain one ordered row per primary input"))


def _validate_contract_locations_against_scopes(
    doc: HandoffDocument,
    errors: list[ValidationError],
) -> None:
    primary_by_path = {
        entry.path: entry for entry in doc.manifest if entry.role in PRIMARY_ROLES
    }

    def check(location: str, line: int, label: str) -> None:
        path = _location_path(location)
        primary = primary_by_path.get(path or "")
        if primary is None:
            return
        scope = doc.lesson_source_scopes.get(primary.item_id)
        if scope is None or scope.scope_kind == "entire-source":
            return
        effective = scope.registered_scope or CourseScope(
            scope.scope_id,
            "none",
            "ephemeral",
            scope.included_units,
            scope.boundary_units,
            scope.outside_disposition,
            scope.line,
        )
        if location_is_boundary(location, effective):
            errors.append(ValidationError(line, "LESSON_SCOPE_BOUNDARY", f"{label} may not use boundary-only context: {location}"))
        elif not location_is_included(location, effective):
            errors.append(ValidationError(line, "LESSON_SCOPE_RELATION", f"{label} lies outside the selected lesson slice: {location}"))

    for item in doc.guidance.values():
        check(item.source_location, item.line, item.guidance_id)
    for item in doc.objectives.values():
        if item.requirement == "source-core":
            check(item.source_location, item.line, item.objective_id)
    for item in doc.declared_goals.values():
        check(item.goal_location, item.line, item.goal_id)
        for support in item.body_support:
            check(support, item.line, f"{item.goal_id} body support")
    for item in doc.findings.values():
        check(item.source_location, item.line, item.finding_id)
    for module in doc.modules.values():
        for location in module.source_locations:
            check(location, module.line, module.module_id)


def _parse_contract(doc: HandoffDocument, errors: list[ValidationError]) -> None:
    marked = _marker_body(doc.text, "<!-- lesson-contract:start -->", "<!-- lesson-contract:end -->", errors)
    if marked is None:
        return
    contract, body_start, _ = marked
    doc.contract = contract
    doc.computed_contract_sha256 = _sha256_bytes(contract.encode("utf-8"))
    sections, headings = _contract_sections(contract)
    if [name for name, _ in headings] != list(CONTRACT_HEADINGS):
        errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", "Lesson Contract headings are missing, duplicated, extra, or out of order"))
        return
    for heading in CONTRACT_HEADINGS:
        if not sections.get(heading, "").strip():
            relative_line = next((offset for name, offset in headings if name == heading), 0)
            errors.append(ValidationError(_line_number(doc.text, body_start + relative_line), "SCHEMA", f"contract section must not be empty: {heading}"))

    mode_lines = [line.strip() for line in sections["Coverage Mode"].splitlines() if line.strip()]
    if len(mode_lines) != 1 or re.fullmatch(r"- mode: (full-source|focused)", mode_lines[0]) is None:
        errors.append(
            ValidationError(
                _line_number(doc.text, body_start),
                "SCHEMA",
                "Coverage Mode must contain exactly '- mode: full-source' or '- mode: focused'",
            )
        )
    else:
        doc.coverage_mode = mode_lines[0].removeprefix("- mode: ")

    target_lines = [line.strip()[2:].strip() for line in sections["Curriculum Targets"].splitlines() if line.strip().startswith("- ")]
    if not 1 <= len(target_lines) <= 2 or len(target_lines) != len(set(target_lines)):
        errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", "Curriculum Targets must contain one or two unique IDs"))
    for target in target_lines:
        if not CURRICULUM_ID_RE.fullmatch(target):
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"invalid curriculum target ID: {target}"))
    doc.curriculum_targets = target_lines

    _parse_target_decision(doc, sections["Target Decision"], body_start, errors)
    if doc.target_decision is not None:
        expected_targets = [doc.target_decision.primary_target]
        if doc.target_decision.bridge_target != "none":
            expected_targets.append(doc.target_decision.bridge_target)
        if target_lines != expected_targets:
            errors.append(
                ValidationError(
                    doc.target_decision.line,
                    "TARGET_DECISION",
                    "Curriculum Targets must be primary_target followed by the optional bridge_target",
                )
            )

    _parse_external_identities(
        doc, sections["External Source Identity"], body_start, errors
    )

    concept_rows: list[tuple[int, str, str, str, str]] = []
    for line in sections["Concept Path"].splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"(\d+)\. (C\d{2}) \| (none|\[선수개념\]|\[정정\]|\[보충\]) \| (.+?) \| source: (.+)", line.strip())
        if match is None:
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"invalid Concept Path row: {line.strip()}"))
            continue
        ordinal, concept_id, marker, name, location = match.groups()
        concept_rows.append((int(ordinal), concept_id, marker, name.strip(), location.strip()))
    if not 3 <= len(concept_rows) <= 7:
        errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", "Concept Path must contain three to seven concepts"))
    for index, (ordinal, concept_id, marker, name, location) in enumerate(concept_rows, start=1):
        if ordinal != index or concept_id != f"C{index:02d}":
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", "Concept Path ordinals and IDs must be contiguous"))
        if marker not in CONCEPT_MARKERS or not name:
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"invalid Concept Path entry: {concept_id}"))
        if "#" not in location or not location.rsplit("#", 1)[1].strip():
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"{concept_id} source must include an exact #location"))
        else:
            location_path = location.rsplit("#", 1)[0]
            manifest_paths = {entry.path for entry in doc.manifest}
            if location_path not in manifest_paths:
                errors.append(
                    ValidationError(
                        _line_number(doc.text, body_start),
                        "REVIEW_NOT_PASS",
                        f"{concept_id} source path is not in the Input Manifest: {location_path}",
                    )
                )
            elif not _location_exists(location, doc.repo_root):
                errors.append(
                    ValidationError(
                        _line_number(doc.text, body_start),
                        "SOURCE_LOCATION",
                        f"{concept_id} source location is absent from its manifested file: {location}",
                    )
                )
    doc.contract_concepts = [row[1] for row in concept_rows]

    manifest_paths = {entry.path: entry for entry in doc.manifest}
    primary_entries = [entry for entry in doc.manifest if entry.role in PRIMARY_ROLES]
    primary_by_id = {entry.item_id: entry for entry in primary_entries}

    _parse_source_scope_map(
        doc,
        sections["Source Scope Map"],
        body_start,
        errors,
    )

    guidance_rows = _contract_table_rows(
        sections["Guidance Map"],
        ["Guidance ID", "Kind", "Source location", "Summary", "Trigger"],
        doc,
        body_start,
        errors,
        context="Guidance Map",
    )
    guidance: dict[str, GuidanceItem] = {}
    if (
        len(guidance_rows) == 1
        and guidance_rows[0][0] == ["none", "none", "none", "none", "none"]
    ):
        guidance_rows = []
    for index, (cells, line_no) in enumerate(guidance_rows, start=1):
        guidance_id, kind, source_location, summary, trigger = cells
        expected_id = f"G{index:03d}"
        if guidance_id != expected_id:
            errors.append(ValidationError(line_no, "SCHEMA", f"Guidance ID must be {expected_id}"))
        if guidance_id in guidance:
            errors.append(ValidationError(line_no, "SCHEMA", f"duplicate Guidance ID: {guidance_id}"))
            continue
        if kind not in GUIDANCE_KINDS:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid guidance kind: {kind}"))
        location_path = _location_path(source_location)
        entry = manifest_paths.get(location_path or "")
        if entry is None or entry.role not in PRIMARY_ROLES:
            errors.append(ValidationError(line_no, "SCHEMA", f"{guidance_id} must point to a manifested primary source"))
        elif not _location_exists(source_location, doc.repo_root):
            errors.append(ValidationError(line_no, "SOURCE_LOCATION", f"{guidance_id} source location is absent: {source_location}"))
        if not summary or summary == "none":
            errors.append(ValidationError(line_no, "SCHEMA", f"{guidance_id} Summary must not be empty or none"))
        if not trigger or trigger == "none":
            errors.append(ValidationError(line_no, "SCHEMA", f"{guidance_id} requires a concrete on-demand Trigger"))
        guidance[guidance_id] = GuidanceItem(guidance_id, kind, source_location, summary, trigger, line_no)
    doc.guidance = guidance

    objective_rows = _contract_table_rows(
        sections["Observable Objective Map"],
        [
            "Objective ID",
            "Requirement",
            "Marker",
            "Source location",
            "Observable outcome",
            "Concept ID",
            "Treatment",
            "Teaching move",
            "Baseline evidence",
        ],
        doc,
        body_start,
        errors,
        context="Observable Objective Map",
    )
    objectives: dict[str, Objective] = {}
    for index, (cells, line_no) in enumerate(objective_rows, start=1):
        (
            objective_id,
            requirement,
            marker,
            source_location,
            outcome,
            concept_id,
            treatment,
            teaching_move,
            baseline_evidence,
        ) = cells
        expected_id = f"O{index:03d}"
        if objective_id != expected_id:
            errors.append(ValidationError(line_no, "SCHEMA", f"Objective ID must be {expected_id}"))
        if objective_id in objectives:
            errors.append(ValidationError(line_no, "SCHEMA", f"duplicate Objective ID: {objective_id}"))
            continue
        if requirement not in OBJECTIVE_REQUIREMENTS:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid objective requirement: {requirement}"))
        if marker not in OBJECTIVE_MARKERS:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid objective marker: {marker}"))
        if treatment not in OBJECTIVE_TREATMENTS:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid objective treatment: {treatment}"))
        location_path = _location_path(source_location)
        if location_path is None:
            errors.append(ValidationError(line_no, "SCHEMA", f"{objective_id} source must include an exact #location"))
        elif location_path not in manifest_paths:
            errors.append(
                ValidationError(
                    line_no,
                    "REVIEW_NOT_PASS",
                    f"{objective_id} source path is not in the Input Manifest: {location_path}",
                )
            )
        elif requirement == "source-core" and manifest_paths[location_path].role not in PRIMARY_ROLES:
            errors.append(ValidationError(line_no, "SCHEMA", f"source-core {objective_id} must point to a primary input"))
        elif not _location_exists(source_location, doc.repo_root):
            errors.append(
                ValidationError(
                    line_no,
                    "SOURCE_LOCATION",
                    f"{objective_id} source location is absent from its manifested file: {source_location}",
                )
            )
        if not outcome or outcome == "none":
            errors.append(ValidationError(line_no, "SCHEMA", f"{objective_id} Observable outcome must not be empty or none"))
        if re.search(r"(?<![A-Z0-9])G\d{3,}(?![A-Z0-9])", f"{outcome} {teaching_move} {baseline_evidence}"):
            errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"{objective_id} must not turn Guidance into an objective or teaching move"))
        if concept_id not in doc.contract_concepts:
            errors.append(ValidationError(line_no, "SCHEMA", f"{objective_id} references an unknown Concept ID: {concept_id}"))
        if requirement == "source-core" and marker in {"correction", "supplement"}:
            errors.append(ValidationError(line_no, "SCHEMA", f"source-core {objective_id} cannot be marked {marker}"))
        if requirement == "required-added" and marker == "none":
            errors.append(ValidationError(line_no, "SCHEMA", f"required-added {objective_id} requires a marker"))
        if requirement == "optional-added" and marker != "supplement":
            errors.append(ValidationError(line_no, "SCHEMA", f"optional-added {objective_id} must be marked supplement"))
        if treatment == "deferred":
            if teaching_move != "none":
                errors.append(ValidationError(line_no, "SCHEMA", f"deferred {objective_id} must use Teaching move none"))
        elif not teaching_move or teaching_move == "none":
            errors.append(ValidationError(line_no, "SCHEMA", f"non-deferred {objective_id} requires a Teaching move"))
        if treatment == "bridge":
            if not baseline_evidence or baseline_evidence == "none":
                errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"bridge {objective_id} requires exact baseline evidence"))
        elif baseline_evidence != "none":
            errors.append(ValidationError(line_no, "SCHEMA", f"non-bridge {objective_id} must use Baseline evidence none"))
        if requirement == "required-added" and treatment == "deferred":
            errors.append(
                ValidationError(
                    line_no,
                    "OBJECTIVE_COVERAGE",
                    f"required-added objective cannot be deferred: {objective_id}",
                )
            )
        elif doc.coverage_mode == "full-source" and requirement == "source-core" and treatment == "deferred":
            errors.append(
                ValidationError(
                    line_no,
                    "OBJECTIVE_COVERAGE",
                    f"full-source source-core objective cannot be deferred: {objective_id}",
                )
            )
        objectives[objective_id] = Objective(
            objective_id,
            requirement,
            marker,
            source_location,
            outcome,
            concept_id,
            treatment,
            teaching_move,
            baseline_evidence,
            line_no,
        )
    doc.objectives = objectives
    if not objectives:
        errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", "Observable Objective Map must not be empty"))

    _parse_external_relations(
        doc, sections["External Target Relation"], body_start, errors
    )

    treatment_rows = _contract_table_rows(
        sections["Curriculum Treatment Map"],
        ["Target ID", "Coverage", "Gap action", "Lesson treatment", "Objective IDs", "Note"],
        doc,
        body_start,
        errors,
        context="Curriculum Treatment Map",
    )
    treatments: dict[str, CurriculumTreatment] = {}
    for cells, line_no in treatment_rows:
        target_id, coverage, gap_action, lesson_treatment, raw_objectives, note = cells
        if target_id in treatments:
            errors.append(ValidationError(line_no, "SCHEMA", f"duplicate Curriculum Treatment target: {target_id}"))
            continue
        objective_ids = _comma_ids(raw_objectives, r"O\d{3,}")
        if objective_ids is None or len(objective_ids) != len(set(objective_ids)):
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid Objective IDs for Curriculum Treatment target: {target_id}"))
            objective_ids = []
        if coverage not in CURRICULUM_COVERAGE:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid Curriculum coverage: {coverage}"))
        if gap_action not in CURRICULUM_GAP_ACTIONS:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid Curriculum gap action: {gap_action}"))
        if lesson_treatment not in LESSON_TREATMENTS:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid lesson treatment: {lesson_treatment}"))
        if not note or note == "none":
            errors.append(ValidationError(line_no, "SCHEMA", f"Curriculum Treatment {target_id} requires a concrete note"))
        linked = [objectives[item] for item in objective_ids if item in objectives]
        unknown = [item for item in objective_ids if item not in objectives]
        if unknown:
            errors.append(ValidationError(line_no, "SCHEMA", f"Curriculum Treatment {target_id} references unknown objectives: {', '.join(unknown)}"))
        if lesson_treatment == "source-only":
            if gap_action != "그대로 사용" or coverage != "충분":
                errors.append(ValidationError(line_no, "CURRICULUM_FRESHNESS", "source-only requires current Curriculum values 충분 and 그대로 사용"))
            if not linked or any(item.requirement != "source-core" for item in linked):
                errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", "source-only requires one or more source-core Objective IDs only"))
        elif lesson_treatment == "supplement-now":
            if gap_action != "수업 내 보충":
                errors.append(ValidationError(line_no, "CURRICULUM_FRESHNESS", "supplement-now requires current Curriculum gap action 수업 내 보충"))
            if not any(item.requirement == "required-added" for item in linked):
                errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", "supplement-now requires at least one linked required-added objective"))
        elif lesson_treatment == "resolved-external":
            external_core = [
                item
                for item in linked
                if item.requirement == "source-core"
                and (path := _location_path(item.source_location)) is not None
                and manifest_paths.get(path) is not None
                and manifest_paths[path].role == "external-primary"
            ]
            if not external_core:
                errors.append(
                    ValidationError(
                        line_no,
                        "OBJECTIVE_COVERAGE",
                        "resolved-external requires one or more external source-core objectives",
                    )
                )
        elif lesson_treatment == "defer-gap":
            if gap_action not in {"별도 자료 확보", "원본 복구 후 재감사"}:
                errors.append(ValidationError(line_no, "CURRICULUM_FRESHNESS", "defer-gap requires 별도 자료 확보 or 원본 복구 후 재감사"))
            if any(item.requirement != "source-core" for item in linked):
                errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", "defer-gap may link existing source-core objectives only; it must not invent missing content"))
        elif lesson_treatment == "defer-track":
            if not target_id.startswith("TR-") or gap_action != "트랙 선택 시 확보":
                errors.append(ValidationError(line_no, "CURRICULUM_FRESHNESS", "defer-track requires a TR target with gap action 트랙 선택 시 확보"))
            if objective_ids:
                errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", "defer-track must use Objective IDs none"))
        treatments[target_id] = CurriculumTreatment(
            target_id,
            coverage,
            gap_action,
            lesson_treatment,
            objective_ids,
            note,
            line_no,
        )
    doc.curriculum_treatments = treatments
    if list(treatments) != target_lines:
        errors.append(
            ValidationError(
                _line_number(doc.text, body_start),
                "SCHEMA",
                "Curriculum Treatment Map must contain one ordered row per Curriculum Target",
            )
        )

    declared_rows = _contract_table_rows(
        sections["Declared Goal Alignment"],
        ["Goal ID", "Primary ID", "Goal location", "Disposition", "Linked IDs", "Body support", "Reason"],
        doc,
        body_start,
        errors,
        context="Declared Goal Alignment",
    )
    declared_goals: dict[str, DeclaredGoal] = {}
    if (
        len(declared_rows) == 1
        and declared_rows[0][0][0:6] == ["none", "none", "none", "none", "none", "none"]
        and declared_rows[0][0][6] not in {"", "none"}
    ):
        declared_rows = []
    for index, (cells, line_no) in enumerate(declared_rows, start=1):
        goal_id, primary_id, goal_location, disposition, raw_linked, raw_support, reason = cells
        expected_id = f"D{index:03d}"
        if goal_id != expected_id:
            errors.append(ValidationError(line_no, "SCHEMA", f"Goal ID must be {expected_id}"))
        if goal_id in declared_goals:
            errors.append(ValidationError(line_no, "SCHEMA", f"duplicate Goal ID: {goal_id}"))
            continue
        primary_entry = primary_by_id.get(primary_id)
        if primary_entry is None:
            errors.append(ValidationError(line_no, "SCHEMA", f"{goal_id} references an unknown primary ID: {primary_id}"))
        elif _location_path(goal_location) != primary_entry.path:
            errors.append(ValidationError(line_no, "SCHEMA", f"{goal_id} goal location must point to {primary_entry.path}"))
        elif not _location_exists(goal_location, doc.repo_root):
            errors.append(ValidationError(line_no, "SOURCE_LOCATION", f"{goal_id} goal location is absent: {goal_location}"))
        if disposition not in GOAL_DISPOSITIONS:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid goal disposition: {disposition}"))
        linked_ids = _mixed_ids(raw_linked, ("O", "G"))
        if linked_ids is None or len(linked_ids) != len(set(linked_ids)):
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid Linked IDs for {goal_id}"))
            linked_ids = []
        body_support = _locations(raw_support)
        for location in body_support:
            if primary_entry is not None and _location_path(location) != primary_entry.path:
                errors.append(ValidationError(line_no, "SCHEMA", f"{goal_id} body support must point to {primary_entry.path}: {location}"))
            elif not _location_exists(location, doc.repo_root):
                errors.append(ValidationError(line_no, "SOURCE_LOCATION", f"{goal_id} body support is absent: {location}"))
            if location == goal_location:
                errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"{goal_id} goal wording cannot be its own body support"))
        linked_objectives = [objectives[item] for item in linked_ids if item in objectives]
        linked_guidance = [guidance[item] for item in linked_ids if item in guidance]
        unknown_links = [item for item in linked_ids if item not in objectives and item not in guidance]
        if unknown_links:
            errors.append(ValidationError(line_no, "SCHEMA", f"{goal_id} references unknown IDs: {', '.join(unknown_links)}"))
        if disposition == "learning":
            if not linked_objectives or linked_guidance or len(linked_objectives) != len(linked_ids):
                errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"learning {goal_id} must link one or more Objective IDs only"))
            if not body_support:
                errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"learning {goal_id} requires exact body support beyond the goal wording"))
            if reason != "none":
                errors.append(ValidationError(line_no, "SCHEMA", f"learning {goal_id} must use Reason none"))
            for objective in linked_objectives:
                if objective.requirement != "source-core" or (
                    primary_entry is not None and _location_path(objective.source_location) != primary_entry.path
                ):
                    errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"learning {goal_id} must link source-core objectives from the same primary"))
        elif disposition == "guidance":
            if len(linked_ids) != 1 or len(linked_guidance) != 1:
                errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"guidance {goal_id} must link exactly one Guidance ID"))
            elif primary_entry is not None and _location_path(linked_guidance[0].source_location) != primary_entry.path:
                errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"guidance {goal_id} must link Guidance from the same primary"))
            if not reason or reason == "none":
                errors.append(ValidationError(line_no, "SCHEMA", f"guidance {goal_id} requires a reason it is not assessed"))
        elif disposition == "source-gap":
            if body_support:
                errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"source-gap {goal_id} must use Body support none"))
            if not reason or reason == "none":
                errors.append(ValidationError(line_no, "SCHEMA", f"source-gap {goal_id} requires a reason"))
            defers_missing_material = any(
                item.lesson_treatment in {"defer-gap", "defer-track"}
                for item in doc.curriculum_treatments.values()
            )
            if doc.coverage_mode == "full-source" and not linked_objectives and not defers_missing_material:
                errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"full-source source-gap {goal_id} requires a required-added correction or supplement, or a reviewed defer-gap treatment"))
            for objective in linked_objectives:
                if objective.requirement != "required-added" or objective.marker not in {"correction", "supplement"}:
                    errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"source-gap {goal_id} cannot masquerade as source-core; linked objectives must be required-added correction or supplement"))
            if linked_guidance:
                errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"source-gap {goal_id} must not link Guidance"))
        declared_goals[goal_id] = DeclaredGoal(
            goal_id,
            primary_id,
            goal_location,
            disposition,
            linked_ids,
            body_support,
            reason,
            line_no,
        )
    doc.declared_goals = declared_goals

    finding_rows = _contract_table_rows(
        sections["Audited Findings"],
        ["Finding ID", "Type", "Source location", "Linked IDs", "Note"],
        doc,
        body_start,
        errors,
        context="Audited Findings",
    )
    findings: dict[str, AuditedFinding] = {}
    if (
        len(finding_rows) == 1
        and finding_rows[0][0][0:4] == ["none", "none", "none", "none"]
        and finding_rows[0][0][4] not in {"", "none"}
    ):
        finding_rows = []
    for index, (cells, line_no) in enumerate(finding_rows, start=1):
        finding_id, finding_type, source_location, raw_linked, note = cells
        expected_id = f"F{index:03d}"
        if finding_id != expected_id:
            errors.append(ValidationError(line_no, "SCHEMA", f"Finding ID must be {expected_id}"))
        if finding_id in findings:
            errors.append(ValidationError(line_no, "SCHEMA", f"duplicate Finding ID: {finding_id}"))
            continue
        if finding_type not in FINDING_TYPES - {"none"}:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid audited finding type: {finding_type}"))
        source_path = _location_path(source_location)
        if source_path not in manifest_paths:
            errors.append(ValidationError(line_no, "SCHEMA", f"{finding_id} source must be an exact manifested location"))
        elif not _location_exists(source_location, doc.repo_root):
            errors.append(ValidationError(line_no, "SOURCE_LOCATION", f"{finding_id} source location is absent: {source_location}"))
        linked_ids = _mixed_ids(raw_linked, ("D", "G", "O"))
        if linked_ids is None or not linked_ids or len(linked_ids) != len(set(linked_ids)):
            errors.append(ValidationError(line_no, "SCHEMA", f"{finding_id} requires unique Goal, Guidance, or Objective Linked IDs"))
            linked_ids = []
        known_ids = set(declared_goals) | set(guidance) | set(objectives)
        unknown_links = [item for item in linked_ids if item not in known_ids]
        if unknown_links:
            errors.append(ValidationError(line_no, "SCHEMA", f"{finding_id} references unknown IDs: {', '.join(unknown_links)}"))
        if not note or note == "none":
            errors.append(ValidationError(line_no, "SCHEMA", f"{finding_id} Note must not be empty or none"))
        marker_by_type = {"correction": "correction", "prerequisite": "prerequisite", "supplement": "supplement"}
        expected_marker = marker_by_type.get(finding_type)
        if expected_marker is not None and not any(
            objectives[item].marker == expected_marker for item in linked_ids if item in objectives
        ):
            errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"{finding_id} must link an Objective marked {expected_marker}"))
        if finding_type == "underspecification" and not any(
            (item in declared_goals and declared_goals[item].disposition == "source-gap") or item in guidance
            for item in linked_ids
        ):
            errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"{finding_id} underspecification must link a source-gap Goal or Guidance ID"))
        findings[finding_id] = AuditedFinding(finding_id, finding_type, source_location, linked_ids, note, line_no)
    doc.findings = findings
    marker_types = {"prerequisite": "prerequisite", "correction": "correction", "supplement": "supplement"}
    for objective in objectives.values():
        expected_type = marker_types.get(objective.marker)
        if expected_type is not None and not any(
            finding.finding_type == expected_type and objective.objective_id in finding.linked_ids
            for finding in findings.values()
        ):
            errors.append(ValidationError(objective.line, "OBJECTIVE_COVERAGE", f"marked objective {objective.objective_id} requires a linked {expected_type} Audited Finding"))
        if objective.treatment == "deferred" and not any(
            finding.finding_type == "intentional-deferral" and objective.objective_id in finding.linked_ids
            for finding in findings.values()
        ):
            errors.append(ValidationError(objective.line, "OBJECTIVE_COVERAGE", f"deferred objective {objective.objective_id} requires a linked intentional-deferral Audited Finding"))
    for goal in declared_goals.values():
        if goal.disposition == "source-gap" and not any(
            finding.finding_type == "underspecification" and goal.goal_id in finding.linked_ids
            for finding in findings.values()
        ):
            errors.append(ValidationError(goal.line, "OBJECTIVE_COVERAGE", f"source-gap {goal.goal_id} requires a linked underspecification Audited Finding"))

    coverage_rows = _contract_table_rows(
        sections["Source Coverage Index"],
        ["Primary ID", "Declared Goal IDs", "Objective IDs", "Guidance IDs"],
        doc,
        body_start,
        errors,
        context="Source Coverage Index",
    )
    source_coverage: dict[str, SourceCoverage] = {}
    for cells, line_no in coverage_rows:
        primary_id, raw_goals, raw_objectives, raw_guidance = cells
        if primary_id in source_coverage:
            errors.append(ValidationError(line_no, "SCHEMA", f"duplicate Source Coverage primary: {primary_id}"))
            continue
        goal_ids = _comma_ids(raw_goals, r"D\d{3,}")
        objective_ids = _comma_ids(raw_objectives, r"O\d{3,}")
        guidance_ids = _comma_ids(raw_guidance, r"G\d{3,}")
        for label, item_ids in (("Declared Goal IDs", goal_ids), ("Objective IDs", objective_ids), ("Guidance IDs", guidance_ids)):
            if item_ids is None or len(item_ids) != len(set(item_ids)):
                errors.append(ValidationError(line_no, "SCHEMA", f"invalid {label} for {primary_id}"))
        goal_ids = goal_ids or []
        objective_ids = objective_ids or []
        guidance_ids = guidance_ids or []
        primary_entry = primary_by_id.get(primary_id)
        if primary_entry is None:
            errors.append(ValidationError(line_no, "SCHEMA", f"Source Coverage references an unknown primary ID: {primary_id}"))
        if doc.coverage_mode == "full-source" and not (goal_ids or objective_ids or guidance_ids):
            errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"full-source primary requires a declared goal, technical objective, or guidance item: {primary_id}"))
        if doc.coverage_mode == "focused" and not (goal_ids or objective_ids or guidance_ids):
            errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"focused primary requires mapped content inside its selected slice: {primary_id}"))
        source_coverage[primary_id] = SourceCoverage(
            primary_id,
            goal_ids,
            objective_ids,
            guidance_ids,
            line_no,
        )
    doc.source_coverage = source_coverage
    if list(source_coverage) != [entry.item_id for entry in primary_entries]:
        errors.append(ValidationError(_line_number(doc.text, body_start), "OBJECTIVE_COVERAGE", "Source Coverage Index must contain one ordered row per primary input"))
    for entry in primary_entries:
        row = source_coverage.get(entry.item_id)
        if row is None:
            continue
        expected_goals = [goal.goal_id for goal in declared_goals.values() if goal.primary_id == entry.item_id]
        expected_objectives = [
            objective.objective_id
            for objective in objectives.values()
            if objective.requirement == "source-core" and _location_path(objective.source_location) == entry.path
        ]
        expected_guidance = [item.guidance_id for item in guidance.values() if _location_path(item.source_location) == entry.path]
        if row.goal_ids != expected_goals:
            errors.append(ValidationError(row.line, "OBJECTIVE_COVERAGE", f"{entry.item_id} Declared Goal IDs must exactly match its declared goals"))
        if row.objective_ids != expected_objectives:
            errors.append(ValidationError(row.line, "OBJECTIVE_COVERAGE", f"{entry.item_id} Objective IDs must exactly match its source-core objectives"))
        if row.guidance_ids != expected_guidance:
            errors.append(ValidationError(row.line, "OBJECTIVE_COVERAGE", f"{entry.item_id} Guidance IDs must exactly match its guidance items"))

    curriculum_entry = next((entry for entry in doc.manifest if entry.role == "curriculum" and entry.path == "CURRICULUM.md"), None)
    if curriculum_entry is not None:
        curriculum_path, path_error = _safe_repo_path(curriculum_entry.path, doc.repo_root)
        if path_error is None and curriculum_path is not None and curriculum_path.is_file():
            try:
                curriculum_text = curriculum_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                errors.append(ValidationError(curriculum_entry.line, "SCHEMA", "CURRICULUM.md is not valid UTF-8"))
            else:
                curriculum_rows = _curriculum_target_rows(curriculum_text)
                curriculum_snapshot = curriculum_snapshot_from_text(curriculum_text)
                decision = doc.target_decision
                _validate_target_endpoint_relation(doc, curriculum_snapshot, errors)
                if decision is not None and decision.primary_target in curriculum_snapshot.targets:
                    primary_snapshot = curriculum_snapshot.targets[decision.primary_target]
                    unknown_evidence = set(decision.evidence_gap) - set(primary_snapshot.required_evidence)
                    if unknown_evidence:
                        errors.append(
                            ValidationError(
                                decision.line,
                                "TARGET_DECISION",
                                "evidence_gap is not required by the primary target: "
                                + ", ".join(sorted(unknown_evidence)),
                            )
                        )
                    if decision.bridge_target != "none":
                        try:
                            closure = set(
                                prerequisite_closure(
                                    decision.primary_target,
                                    curriculum_snapshot.targets,
                                )
                            )
                        except ValueError:
                            closure = set()
                        if decision.bridge_target not in closure:
                            errors.append(
                                ValidationError(
                                    decision.line,
                                    "TARGET_DECISION",
                                    f"bridge_target is not a prerequisite of {decision.primary_target}",
                                )
                            )
                for target in target_lines:
                    row = curriculum_rows.get(target)
                    if CURRICULUM_ID_RE.fullmatch(target) and row is None:
                        errors.append(
                            ValidationError(
                                _line_number(doc.text, body_start),
                                "REVIEW_NOT_PASS",
                                f"Curriculum Target has no competency row in CURRICULUM.md: {target}",
                            )
                        )
                        continue
                    treatment = treatments.get(target)
                    if row is not None and treatment is not None:
                        actual_coverage, actual_gap_action, _ = row
                        if treatment.coverage != actual_coverage or treatment.gap_action != actual_gap_action:
                            errors.append(
                                ValidationError(
                                    treatment.line,
                                    "CURRICULUM_FRESHNESS",
                                    f"Curriculum Treatment {target} is stale: expected {actual_coverage} / {actual_gap_action}",
                                )
                            )

    module_rows = _contract_table_rows(
        sections["Module Plan"],
        [
            "Module ID",
            "Topic",
            "Concept IDs",
            "Source locators",
            "Application step",
            "Expected minutes",
        ],
        doc,
        body_start,
        errors,
        context="Module Plan",
    )
    modules: dict[str, LessonModule] = {}
    for index, (cells, line_no) in enumerate(module_rows, start=1):
        module_id, topic, raw_concepts, raw_locations, application_step, raw_minutes = cells
        expected_id = f"M{index:02d}"
        if module_id != expected_id or module_id in modules:
            errors.append(ValidationError(line_no, "SCHEMA", f"Module ID must be unique and contiguous: {expected_id}"))
            continue
        concept_ids = _comma_ids(raw_concepts, r"C\d{2}")
        if concept_ids is None or not concept_ids or len(concept_ids) != len(set(concept_ids)):
            errors.append(ValidationError(line_no, "SESSION_DEPTH", f"{module_id} requires unique Concept IDs"))
            concept_ids = []
        unknown_concepts = [item for item in concept_ids if item not in doc.contract_concepts]
        if unknown_concepts:
            errors.append(ValidationError(line_no, "SESSION_DEPTH", f"{module_id} references unknown concepts: {', '.join(unknown_concepts)}"))
        locations = [item.strip() for item in raw_locations.split(";") if item.strip()]
        if not locations or len(locations) != len(set(locations)):
            errors.append(ValidationError(line_no, "SESSION_DEPTH", f"{module_id} requires unique source locators"))
        for location in locations:
            path = _location_path(location)
            if path is None or path not in manifest_paths:
                errors.append(ValidationError(line_no, "SOURCE_LOCATION", f"{module_id} locator is not manifested: {location}"))
            elif not _location_exists(location, doc.repo_root):
                errors.append(ValidationError(line_no, "SOURCE_LOCATION", f"{module_id} locator does not exist: {location}"))
        if application_step != "none" and re.fullmatch(r"T\d{3,}", application_step) is None:
            errors.append(ValidationError(line_no, "SESSION_DEPTH", f"{module_id} Application step must be T### or none"))
        try:
            minutes = int(raw_minutes)
        except ValueError:
            minutes = 0
        if minutes <= 0:
            errors.append(ValidationError(line_no, "SESSION_DEPTH", f"{module_id} Expected minutes must be positive"))
        if not topic or topic == "none":
            errors.append(ValidationError(line_no, "SESSION_DEPTH", f"{module_id} requires a substantive topic"))
        modules[module_id] = LessonModule(
            module_id,
            topic,
            concept_ids,
            locations,
            application_step,
            minutes,
            line_no,
        )
    doc.modules = modules
    _validate_contract_locations_against_scopes(doc, errors)

    session_fields = re.findall(
        r"^- (session_goal|exit_step|exit_evidence_kind):[ \t]*(.*)$",
        sections["Session Plan"],
        re.MULTILINE,
    )
    if [key for key, _ in session_fields] != list(SESSION_PLAN_KEYS) or not all(
        value.strip() for _, value in session_fields
    ):
        errors.append(
            ValidationError(
                _line_number(doc.text, body_start),
                "SCHEMA",
                "Session Plan requires session_goal, exit_step, and exit_evidence_kind in order",
            )
        )
    doc.session_plan = {key: value.strip() for key, value in session_fields}
    if doc.session_plan.get("exit_evidence_kind") not in EVIDENCE_KINDS:
        errors.append(
            ValidationError(
                _line_number(doc.text, body_start),
                "SCHEMA",
                "Session Plan exit_evidence_kind is not an allowed learner evidence kind",
            )
        )

    example_rows = _contract_table_rows(
        sections["Example Map"],
        ["Example ID", "Purpose", "Fixture", "Objective IDs"],
        doc,
        body_start,
        errors,
        context="Example Map",
    )
    examples: dict[str, LessonExample] = {}
    for cells, line_no in example_rows:
        example_id, purpose, fixture, raw_objectives = cells
        objective_ids = _comma_ids(raw_objectives, r"O\d{3,}")
        if not re.fullmatch(r"X\d{3}", example_id) or example_id in examples:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid or duplicate Example ID: {example_id}"))
            continue
        if not purpose or purpose == "none" or not fixture or fixture == "none":
            errors.append(ValidationError(line_no, "SESSION_DEPTH", f"{example_id} requires a concrete purpose and fixture"))
        if objective_ids is None or not objective_ids or len(objective_ids) != len(set(objective_ids)):
            errors.append(ValidationError(line_no, "SCHEMA", f"{example_id} requires unique Objective IDs"))
            objective_ids = []
        for objective_id in objective_ids:
            if objective_id not in objectives:
                errors.append(ValidationError(line_no, "SCHEMA", f"{example_id} references an unknown objective: {objective_id}"))
        examples[example_id] = LessonExample(example_id, purpose, fixture, objective_ids, line_no)
    expected_examples = [f"X{index:03d}" for index in range(1, len(examples) + 1)]
    if list(examples) != expected_examples:
        errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", "Example IDs must be unique and contiguous from X001"))
    doc.examples = examples

    steps_body = sections["Prepared Teaching Steps"]
    step_matches = list(re.finditer(r"^#### (T\d{3,})$", steps_body, re.MULTILINE))
    expected_step_ids = [f"T{index:03d}" for index in range(1, len(step_matches) + 1)]
    if [match.group(1) for match in step_matches] != expected_step_ids:
        errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", "Prepared Teaching Step IDs must be unique and contiguous from T001"))
    assigned_objectives: list[str] = []
    teaching_steps: dict[str, TeachingStep] = {}
    for index, match in enumerate(step_matches):
        step_id = match.group(1)
        step_start = match.end()
        step_end = step_matches[index + 1].start() if index + 1 < len(step_matches) else len(steps_body)
        step_body = steps_body[step_start:step_end]
        field_matches = re.findall(
            r"^- (step_role|concept_ids|objective_ids|example_id|delivery_outline|tiny_example|check_policy|check_basis|check_question):[ \t]*(.*)$",
            step_body,
            re.MULTILINE,
        )
        expected_fields = [
            "step_role",
            "concept_ids",
            "objective_ids",
            "example_id",
            "delivery_outline",
            "tiny_example",
            "check_policy",
            "check_basis",
            "check_question",
        ]
        if [key for key, _ in field_matches] != expected_fields or not all(value.strip() for _, value in field_matches):
            errors.append(
                ValidationError(
                    _line_number(doc.text, body_start),
                    "SCHEMA",
                    f"{step_id} requires every ordered Prepared Teaching Step field with a non-empty value",
                )
            )
            continue
        fields = {key: value.strip() for key, value in field_matches}
        step_role = fields["step_role"]
        if step_role not in STEP_ROLES:
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"{step_id} step_role is not allowed: {step_role}"))
        concept_ids = _comma_ids(fields["concept_ids"], r"C\d{2}")
        if concept_ids is None or not concept_ids or len(concept_ids) != len(set(concept_ids)):
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"{step_id} concept_ids are invalid"))
            concept_ids = []
        unknown_concepts = [item for item in concept_ids if item not in doc.contract_concepts]
        if unknown_concepts:
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"{step_id} references unknown Concept IDs: {', '.join(unknown_concepts)}"))
        step_objectives = _comma_ids(fields["objective_ids"], r"O\d{3,}")
        if step_objectives is None or not step_objectives or len(step_objectives) != len(set(step_objectives)):
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"{step_id} objective_ids are invalid"))
            continue
        for objective_id in step_objectives:
            objective = objectives.get(objective_id)
            if objective is None:
                errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"unknown Teaching Step objective: {objective_id}"))
            elif objective.concept_id not in concept_ids:
                errors.append(ValidationError(_line_number(doc.text, body_start), "OBJECTIVE_COVERAGE", f"{objective_id} is assigned to a Teaching Step without its concept"))
            elif objective.treatment == "deferred":
                errors.append(ValidationError(_line_number(doc.text, body_start), "OBJECTIVE_COVERAGE", f"deferred objective appears in a Teaching Step: {objective_id}"))
        example_id = fields["example_id"]
        if example_id != "none" and example_id not in examples:
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"{step_id} references an unknown Example ID: {example_id}"))
        if example_id in examples:
            unlinked = [item for item in step_objectives if item not in examples[example_id].objective_ids]
            if unlinked:
                errors.append(ValidationError(_line_number(doc.text, body_start), "SESSION_DEPTH", f"{step_id} Example {example_id} does not cover: {', '.join(unlinked)}"))
        check_policy = fields["check_policy"]
        if check_policy not in CHECK_POLICIES:
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"{step_id} check_policy must be adaptive or none"))
        if check_policy == "adaptive":
            branch_match = re.fullmatch(r"if (.+) -> (.+); else -> (.+)", fields["check_basis"])
            if branch_match is None:
                errors.append(
                    ValidationError(
                        _line_number(doc.text, body_start),
                        "ASSESSMENT_ALIGNMENT",
                        f"{step_id} adaptive check_basis must state how each answer changes the next explanation using 'if ... -> ...; else -> ...'",
                    )
                )
            elif branch_match.group(2).strip() == branch_match.group(3).strip():
                errors.append(
                    ValidationError(
                        _line_number(doc.text, body_start),
                        "ASSESSMENT_ALIGNMENT",
                        f"{step_id} adaptive branches must lead to different next teaching moves",
                    )
                )
            if fields["check_question"] == "none":
                errors.append(ValidationError(_line_number(doc.text, body_start), "ASSESSMENT_ALIGNMENT", f"{step_id} adaptive Step requires a check question"))
            meta_question = (
                any(term in fields["check_question"] for term in ("수업 설계", "학습 방법", "강의 목차", "course outline", "teaching method"))
                or all(term in fields["check_question"] for term in ("이론", "복습", "실습"))
            )
            if doc.coverage_mode != "focused" and meta_question:
                errors.append(
                    ValidationError(
                        _line_number(doc.text, body_start),
                        "ASSESSMENT_ALIGNMENT",
                        f"{step_id} asks the learner to explain lesson design or study method instead of its technical objectives",
                    )
                )
        elif check_policy == "none":
            if fields["check_basis"] == "none":
                errors.append(ValidationError(_line_number(doc.text, body_start), "ASSESSMENT_ALIGNMENT", f"{step_id} check_basis must explain why no question is useful"))
            if fields["check_question"] != "none":
                errors.append(ValidationError(_line_number(doc.text, body_start), "ASSESSMENT_ALIGNMENT", f"{step_id} check_policy none requires check_question none"))
        guidance_refs = re.findall(r"(?<![A-Z0-9])G\d{3,}(?![A-Z0-9])", " ".join(fields.values()))
        if guidance_refs:
            errors.append(ValidationError(_line_number(doc.text, body_start), "OBJECTIVE_COVERAGE", f"{step_id} must not include Guidance IDs in teaching or assessment"))
        assigned_objectives.extend(step_objectives)
        teaching_steps[step_id] = TeachingStep(
            step_id,
            step_role,
            concept_ids,
            step_objectives,
            example_id,
            fields["delivery_outline"],
            fields["tiny_example"],
            check_policy,
            fields["check_basis"],
            fields["check_question"],
            _line_number(doc.text, body_start),
        )
    doc.teaching_steps = teaching_steps
    expected_assigned = [objective.objective_id for objective in objectives.values() if objective.treatment != "deferred"]
    if set(assigned_objectives) != set(expected_assigned):
        errors.append(
            ValidationError(
                _line_number(doc.text, body_start),
                "OBJECTIVE_COVERAGE",
                "every non-deferred objective must appear in Prepared Teaching Steps; synthesis Steps may deliberately revisit objectives",
            )
        )
    concepts_with_steps = {concept for step in teaching_steps.values() for concept in step.concept_ids}
    missing_concepts = [concept for concept in doc.contract_concepts if concept not in concepts_with_steps]
    if missing_concepts:
        errors.append(
            ValidationError(
                _line_number(doc.text, body_start),
                "OBJECTIVE_COVERAGE",
                "Concept Path entries without a Prepared Teaching Step: " + ", ".join(missing_concepts),
            )
        )

    profile = doc.metadata.get("session_profile")
    if profile == "standard":
        if not 3 <= len(doc.contract_concepts) <= 5:
            errors.append(ValidationError(_line_number(doc.text, body_start), "SESSION_DEPTH", "standard sessions require three to five connected Concept Path entries"))
        if not 3 <= len(doc.modules) <= 5:
            errors.append(ValidationError(_line_number(doc.text, body_start), "SESSION_DEPTH", "standard sessions require three to five substantive Module Plan rows"))
        total_minutes = sum(module.expected_minutes for module in doc.modules.values())
        if not 60 <= total_minutes <= 90:
            errors.append(ValidationError(_line_number(doc.text, body_start), "SESSION_DEPTH", f"standard Module Plan must total 60 to 90 minutes, got {total_minutes}"))
        normalized_topics = [re.sub(r"[^0-9a-z가-힣]+", "", module.topic.casefold()) for module in doc.modules.values()]
        if len(normalized_topics) != len(set(normalized_topics)):
            errors.append(ValidationError(_line_number(doc.text, body_start), "SESSION_DEPTH", "standard Module Plan topics must be substantively distinct"))
        module_signatures = [
            (tuple(module.concept_ids), tuple(module.source_locations))
            for module in doc.modules.values()
        ]
        if len(module_signatures) != len(set(module_signatures)):
            errors.append(ValidationError(_line_number(doc.text, body_start), "SESSION_DEPTH", "standard Module Plan contains duplicate concept/source slices"))
        planned_concepts = {concept for module in doc.modules.values() for concept in module.concept_ids}
        required_concepts = {
            objective.concept_id
            for objective in doc.objectives.values()
            if objective.treatment != "deferred"
        }
        if not required_concepts.issubset(planned_concepts):
            errors.append(ValidationError(_line_number(doc.text, body_start), "SESSION_DEPTH", "Module Plan must cover every non-deferred concept"))
        application_steps = [module.application_step for module in doc.modules.values() if module.application_step != "none"]
        if len(set(application_steps)) < 2:
            errors.append(ValidationError(_line_number(doc.text, body_start), "SESSION_DEPTH", "standard sessions require at least two distinct learner-application Steps"))
        for module in doc.modules.values():
            if module.application_step == "none":
                continue
            step = teaching_steps.get(module.application_step)
            if step is None:
                errors.append(ValidationError(module.line, "SESSION_DEPTH", f"{module.module_id} references an unknown application Step: {module.application_step}"))
            elif not set(module.concept_ids).intersection(step.concept_ids):
                errors.append(ValidationError(module.line, "SESSION_DEPTH", f"{module.module_id} application Step does not exercise its concepts"))
        roles = [step.step_role for step in teaching_steps.values()]
        role_positions = [roles.index(role) for role in STANDARD_STEP_ROLES if role in roles]
        if any(role not in roles for role in STANDARD_STEP_ROLES) or role_positions != sorted(role_positions):
            errors.append(ValidationError(_line_number(doc.text, body_start), "SESSION_DEPTH", "standard sessions require motivation, concept-model, worked-example, contrast-limit, and synthesis-transfer in order"))
        used_examples = {step.example_id for step in teaching_steps.values() if step.example_id != "none"}
        if len(used_examples) < 2:
            errors.append(ValidationError(_line_number(doc.text, body_start), "SESSION_DEPTH", "standard sessions require at least two distinct examples"))
        used_fixtures = {
            " ".join(examples[example_id].fixture.split()).casefold()
            for example_id in used_examples
            if example_id in examples
        }
        if len(used_fixtures) < 2:
            errors.append(ValidationError(_line_number(doc.text, body_start), "SESSION_DEPTH", "standard sessions require at least two distinct example fixtures"))
        final_step = next(reversed(teaching_steps.values()), None)
        if final_step is None or final_step.step_role != "synthesis-transfer":
            errors.append(ValidationError(_line_number(doc.text, body_start), "SESSION_DEPTH", "the final standard Step must be synthesis-transfer"))
        elif len(final_step.concept_ids) < 2 or final_step.check_policy != "adaptive":
            errors.append(ValidationError(final_step.line, "SESSION_DEPTH", "the final synthesis-transfer Step must adaptively integrate at least two concepts"))
        if doc.session_plan.get("exit_step") != (final_step.step_id if final_step else None):
            errors.append(ValidationError(_line_number(doc.text, body_start), "SESSION_DEPTH", "Session Plan exit_step must be the final synthesis-transfer Step"))
    elif profile in {"short", "custom"}:
        exit_step = doc.session_plan.get("exit_step")
        if exit_step not in teaching_steps:
            errors.append(ValidationError(_line_number(doc.text, body_start), "SESSION_DEPTH", "Session Plan exit_step must name a Prepared Teaching Step"))

    deferred_rows = _contract_table_rows(
        sections["Deferred"],
        ["Objective ID", "Source location", "Reason"],
        doc,
        body_start,
        errors,
        context="Deferred",
    )
    expected_deferred = [objective for objective in objectives.values() if objective.treatment == "deferred"]
    if not expected_deferred:
        if len(deferred_rows) != 1 or deferred_rows[0][0][0:2] != ["none", "none"] or deferred_rows[0][0][2] in {"", "none"}:
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", "Deferred without objectives requires one none | none | reason row"))
    else:
        actual_deferred: list[str] = []
        for cells, line_no in deferred_rows:
            objective_id, source_location, reason = cells
            objective = objectives.get(objective_id)
            actual_deferred.append(objective_id)
            if objective is None or objective.treatment != "deferred":
                errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"Deferred references a non-deferred or unknown objective: {objective_id}"))
            elif source_location != objective.source_location:
                errors.append(ValidationError(line_no, "SCHEMA", f"Deferred source location differs from {objective_id}"))
            if not reason or reason == "none":
                errors.append(ValidationError(line_no, "SCHEMA", f"Deferred {objective_id} requires a reason"))
        if actual_deferred != [objective.objective_id for objective in expected_deferred]:
            errors.append(ValidationError(_line_number(doc.text, body_start), "OBJECTIVE_COVERAGE", "Deferred must list every deferred objective once in objective order"))


def _parse_semantic_review(
    doc: HandoffDocument,
    section: tuple[int, int, int] | None,
    errors: list[ValidationError],
) -> None:
    if section is None:
        return
    start, end, _ = section
    region = doc.text[start:end]
    repair_heading = re.search(r"^### Repair Findings\s*$", region, re.MULTILINE)
    blocker_heading = re.search(r"^### Blocking Findings\s*$", region, re.MULTILINE)
    if repair_heading is None or blocker_heading is None or repair_heading.start() > blocker_heading.start():
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "Semantic Review requires ordered Repair Findings and Blocking Findings tables"))
        return

    values, lines, _ = _parse_bullets(
        doc.text,
        start,
        start + repair_heading.start(),
        REVIEW_KEYS,
        errors,
        context="Semantic Review",
    )
    try:
        iteration = int(values.get("review_iteration", ""))
    except ValueError:
        iteration = -1
    if iteration not in {0, 1, 2}:
        errors.append(ValidationError(lines.get("review_iteration", _line_number(doc.text, start)), "SCHEMA", "review_iteration must be 0, 1, or 2"))

    repair_rows = _contract_table_rows(
        region[repair_heading.end() : blocker_heading.start()],
        ["Finding ID", "Location", "Detail"],
        doc,
        start + repair_heading.end(),
        errors,
        context="Repair Findings",
    )
    blocker_rows = _contract_table_rows(
        region[blocker_heading.end() :],
        ["Finding ID", "Kind", "Location", "Detail"],
        doc,
        start + blocker_heading.end(),
        errors,
        context="Blocking Findings",
    )
    if len(repair_rows) == 1 and repair_rows[0][0] == ["none", "none", "none"]:
        repair_rows = []
    if len(blocker_rows) == 1 and blocker_rows[0][0] == ["none", "none", "none", "none"]:
        blocker_rows = []
    repair_ids: list[str] = []
    for cells, line_no in repair_rows:
        finding_id, location, detail = cells
        if not REPAIR_FINDING_RE.fullmatch(finding_id) or finding_id in repair_ids:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid or duplicate repair Finding ID: {finding_id}"))
        repair_ids.append(finding_id)
        if location == "none" or detail == "none" or not location or not detail:
            errors.append(ValidationError(line_no, "SCHEMA", f"repair finding {finding_id} requires a concrete location and detail"))
    blocker_ids: list[str] = []
    for cells, line_no in blocker_rows:
        finding_id, kind, location, detail = cells
        if not BLOCKER_FINDING_RE.fullmatch(finding_id) or finding_id in blocker_ids:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid or duplicate blocker Finding ID: {finding_id}"))
        blocker_ids.append(finding_id)
        if kind not in TRUE_BLOCKER_KINDS:
            errors.append(ValidationError(line_no, "REVIEW_NOT_PASS", f"{finding_id} uses a repairable or unsupported blocker kind: {kind}"))
        if location == "none" or detail == "none" or not location or not detail:
            errors.append(ValidationError(line_no, "SCHEMA", f"blocker {finding_id} requires a concrete location and detail"))
    values["repair_finding_ids"] = ",".join(repair_ids)
    values["blocker_finding_ids"] = ",".join(blocker_ids)

    phase = values.get("review_phase")
    verdict = values.get("verdict")
    recheck_ids = _comma_ids(values.get("recheck_of", "none"), r"R\d{3}")
    if phase not in REVIEW_PHASES:
        errors.append(ValidationError(lines.get("review_phase", _line_number(doc.text, start)), "SCHEMA", "review_phase is not allowed"))
    if verdict not in REVIEW_VERDICTS:
        errors.append(ValidationError(lines.get("verdict", _line_number(doc.text, start)), "SCHEMA", "review verdict is not allowed"))
    if recheck_ids is None or len(recheck_ids) != len(set(recheck_ids)):
        errors.append(ValidationError(lines.get("recheck_of", _line_number(doc.text, start)), "SCHEMA", "recheck_of must be none or unique R### IDs"))
        recheck_ids = []
    initial_reviewer_id = values.get("initial_reviewer_id", "")
    reviewer_id = values.get("reviewer_id", "")
    if iteration == 0:
        expected_pending = {
            "initial_reviewer_id": "none",
            "reviewer_id": "none",
            "review_phase": "none",
            "recheck_of": "none",
            "reviewed_at": "pending",
            "verdict": "pending",
            "reviewed_input_manifest_sha256": "pending",
            "reviewed_contract_sha256": "pending",
        }
        for key, expected in expected_pending.items():
            if values.get(key) != expected:
                errors.append(ValidationError(lines.get(key, _line_number(doc.text, start)), "SCHEMA", f"review_iteration 0 requires {key}: {expected}"))
        if repair_rows or blocker_rows:
            errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "pending review must not contain findings"))
        doc.semantic_review = SemanticReviewRecord(
            iteration, values, _line_number(doc.text, start)
        )
    else:
        if (
            not AGENT_ID_RE.fullmatch(initial_reviewer_id)
            or not AGENT_ID_RE.fullmatch(reviewer_id)
            or reviewer_id != initial_reviewer_id
            or reviewer_id == doc.metadata.get("author_id")
        ):
            errors.append(ValidationError(lines.get("reviewer_id", _line_number(doc.text, start)), "REVIEW_NOT_PASS", "semantic reviewer must have a valid ID different from the contract author"))
        if not _is_rfc3339(values.get("reviewed_at", "")):
            errors.append(ValidationError(lines.get("reviewed_at", _line_number(doc.text, start)), "SCHEMA", "reviewed_at must be an RFC 3339 timestamp with a timezone"))
        for key in ("reviewed_input_manifest_sha256", "reviewed_contract_sha256"):
            if not HASH_RE.fullmatch(values.get(key, "")):
                errors.append(ValidationError(lines.get(key, _line_number(doc.text, start)), "SCHEMA", f"{key} must be 64 lowercase hexadecimal characters"))
        if iteration == 1 and (phase != "independent-slice" or recheck_ids):
            errors.append(ValidationError(lines.get("review_phase", _line_number(doc.text, start)), "REVIEW_NOT_PASS", "review_iteration 1 requires independent-slice and recheck_of none"))
        if iteration == 2 and (phase != "targeted-recheck" or not recheck_ids):
            errors.append(ValidationError(lines.get("review_phase", _line_number(doc.text, start)), "REVIEW_NOT_PASS", "review_iteration 2 requires targeted-recheck and one or more recheck_of IDs"))
        if verdict == "pass" and (repair_rows or blocker_rows):
            errors.append(ValidationError(_line_number(doc.text, start), "REVIEW_NOT_PASS", "pass review must not contain current findings"))
        if verdict == "repair_required" and (not repair_rows or blocker_rows):
            errors.append(ValidationError(_line_number(doc.text, start), "REVIEW_NOT_PASS", "repair_required requires only repair findings"))
        if verdict == "blocked" and (repair_rows or not blocker_rows):
            errors.append(ValidationError(_line_number(doc.text, start), "REVIEW_NOT_PASS", "blocked verdict requires only true blocking findings"))
        doc.semantic_review = SemanticReviewRecord(
            iteration, values, _line_number(doc.text, start)
        )

    status = doc.metadata.get("status")
    current = doc.semantic_review
    if status == "preparing" and iteration != 0:
        errors.append(ValidationError(_line_number(doc.text, start), "REVIEW_NOT_PASS", "preparing status requires a pending review record"))
    if status == "repair_pending" and (current is None or current.values.get("verdict") != "repair_required"):
        errors.append(ValidationError(_line_number(doc.text, start), "REVIEW_NOT_PASS", "repair_pending requires a repair_required verdict"))
    if current is not None and current.values.get("verdict") == "repair_required" and status != "repair_pending":
        errors.append(ValidationError(current.line, "REVIEW_NOT_PASS", "repair_required verdict requires repair_pending status"))
    if status == "blocked" and (current is None or current.values.get("verdict") != "blocked"):
        errors.append(ValidationError(_line_number(doc.text, start), "REVIEW_NOT_PASS", "blocked status requires a true blocked verdict"))
    if current is not None and current.values.get("verdict") == "blocked" and status != "blocked":
        errors.append(ValidationError(current.line, "REVIEW_NOT_PASS", "true blocked verdict requires blocked status"))
    if status in {"active", "paused", "completed"}:
        if current is None or current.values.get("verdict") != "pass":
            errors.append(ValidationError(_line_number(doc.text, start), "REVIEW_NOT_PASS", f"{status} status requires a current pass verdict"))
    if current is not None and current.values.get("verdict") == "pass":
        if (
            current.values.get("reviewed_input_manifest_sha256") != doc.computed_manifest_sha256
            or current.values.get("reviewed_contract_sha256") != doc.computed_contract_sha256
        ):
            errors.append(ValidationError(current.line, "REVIEW_STALE", "pass verdict hashes do not match the current manifest and contract"))
        if any(error.code in {"SOURCE_MISSING", "SOURCE_HASH", "SOURCE_LOCATION", "PATH"} for error in errors):
            errors.append(ValidationError(current.line, "REVIEW_STALE", "pass verdict is stale because a manifested input is unavailable or changed"))


def _parse_current_position(
    doc: HandoffDocument,
    section: tuple[int, int, int] | None,
    errors: list[ValidationError],
) -> None:
    if section is None:
        return
    start, end, _ = section
    values, lines, _ = _parse_bullets(doc.text, start, end, CURRENT_POSITION_KEYS, errors, context="Current Position")
    doc.current_position = values
    for key in CURRENT_POSITION_KEYS:
        if key in values and not values[key]:
            errors.append(ValidationError(lines[key], "SCHEMA", f"{key} must not be empty"))
    last_completed = values.get("last_completed_step")
    current_step = values.get("current_step")
    next_action = values.get("next_action")
    target_objectives = _comma_ids(values.get("target_objectives", ""), r"O\d{3,}")
    basis = values.get("basis")
    resume_note = values.get("resume_note")
    status = doc.metadata.get("status")
    for key, value in (("last_completed_step", last_completed), ("current_step", current_step)):
        if value and value != "none" and value not in doc.teaching_steps:
            errors.append(ValidationError(lines.get(key, 1), "SCHEMA", f"{key} must be a Prepared Teaching Step ID or none"))
    if next_action not in POSITION_ACTIONS:
        errors.append(ValidationError(lines.get("next_action", 1), "SCHEMA", "next_action must be teach, await-answer, remediate, or complete"))
    if target_objectives is None or len(target_objectives) != len(set(target_objectives)):
        errors.append(ValidationError(lines.get("target_objectives", 1), "SCHEMA", "target_objectives must be none or unique Objective IDs"))
        target_objectives = []
    unknown_targets = [item for item in target_objectives if item not in doc.objectives]
    if unknown_targets:
        errors.append(ValidationError(lines.get("target_objectives", 1), "SCHEMA", "target_objectives contains unknown Objective IDs: " + ", ".join(unknown_targets)))
    if re.search(r"(?<![A-Z0-9])G\d{3,}(?![A-Z0-9])", " ".join(values.values())):
        errors.append(ValidationError(lines.get("target_objectives", 1), "OBJECTIVE_COVERAGE", "Current Position must not target or assess Guidance"))
    step = doc.teaching_steps.get(current_step or "")
    if next_action == "complete":
        if current_step != "none" or target_objectives or basis != "none":
            errors.append(ValidationError(lines.get("next_action", 1), "OBJECTIVE_COVERAGE", "complete requires current_step, target_objectives, and basis none"))
        if status != "completed":
            errors.append(ValidationError(lines.get("next_action", 1), "OBJECTIVE_COVERAGE", "next_action complete requires completed lesson status"))
    else:
        if current_step == "none" or step is None:
            errors.append(ValidationError(lines.get("current_step", 1), "OBJECTIVE_COVERAGE", "a non-complete action requires a current Teaching Step"))
        if not target_objectives:
            errors.append(ValidationError(lines.get("target_objectives", 1), "OBJECTIVE_COVERAGE", f"{next_action} requires target_objectives"))
        elif step is not None and any(item not in step.objective_ids for item in target_objectives):
            errors.append(ValidationError(lines.get("target_objectives", 1), "OBJECTIVE_COVERAGE", "target_objectives must belong to current_step"))
        if not resume_note or resume_note == "none":
            errors.append(ValidationError(lines.get("resume_note", 1), "SCHEMA", f"{next_action} requires a concrete resume_note"))
    if next_action == "await-answer":
        if step is not None and step.check_policy != "adaptive":
            errors.append(ValidationError(lines.get("next_action", 1), "ASSESSMENT_ALIGNMENT", "await-answer is allowed only for an adaptive Teaching Step"))
        if basis != "none":
            errors.append(ValidationError(lines.get("basis", 1), "ASSESSMENT_ALIGNMENT", "await-answer must use basis none until the learner answers"))
    elif next_action == "remediate":
        if re.fullmatch(r"learner-evidence:E\d{3,}", basis or "") is None:
            errors.append(ValidationError(lines.get("basis", 1), "ASSESSMENT_ALIGNMENT", "remediate requires basis learner-evidence:E###"))
    elif next_action == "teach" and basis != "none":
        errors.append(ValidationError(lines.get("basis", 1), "ASSESSMENT_ALIGNMENT", "teach must use basis none"))


def _parse_objective_delivery(
    doc: HandoffDocument,
    section: tuple[int, int, int] | None,
    errors: list[ValidationError],
) -> None:
    if section is None:
        return
    start, end, _ = section
    rows = _contract_table_rows(
        doc.text[start:end].strip(),
        ["Objective ID", "State", "Mode", "Basis/Note"],
        doc,
        start,
        errors,
        context="Objective Delivery",
    )
    delivery: dict[str, ObjectiveDelivery] = {}
    for cells, line_no in rows:
        objective_id, state, mode, note = cells
        if objective_id in delivery:
            errors.append(ValidationError(line_no, "SCHEMA", f"duplicate Objective Delivery row: {objective_id}"))
            continue
        if state not in DELIVERY_STATES:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid Objective Delivery state: {state}"))
        if mode not in DELIVERY_MODES:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid Objective Delivery mode: {mode}"))
        if not note:
            errors.append(ValidationError(line_no, "SCHEMA", f"Objective Delivery note must not be empty: {objective_id}"))
        if re.search(r"(?<![A-Z0-9])G\d{3,}(?![A-Z0-9])", note):
            errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"Objective Delivery must not include Guidance: {objective_id}"))
        objective = doc.objectives.get(objective_id)
        if objective is None:
            errors.append(ValidationError(line_no, "SCHEMA", f"Objective Delivery references an unknown objective: {objective_id}"))
        if state == "pending" and mode != "none":
            errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"pending {objective_id} must use mode none"))
        if state == "delivered" and mode not in {"full", "bridge"}:
            errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"delivered {objective_id} must use full or bridge mode"))
        if objective is not None and state == "delivered":
            if objective.treatment == "deferred":
                errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"deferred objective cannot be delivered without a reviewed contract change: {objective_id}"))
            elif objective.treatment == "full" and mode != "full":
                errors.append(ValidationError(line_no, "OBJECTIVE_COVERAGE", f"full objective must be delivered in full mode: {objective_id}"))
        delivery[objective_id] = ObjectiveDelivery(objective_id, state, mode, note, line_no)
    doc.objective_delivery = delivery
    if list(delivery) != list(doc.objectives):
        errors.append(
            ValidationError(
                _line_number(doc.text, start),
                "OBJECTIVE_COVERAGE",
                "Objective Delivery must contain one ordered row per Observable Objective",
            )
        )


def _parse_step_delivery(
    doc: HandoffDocument,
    section: tuple[int, int, int] | None,
    errors: list[ValidationError],
) -> None:
    if section is None:
        return
    start, end, _ = section
    rows = _contract_table_rows(
        doc.text[start:end].strip(),
        ["Step ID", "State", "Basis/Note"],
        doc,
        start,
        errors,
        context="Teaching Step Delivery",
    )
    delivery: dict[str, TeachingStepDelivery] = {}
    for cells, line_no in rows:
        step_id, state, note = cells
        if step_id in delivery:
            errors.append(ValidationError(line_no, "SCHEMA", f"duplicate Teaching Step Delivery row: {step_id}"))
            continue
        if step_id not in doc.teaching_steps:
            errors.append(ValidationError(line_no, "SCHEMA", f"Teaching Step Delivery references an unknown Step: {step_id}"))
        if state not in STEP_DELIVERY_STATES:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid Teaching Step Delivery state: {state}"))
        if not note:
            errors.append(ValidationError(line_no, "SCHEMA", f"Teaching Step Delivery note must not be empty: {step_id}"))
        delivery[step_id] = TeachingStepDelivery(step_id, state, note, line_no)
    doc.step_delivery = delivery
    if list(delivery) != list(doc.teaching_steps):
        errors.append(
            ValidationError(
                _line_number(doc.text, start),
                "SESSION_DEPTH",
                "Teaching Step Delivery must contain one ordered row per Prepared Teaching Step",
            )
        )


def _parse_evidence(
    doc: HandoffDocument,
    section: tuple[int, int, int] | None,
    errors: list[ValidationError],
) -> None:
    if section is None:
        return
    start, end, _ = section
    region = doc.text[start:end]
    start_matches = list(re.finditer(r"^<!-- learner-evidence:(E\d{3}):start -->[ \t]*$", region, re.MULTILINE))
    end_matches = list(re.finditer(r"^<!-- learner-evidence:(E\d{3}):end -->[ \t]*$", region, re.MULTILINE))
    if len(start_matches) != len(end_matches):
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "learner-evidence markers are unbalanced"))
        return
    evidence_items: list[Evidence] = []
    for start_match in start_matches:
        evidence_id = start_match.group(1)
        end_match = next((candidate for candidate in end_matches if candidate.group(1) == evidence_id and candidate.start() > start_match.end()), None)
        if end_match is None:
            errors.append(ValidationError(_line_number(doc.text, start + start_match.start()), "SCHEMA", f"missing end marker for {evidence_id}"))
            continue
        body_start = start + start_match.end()
        if doc.text[body_start : body_start + 1] == "\n":
            body_start += 1
        body_end = start + end_match.start()
        body = doc.text[body_start:body_end]
        heading = re.search(rf"^### {evidence_id}$", body, re.MULTILINE)
        content_heading = re.search(r"^#### Learner Content$", body, re.MULTILINE)
        assessment_heading = re.search(r"^#### Tutor Assessment$", body, re.MULTILINE)
        if heading is None or content_heading is None or assessment_heading is None or not (heading.start() < content_heading.start() < assessment_heading.start()):
            errors.append(ValidationError(_line_number(doc.text, body_start), "SCHEMA", f"{evidence_id} structure is invalid"))
            continue
        values_start = body_start + heading.end()
        values_end = body_start + content_heading.start()
        values, lines, spans = _parse_bullets(doc.text, values_start, values_end, EVIDENCE_KEYS, errors, context=evidence_id)
        content_region_start = body_start + content_heading.end()
        content_region_end = body_start + assessment_heading.start()
        marked = _marker_body(
            doc.text[content_region_start:content_region_end],
            "<!-- learner-content:start -->",
            "<!-- learner-content:end -->",
            errors,
        )
        content = ""
        if marked is not None:
            content = marked[0]
        assessment_start = body_start + assessment_heading.end()
        assessment = doc.text[assessment_start:body_end].strip()
        item_line = _line_number(doc.text, start + start_match.start())
        if not content:
            errors.append(ValidationError(item_line, "SCHEMA", f"{evidence_id} Learner Content must not be empty"))
        if not assessment:
            errors.append(ValidationError(item_line, "SCHEMA", f"{evidence_id} Tutor Assessment must not be empty"))
        if re.search(r"(?<![A-Z0-9])G\d{3,}(?![A-Z0-9])", f"{content}\n{assessment}"):
            errors.append(ValidationError(item_line, "EVIDENCE_STATE", f"{evidence_id} must not treat Guidance as learner evidence"))
        concept_ids = _comma_ids(values.get("concept_ids", ""), r"C\d{2}")
        if concept_ids is None or not concept_ids or len(concept_ids) != len(set(concept_ids)):
            errors.append(ValidationError(lines.get("concept_ids", item_line), "EVIDENCE_STATE", f"{evidence_id} requires unique Concept IDs"))
            concept_ids = []
        unknown_concepts = [item for item in concept_ids if item not in doc.contract_concepts]
        if unknown_concepts:
            errors.append(ValidationError(lines.get("concept_ids", item_line), "EVIDENCE_STATE", f"{evidence_id} concepts are not in the reviewed contract: {', '.join(unknown_concepts)}"))
        objective_ids = _comma_ids(values.get("objective_ids", ""), r"O\d{3,}")
        if objective_ids is None or not objective_ids or len(objective_ids) != len(set(objective_ids)):
            errors.append(ValidationError(lines.get("objective_ids", item_line), "EVIDENCE_STATE", f"{evidence_id} requires unique Objective IDs"))
            objective_ids = []
        for objective_id in objective_ids:
            objective = doc.objectives.get(objective_id)
            if objective is None:
                errors.append(ValidationError(lines.get("objective_ids", item_line), "EVIDENCE_STATE", f"{evidence_id} references an unknown objective: {objective_id}"))
                continue
            if objective.concept_id not in concept_ids:
                errors.append(ValidationError(lines.get("objective_ids", item_line), "EVIDENCE_STATE", f"{evidence_id} objective belongs to a different concept: {objective_id}"))
            delivery = doc.objective_delivery.get(objective_id)
            if delivery is None or delivery.state != "delivered":
                errors.append(ValidationError(lines.get("objective_ids", item_line), "EVIDENCE_STATE", f"{evidence_id} may reference delivered objectives only: {objective_id}"))
        if values.get("kind") not in EVIDENCE_KINDS:
            errors.append(ValidationError(lines.get("kind", item_line), "SCHEMA", f"{evidence_id} kind is not allowed"))
        if values.get("provenance") != "learner":
            errors.append(ValidationError(lines.get("provenance", item_line), "EVIDENCE_STATE", f"{evidence_id} provenance must be learner"))
        verdict = values.get("verdict")
        capture_state = values.get("capture_state")
        if verdict not in EVIDENCE_VERDICTS:
            errors.append(ValidationError(lines.get("verdict", item_line), "SCHEMA", f"{evidence_id} verdict is not allowed"))
        if capture_state not in CAPTURE_STATES:
            errors.append(ValidationError(lines.get("capture_state", item_line), "SCHEMA", f"{evidence_id} capture_state is not allowed"))
        if verdict == "confirmed" and capture_state not in {"pending", "captured"}:
            errors.append(ValidationError(lines.get("capture_state", item_line), "EVIDENCE_STATE", f"confirmed {evidence_id} must be pending or captured"))
        if verdict in {"partial", "misconception", "unconfirmed"} and capture_state != "not_eligible":
            errors.append(ValidationError(lines.get("capture_state", item_line), "EVIDENCE_STATE", f"non-confirmed {evidence_id} must be not_eligible"))
        if "captured_at" in values and not _is_rfc3339(values["captured_at"]):
            errors.append(ValidationError(lines["captured_at"], "SCHEMA", f"{evidence_id} captured_at must be an RFC 3339 timestamp"))
        actual_content_hash = _sha256_bytes(content.encode("utf-8"))
        if "content_sha256" in values and not HASH_RE.fullmatch(values["content_sha256"]):
            errors.append(ValidationError(lines["content_sha256"], "SCHEMA", f"{evidence_id} content_sha256 must be lowercase SHA-256"))
        elif values.get("content_sha256") != actual_content_hash:
            errors.append(ValidationError(lines.get("content_sha256", item_line), "EVIDENCE_STATE", f"{evidence_id} content hash mismatch: got {actual_content_hash}"))
        evidence_items.append(
            Evidence(
                evidence_id=evidence_id,
                values=values,
                content=content,
                assessment=assessment,
                line=item_line,
                capture_value_span=spans.get("capture_state", (0, 0)),
            )
        )

    evidence_items.sort(key=lambda item: item.evidence_id)
    expected = [f"E{index:03d}" for index in range(1, len(evidence_items) + 1)]
    actual = [item.evidence_id for item in evidence_items]
    if actual != expected:
        errors.append(ValidationError(_line_number(doc.text, start), "SCHEMA", "learner evidence IDs must be unique and contiguous from E001"))
    doc.evidence = {item.evidence_id: item for item in evidence_items}


def _parse_session_concept_coverage(
    doc: HandoffDocument,
    section: tuple[int, int, int] | None,
    errors: list[ValidationError],
) -> None:
    if section is None:
        return
    start, end, _ = section
    region = doc.text[start:end]
    table_header = re.search(
        r"^\| Concept ID \| Session state \| Evidence IDs \| Note \|[ \t]*$",
        region,
        re.MULTILINE,
    )
    if table_header is None:
        errors.append(
            ValidationError(
                _line_number(doc.text, start),
                "SCHEMA",
                "Session Concept Coverage table columns must be Concept ID | Session state | Evidence IDs | Note",
            )
        )
        return
    table_start = start + table_header.start()
    table_lines = doc.text[table_start:end].splitlines()
    if len(table_lines) < 2:
        errors.append(ValidationError(_line_number(doc.text, table_start), "SCHEMA", "Session Concept Coverage table is incomplete"))
        return
    separator = _split_table_row(table_lines[1])
    if separator is None or len(separator) != 4 or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
        errors.append(ValidationError(_line_number(doc.text, table_start) + 1, "SCHEMA", "Session Concept Coverage separator is invalid"))

    coverage: dict[str, LearningCoverage] = {}
    cursor = table_start + len(table_lines[0]) + 1 + len(table_lines[1]) + 1
    for raw_line in table_lines[2:]:
        line_no = _line_number(doc.text, cursor)
        cursor += len(raw_line) + 1
        if not raw_line.strip():
            continue
        cells = _split_table_row(raw_line)
        if cells is None or len(cells) != 4:
            errors.append(ValidationError(line_no, "SCHEMA", "Session Concept Coverage row must have four cells"))
            continue
        concept_id, today_state, raw_evidence, note = cells
        if concept_id in coverage:
            errors.append(ValidationError(line_no, "SCHEMA", f"duplicate coverage concept: {concept_id}"))
            continue
        evidence_ids = [] if raw_evidence == "none" else [item.strip() for item in raw_evidence.split(",") if item.strip()]
        row = LearningCoverage(concept_id, today_state, evidence_ids, note, line_no)
        coverage[concept_id] = row
        if today_state not in SESSION_CONCEPT_STATES:
            errors.append(ValidationError(line_no, "SCHEMA", f"invalid Session state for {concept_id}: {today_state}"))
        if not note:
            errors.append(ValidationError(line_no, "SCHEMA", f"coverage note must not be empty: {concept_id}"))
        if re.search(r"(?<![A-Z0-9])G\d{3,}(?![A-Z0-9])", f"{raw_evidence} {note}"):
            errors.append(ValidationError(line_no, "SESSION_CONCEPT_INCOMPLETE", f"Session Concept Coverage must not include Guidance: {concept_id}"))
        if today_state == "deferred":
            if evidence_ids:
                errors.append(ValidationError(line_no, "SESSION_CONCEPT_INCOMPLETE", f"deferred {concept_id} requires evidence none"))
        elif today_state == "confirmed":
            if not evidence_ids:
                errors.append(ValidationError(line_no, "SESSION_CONCEPT_INCOMPLETE", f"confirmed {concept_id} requires learner evidence"))

    doc.learning_coverage = coverage
    if list(coverage) != doc.contract_concepts:
        errors.append(
            ValidationError(
                _line_number(doc.text, table_start),
                "SCHEMA",
                "Session Concept Coverage must contain one ordered row per Concept Path concept",
            )
        )
    for row in coverage.values():
        for evidence_id in row.evidence_ids:
            if not re.fullmatch(r"E\d{3}", evidence_id):
                errors.append(ValidationError(row.line, "SCHEMA", f"invalid evidence ID in coverage: {evidence_id}"))
                continue
            evidence = doc.evidence.get(evidence_id)
            if evidence is None:
                errors.append(ValidationError(row.line, "SESSION_CONCEPT_INCOMPLETE", f"coverage references missing evidence: {evidence_id}"))
                continue
            evidence_concepts = _comma_ids(evidence.values.get("concept_ids", ""), r"C\d{2}") or []
            if row.concept_id not in evidence_concepts:
                errors.append(ValidationError(row.line, "SESSION_CONCEPT_INCOMPLETE", f"{evidence_id} belongs to a different concept"))
        if row.today_state == "confirmed" and row.evidence_ids:
            confirmed_evidence = [
                doc.evidence[evidence_id]
                for evidence_id in row.evidence_ids
                if evidence_id in doc.evidence and doc.evidence[evidence_id].values.get("verdict") == "confirmed"
            ]
            covered_objectives = {
                objective_id
                for evidence in confirmed_evidence
                for objective_id in (_comma_ids(evidence.values.get("objective_ids", ""), r"O\d{3,}") or [])
                if objective_id in doc.objectives
                and doc.objectives[objective_id].concept_id == row.concept_id
            }
            delivered_objectives = {
                objective.objective_id
                for objective in doc.objectives.values()
                if objective.concept_id == row.concept_id
                and doc.objective_delivery.get(objective.objective_id) is not None
                and doc.objective_delivery[objective.objective_id].state == "delivered"
            }
            if not confirmed_evidence:
                errors.append(ValidationError(row.line, "SESSION_CONCEPT_INCOMPLETE", f"confirmed {row.concept_id} requires confirmed evidence"))
            if not delivered_objectives or covered_objectives != delivered_objectives:
                missing = sorted(delivered_objectives - covered_objectives)
                extra = sorted(covered_objectives - delivered_objectives)
                detail = []
                if missing:
                    detail.append("missing " + ", ".join(missing))
                if extra:
                    detail.append("non-delivered " + ", ".join(extra))
                errors.append(
                    ValidationError(
                        row.line,
                        "SESSION_CONCEPT_INCOMPLETE",
                        f"confirmed {row.concept_id} evidence must exactly cover all delivered objectives"
                        + (": " + "; ".join(detail) if detail else ""),
                    )
                )


def _validate_objective_state(doc: HandoffDocument, errors: list[ValidationError]) -> None:
    manifest_by_path = {entry.path: entry for entry in doc.manifest}
    for objective in doc.objectives.values():
        if objective.treatment != "bridge":
            continue
        references = [item.strip() for item in objective.baseline_evidence.split(";") if item.strip()]
        if not references:
            errors.append(ValidationError(objective.line, "OBJECTIVE_COVERAGE", f"bridge {objective.objective_id} requires exact baseline evidence"))
            continue
        for reference in references:
            evidence_match = re.fullmatch(r"learner-evidence:(E\d{3})", reference)
            if evidence_match is not None:
                evidence = doc.evidence.get(evidence_match.group(1))
                if evidence is None or evidence.values.get("provenance") != "learner" or evidence.values.get("verdict") != "confirmed":
                    errors.append(
                        ValidationError(
                            objective.line,
                            "OBJECTIVE_COVERAGE",
                            f"bridge {objective.objective_id} references non-confirmed learner evidence: {reference}",
                        )
                    )
                continue
            path = _location_path(reference)
            entry = manifest_by_path.get(path or "")
            if entry is None or entry.role not in {"knowledge", "til", "practice"}:
                errors.append(
                    ValidationError(
                        objective.line,
                        "OBJECTIVE_COVERAGE",
                        f"bridge {objective.objective_id} baseline must be confirmed learner evidence or an exact manifested knowledge, til, or practice location: {reference}",
                    )
                )
            elif not _location_exists(reference, doc.repo_root):
                errors.append(
                    ValidationError(
                        objective.line,
                        "SOURCE_LOCATION",
                        f"bridge {objective.objective_id} baseline location is absent from its manifested file: {reference}",
                    )
                )

    delivery = doc.objective_delivery
    non_deferred = [objective for objective in doc.objectives.values() if objective.treatment != "deferred"]
    delivered_ids = {
        objective.objective_id
        for objective in doc.objectives.values()
        if delivery.get(objective.objective_id) is not None and delivery[objective.objective_id].state == "delivered"
    }
    pending_ids = [objective.objective_id for objective in non_deferred if objective.objective_id not in delivered_ids]
    status = doc.metadata.get("status")
    position = doc.current_position
    action = position.get("next_action")
    step_ids = list(doc.teaching_steps)
    current_step = position.get("current_step")
    last_completed = position.get("last_completed_step")
    target_ids = _comma_ids(position.get("target_objectives", ""), r"O\d{3,}") or []
    pending_steps = [
        step_id
        for step_id in step_ids
        if doc.step_delivery.get(step_id) is None
        or doc.step_delivery[step_id].state != "completed"
    ]

    if status == "completed" and pending_ids:
        first = delivery.get(pending_ids[0])
        errors.append(ValidationError(first.line if first is not None else 1, "OBJECTIVE_COVERAGE", "completed lesson still has pending required delivery: " + ", ".join(pending_ids)))
    if action == "complete" and pending_ids:
        errors.append(ValidationError(1, "OBJECTIVE_COVERAGE", "next_action complete is forbidden while objectives remain pending: " + ", ".join(pending_ids)))
    if status == "completed" and pending_steps:
        errors.append(ValidationError(1, "SESSION_DEPTH", "completed lesson still has unfinished Teaching Steps: " + ", ".join(pending_steps)))
    if action == "complete" and pending_steps:
        errors.append(ValidationError(1, "SESSION_DEPTH", "next_action complete is forbidden while Teaching Steps remain unfinished: " + ", ".join(pending_steps)))

    if action == "complete":
        expected_last = step_ids[-1] if step_ids else "none"
        if last_completed != expected_last:
            errors.append(ValidationError(1, "OBJECTIVE_COVERAGE", f"completed lesson last_completed_step must be {expected_last}"))
    elif current_step in doc.teaching_steps:
        current_index = step_ids.index(current_step)
        completed_prefix = [
            step_id
            for step_id in step_ids[:current_index]
            if doc.step_delivery.get(step_id) is not None
            and doc.step_delivery[step_id].state == "completed"
        ]
        expected_last = completed_prefix[-1] if completed_prefix else "none"
        if last_completed != expected_last:
            errors.append(ValidationError(1, "SESSION_DEPTH", f"last_completed_step must match the completed prefix before current_step: {expected_last}"))
        incomplete_prior = [
            step_id
            for step_id in step_ids[:current_index]
            if doc.step_delivery.get(step_id) is None
            or doc.step_delivery[step_id].state != "completed"
        ]
        if incomplete_prior:
            errors.append(ValidationError(1, "SESSION_DEPTH", "current_step may not skip unfinished Teaching Steps: " + ", ".join(incomplete_prior)))
        completed_later = [
            step_id
            for step_id in step_ids[current_index + 1 :]
            if doc.step_delivery.get(step_id) is not None
            and doc.step_delivery[step_id].state == "completed"
        ]
        if completed_later:
            errors.append(ValidationError(1, "SESSION_DEPTH", "Teaching Steps after current_step may not already be completed: " + ", ".join(completed_later)))
        current = doc.teaching_steps[current_step]
        current_delivery = doc.step_delivery.get(current_step)
        if action == "teach":
            if current_delivery is not None and current_delivery.state != "pending":
                errors.append(ValidationError(current.line, "SESSION_DEPTH", "teach requires the current Step delivery state pending"))
            if target_ids != current.objective_ids:
                errors.append(ValidationError(current.line, "OBJECTIVE_COVERAGE", f"teach target_objectives must exactly match {current_step} objectives"))
        elif action == "await-answer":
            if current_delivery is not None and current_delivery.state != "delivered":
                errors.append(ValidationError(current.line, "SESSION_DEPTH", "await-answer requires the current Step to be delivered"))
            if target_ids != current.objective_ids:
                errors.append(ValidationError(current.line, "ASSESSMENT_ALIGNMENT", f"await-answer target_objectives must exactly match {current_step} objectives"))
        elif action == "remediate":
            if current_delivery is not None and current_delivery.state != "delivered":
                errors.append(ValidationError(current.line, "SESSION_DEPTH", "remediate requires the current Step to be delivered"))
            evidence_match = re.fullmatch(r"learner-evidence:(E\d{3,})", position.get("basis", ""))
            evidence = doc.evidence.get(evidence_match.group(1)) if evidence_match is not None else None
            if evidence is None or evidence.values.get("verdict") not in {"partial", "misconception", "unconfirmed"}:
                errors.append(ValidationError(current.line, "ASSESSMENT_ALIGNMENT", "remediate basis must reference partial, misconception, or unconfirmed learner evidence"))
            elif not set(_comma_ids(evidence.values.get("concept_ids", ""), r"C\d{2}") or []).intersection(current.concept_ids):
                errors.append(ValidationError(current.line, "ASSESSMENT_ALIGNMENT", "remediate evidence must belong to a current Step concept"))

    if status == "completed":
        uncaptured = [
            evidence.evidence_id
            for evidence in doc.evidence.values()
            if evidence.values.get("verdict") == "confirmed"
            and evidence.values.get("capture_state") != "captured"
        ]
        if uncaptured:
            errors.append(
                ValidationError(
                    1,
                    "EVIDENCE_STATE",
                    "completed lesson has confirmed evidence not captured in the daily cursor: "
                    + ", ".join(uncaptured),
                )
            )
        exit_step = doc.teaching_steps.get(doc.session_plan.get("exit_step", ""))
        exit_kind = doc.session_plan.get("exit_evidence_kind")
        matching_exit_evidence = []
        if exit_step is not None:
            for evidence in doc.evidence.values():
                evidence_concepts = set(_comma_ids(evidence.values.get("concept_ids", ""), r"C\d{2}") or [])
                evidence_objectives = set(_comma_ids(evidence.values.get("objective_ids", ""), r"O\d{3,}") or [])
                if (
                    evidence.values.get("kind") == exit_kind
                    and evidence.values.get("verdict") == "confirmed"
                    and set(exit_step.concept_ids).issubset(evidence_concepts)
                    and set(exit_step.objective_ids).issubset(evidence_objectives)
                ):
                    matching_exit_evidence.append(evidence)
        if not matching_exit_evidence:
            errors.append(ValidationError(1, "SESSION_EXIT_EVIDENCE", "completed lesson requires confirmed learner evidence matching the Session Plan exit Step, concepts, objectives, and evidence kind"))

        incomplete_concepts = [
            concept_id
            for concept_id, row in doc.learning_coverage.items()
            if any(
                objective.concept_id == concept_id and objective.treatment != "deferred"
                for objective in doc.objectives.values()
            )
            and row.today_state != "confirmed"
        ]
        if incomplete_concepts:
            errors.append(
                ValidationError(
                    1,
                    "SESSION_CONCEPT_INCOMPLETE",
                    "completed lesson still has unconfirmed non-deferred concepts: "
                    + ", ".join(incomplete_concepts),
                )
            )

    delivered_concepts = {doc.objectives[objective_id].concept_id for objective_id in delivered_ids if objective_id in doc.objectives}
    for concept_id in delivered_concepts:
        coverage = doc.learning_coverage.get(concept_id)
        if coverage is not None and coverage.today_state == "deferred":
            errors.append(
                ValidationError(
                    coverage.line,
                    "OBJECTIVE_COVERAGE",
                    f"delivered objectives cannot belong to a deferred Session Concept Coverage concept: {concept_id}",
                )
            )


def _validate_session_capture_readiness(
    doc: HandoffDocument, errors: list[ValidationError]
) -> None:
    """Retain the old CLI gate as a capture preflight, not a TIL gate."""

    if doc.metadata.get("status") != "completed":
        errors.append(
            ValidationError(
                1,
                "SESSION_CONCEPT_INCOMPLETE",
                "--capture-ready requires completed status",
            )
        )
    latest = doc.semantic_review
    if latest is None or latest.values.get("verdict") != "pass":
        errors.append(
            ValidationError(
                latest.line if latest else 1,
                "REVIEW_NOT_PASS",
                "session capture requires a current independent lesson-contract pass",
            )
        )
    elif (
        latest.values.get("reviewed_input_manifest_sha256") != doc.computed_manifest_sha256
        or latest.values.get("reviewed_contract_sha256") != doc.computed_contract_sha256
    ):
        errors.append(ValidationError(latest.line, "REVIEW_STALE", "session-capture review hashes are stale"))
    for row in doc.learning_coverage.values():
        if row.today_state == "uncertain":
            errors.append(
                ValidationError(
                    row.line,
                    "SESSION_CONCEPT_INCOMPLETE",
                    f"session capture cannot close uncertain concept {row.concept_id}; teach differently or pause",
                )
            )


def _validate_declared_hashes(doc: HandoffDocument, metadata_lines: dict[str, int], errors: list[ValidationError]) -> None:
    declared_manifest = doc.metadata.get("input_manifest_sha256")
    if HASH_RE.fullmatch(declared_manifest or "") and declared_manifest != doc.computed_manifest_sha256:
        errors.append(ValidationError(metadata_lines.get("input_manifest_sha256", 1), "SOURCE_HASH", f"input manifest hash mismatch: got {doc.computed_manifest_sha256}"))
    declared_contract = doc.metadata.get("contract_sha256")
    if HASH_RE.fullmatch(declared_contract or "") and declared_contract != doc.computed_contract_sha256:
        errors.append(ValidationError(metadata_lines.get("contract_sha256", 1), "CONTRACT_HASH", f"contract hash mismatch: got {doc.computed_contract_sha256}"))


def _validate_curriculum_source_relations(
    doc: HandoffDocument,
    curriculum_text: str,
    errors: list[ValidationError],
) -> None:
    snapshot = curriculum_snapshot_from_text(curriculum_text)
    manifest_by_path = {entry.path: entry for entry in doc.manifest}
    expected_external: dict[tuple[str, str], list[str]] = {}
    for target_id, treatment in doc.curriculum_treatments.items():
        if treatment.lesson_treatment == "defer-track":
            continue
        source_core = [
            (objective_id, path, manifest_by_path.get(path))
            for objective_id in treatment.objective_ids
            if (objective := doc.objectives.get(objective_id)) is not None
            and objective.requirement == "source-core"
            if (path := _location_path(objective.source_location)) is not None
        ]
        if not source_core:
            continue
        target = snapshot.targets.get(target_id)
        if target is None:
            continue
        unrelated_local = sorted(
            {
                path
                for _, path, entry in source_core
                if entry is not None
                and entry.role == "primary"
                and path not in target.direct_source_paths
            }
        )
        if unrelated_local:
            errors.append(
                ValidationError(
                    treatment.line,
                    "CURRICULUM_SOURCE_RELATION",
                    f"Curriculum Treatment {target_id} has local source-core primaries "
                    "without a primary or supporting relation: "
                    + ", ".join(unrelated_local),
                )
            )
        for objective_id, _, entry in source_core:
            if entry is not None and entry.role == "external-primary":
                expected_external.setdefault((target_id, entry.item_id), []).append(
                    objective_id
                )

    for key, objective_ids in expected_external.items():
        relation = doc.external_relations.get(key)
        if relation is None:
            errors.append(
                ValidationError(
                    doc.curriculum_treatments[key[0]].line,
                    "EXTERNAL_SOURCE_RELATION",
                    f"missing external target relation for {key[0]} / {key[1]}",
                )
            )
        elif relation.objective_ids != objective_ids:
            errors.append(
                ValidationError(
                    relation.line,
                    "EXTERNAL_SOURCE_RELATION",
                    f"{key[0]} / {key[1]} Objective IDs must exactly match its linked source-core objectives",
                )
            )
    for key, relation in doc.external_relations.items():
        if key not in expected_external:
            errors.append(
                ValidationError(
                    relation.line,
                    "EXTERNAL_SOURCE_RELATION",
                    f"external relation is not used by its Curriculum Treatment: {key[0]} / {key[1]}",
                )
            )


def _validate_course_freshness(
    doc: HandoffDocument,
    errors: list[ValidationError],
    warnings: list[ValidationWarning],
) -> None:
    curriculum = next(
        (entry for entry in doc.manifest if entry.role == "curriculum" and entry.path == "CURRICULUM.md"),
        None,
    )
    if curriculum is None:
        return
    curriculum_path = doc.repo_root / curriculum.path
    try:
        curriculum_text = curriculum_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        curriculum_text = None
    if curriculum_text is not None:
        _validate_curriculum_source_relations(doc, curriculum_text, errors)
    for entry in (item for item in doc.manifest if item.role == "course-index"):
        index_path = doc.repo_root / entry.path
        index_parts = PurePosixPath(entry.path).parts
        selected_paths = {
            item.path
            for item in doc.manifest
            if item.role == "primary"
            and len(PurePosixPath(item.path).parts) >= 4
            and PurePosixPath(item.path).parts[:3] == index_parts[:3]
        }
        freshness = validate_lesson_slice_freshness(
            curriculum_path,
            index_path,
            selected_paths,
            repo_root=doc.repo_root,
        )
        for finding in freshness.errors:
            errors.append(
                ValidationError(
                    entry.line,
                    "CURRICULUM_FRESHNESS",
                    f"{finding.code}: {finding.path}:{finding.line}: {finding.message}",
                )
            )
        for finding in freshness.warnings:
            warnings.append(
                ValidationWarning(
                    entry.line,
                    "CURRICULUM_FRESHNESS",
                    f"{finding.code}: {finding.path}:{finding.line}: {finding.message}",
                )
            )


def validate_handoff(
    path: Path | str,
    *,
    repo_root: Path | str | None = None,
    ready: bool = False,
    capture_ready: bool = False,
    check_draft: bool = True,
) -> ValidationReport:
    handoff_path = Path(path)
    root = Path(repo_root).resolve() if repo_root is not None else _repo_root_from_script()
    errors: list[ValidationError] = []
    warnings: list[ValidationWarning] = []
    if not handoff_path.is_absolute():
        handoff_path = root / handoff_path
    try:
        resolved = handoff_path.resolve(strict=False)
        resolved.relative_to(root)
    except (OSError, ValueError):
        return ValidationReport(
            handoff_path,
            ready,
            capture_ready,
            [ValidationError(1, "PATH", "handoff path escapes the repository")],
            None,
        )
    if not handoff_path.exists() or not handoff_path.is_file():
        return ValidationReport(
            handoff_path,
            ready,
            capture_ready,
            [ValidationError(1, "SOURCE_MISSING", "handoff file does not exist")],
            None,
        )
    try:
        text = _normalize_newlines(handoff_path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return ValidationReport(
            handoff_path,
            ready,
            capture_ready,
            [ValidationError(1, "SCHEMA", "handoff is not valid UTF-8")],
            None,
        )

    doc = HandoffDocument(path=handoff_path, repo_root=root, text=text)
    if not text.startswith("# Active Lesson Handoff\n"):
        errors.append(ValidationError(1, "SCHEMA", "handoff must start with '# Active Lesson Handoff'"))
    if "Codex-generated temporary operational cache" not in text[:500]:
        errors.append(ValidationError(1, "SCHEMA", "handoff must include the temporary operational-cache banner"))
    sections = _section_ranges(text, errors)
    metadata_lines = _parse_metadata(doc, sections.get("Metadata"), errors)
    _parse_manifest(doc, sections.get("Input Manifest"), errors)
    _parse_contract(doc, errors)
    _validate_declared_hashes(doc, metadata_lines, errors)
    _parse_semantic_review(doc, sections.get("Semantic Review"), errors)
    _parse_current_position(doc, sections.get("Current Position"), errors)
    _parse_objective_delivery(doc, sections.get("Objective Delivery"), errors)
    _parse_step_delivery(doc, sections.get("Teaching Step Delivery"), errors)
    _parse_evidence(doc, sections.get("Learner Evidence"), errors)
    _parse_session_concept_coverage(doc, sections.get("Session Concept Coverage"), errors)
    _validate_objective_state(doc, errors)
    del check_draft  # v9 stores learner evidence in the daily cursor, not til/today.md

    if ready:
        _validate_course_freshness(doc, errors, warnings)
        _validate_external_receipts(doc, errors)
        status = doc.metadata.get("status")
        if status not in {"active", "paused"}:
            errors.append(ValidationError(metadata_lines.get("status", 1), "REVIEW_NOT_PASS", "--ready requires active or paused status"))
        latest = doc.semantic_review
        if latest is None or latest.values.get("verdict") != "pass":
            errors.append(ValidationError(latest.line if latest else 1, "REVIEW_NOT_PASS", "--ready requires a latest pass verdict"))
        elif (
            latest.values.get("reviewed_input_manifest_sha256") != doc.computed_manifest_sha256
            or latest.values.get("reviewed_contract_sha256") != doc.computed_contract_sha256
        ):
            errors.append(ValidationError(latest.line, "REVIEW_STALE", "--ready review hashes are stale"))

    if capture_ready:
        _validate_course_freshness(doc, errors, warnings)
        _validate_external_receipts(doc, errors)
        _validate_session_capture_readiness(doc, errors)

    deduplicated: list[ValidationError] = []
    seen: set[tuple[int, str, str]] = set()
    for error in errors:
        key = (error.line, error.code, error.message)
        if key not in seen:
            seen.add(key)
            deduplicated.append(error)
    deduplicated_warnings: list[ValidationWarning] = []
    seen_warnings: set[tuple[int, str, str]] = set()
    for warning in warnings:
        key = (warning.line, warning.code, warning.message)
        if key not in seen_warnings:
            seen_warnings.add(key)
            deduplicated_warnings.append(warning)
    return ValidationReport(
        handoff_path,
        ready,
        capture_ready,
        deduplicated,
        doc,
        deduplicated_warnings,
    )


class _ContractArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.exit(2, f"ERROR <cli>:1 [SCHEMA] {message}\n")


def _build_parser() -> argparse.ArgumentParser:
    parser = _ContractArgumentParser(description=__doc__)
    parser.add_argument("handoff", type=Path, help="repository-relative active handoff Markdown path")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--ready", action="store_true", help="also require a current pass and teachable status")
    mode.add_argument(
        "--capture-ready",
        action="store_true",
        help="also require a completed, fully confirmed session ready for cursor capture",
    )
    parser.add_argument("--json", action="store_true", dest="as_json", help="emit machine-readable JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        report = validate_handoff(args.handoff, ready=args.ready, capture_ready=args.capture_ready)
    except Exception as exc:  # pragma: no cover - last-resort CLI boundary
        if args.as_json:
            print(
                json.dumps(
                    {
                        "ok": False,
                        "path": args.handoff.as_posix(),
                        "ready": False,
                        "capture_ready": False,
                        "workflow_action": "PREPARE_CONTRACT",
                        "computed": {},
                        "errors": [{"line": 1, "code": "SCHEMA", "message": f"internal error: {exc}"}],
                        "warnings": [],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
        else:
            print(f"ERROR {args.handoff.as_posix()}:1 [SCHEMA] internal error: {exc}", file=sys.stderr)
        return 2
    if args.as_json:
        print(json.dumps(report.as_json(), ensure_ascii=False, indent=2, sort_keys=True))
    else:
        for warning in report.warnings:
            print(warning.rendered(report.path), file=sys.stderr)
        if report.ok:
            result_mode = "ready" if args.ready else "capture-ready" if args.capture_ready else "valid"
            print(f"OK {report.path.as_posix()} [{result_mode}]")
        else:
            for error in report.errors:
                print(error.rendered(report.path), file=sys.stderr)
    return report.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
