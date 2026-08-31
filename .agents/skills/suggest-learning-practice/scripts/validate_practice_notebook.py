#!/usr/bin/env python3
"""Validate guided-fading Notebook practice backed by metadata v3, v4, or v5."""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit


ACTIONS = {"implement", "test", "debug", "interpret", "design"}
REQUIREMENT_KINDS = {"source-given", "practice-given", "derive"}
REQUIREMENT_OWNERS = {"provided", "learner"}
TARGET_KINDS = {"code", "debug", "prediction", "design", "interpretation"}
SCAFFOLD_STAGES = {"guided", "partial", "independent"}
SOURCE_KINDS = {
    "course-index",
    "lesson",
    "instructor-practice",
    "reference",
    "external-reference",
}
PRACTICE_MODES = {"NOTEBOOK", "BENCHMARK", "DATASET_PROJECT"}
PRACTICE_LAYERS = {"PRE_LAB", "MODULE_ASSIGNMENT", "PHASE_CAPSTONE"}
PRACTICE_LIFECYCLES = {"fresh", "preserved_attempt"}
IMPLEMENTATION_DEPTHS = {
    "I1_MECHANISM": 1,
    "I2_COMPONENT": 2,
    "I3_WORKFLOW": 3,
    "I4_EXPERIMENT": 4,
    "I5_RESEARCH": 5,
}
MILESTONE_ID_RE = re.compile(r"(?:MA|PC)-[A-Z0-9][A-Z0-9-]{2,95}\Z")
LEARNING_INPUT_ID_RE = re.compile(r"L\d{3}\Z")
PRIOR_PRACTICE_ID_RE = re.compile(r"P\d{3}\Z")
COMMIT_RE = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")
CELL_ROLES = {
    "intro",
    "setup",
    "brief",
    "implementation",
    "fixture",
    "check",
    "reflection",
}
EXERCISE_ROLES = ("brief", "implementation", "fixture", "check", "reflection")
ROLE_CELL_TYPES = {
    "intro": "markdown",
    "setup": "code",
    "brief": "markdown",
    "implementation": "code",
    "fixture": "code",
    "check": "code",
    "reflection": "markdown",
}
TARGET_ROLES = {"implementation", "reflection"}
CHECK_CATEGORIES = {"normal", "edge", "failure"}
OPTIONAL_REFLECTION_RE = re.compile(
    r"(?:실습 완료 조건이 아닙니다|not required for (?:exercise )?completion)",
    re.IGNORECASE,
)
TIL_RE = re.compile(r"til/\d{4}/\d{2}/\d{4}-\d{2}-\d{2}\.md\Z")
CYCLE_ID_RE = re.compile(r"[a-z0-9][a-z0-9-]{2,95}\Z")
EXERCISE_ID_RE = re.compile(r"E\d{2}\Z")
REQUIREMENT_ID_RE = re.compile(r"C-(E\d{2})-(\d{2})\Z")
TARGET_ID_RE = re.compile(r"T-(E\d{2})-(\d{2})\Z")
CELL_ID_RE = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
SOURCE_ID_RE = re.compile(r"S\d{3}\Z")
CURRICULUM_ID_RE = re.compile(r"(?:CC|TR)-[A-Z]+-\d{2}\Z")
EXTERNAL_CACHE_RE = re.compile(
    r"tmp/active-lesson-sources/([a-z0-9][a-z0-9-]{2,63})/([0-9a-f]{64})\.(?:pdf|html|md|txt)\Z"
)
PRESERVED_EXTERNAL_CACHE_RE = re.compile(
    r"tmp/lesson-attempts/([a-z0-9][a-z0-9-]{2,95})/source-cache/([0-9a-f]{64})\.(?:pdf|html|md|txt)\Z"
)
LEAK_PATTERNS = (
    (re.compile(r"\bC-E\d{2}-\d{2}\b"), "internal Requirement ID"),
    (re.compile(r"\bT-E\d{2}-\d{2}\b"), "internal Learner Target ID"),
    (re.compile(r"\bContract ID\b", re.IGNORECASE), "Contract ID label"),
    (re.compile(r"\bLearner Target\b", re.IGNORECASE), "Learner Target label"),
    (re.compile(r"\bsource-given\b"), "source-given audit kind"),
    (re.compile(r"\bpractice-given\b"), "practice-given audit kind"),
    (re.compile(r"\bguided-fading\b"), "scaffold audit mode"),
    (re.compile(r"^#{1,6}\s+Practice Coverage Map\s*$", re.MULTILINE), "coverage audit heading"),
    (re.compile(r"^\s*#\s*contract\s*:", re.MULTILINE | re.IGNORECASE), "contract trace marker"),
    (re.compile(r"^\s*#\s*provided-fixture\s*:", re.MULTILINE | re.IGNORECASE), "fixture role marker"),
    (re.compile(r"^\s*#\s*test-check\s*:", re.MULTILINE | re.IGNORECASE), "check role marker"),
    (re.compile(r"^\s*#\s*setup-check\s*:", re.MULTILINE | re.IGNORECASE), "setup role marker"),
    (re.compile(r"^\s*#\s*TODO\s*:\s*E\d{2}\b", re.MULTILINE), "exercise audit marker"),
    (re.compile(r"^#{1,6}\s+실제 사용 맥락\s*$", re.MULTILINE), "authoring-rubric heading"),
    (re.compile(r"^#{1,6}\s+작은 유사 사례와 계약\s*$", re.MULTILINE), "authoring-rubric heading"),
    (re.compile(r"^#{1,6}\s+학습자가 구현·판단할 것\s*$", re.MULTILINE), "authoring-rubric heading"),
)


@dataclass(frozen=True)
class NotebookIssue:
    line: int
    code: str
    message: str


@dataclass(frozen=True)
class NotebookValidation:
    issues: list[NotebookIssue]
    source_links: set[str]
    setup_cells: list[tuple[int, str]]
    warnings: list[NotebookIssue] = field(default_factory=list)


@dataclass(frozen=True)
class Observable:
    ordinal: int
    kind: str
    fingerprint: str
    direct_members: frozenset[tuple[str, str]]


def _cell_text(cell: dict[str, object]) -> str:
    source = cell.get("source", [])
    if isinstance(source, str):
        return source
    if isinstance(source, list) and all(isinstance(item, str) for item in source):
        return "".join(source)
    return ""


def _cell_audit(cell: dict[str, object]) -> dict[str, object] | None:
    metadata = cell.get("metadata")
    if not isinstance(metadata, dict):
        return None
    lab = metadata.get("llm_research_lab")
    if not isinstance(lab, dict):
        return None
    practice = lab.get("practice")
    return practice if isinstance(practice, dict) else None


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_hash(value: object) -> str:
    encoded = (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


CAPTURED_SESSION_FIELDS = (
    "schema_version",
    "cycle_id",
    "lesson_id",
    "primary_target",
    "bridge_target",
    "handoff_sha256",
    "concepts",
    "learner_evidence",
    "learner_evidence_sha256",
    "source_provenance",
    "projection_sha256",
)


def captured_session_projection_hash(captured_session: dict[str, object]) -> str:
    """Hash the immutable cursor projection, excluding its self-hash field."""

    projection = {
        key: captured_session.get(key)
        for key in CAPTURED_SESSION_FIELDS
        if key != "projection_sha256"
    }
    return _canonical_hash(projection)


def practice_contract_hash(payload: dict[str, object]) -> str:
    """Hash the reviewed assignment contract without learner-editable bodies.

    Execution state and learner implementation/reflection text can change during
    an attempt.  Briefs, setup, fixtures, checks, topology, and audit metadata
    remain part of the reviewed contract.
    """

    projection = copy.deepcopy(payload)
    practice = None
    metadata = projection.get("metadata")
    if isinstance(metadata, dict):
        lab = metadata.get("llm_research_lab")
        if isinstance(lab, dict):
            practice = lab.get("practice")
            if isinstance(practice, dict):
                practice["creation_reviews"] = []
    targets_by_cell: dict[str, list[dict[str, object]]] = {}
    if isinstance(practice, dict):
        raw_targets = practice.get("learner_targets")
        if isinstance(raw_targets, list):
            for target in raw_targets:
                if not isinstance(target, dict):
                    continue
                cell_id = target.get("cell_id")
                if isinstance(cell_id, str):
                    targets_by_cell.setdefault(cell_id, []).append(target)
    cells = projection.get("cells")
    if isinstance(cells, list):
        for cell in cells:
            if not isinstance(cell, dict):
                continue
            if cell.get("cell_type") == "code":
                cell["execution_count"] = None
                cell["outputs"] = []
            audit = _cell_audit(cell)
            role = audit.get("role") if audit is not None else None
            cell_id = cell.get("id")
            target_group = (
                targets_by_cell.get(cell_id, [])
                if isinstance(cell_id, str)
                else []
            )
            source_text = _cell_text(cell)
            if role == "implementation" and target_group:
                cell["source"] = [
                    _normalize_implementation_cell_for_contract(
                        source_text,
                        target_group,
                    )
                ]
            elif role == "reflection" and target_group:
                cell["source"] = [
                    _normalize_reflection_cell_for_contract(
                        source_text,
                        target_group,
                    )
                ]
    return _canonical_hash(projection)


def _milestone_definition_hash(repo: Path, milestone_id: str) -> str | None:
    curriculum = repo / "CURRICULUM.md"
    if not curriculum.is_file():
        return None
    try:
        lines = curriculum.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    matches = [
        re.sub(r"\s+", " ", line.strip())
        for line in lines
        if re.match(rf"^\|\s*{re.escape(milestone_id)}\s*\|", line)
    ]
    if len(matches) != 1:
        return None
    return hashlib.sha256((matches[0] + "\n").encode("utf-8")).hexdigest()


def _validate_learning_input(
    issues: list[NotebookIssue],
    warnings: list[NotebookIssue],
    *,
    practice: dict[str, object],
    repo: Path,
    learner_state: bool,
    completion_ready: bool,
) -> tuple[str | None, set[str], set[str]]:
    """Validate the v4 lesson-session/finalized-til union."""

    raw = practice.get("learning_input")
    if not isinstance(raw, dict):
        issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", "schema v4 requires learning_input"))
        return None, set(), set()
    kind = raw.get("kind")
    if kind == "finalized-til":
        til_path = _validate_hash_record(issues, record=raw, repo=repo, label="learning_input")
        if til_path is not None and TIL_RE.fullmatch(til_path) is None:
            issues.append(NotebookIssue(1, "TIL_REPAIR_REQUIRED", "finalized-til input must name one dated TIL"))
        return kind, set(), set()
    if kind != "lesson-session":
        issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", "learning_input.kind must be lesson-session or finalized-til"))
        return None, set(), set()

    required_strings = (
        "cycle_id",
        "lesson_id",
        "handoff_path",
        "handoff_sha256",
        "primary_target",
        "concept_sha256",
        "learner_evidence_sha256",
    )
    for key in required_strings:
        if not isinstance(raw.get(key), str) or not str(raw[key]).strip():
            issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", f"lesson-session requires {key}"))
    if not CYCLE_ID_RE.fullmatch(str(raw.get("cycle_id", ""))):
        issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", "lesson-session cycle_id is invalid"))
    if not CURRICULUM_ID_RE.fullmatch(str(raw.get("primary_target", ""))):
        issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", "lesson-session primary_target is invalid"))
    bridge = raw.get("bridge_target")
    if bridge is not None and (
        not isinstance(bridge, str) or CURRICULUM_ID_RE.fullmatch(bridge) is None
    ):
        issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", "lesson-session bridge_target must be null or a Curriculum ID"))
    raw_concepts = raw.get("concept_ids")
    raw_evidence = raw.get("evidence_ids")
    concept_ids = (
        set(raw_concepts)
        if isinstance(raw_concepts, list)
        and raw_concepts
        and len(raw_concepts) == len(set(raw_concepts))
        and all(isinstance(item, str) and re.fullmatch(r"C\d{2}", item) for item in raw_concepts)
        else set()
    )
    evidence_ids = (
        set(raw_evidence)
        if isinstance(raw_evidence, list)
        and raw_evidence
        and len(raw_evidence) == len(set(raw_evidence))
        and all(isinstance(item, str) and re.fullmatch(r"E\d{3}", item) for item in raw_evidence)
        else set()
    )
    if not concept_ids:
        issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", "lesson-session requires unique concept_ids"))
    if not evidence_ids:
        issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", "lesson-session requires unique evidence_ids"))
    for key in ("handoff_sha256", "concept_sha256", "learner_evidence_sha256"):
        if SHA256_RE.fullmatch(str(raw.get(key, ""))) is None:
            issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", f"lesson-session {key} must be SHA-256"))

    handoff_path, path_error = _resolve_repo_file(raw.get("handoff_path"), repo)
    if path_error is not None or handoff_path is None:
        message = f"lesson-session handoff is offline: {raw.get('handoff_path')}"
        if learner_state and not completion_ready:
            warnings.append(NotebookIssue(1, "SESSION_SOURCE_OFFLINE", message))
        else:
            issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", message))
        return kind, concept_ids, evidence_ids
    if _sha256(handoff_path) != raw.get("handoff_sha256"):
        issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", "lesson-session handoff hash drift"))
        return kind, concept_ids, evidence_ids

    coach_scripts = repo / ".agents/skills/coach-llm-research-study/scripts"
    if str(coach_scripts) not in sys.path:
        sys.path.insert(0, str(coach_scripts))
    try:
        from validate_lesson_handoff import validate_handoff  # noqa: PLC0415

        report = validate_handoff(
            handoff_path,
            repo_root=repo,
            capture_ready=True,
        )
    except Exception as error:  # pragma: no cover - defensive import boundary
        issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", f"cannot validate lesson handoff: {error}"))
        return kind, concept_ids, evidence_ids
    if not report.ok or report.document is None:
        issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", "lesson-session handoff is not a valid completed v9/v10 session"))
        return kind, concept_ids, evidence_ids
    doc = report.document
    decision = doc.target_decision
    mismatches: list[str] = []
    expected_bridge = None if decision is None or decision.bridge_target == "none" else decision.bridge_target
    if doc.metadata.get("schema_version") not in {"9", "10"} or doc.metadata.get("status") != "completed":
        mismatches.append("schema/status")
    if doc.metadata.get("cycle_id") != raw.get("cycle_id"):
        mismatches.append("cycle_id")
    if doc.metadata.get("lesson_id") != raw.get("lesson_id"):
        mismatches.append("lesson_id")
    if decision is None or decision.primary_target != raw.get("primary_target"):
        mismatches.append("primary_target")
    if expected_bridge != bridge:
        mismatches.append("bridge_target")
    confirmed_concepts = [
        concept_id
        for concept_id, coverage in doc.learning_coverage.items()
        if coverage.today_state == "confirmed"
    ]
    confirmed_evidence = [
        {
            "evidence_id": item.evidence_id,
            "concept_ids": [value.strip() for value in item.values["concept_ids"].split(",")],
            "objective_ids": [value.strip() for value in item.values["objective_ids"].split(",")],
            "kind": item.values["kind"],
            "content": item.content,
            "content_sha256": item.values["content_sha256"],
            "captured_at": item.values["captured_at"],
        }
        for item in doc.evidence.values()
        if item.values.get("verdict") == "confirmed"
    ]
    concept_projection = [
        {
            "concept_id": concept_id,
            "objective_ids": [
                objective.objective_id
                for objective in doc.objectives.values()
                if objective.concept_id == concept_id and objective.treatment != "deferred"
            ],
            "evidence_ids": list(doc.learning_coverage[concept_id].evidence_ids),
        }
        for concept_id in confirmed_concepts
    ]
    if list(raw_concepts or []) != confirmed_concepts:
        mismatches.append("concept_ids")
    if list(raw_evidence or []) != [item["evidence_id"] for item in confirmed_evidence]:
        mismatches.append("evidence_ids")
    if raw.get("concept_sha256") != _canonical_hash(concept_projection):
        mismatches.append("concept_sha256")
    if raw.get("learner_evidence_sha256") != _canonical_hash(confirmed_evidence):
        mismatches.append("learner_evidence_sha256")
    if mismatches:
        issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", "lesson-session identity differs: " + ", ".join(mismatches)))
    return kind, concept_ids, evidence_ids


def _curriculum_target_ids(repo: Path) -> set[str]:
    curriculum = repo / "CURRICULUM.md"
    if not curriculum.is_file():
        return set()
    try:
        text = curriculum.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return set()
    return set(re.findall(r"^\|\s*((?:CC|TR)-[A-Z]+-\d{2})\s*\|", text, re.MULTILINE))


def _validate_learning_inputs_v5(
    issues: list[NotebookIssue],
    warnings: list[NotebookIssue],
    *,
    practice: dict[str, object],
    repo: Path,
    learner_state: bool,
    completion_ready: bool,
) -> tuple[
    set[str],
    set[str],
    set[str],
    set[str],
    set[str],
    dict[tuple[str, str], set[str]],
    set[int],
]:
    """Validate namespaced v5 inputs against immutable cursor projections."""

    raw_inputs = practice.get("learning_inputs")
    if not isinstance(raw_inputs, list) or not raw_inputs:
        issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", "schema v5 requires non-empty learning_inputs"))
        return set(), set(), set(), set(), set(), {}, set()
    cursor_path = repo / "tmp/active-learning-flow.json"
    cursor: dict[str, object] | None = None
    if cursor_path.is_file():
        try:
            loaded = json.loads(cursor_path.read_text(encoding="utf-8"))
            cursor = loaded if isinstance(loaded, dict) else None
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            cursor = None
    cursor_is_v2 = isinstance(cursor, dict) and cursor.get("schema_version") == 2
    cycles = {
        item.get("cycle_id"): item
        for item in (cursor.get("cycles", []) if cursor_is_v2 else [])
        if isinstance(item, dict) and isinstance(item.get("cycle_id"), str)
    }
    known_targets = _curriculum_target_ids(repo)
    input_ids: list[str] = []
    concept_refs: set[str] = set()
    evidence_refs: set[str] = set()
    input_targets: set[str] = set()
    input_kinds: set[str] = set()
    input_paths: set[str] = set()
    captured_source_cycles: dict[tuple[str, str], set[str]] = {}
    captured_schema_versions: set[int] = set()
    primary_count = 0

    for index, item in enumerate(raw_inputs, start=1):
        if not isinstance(item, dict):
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"learning_inputs[{index - 1}] must be an object"))
            continue
        input_id = item.get("id")
        input_ids.append(str(input_id))
        if input_id != f"L{index:03d}" or LEARNING_INPUT_ID_RE.fullmatch(str(input_id)) is None:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", "learning input IDs must be contiguous L001, L002, ..."))
            continue
        role = item.get("role")
        if role not in {"primary", "supporting"}:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{input_id} role must be primary or supporting"))
        elif role == "primary":
            primary_count += 1
        kind = item.get("kind")
        if kind not in {"captured-cycle", "finalized-til"}:
            issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", f"{input_id} has invalid input kind"))
            continue
        input_kinds.add(kind)
        if kind == "finalized-til":
            til_path = _validate_hash_record(issues, record=item, repo=repo, label=input_id)
            if til_path is not None and TIL_RE.fullmatch(til_path) is None:
                issues.append(NotebookIssue(1, "TIL_REPAIR_REQUIRED", f"{input_id} must name one dated TIL"))
            elif til_path is not None:
                input_paths.add(til_path)
            continue

        raw_concepts = item.get("concept_ids")
        raw_evidence = item.get("evidence_ids")
        declared_concepts = raw_concepts if isinstance(raw_concepts, list) else []
        declared_evidence = raw_evidence if isinstance(raw_evidence, list) else []
        if (
            not declared_concepts
            or not all(isinstance(value, str) and re.fullmatch(r"C\d{2}", value) for value in declared_concepts)
            or len(declared_concepts) != len(set(declared_concepts))
        ):
            issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", f"{input_id} needs unique concept_ids"))
        if (
            not declared_evidence
            or not all(isinstance(value, str) and re.fullmatch(r"E\d{3}", value) for value in declared_evidence)
            or len(declared_evidence) != len(set(declared_evidence))
        ):
            issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", f"{input_id} needs unique evidence_ids"))
        concept_refs.update(f"{input_id}:{value}" for value in declared_concepts if isinstance(value, str))
        evidence_refs.update(f"{input_id}:{value}" for value in declared_evidence if isinstance(value, str))

        cycle_id = item.get("cycle_id")
        projection_hash = item.get("captured_session_sha256")
        if not isinstance(cycle_id, str) or CYCLE_ID_RE.fullmatch(cycle_id) is None:
            issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", f"{input_id} has invalid cycle_id"))
            continue
        if SHA256_RE.fullmatch(str(projection_hash or "")) is None:
            issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", f"{input_id} needs captured_session_sha256"))
        primary_target = item.get("primary_target")
        bridge_target = item.get("bridge_target")
        for target in (primary_target, bridge_target):
            if target is None:
                continue
            if not isinstance(target, str) or CURRICULUM_ID_RE.fullmatch(target) is None:
                issues.append(NotebookIssue(1, "TARGET_RELATION", f"{input_id} has invalid target ID"))
            else:
                input_targets.add(target)
                if known_targets and target not in known_targets:
                    issues.append(NotebookIssue(1, "TARGET_RELATION", f"{input_id} target no longer exists in CURRICULUM.md: {target}"))

        cycle = cycles.get(cycle_id)
        if cycle is None:
            message = (
                f"captured cycle is offline in cursor schema v2: {cycle_id}"
                if cursor_is_v2
                else "captured-cycle input requires tmp/active-learning-flow.json schema v2"
            )
            if learner_state and not completion_ready:
                warnings.append(NotebookIssue(1, "SESSION_SOURCE_OFFLINE", message))
            else:
                issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", message))
            continue
        projection = cycle.get("captured_session")
        if not isinstance(projection, dict):
            issues.append(
                NotebookIssue(
                    1,
                    "SESSION_REPAIR_REQUIRED",
                    f"{input_id} cycle has no immutable captured_session",
                )
            )
            continue
        if set(projection) != set(CAPTURED_SESSION_FIELDS):
            issues.append(
                NotebookIssue(
                    1,
                    "SESSION_REPAIR_REQUIRED",
                    f"{input_id} captured_session fields differ from projection schema",
                )
            )
        if projection.get("schema_version") not in {9, 10}:
            issues.append(
                NotebookIssue(
                    1,
                    "SESSION_REPAIR_REQUIRED",
                    f"{input_id} captured_session schema_version must be 9 or 10",
                )
            )
        stored_projection_hash = projection.get("projection_sha256")
        computed_projection_hash = captured_session_projection_hash(projection)
        if (
            SHA256_RE.fullmatch(str(stored_projection_hash or "")) is None
            or stored_projection_hash != computed_projection_hash
        ):
            issues.append(
                NotebookIssue(
                    1,
                    "SESSION_REPAIR_REQUIRED",
                    f"{input_id} captured_session self-hash is invalid",
                )
            )
        learner_evidence = projection.get("learner_evidence")
        if (
            not isinstance(learner_evidence, list)
            or projection.get("learner_evidence_sha256")
            != _canonical_hash(learner_evidence)
        ):
            issues.append(
                NotebookIssue(
                    1,
                    "SESSION_REPAIR_REQUIRED",
                    f"{input_id} captured_session learner-evidence hash is invalid",
                )
            )
        source_provenance = projection.get("source_provenance")
        if not isinstance(source_provenance, list):
            issues.append(
                NotebookIssue(
                    1,
                    "SESSION_REPAIR_REQUIRED",
                    f"{input_id} captured_session source_provenance must be a list",
                )
            )
        else:
            for source in source_provenance:
                if not isinstance(source, dict):
                    issues.append(
                        NotebookIssue(
                            1,
                            "SESSION_REPAIR_REQUIRED",
                            f"{input_id} captured source provenance must contain objects",
                        )
                    )
                    continue
                path = source.get("path")
                digest = source.get("sha256")
                if isinstance(path, str) and SHA256_RE.fullmatch(str(digest or "")):
                    captured_source_cycles.setdefault(
                        (path, str(digest)), set()
                    ).add(cycle_id)
                else:
                    issues.append(
                        NotebookIssue(
                            1,
                            "SESSION_REPAIR_REQUIRED",
                            f"{input_id} captured source provenance needs path and sha256",
                        )
                    )
        projection_concepts = projection.get("concepts")
        projection_evidence = projection.get("learner_evidence")
        observed_concepts = [
            value.get("concept_id")
            for value in (projection_concepts if isinstance(projection_concepts, list) else [])
            if isinstance(value, dict) and isinstance(value.get("concept_id"), str)
        ]
        observed_evidence = [
            value.get("evidence_id")
            for value in (projection_evidence if isinstance(projection_evidence, list) else [])
            if isinstance(value, dict) and isinstance(value.get("evidence_id"), str)
        ]
        if isinstance(projection.get("schema_version"), int):
            captured_schema_versions.add(int(projection["schema_version"]))
        mismatches: list[str] = []
        if cycle_id != projection.get("cycle_id"):
            mismatches.append("cycle_id")
        if item.get("lesson_id") != projection.get("lesson_id"):
            mismatches.append("lesson_id")
        if primary_target != projection.get("primary_target"):
            mismatches.append("primary_target")
        if bridge_target != projection.get("bridge_target"):
            mismatches.append("bridge_target")
        if declared_concepts != observed_concepts:
            mismatches.append("concept_ids")
        if declared_evidence != observed_evidence:
            mismatches.append("evidence_ids")
        if projection_hash != stored_projection_hash:
            mismatches.append("captured_session_sha256")
        if mismatches:
            issues.append(
                NotebookIssue(
                    1,
                    "SESSION_REPAIR_REQUIRED",
                    f"{input_id} captured-cycle projection differs: {', '.join(mismatches)}",
                )
            )
    if len(input_ids) != len(set(input_ids)):
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "learning input IDs must be unique"))
    if primary_count != 1:
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "schema v5 requires exactly one primary learning input"))
    if len(input_kinds) > 1:
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "schema v5 may not mix captured-cycle and finalized-til inputs"))
    captured_input_count = sum(
        isinstance(item, dict) and item.get("kind") == "captured-cycle"
        for item in raw_inputs
    )
    if (
        practice.get("lifecycle") == "preserved_attempt"
        and captured_input_count
        and (captured_input_count != 1 or len(raw_inputs) != 1)
    ):
        issues.append(
            NotebookIssue(
                1,
                "SESSION_REPAIR_REQUIRED",
                "a preserved_attempt may bind exactly one captured-cycle input",
            )
        )
    return (
        concept_refs,
        evidence_refs,
        input_targets,
        input_kinds,
        input_paths,
        captured_source_cycles,
        captured_schema_versions,
    )


def _resolve_repo_file(raw: object, repo: Path) -> tuple[Path | None, str | None]:
    if not isinstance(raw, str) or not raw or Path(raw).is_absolute():
        return None, "path must be a non-empty repository-relative string"
    candidate = repo / raw
    try:
        resolved = candidate.resolve(strict=False)
        resolved.relative_to(repo)
    except (OSError, ValueError):
        return None, "path escapes the repository"
    if not resolved.is_file():
        return resolved, "path does not name an existing file"
    return resolved, None


def _path_uses_symlink(raw: object, repo: Path) -> bool:
    if not isinstance(raw, str) or not raw or Path(raw).is_absolute():
        return False
    current = repo.resolve()
    for part in Path(raw).parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


def _normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _call_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return None


def _has_assertion_error_raise(nodes: list[ast.stmt]) -> bool:
    for node in nodes:
        if not isinstance(node, ast.Raise) or node.exc is None:
            continue
        target = node.exc.func if isinstance(node.exc, ast.Call) else node.exc
        if _call_name(target) == "AssertionError":
            return True
    return False


def _observable_fingerprint(node: ast.AST) -> str:
    normalized = ast.dump(node, annotate_fields=True, include_attributes=False)
    return "sha256:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _direct_members(node: ast.AST) -> frozenset[tuple[str, str]]:
    """Return direct ``instance.member`` references made by one check.

    A learner-created class may intentionally expose named modules or fields.
    When a public check reaches one of those fields, the exact field name is
    part of the learner-facing interface and cannot remain an implicit test
    detail.
    """

    return frozenset(
        (candidate.value.id, candidate.attr)
        for candidate in ast.walk(node)
        if isinstance(candidate, ast.Attribute) and isinstance(candidate.value, ast.Name)
    )


def _learner_class_api(implementation_code: str, check_code: str) -> tuple[set[str], set[str]]:
    """Find learner-defined classes, their stored attributes, and test instances."""

    try:
        implementation_tree = ast.parse(implementation_code)
        check_tree = ast.parse(check_code)
    except SyntaxError:
        return set(), set()
    classes = {node.name for node in implementation_tree.body if isinstance(node, ast.ClassDef)}
    attributes = {
        target.attr
        for node in ast.walk(implementation_tree)
        for target in (
            list(node.targets) if isinstance(node, ast.Assign) else [node.target] if isinstance(node, ast.AnnAssign) else []
        )
        if isinstance(target, ast.Attribute)
        and isinstance(target.value, ast.Name)
        and target.value.id == "self"
    }
    instances: set[str] = set()
    for node in ast.walk(check_tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)) or not isinstance(node.value, ast.Call):
            continue
        call_name = _call_name(node.value.func)
        if call_name not in classes:
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        instances.update(target.id for target in targets if isinstance(target, ast.Name))
    return attributes, instances


def collect_observables(code: str) -> tuple[list[Observable], SyntaxError | None]:
    """Return testing calls and expected-exception blocks in source order."""
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return [], exc
    found: list[tuple[int, int, str, ast.AST]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = _call_name(node.func) or ""
            if name.startswith(("np.testing.", "torch.testing.")):
                found.append((node.lineno, node.col_offset, "assertion", node))
        elif isinstance(node, ast.Try) and node.handlers and _has_assertion_error_raise(node.orelse):
            found.append((node.lineno, node.col_offset, "exception", node))
    found.sort(key=lambda item: (item[0], item[1], item[2]))
    return [
        Observable(index, kind, _observable_fingerprint(node), _direct_members(node))
        for index, (_, _, kind, node) in enumerate(found, start=1)
    ], None


def _symbol_node(tree: ast.Module, symbol: str) -> ast.AST | None:
    parts = symbol.split(".")
    if len(parts) == 1:
        return next(
            (
                node
                for node in tree.body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                and node.name == parts[0]
            ),
            None,
        )
    if len(parts) == 2:
        owner = next(
            (node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == parts[0]),
            None,
        )
        if owner is None:
            return None
        return next(
            (
                node
                for node in owner.body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == parts[1]
            ),
            None,
        )
    return None


def _replacement_line(prefix: str, marker: str) -> str:
    token = f"<{marker}>"
    if prefix:
        return f"{prefix}# {token}\n"
    return f"# {token}\n"


def _line_prefix(line: str) -> str:
    match = re.match(r"[ \t]*", line)
    return match.group(0) if match is not None else ""


def _replace_line_spans(
    text: str,
    spans: list[tuple[int, int, str]],
) -> str:
    if not spans:
        return text
    lines = text.splitlines(keepends=True)
    for start_line, end_line, replacement in sorted(
        spans,
        key=lambda item: (item[0], item[1]),
        reverse=True,
    ):
        if start_line < 1 or end_line < start_line:
            continue
        start_index = start_line - 1
        end_index = min(end_line, len(lines))
        lines[start_index:end_index] = [replacement]
    return "".join(lines)


def _implementation_contract_spans(
    code: str,
    targets: list[dict[str, object]],
) -> list[tuple[int, int, str]]:
    """Locate only the syntactic statement owned by each learner TODO.

    The target marker is reviewed scaffold, and statements after the TODO may
    assemble or post-process the learner value.  Masking the rest of a symbol
    would therefore hide changes to that reviewed suffix.
    """

    try:
        tree = ast.parse(code)
    except SyntaxError:
        tree = None
    lines = code.splitlines(keepends=True)
    spans: list[tuple[int, int, str]] = []
    for target in targets:
        symbol = target.get("symbol")
        marker = target.get("marker")
        placeholder = target.get("placeholder")
        if not isinstance(symbol, str) or not symbol.strip():
            continue
        if not isinstance(marker, str) or not marker.strip():
            marker = None
        if not isinstance(placeholder, str) or not placeholder.strip():
            placeholder = None
        node = _symbol_node(tree, symbol) if tree is not None else None
        if node is None or not hasattr(node, "lineno") or not hasattr(node, "end_lineno"):
            continue
        node_start = int(node.lineno)
        node_end = int(node.end_lineno)
        symbol_text = "".join(lines[node_start - 1 : node_end])
        marker_line: int | None = None
        if marker and marker in symbol_text:
            marker_line = (
                node_start + symbol_text[: symbol_text.index(marker)].count("\n")
            )
        placeholder_start: int | None = None
        placeholder_end: int | None = None
        if placeholder and placeholder in symbol_text:
            placeholder_start = (
                node_start + symbol_text[: symbol_text.index(placeholder)].count("\n")
            )
            placeholder_end = placeholder_start + placeholder.count("\n")
        statement_nodes = [
            candidate
            for candidate in ast.walk(node)
            if isinstance(candidate, ast.stmt)
            and not isinstance(
                candidate,
                (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef),
            )
            and hasattr(candidate, "lineno")
            and hasattr(candidate, "end_lineno")
        ]
        statement: ast.stmt | None = None
        if marker_line is not None:
            after_marker = [
                candidate
                for candidate in statement_nodes
                if int(candidate.lineno) > marker_line
            ]
            if after_marker:
                statement = min(
                    after_marker,
                    key=lambda candidate: (
                        int(candidate.lineno),
                        int(candidate.col_offset),
                        int(candidate.end_lineno) - int(candidate.lineno),
                    ),
                )
        if statement is None and placeholder_start is not None:
            containing = [
                candidate
                for candidate in statement_nodes
                if int(candidate.lineno) <= placeholder_start
                and int(candidate.end_lineno) >= int(placeholder_end or placeholder_start)
            ]
            if containing:
                statement = min(
                    containing,
                    key=lambda candidate: (
                        int(candidate.end_lineno) - int(candidate.lineno),
                        -int(candidate.col_offset),
                    ),
                )
        if statement is not None:
            start_line = int(statement.lineno)
            end_line = int(statement.end_lineno)
        elif placeholder_start is not None:
            start_line = placeholder_start
            end_line = int(placeholder_end or placeholder_start)
        else:
            continue
        prefix = _line_prefix(lines[start_line - 1]) if start_line - 1 < len(lines) else ""
        spans.append(
            (start_line, end_line, _replacement_line(prefix, "learner-editable-body"))
        )
    return spans


def _normalize_implementation_cell_for_contract(
    code: str,
    targets: list[dict[str, object]],
) -> str:
    return _replace_line_spans(code, _implementation_contract_spans(code, targets))


def _normalize_reflection_cell_for_contract(
    text: str,
    targets: list[dict[str, object]],
) -> str:
    """Mask one learner response line while retaining reviewed postlude text."""

    lines = text.splitlines(keepends=True)
    spans: list[tuple[int, int, str]] = []
    for target in targets:
        marker = target.get("marker")
        placeholder = target.get("placeholder")
        if isinstance(placeholder, str) and placeholder in text:
            line_no = text[: text.index(placeholder)].count("\n") + 1
            prefix = _line_prefix(lines[line_no - 1]) if line_no - 1 < len(lines) else ""
            spans.append(
                (
                    line_no,
                    line_no,
                    _replacement_line(prefix, "learner-editable-reflection"),
                )
            )
            continue
        if isinstance(marker, str) and marker in text:
            marker_line = text[: text.index(marker)].count("\n") + 1
            response_line = next(
                (
                    line_no
                    for line_no in range(marker_line + 1, len(lines) + 1)
                    if lines[line_no - 1].strip()
                ),
                None,
            )
            if response_line is not None:
                prefix = _line_prefix(lines[response_line - 1])
                spans.append(
                    (
                        response_line,
                        response_line,
                        _replacement_line(prefix, "learner-editable-reflection"),
                    )
                )
    return _replace_line_spans(text, spans)


def _is_git_repo(repo: Path) -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )
    return result.returncode == 0


def _git_commit_exists(repo: Path, commit: str) -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", f"{commit}^{{commit}}"],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )
    return result.returncode == 0


def _git_show_file_bytes(repo: Path, commit: str, relative_path: str) -> bytes | None:
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative_path}"],
        cwd=repo,
        capture_output=True,
        check=False,
        timeout=30,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def _git_commit_changed_paths(repo: Path, commit: str) -> list[str] | None:
    result = subprocess.run(
        [
            "git",
            "diff-tree",
            "--root",
            "--no-commit-id",
            "--name-only",
            "-r",
            "-z",
            commit,
        ],
        cwd=repo,
        capture_output=True,
        check=False,
        timeout=30,
    )
    if result.returncode != 0:
        return None
    return [
        item.decode("utf-8", errors="surrogateescape")
        for item in result.stdout.split(b"\0")
        if item
    ]


def _matches_contract_text(claim: object, contract_text: str) -> bool:
    if not isinstance(claim, str):
        return False
    normalized_claim = _normalized(claim)
    normalized_contract = _normalized(contract_text)
    return bool(normalized_contract) and normalized_contract in normalized_claim


def _find_contract_requirements(
    requirements: dict[str, dict[str, object]],
    contract_text: str,
) -> list[tuple[str, dict[str, object]]]:
    return [
        (requirement_id, requirement)
        for requirement_id, requirement in requirements.items()
        if _matches_contract_text(requirement.get("claim"), contract_text)
    ]


def _target_result_links(
    target: dict[str, object],
    declared_results: set[str],
) -> set[str]:
    linked = target.get("result_cell_ids")
    if (
        not isinstance(linked, list)
        or not linked
        or not all(isinstance(cell_id, str) for cell_id in linked)
    ):
        return set()
    linked_set = set(linked)
    if not linked_set.issubset(declared_results):
        return set()
    return linked_set


def _statement_target_is_stateful(statement: ast.stmt) -> bool:
    assignment_targets: list[ast.expr] = []
    if isinstance(statement, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
        if isinstance(statement, ast.Assign):
            assignment_targets.extend(statement.targets)
        else:
            assignment_targets.append(statement.target)
    return any(
        isinstance(node, (ast.Attribute, ast.Subscript))
        for target in assignment_targets
        for node in ast.walk(target)
    )


def _nonempty_return(node: ast.AST) -> bool:
    if not isinstance(node, ast.Return) or node.value is None:
        return False
    if isinstance(node.value, (ast.Dict, ast.List, ast.Set, ast.Tuple)):
        values = (
            node.value.keys
            if isinstance(node.value, ast.Dict)
            else node.value.elts
        )
        return bool(values)
    return not (isinstance(node.value, ast.Constant) and node.value.value is None)


def _stage_target_exposes_semantics(
    stage: str,
    *,
    cell: dict[str, object],
    target: dict[str, object],
) -> bool:
    """Check stage API/data-flow structure without relying on stage keywords."""

    code = _cell_text(cell)
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    symbol = target.get("symbol")
    if not isinstance(symbol, str):
        return False
    symbol_node = _symbol_node(tree, symbol)
    if symbol_node is None:
        return False
    spans = _implementation_contract_spans(code, [target])

    def overlaps_todo(node: ast.AST) -> bool:
        if not hasattr(node, "lineno") or not hasattr(node, "end_lineno"):
            return False
        return any(
            int(node.lineno) <= end_line and int(node.end_lineno) >= start_line
            for start_line, end_line, _ in spans
        )

    outside_nodes = [
        node
        for node in ast.walk(symbol_node)
        if not overlaps_todo(node)
    ]
    todo_statements = [
        node
        for node in ast.walk(symbol_node)
        if isinstance(node, ast.stmt)
        and hasattr(node, "lineno")
        and hasattr(node, "end_lineno")
        and any(
            int(node.lineno) >= start_line and int(node.end_lineno) <= end_line
            for start_line, end_line, _ in spans
        )
    ]

    if stage == "model":
        if isinstance(symbol_node, ast.ClassDef):
            has_component_entry = any(
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name in {"forward", "__call__"}
                for node in symbol_node.body
            )
        else:
            has_component_entry = isinstance(
                symbol_node, (ast.FunctionDef, ast.AsyncFunctionDef)
            )
        has_component_scaffold = any(
            isinstance(node, ast.Call)
            or (
                isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign))
                and _statement_target_is_stateful(node)
            )
            for node in outside_nodes
        )
        return has_component_entry and has_component_scaffold

    if not isinstance(symbol_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return False
    positional_args = [
        argument.arg
        for argument in (
            list(symbol_node.args.posonlyargs) + list(symbol_node.args.args)
        )
        if argument.arg not in {"self", "cls"}
    ]
    if stage == "loss":
        has_computation_scaffold = any(
            isinstance(node, (ast.Call, ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare))
            for node in outside_nodes
        )
        has_result = any(_nonempty_return(node) for node in outside_nodes)
        return len(positional_args) >= 2 and has_computation_scaffold and has_result

    if stage == "train":
        has_control_or_data_flow = any(
            isinstance(node, (ast.Call, ast.For, ast.AsyncFor, ast.While, ast.With))
            for node in outside_nodes
        )
        has_stateful_target = any(
            _statement_target_is_stateful(node) for node in todo_statements
        )
        has_observable_result = any(_nonempty_return(node) for node in outside_nodes)
        return (
            bool(positional_args)
            and has_control_or_data_flow
            and (has_stateful_target or any(isinstance(node, (ast.For, ast.While)) for node in outside_nodes))
            and has_observable_result
        )
    return False


def _validate_hash_record(
    issues: list[NotebookIssue],
    *,
    record: object,
    repo: Path,
    label: str,
) -> str | None:
    if not isinstance(record, dict):
        issues.append(NotebookIssue(1, "SOURCE_AUDIT", f"{label} must be an object"))
        return None
    raw_path = record.get("path")
    if (
        isinstance(raw_path, str)
        and raw_path.startswith("tmp/lesson-attempts/")
        and _path_uses_symlink(raw_path, repo)
    ):
        issues.append(
            NotebookIssue(
                1,
                "SOURCE_AUDIT",
                f"{label} archived path cannot use symbolic links: {raw_path}",
            )
        )
        return raw_path
    resolved, error = _resolve_repo_file(raw_path, repo)
    if error:
        issues.append(NotebookIssue(1, "SOURCE_AUDIT", f"{label} {error}: {raw_path!r}"))
        return raw_path if isinstance(raw_path, str) else None
    expected = record.get("sha256")
    if not isinstance(expected, str) or SHA256_RE.fullmatch(expected) is None:
        issues.append(NotebookIssue(1, "SOURCE_AUDIT", f"{label} needs a lowercase SHA-256"))
    elif resolved is not None and _sha256(resolved) != expected:
        issues.append(NotebookIssue(1, "SOURCE_AUDIT", f"{label} hash does not match: {raw_path}"))
    return raw_path if isinstance(raw_path, str) else None


def _rfc3339(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(
            value[:-1] + "+00:00" if value.endswith("Z") else value
        )
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _validate_external_record(
    issues: list[NotebookIssue],
    warnings: list[NotebookIssue],
    *,
    record: dict[str, object],
    repo: Path,
    label: str,
    strict: bool,
    preserved_source_cycles: dict[tuple[str, str], set[str]],
) -> Path | None:
    required_text = (
        "provider",
        "course",
        "offering_or_edition",
        "artifact",
        "url",
        "final_url",
        "media_type",
        "scope",
        "cache_path",
        "receipt_path",
    )
    for key in required_text:
        if not isinstance(record.get(key), str) or not str(record[key]).strip():
            issues.append(NotebookIssue(1, "EXTERNAL_SOURCE_IDENTITY", f"{label} needs {key}"))
    for key in ("url", "final_url"):
        value = record.get(key)
        if isinstance(value, str):
            parsed = urlsplit(value)
            if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
                issues.append(NotebookIssue(1, "EXTERNAL_SOURCE_IDENTITY", f"{label} {key} must be public HTTPS without credentials"))
    if not _rfc3339(record.get("retrieved_at")):
        issues.append(NotebookIssue(1, "EXTERNAL_SOURCE_IDENTITY", f"{label} retrieved_at must be RFC 3339"))
    if not isinstance(record.get("sha256"), str) or SHA256_RE.fullmatch(str(record["sha256"])) is None:
        issues.append(NotebookIssue(1, "EXTERNAL_SOURCE_IDENTITY", f"{label} sha256 must be lowercase SHA-256"))

    raw_cache_path = record.get("cache_path")
    raw_receipt_path = record.get("receipt_path")
    cache_match = (
        EXTERNAL_CACHE_RE.fullmatch(raw_cache_path)
        if isinstance(raw_cache_path, str)
        else None
    )
    archive_match = (
        PRESERVED_EXTERNAL_CACHE_RE.fullmatch(raw_cache_path)
        if isinstance(raw_cache_path, str)
        else None
    )
    expected_digest = record.get("sha256")
    raw_captured_path = record.get("captured_path")
    raw_captured_receipt_path = record.get("captured_receipt_path")
    captured_match = (
        EXTERNAL_CACHE_RE.fullmatch(raw_captured_path)
        if isinstance(raw_captured_path, str)
        else None
    )
    archive_allowed = (
        archive_match is not None
        and isinstance(expected_digest, str)
        and archive_match.group(1)
        in preserved_source_cycles.get(
            (str(raw_captured_path), expected_digest), set()
        )
    )
    if (
        (cache_match is None or cache_match.group(2) != expected_digest)
        and (not archive_allowed or archive_match.group(2) != expected_digest)
    ):
        issues.append(
            NotebookIssue(
                1,
                "EXTERNAL_SOURCE_IDENTITY",
                f"{label} cache_path must be content-addressed inside one active lesson or the archive owned by that captured source",
            )
        )
    receipt_identity_path = raw_cache_path
    receipt_identity_receipt_path = raw_receipt_path
    if archive_match is not None:
        if captured_match is None or captured_match.group(2) != expected_digest:
            issues.append(
                NotebookIssue(
                    1,
                    "EXTERNAL_SOURCE_IDENTITY",
                    f"{label} captured_path must preserve the immutable active-cache identity",
                )
            )
        expected_captured_receipt_path = (
            f"tmp/active-lesson-sources/{captured_match.group(1)}/{captured_match.group(2)}.receipt.json"
            if captured_match is not None
            else None
        )
        if raw_captured_receipt_path != expected_captured_receipt_path:
            issues.append(
                NotebookIssue(
                    1,
                    "EXTERNAL_SOURCE_IDENTITY",
                    f"{label} captured_receipt_path must match captured_path",
                )
            )
        receipt_identity_path = raw_captured_path
        receipt_identity_receipt_path = raw_captured_receipt_path
    expected_receipt_path = None
    if cache_match is not None:
        expected_receipt_path = (
            f"tmp/active-lesson-sources/{cache_match.group(1)}/{cache_match.group(2)}.receipt.json"
        )
    elif archive_match is not None:
        expected_receipt_path = (
            f"tmp/lesson-attempts/{archive_match.group(1)}/source-cache/"
            f"{archive_match.group(2)}.receipt.json"
        )
    if raw_receipt_path != expected_receipt_path:
        issues.append(
            NotebookIssue(
                1,
                "EXTERNAL_SOURCE_IDENTITY",
                f"{label} receipt_path must match its content-addressed cache path",
            )
        )

    if archive_match is not None and (
        _path_uses_symlink(raw_cache_path, repo)
        or _path_uses_symlink(raw_receipt_path, repo)
    ):
        issues.append(
            NotebookIssue(
                1,
                "EXTERNAL_SOURCE_IDENTITY",
                f"{label} archived cache and receipt cannot use symbolic links",
            )
        )
        return None

    cache_path, cache_error = _resolve_repo_file(raw_cache_path, repo)
    receipt_path, receipt_error = _resolve_repo_file(raw_receipt_path, repo)
    if cache_error or receipt_error or cache_path is None or receipt_path is None:
        issue = NotebookIssue(
            1,
            "EXTERNAL_SOURCE_OFFLINE",
            f"{label} temporary cache is unavailable; preserve the identity and re-fetch before strict provenance validation",
        )
        (issues if strict else warnings).append(issue)
        return None
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        issues.append(NotebookIssue(1, "EXTERNAL_SOURCE_RECEIPT", f"{label} receipt is unreadable"))
        return None
    expected = {
        "status": "CACHED",
        "lesson_id": (
            cache_match.group(1)
            if cache_match is not None
            else captured_match.group(1) if captured_match is not None else None
        ),
        "kind": "primary",
        "original_url": record.get("url"),
        "final_url": record.get("final_url"),
        "media_type": record.get("media_type"),
        "retrieved_at": record.get("retrieved_at"),
        "sha256": record.get("sha256"),
        "path": receipt_identity_path,
        "receipt_path": receipt_identity_receipt_path,
    }
    mismatches = [key for key, value in expected.items() if receipt.get(key) != value]
    if SHA256_RE.fullmatch(str(record.get("sha256", ""))) and _sha256(cache_path) != record.get("sha256"):
        mismatches.append("cache sha256")
    if receipt.get("byte_count") != cache_path.stat().st_size:
        mismatches.append("byte_count")
    if mismatches:
        issues.append(
            NotebookIssue(
                1,
                "EXTERNAL_SOURCE_RECEIPT",
                f"{label} receipt or cache mismatch: {', '.join(sorted(set(mismatches)))}",
            )
        )
    return cache_path


def _validate_visible_links(
    issues: list[NotebookIssue],
    *,
    notebook: Path,
    repo: Path,
    markdown: str,
) -> None:
    for wrapped, bare in re.findall(r"\[[^\]]+\]\((?:<([^>]+)>|([^\s)]+))\)", markdown):
        target = unquote((wrapped or bare).split("#", 1)[0].strip())
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        candidate = notebook.parent / target
        try:
            resolved = candidate.resolve(strict=False)
            resolved.relative_to(repo)
        except (OSError, ValueError):
            issues.append(NotebookIssue(1, "BROKEN_LINK", f"link escapes the repository: {target}"))
            continue
        if not resolved.exists():
            issues.append(NotebookIssue(1, "BROKEN_LINK", f"link target does not exist: {target}"))


def _validate_v5_header(
    issues: list[NotebookIssue],
    *,
    payload: dict[str, object],
    practice: dict[str, object],
    repo: Path,
) -> tuple[str | None, str | None]:
    layer = practice.get("practice_layer")
    depth = practice.get("implementation_depth")
    lifecycle = practice.get("lifecycle")
    if layer not in PRACTICE_LAYERS:
        issues.append(NotebookIssue(1, "PRACTICE_PROGRESSION", "practice_layer is invalid"))
        layer = None
    if depth not in IMPLEMENTATION_DEPTHS:
        issues.append(NotebookIssue(1, "PRACTICE_PROGRESSION", "implementation_depth is invalid"))
        depth = None
    if lifecycle not in PRACTICE_LIFECYCLES:
        issues.append(NotebookIssue(1, "PRACTICE_PROGRESSION", "lifecycle must be fresh or preserved_attempt"))
    elif lifecycle == "preserved_attempt" and layer != "PRE_LAB":
        issues.append(
            NotebookIssue(
                1,
                "PRACTICE_PROGRESSION",
                "preserved_attempt artifacts remain PRE_LAB and cannot gain milestone credit",
            )
        )

    milestone_id = practice.get("milestone_id")
    milestone_hash = practice.get("milestone_definition_sha256")
    if layer == "PRE_LAB":
        if depth != "I1_MECHANISM":
            issues.append(NotebookIssue(1, "PRACTICE_PROGRESSION", "PRE_LAB must use I1_MECHANISM"))
        if milestone_id is not None or milestone_hash is not None:
            issues.append(NotebookIssue(1, "MILESTONE_CREDIT", "PRE_LAB cannot claim a milestone"))
    elif layer in {"MODULE_ASSIGNMENT", "PHASE_CAPSTONE"}:
        expected_prefix = "MA-" if layer == "MODULE_ASSIGNMENT" else "PC-"
        if (
            not isinstance(milestone_id, str)
            or MILESTONE_ID_RE.fullmatch(milestone_id) is None
            or not milestone_id.startswith(expected_prefix)
        ):
            issues.append(NotebookIssue(1, "MILESTONE_CREDIT", f"{layer} needs an {expected_prefix} milestone_id"))
        if SHA256_RE.fullmatch(str(milestone_hash or "")) is None:
            issues.append(NotebookIssue(1, "MILESTONE_CREDIT", f"{layer} needs milestone_definition_sha256"))
        elif isinstance(milestone_id, str):
            observed = _milestone_definition_hash(repo, milestone_id)
            if observed is None:
                issues.append(NotebookIssue(1, "MILESTONE_CREDIT", f"milestone definition is missing or ambiguous: {milestone_id}"))
            elif observed != milestone_hash:
                issues.append(NotebookIssue(1, "MILESTONE_CREDIT", f"milestone definition hash drift: {milestone_id}"))
        if layer == "MODULE_ASSIGNMENT" and (
            depth is None or IMPLEMENTATION_DEPTHS.get(str(depth), 0) < IMPLEMENTATION_DEPTHS["I3_WORKFLOW"]
        ):
            issues.append(NotebookIssue(1, "PRACTICE_PROGRESSION", "MODULE_ASSIGNMENT requires I3_WORKFLOW or deeper"))
        if layer == "PHASE_CAPSTONE" and depth != "I5_RESEARCH":
            issues.append(NotebookIssue(1, "PRACTICE_PROGRESSION", "PHASE_CAPSTONE must use I5_RESEARCH"))

    reviews = practice.get("creation_reviews")
    if not isinstance(reviews, list) or len(reviews) > 2:
        issues.append(NotebookIssue(1, "PRACTICE_REVIEW", "creation_reviews must contain at most two records"))
    elif not reviews and lifecycle != "preserved_attempt":
        issues.append(NotebookIssue(1, "PRACTICE_REVIEW", "fresh schema v5 practice needs one or two creation_reviews"))
    elif reviews:
        expected_hash = practice_contract_hash(payload)
        reviewer_ids: list[str] = []
        for index, review in enumerate(reviews, start=1):
            if not isinstance(review, dict):
                issues.append(NotebookIssue(1, "PRACTICE_REVIEW", "creation review entries must be objects"))
                continue
            if review.get("iteration") != index:
                issues.append(NotebookIssue(1, "PRACTICE_REVIEW", "creation review iterations must be contiguous"))
            reviewer_id = review.get("reviewer_id")
            if not isinstance(reviewer_id, str) or not reviewer_id.strip():
                issues.append(NotebookIssue(1, "PRACTICE_REVIEW", f"review {index} needs reviewer_id"))
            else:
                reviewer_ids.append(reviewer_id)
            verdict = review.get("verdict")
            surface_verdict = review.get("learner_surface_verdict")
            metadata_verdict = review.get("metadata_verdict")
            if verdict not in {"pass", "repair_required"}:
                issues.append(NotebookIssue(1, "PRACTICE_REVIEW", f"review {index} has invalid verdict"))
            if surface_verdict not in {"pass", "repair_required"}:
                issues.append(NotebookIssue(1, "PRACTICE_REVIEW", f"review {index} needs learner_surface_verdict"))
            if metadata_verdict not in {"pass", "repair_required"}:
                issues.append(NotebookIssue(1, "PRACTICE_REVIEW", f"review {index} needs metadata_verdict"))
            if verdict == "pass" and {surface_verdict, metadata_verdict} != {"pass"}:
                issues.append(NotebookIssue(1, "PRACTICE_REVIEW", f"review {index} cannot pass before both review surfaces pass"))
            review_hash = review.get("contract_sha256")
            if SHA256_RE.fullmatch(str(review_hash or "")) is None:
                issues.append(NotebookIssue(1, "PRACTICE_REVIEW", f"review {index} needs contract_sha256"))
            elif index == len(reviews) and review_hash != expected_hash:
                issues.append(NotebookIssue(1, "PRACTICE_REVIEW_STALE", f"review {index} contract hash is stale"))
            if not _rfc3339(review.get("reviewed_at")):
                issues.append(NotebookIssue(1, "PRACTICE_REVIEW", f"review {index} needs RFC 3339 reviewed_at"))
            if index == 1 and review.get("recheck_of") is not None:
                issues.append(NotebookIssue(1, "PRACTICE_REVIEW", "first review recheck_of must be null"))
            if index == 2 and review.get("recheck_of") != 1:
                issues.append(NotebookIssue(1, "PRACTICE_REVIEW", "second review must recheck iteration 1"))
        if len(reviewer_ids) == 2 and reviewer_ids[0] == reviewer_ids[1]:
            issues.append(NotebookIssue(1, "PRACTICE_REVIEW", "the second review must use a fresh reviewer"))
        if len(reviews) == 2 and isinstance(reviews[0], dict) and reviews[0].get("verdict") != "repair_required":
            issues.append(NotebookIssue(1, "PRACTICE_REVIEW", "a second review is allowed only after one repair"))
        latest = reviews[-1]
        if not isinstance(latest, dict) or latest.get("verdict") != "pass":
            issues.append(NotebookIssue(1, "PRACTICE_REVIEW", "latest creation review must pass"))

    return layer if isinstance(layer, str) else None, depth if isinstance(depth, str) else None


def validate_notebook_v3(
    notebook: Path,
    repo: Path,
    *,
    learner_state: bool = False,
    strict_external_sources: bool = False,
    completion_ready: bool = False,
) -> NotebookValidation:
    issues: list[NotebookIssue] = []
    warnings: list[NotebookIssue] = []
    source_links: set[str] = set()
    setup_cells: list[tuple[int, str]] = []
    try:
        payload = json.loads(notebook.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return NotebookValidation(
            [NotebookIssue(getattr(exc, "lineno", 1), "NOTEBOOK_JSON", f"invalid Notebook JSON: {exc}")],
            set(),
            [],
        )
    if payload.get("nbformat") != 4 or not isinstance(payload.get("cells"), list):
        return NotebookValidation(
            [NotebookIssue(1, "NOTEBOOK_JSON", "Notebook must use nbformat 4 and contain cells")],
            set(),
            [],
        )
    if not isinstance(payload.get("nbformat_minor"), int) or payload["nbformat_minor"] < 5:
        issues.append(NotebookIssue(1, "NOTEBOOK_JSON", "stable cell IDs require nbformat_minor 5 or newer"))

    metadata = payload.get("metadata")
    practice: dict[str, object] | None = None
    if isinstance(metadata, dict):
        lab = metadata.get("llm_research_lab")
        if isinstance(lab, dict) and isinstance(lab.get("practice"), dict):
            practice = lab["practice"]
    if practice is None:
        return NotebookValidation(
            [NotebookIssue(1, "AUDIT_METADATA", "missing metadata.llm_research_lab.practice")],
            set(),
            [],
        )
    schema_version = practice.get("schema_version")
    if schema_version not in {3, 4, 5}:
        message = (
            "practice schema v2 must be mechanically migrated to v3 without changing learner cells"
            if schema_version == 2
            else "practice schema_version must be 3, 4, or 5"
        )
        return NotebookValidation([NotebookIssue(1, "SCHEMA_MIGRATION", message)], set(), [])
    v5_fields = {
        "practice_layer",
        "implementation_depth",
        "lifecycle",
        "milestone_id",
        "milestone_definition_sha256",
        "learning_inputs",
        "prior_practice_evidence",
        "creation_reviews",
        "result_cell_ids",
        "workflow_contract",
        "research_contract",
    }
    if schema_version in {3, 4} and any(field in practice for field in v5_fields):
        issues.append(
            NotebookIssue(
                1,
                "LEGACY_MILESTONE_CREDIT",
                "schema v3/v4 is legacy-unclassified and cannot claim v5 layer, depth, or milestone credit",
            )
        )
    if practice.get("artifact_kind") != "standalone-practice":
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "artifact_kind must be standalone-practice"))
    if practice.get("scaffold_mode") != "guided-fading":
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "scaffold_mode must be guided-fading"))
    if practice.get("practice_mode") not in PRACTICE_MODES:
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "practice_mode must be NOTEBOOK, BENCHMARK, or DATASET_PROJECT"))
    practice_layer: str | None = None
    implementation_depth: str | None = None
    if schema_version == 5:
        practice_layer, implementation_depth = _validate_v5_header(
            issues,
            payload=payload,
            practice=practice,
            repo=repo,
        )
    raw_curriculum_targets = practice.get("curriculum_targets")
    if (
        not isinstance(raw_curriculum_targets, list)
        or not raw_curriculum_targets
        or len(raw_curriculum_targets) != len(set(raw_curriculum_targets))
        or not all(
            isinstance(value, str) and CURRICULUM_ID_RE.fullmatch(value)
            for value in raw_curriculum_targets
        )
    ):
        issues.append(NotebookIssue(1, "TARGET_RELATION", "curriculum_targets must contain unique Curriculum IDs"))
        curriculum_targets: list[str] = []
    else:
        curriculum_targets = raw_curriculum_targets

    cells: list[dict[str, object]] = payload["cells"]
    cells_by_id: dict[str, tuple[int, dict[str, object], dict[str, object]]] = {}
    role_cells: dict[str, list[tuple[int, str, dict[str, object], dict[str, object]]]] = {}
    exercise_roles: dict[str, dict[str, list[tuple[int, str, dict[str, object], dict[str, object]]]]] = {}
    markdown_parts: list[str] = []
    seen_ids: set[str] = set()
    for index, cell in enumerate(cells):
        if not isinstance(cell, dict):
            issues.append(NotebookIssue(1, "NOTEBOOK_JSON", f"cell {index} is not an object"))
            continue
        text = _cell_text(cell)
        if cell.get("cell_type") == "markdown":
            markdown_parts.append(text)
        elif cell.get("cell_type") == "code":
            if not learner_state and (
                cell.get("execution_count") is not None or cell.get("outputs") not in ([], None)
            ):
                issues.append(NotebookIssue(1, "EXECUTED", f"code cell {index} contains execution state or output"))
            try:
                ast.parse(text)
            except SyntaxError as exc:
                issues.append(NotebookIssue(exc.lineno or 1, "PYTHON_SYNTAX", f"code cell {index}: {exc.msg}"))
        cell_id = cell.get("id")
        if not isinstance(cell_id, str) or CELL_ID_RE.fullmatch(cell_id) is None:
            issues.append(NotebookIssue(1, "CELL_ID", f"cell {index} needs a stable valid id"))
            cell_id = f"<cell-{index}>"
        elif cell_id in seen_ids:
            issues.append(NotebookIssue(1, "CELL_ID", f"duplicate cell id: {cell_id}"))
        seen_ids.add(cell_id)
        audit = _cell_audit(cell)
        if audit is None:
            issues.append(NotebookIssue(1, "CELL_ROLE", f"cell {cell_id} lacks practice role metadata"))
            continue
        role = audit.get("role")
        if role not in CELL_ROLES:
            issues.append(NotebookIssue(1, "CELL_ROLE", f"cell {cell_id} has invalid role: {role}"))
            continue
        if cell.get("cell_type") != ROLE_CELL_TYPES[role]:
            issues.append(NotebookIssue(1, "CELL_ROLE", f"{role} cell {cell_id} has the wrong cell type"))
        exercise_id = audit.get("exercise_id")
        if role in EXERCISE_ROLES:
            if not isinstance(exercise_id, str) or EXERCISE_ID_RE.fullmatch(exercise_id) is None:
                issues.append(NotebookIssue(1, "CELL_ROLE", f"{role} cell {cell_id} needs an E## exercise_id"))
            else:
                exercise_roles.setdefault(exercise_id, {}).setdefault(role, []).append((index, cell_id, cell, audit))
        elif exercise_id is not None:
            issues.append(NotebookIssue(1, "CELL_ROLE", f"{role} cell {cell_id} must not have exercise_id"))
        role_cells.setdefault(role, []).append((index, cell_id, cell, audit))
        cells_by_id[cell_id] = (index, cell, audit)
        for pattern, label in LEAK_PATTERNS:
            if pattern.search(text):
                issues.append(NotebookIssue(1, "LEARNER_SURFACE_LEAK", f"cell {cell_id} exposes {label}"))

    markdown = "\n".join(markdown_parts)
    _validate_visible_links(issues, notebook=notebook, repo=repo, markdown=markdown)
    if re.search(r"^#{1,6} (?:전역 |점진적 )?힌트", markdown, re.MULTILINE):
        issues.append(NotebookIssue(1, "GLOBAL_HINT", "put progressive hints beside the relevant implementation"))
    if re.search(r"^#{1,6}\s+.*(?:모범답안|완성 답안|Solution|Answer)\b", markdown, re.MULTILINE | re.IGNORECASE):
        issues.append(NotebookIssue(1, "SOLUTION", "learner-facing solution or answer section is not allowed"))

    for role in ("intro", "setup"):
        if len(role_cells.get(role, [])) != 1:
            issues.append(NotebookIssue(1, "CELL_ROLE", f"Notebook needs exactly one {role} cell"))
    if len(role_cells.get("setup", [])) == 1:
        index, _, cell, _ = role_cells["setup"][0]
        setup_cells.append((index, _cell_text(cell)))

    exercise_ids = sorted(exercise_roles)
    expected_exercises = [f"E{index:02d}" for index in range(1, len(exercise_ids) + 1)]
    if not exercise_ids or exercise_ids != expected_exercises:
        issues.append(NotebookIssue(1, "CELL_ROLE", "exercise IDs must be contiguous E01, E02, ..."))
    expected_order: list[int] = []
    if len(role_cells.get("intro", [])) == 1:
        expected_order.append(role_cells["intro"][0][0])
    if len(role_cells.get("setup", [])) == 1:
        expected_order.append(role_cells["setup"][0][0])
    for exercise_id in exercise_ids:
        roles = exercise_roles[exercise_id]
        for role in EXERCISE_ROLES:
            matches = roles.get(role, [])
            if len(matches) != 1:
                issues.append(NotebookIssue(1, "CELL_ROLE", f"{exercise_id} needs exactly one {role} cell"))
                continue
            expected_order.append(matches[0][0])
            if not _cell_text(matches[0][2]).strip():
                issues.append(NotebookIssue(1, "CELL_ROLE", f"{exercise_id} {role} cell is empty"))
        brief_matches = roles.get("brief", [])
        if len(brief_matches) == 1:
            brief = _cell_text(brief_matches[0][2])
            for hint in ("<summary>힌트 1", "<summary>힌트 2"):
                if hint not in brief:
                    issues.append(NotebookIssue(1, "HINT_ADJACENCY", f"{exercise_id} brief needs adjacent {hint[9:]}"))
    if len(expected_order) == len(cells) and expected_order != sorted(expected_order):
        issues.append(NotebookIssue(1, "EXERCISE_ORDER", "cells must follow intro, setup, then each exercise role order"))
    elif len(expected_order) != len(cells):
        issues.append(NotebookIssue(1, "CELL_ROLE", "every cell must have exactly one recognized learner-flow role"))

    learning_kind: str | None = None
    session_concept_ids: set[str] = set()
    session_evidence_ids: set[str] = set()
    v5_input_targets: set[str] = set()
    v5_input_kinds: set[str] = set()
    v5_input_paths: set[str] = set()
    v5_captured_sources: dict[tuple[str, str], set[str]] = {}
    v5_captured_schema_versions: set[int] = set()
    if schema_version == 3:
        til_path = _validate_hash_record(issues, record=practice.get("til"), repo=repo, label="til")
        if til_path is not None:
            source_links.add(til_path)
            if TIL_RE.fullmatch(til_path) is None:
                issues.append(NotebookIssue(1, "SOURCE_AUDIT", "til path must name one finalized dated TIL"))
    elif schema_version == 4:
        if "til" in practice:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", "schema v4 stores the input only under learning_input"))
        learning_kind, session_concept_ids, session_evidence_ids = _validate_learning_input(
            issues,
            warnings,
            practice=practice,
            repo=repo,
            learner_state=learner_state,
            completion_ready=completion_ready,
        )
        raw_input = practice.get("learning_input")
        if learning_kind == "lesson-session" and isinstance(raw_input, dict):
            expected_targets = [raw_input.get("primary_target")]
            if raw_input.get("bridge_target") is not None:
                expected_targets.append(raw_input.get("bridge_target"))
            if curriculum_targets != expected_targets:
                issues.append(
                    NotebookIssue(
                        1,
                        "TARGET_RELATION",
                        "artifact curriculum_targets must be the session primary followed by its optional bridge",
                    )
                )
        if learning_kind == "finalized-til" and isinstance(raw_input, dict):
            path = raw_input.get("path")
            if isinstance(path, str):
                source_links.add(path)
    else:
        if "til" in practice or "learning_input" in practice:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", "schema v5 stores inputs only under learning_inputs"))
        (
            session_concept_ids,
            session_evidence_ids,
            v5_input_targets,
            v5_input_kinds,
            v5_input_paths,
            v5_captured_sources,
            v5_captured_schema_versions,
        ) = _validate_learning_inputs_v5(
            issues,
            warnings,
            practice=practice,
            repo=repo,
            learner_state=learner_state,
            completion_ready=completion_ready,
        )
        source_links.update(v5_input_paths)
        if v5_input_targets and v5_input_targets != set(curriculum_targets):
            issues.append(
                NotebookIssue(
                    1,
                    "TARGET_RELATION",
                    "artifact curriculum_targets must equal the captured-cycle primary and bridge target union",
                )
            )
        if 9 in v5_captured_schema_versions and (
            practice.get("lifecycle") != "preserved_attempt"
            or practice.get("practice_layer") != "PRE_LAB"
            or practice.get("implementation_depth") != "I1_MECHANISM"
            or practice.get("milestone_id") is not None
            or practice.get("milestone_definition_sha256") is not None
        ):
            issues.append(
                NotebookIssue(
                    1,
                    "PRACTICE_PROGRESSION",
                    "captured-session schema v9 may appear only as preserved_attempt PRE_LAB without milestone credit",
                )
            )

    raw_sources = practice.get("sources")
    if not isinstance(raw_sources, list):
        issues.append(NotebookIssue(1, "SOURCE_AUDIT", "sources must be a list"))
        raw_sources = []
    source_records = [item for item in raw_sources if isinstance(item, dict)]
    source_by_id: dict[str, dict[str, object]] = {}
    source_order: list[str] = []
    listed_source_paths = {
        item.get("path")
        for item in source_records
        if item.get("kind") != "external-reference" and isinstance(item.get("path"), str)
    }
    valid_source_paths: set[str] = set()
    cached_external_paths: dict[str, Path] = {}
    preserved_source_cycles = (
        v5_captured_sources
        if schema_version == 5 and practice.get("lifecycle") == "preserved_attempt"
        else {}
    )
    for index, record in enumerate(raw_sources):
        if not isinstance(record, dict):
            issues.append(NotebookIssue(1, "SOURCE_AUDIT", f"source[{index}] must be an object"))
            continue
        source_id = record.get("id")
        if not isinstance(source_id, str) or SOURCE_ID_RE.fullmatch(source_id) is None or source_id in source_by_id:
            issues.append(NotebookIssue(1, "SOURCE_AUDIT", f"source[{index}] has invalid or duplicate stable id: {source_id}"))
        else:
            source_by_id[source_id] = record
            source_order.append(source_id)
        kind = record.get("kind")
        if kind not in SOURCE_KINDS:
            issues.append(NotebookIssue(1, "SOURCE_AUDIT", f"source[{index}] has invalid kind: {kind}"))
            continue
        if kind == "external-reference":
            cache_path = _validate_external_record(
                issues,
                warnings,
                record=record,
                repo=repo,
                label=f"source[{index}]",
                strict=strict_external_sources or completion_ready,
                preserved_source_cycles=preserved_source_cycles,
            )
            if cache_path is not None and isinstance(source_id, str):
                cached_external_paths[source_id] = cache_path
            continue
        path = _validate_hash_record(issues, record=record, repo=repo, label=f"source[{index}]")
        if path is not None:
            if path in valid_source_paths:
                issues.append(NotebookIssue(1, "SOURCE_AUDIT", f"duplicate source path: {path}"))
            valid_source_paths.add(path)
            source_links.add(path)
        if kind == "instructor-practice":
            if record.get("variant") not in {"basic", "advanced", "single"}:
                issues.append(NotebookIssue(1, "SOURCE_AUDIT", f"source[{index}] needs a valid practice variant"))
            related = record.get("related_lesson")
            if not isinstance(related, str) or related not in listed_source_paths:
                issues.append(NotebookIssue(1, "SOURCE_AUDIT", f"source[{index}] needs a listed related_lesson"))
    if source_order != [f"S{index:03d}" for index in range(1, len(source_order) + 1)] or not source_order:
        issues.append(NotebookIssue(1, "SOURCE_AUDIT", "source IDs must be contiguous S001, S002, ..."))
    if schema_version == 5 and v5_captured_sources:
        declared_source_identities: set[tuple[str, str]] = set()
        for record in source_records:
            identity_path = record.get("path")
            digest = record.get("sha256")
            if record.get("kind") == "external-reference":
                cache_path = record.get("cache_path")
                archive_match = (
                    PRESERVED_EXTERNAL_CACHE_RE.fullmatch(cache_path)
                    if isinstance(cache_path, str)
                    else None
                )
                captured_path = record.get("captured_path")
                owning_cycles = (
                    preserved_source_cycles.get(
                        (str(captured_path), str(digest)), set()
                    )
                    if isinstance(captured_path, str)
                    and isinstance(digest, str)
                    else set()
                )
                identity_path = (
                    captured_path
                    if archive_match is not None
                    and archive_match.group(1) in owning_cycles
                    else cache_path
                )
            if isinstance(identity_path, str) and SHA256_RE.fullmatch(
                str(digest or "")
            ):
                declared_source_identities.add((identity_path, str(digest)))
        missing_captured_sources = sorted(
            set(v5_captured_sources) - declared_source_identities
        )
        if missing_captured_sources:
            issues.append(
                NotebookIssue(
                    1,
                    "SOURCE_AUDIT",
                    "practice sources omit captured provenance: "
                    + ", ".join(path for path, _ in missing_captured_sources),
                )
            )

    raw_outcomes = practice.get("outcomes")
    outcomes: dict[str, dict[str, object]] = {}
    outcome_order: list[str] = []
    outcome_curriculum_targets: set[str] = set()
    covered_exercises: set[str] = set()
    if not isinstance(raw_outcomes, list):
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "outcomes must be a list"))
        raw_outcomes = []
    for item in raw_outcomes:
        if not isinstance(item, dict):
            issues.append(NotebookIssue(1, "AUDIT_METADATA", "each outcome must be an object"))
            continue
        outcome_id = item.get("id")
        if not isinstance(outcome_id, str) or outcome_id in outcomes:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"invalid or duplicate outcome id: {outcome_id}"))
            continue
        outcomes[outcome_id] = item
        outcome_order.append(outcome_id)
        if item.get("action") not in ACTIONS:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{outcome_id} has invalid action"))
        if schema_version == 3:
            if not isinstance(item.get("til_location"), str) or not item["til_location"].strip():
                issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{outcome_id} needs til_location"))
        elif learning_kind == "lesson-session" or (
            schema_version == 5 and "captured-cycle" in v5_input_kinds
        ):
            if "til_location" in item:
                issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{outcome_id} must not use til_location with captured session evidence"))
            linked_concepts = item.get("concept_ids")
            linked_evidence = item.get("evidence_ids")
            if (
                not isinstance(linked_concepts, list)
                or not linked_concepts
                or len(linked_concepts) != len(set(linked_concepts))
                or not set(linked_concepts).issubset(session_concept_ids)
            ):
                issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", f"{outcome_id} needs session concept_ids"))
            if (
                not isinstance(linked_evidence, list)
                or not linked_evidence
                or len(linked_evidence) != len(set(linked_evidence))
                or not set(linked_evidence).issubset(session_evidence_ids)
            ):
                issues.append(NotebookIssue(1, "SESSION_REPAIR_REQUIRED", f"{outcome_id} needs session evidence_ids"))
        elif learning_kind == "finalized-til" or (
            schema_version == 5 and v5_input_kinds == {"finalized-til"}
        ):
            if not isinstance(item.get("til_location"), str) or not item["til_location"].strip():
                issues.append(NotebookIssue(1, "TIL_REPAIR_REQUIRED", f"{outcome_id} needs til_location"))
        if not isinstance(item.get("required_evidence"), str) or not item["required_evidence"].strip():
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{outcome_id} needs required_evidence"))
        linked_targets = item.get("curriculum_target_ids")
        if (
            not isinstance(linked_targets, list)
            or not linked_targets
            or len(linked_targets) != len(set(linked_targets))
            or not all(
                isinstance(value, str) and value in curriculum_targets
                for value in linked_targets
            )
        ):
            issues.append(NotebookIssue(1, "TARGET_RELATION", f"{outcome_id} needs unique artifact curriculum_target_ids"))
        else:
            outcome_curriculum_targets.update(linked_targets)
        linked = item.get("exercise_ids")
        if not isinstance(linked, list) or not linked or not all(isinstance(value, str) for value in linked):
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{outcome_id} needs exercise_ids"))
        else:
            covered_exercises.update(linked)
            unknown = sorted(set(linked) - set(exercise_ids))
            if unknown:
                issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{outcome_id} references unknown exercises: {', '.join(unknown)}"))
    if outcome_order != [f"O{index:02d}" for index in range(1, len(outcome_order) + 1)] or not outcome_order:
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "outcome IDs must be contiguous O01, O02, ..."))
    if set(exercise_ids) != covered_exercises:
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "outcomes and learner-flow exercises must cover the same exercise set"))
    if set(curriculum_targets) != outcome_curriculum_targets:
        issues.append(NotebookIssue(1, "TARGET_RELATION", "artifact and Outcome curriculum targets must reference each other"))

    if schema_version == 5:
        actions = {
            str(item.get("action"))
            for item in outcomes.values()
            if isinstance(item.get("action"), str)
        }
        if practice_layer == "MODULE_ASSIGNMENT" and not (
            {"implement", "interpret"}.issubset(actions)
            and bool({"test", "debug"}.intersection(actions))
        ):
            issues.append(
                NotebookIssue(
                    1,
                    "PRACTICE_PROGRESSION",
                    "MODULE_ASSIGNMENT needs implement, interpret, and test or debug Outcomes",
                )
            )
        if practice_layer == "PHASE_CAPSTONE" and not {
            "implement",
            "debug",
            "interpret",
            "design",
        }.issubset(actions):
            issues.append(
                NotebookIssue(
                    1,
                    "PRACTICE_PROGRESSION",
                    "PHASE_CAPSTONE needs implement, debug, interpret, and design Outcomes",
                )
            )

        workflow = practice.get("workflow_contract")
        workflow_fields = (
            "data_contract",
            "component_contract",
            "loss_contract",
            "training_contract",
            "evaluation_contract",
        )
        if practice_layer in {"MODULE_ASSIGNMENT", "PHASE_CAPSTONE"}:
            if not isinstance(workflow, dict) or any(
                not isinstance(workflow.get(field), str) or not str(workflow[field]).strip()
                for field in workflow_fields
            ):
                issues.append(
                    NotebookIssue(
                        1,
                        "WORKFLOW_CONTRACT",
                        "module and capstone practice need bounded data, component, loss, training, and evaluation contracts",
                    )
                )
            else:
                stage_cells = workflow.get("stage_cell_ids")
                stage_names = ("data", "model", "loss", "train", "evaluation")
                if not isinstance(stage_cells, dict) or set(stage_cells) != set(stage_names):
                    issues.append(
                        NotebookIssue(
                            1,
                            "WORKFLOW_CONTRACT",
                            "workflow stage_cell_ids must map data, model, loss, train, and evaluation",
                        )
                    )
                else:
                    for stage in stage_names:
                        linked_cells = stage_cells.get(stage)
                        if (
                            not isinstance(linked_cells, list)
                            or not linked_cells
                            or not all(isinstance(cell_id, str) for cell_id in linked_cells)
                            or len(linked_cells) != len(set(linked_cells))
                        ):
                            issues.append(
                                NotebookIssue(
                                    1,
                                    "WORKFLOW_CONTRACT",
                                    f"workflow stage {stage} needs unique cell IDs",
                                )
                            )
                            continue
                        for cell_id in linked_cells:
                            cell_record = cells_by_id.get(cell_id) if isinstance(cell_id, str) else None
                            if cell_record is None or cell_record[2].get("role") not in {
                                "implementation",
                                "fixture",
                                "check",
                            }:
                                issues.append(
                                    NotebookIssue(
                                        1,
                                        "WORKFLOW_CONTRACT",
                                        f"workflow stage {stage} has invalid code cell: {cell_id}",
                                    )
                                )
        elif workflow is not None:
            issues.append(NotebookIssue(1, "WORKFLOW_CONTRACT", "PRE_LAB must not claim a workflow_contract"))

        research = practice.get("research_contract")
        research_fields = (
            "hypothesis",
            "baseline",
            "control_or_ablation",
            "error_analysis",
            "reproducibility",
            "limitations",
        )
        if practice_layer == "PHASE_CAPSTONE":
            if not isinstance(research, dict) or any(
                not isinstance(research.get(field), str) or not str(research[field]).strip()
                for field in research_fields
            ):
                issues.append(
                    NotebookIssue(
                        1,
                        "RESEARCH_CONTRACT",
                        "PHASE_CAPSTONE needs hypothesis, baseline, control or ablation, error analysis, reproducibility, and limitations",
                    )
                )
        elif research is not None:
            issues.append(NotebookIssue(1, "RESEARCH_CONTRACT", "only PHASE_CAPSTONE may claim a research_contract"))

        raw_prior = practice.get("prior_practice_evidence")
        if not isinstance(raw_prior, list):
            issues.append(NotebookIssue(1, "PRIOR_PRACTICE", "prior_practice_evidence must be a list"))
            raw_prior = []
        repo_is_git = _is_git_repo(repo) if raw_prior else False
        prior_paths: list[str] = []
        for index, prior in enumerate(raw_prior, start=1):
            if not isinstance(prior, dict):
                issues.append(NotebookIssue(1, "PRIOR_PRACTICE", "prior practice entries must be objects"))
                continue
            if prior.get("id") != f"P{index:03d}" or PRIOR_PRACTICE_ID_RE.fullmatch(str(prior.get("id", ""))) is None:
                issues.append(NotebookIssue(1, "PRIOR_PRACTICE", "prior practice IDs must be contiguous P001, P002, ..."))
            path, path_error = _resolve_repo_file(prior.get("path"), repo)
            if path_error is not None or path is None:
                issues.append(NotebookIssue(1, "PRIOR_PRACTICE", f"prior practice is missing: {prior.get('path')}"))
            else:
                relative = path.relative_to(repo).as_posix()
                prior_paths.append(relative)
                if not relative.startswith("practice/") or path.suffix != ".ipynb":
                    issues.append(NotebookIssue(1, "PRIOR_PRACTICE", "prior practice must be one practice/*.ipynb"))
                if relative == notebook.relative_to(repo).as_posix():
                    issues.append(
                        NotebookIssue(
                            1,
                            "PRIOR_PRACTICE",
                            "prior practice must reference earlier module artifacts, not the current notebook",
                        )
                    )
                if prior.get("sha256") != _sha256(path):
                    issues.append(NotebookIssue(1, "PRIOR_PRACTICE_DRIFT", f"prior practice hash drift: {relative}"))
                commit_sha = str(prior.get("commit_sha", ""))
                if COMMIT_RE.fullmatch(commit_sha) is not None:
                    if not repo_is_git:
                        issues.append(
                            NotebookIssue(
                                1,
                                "PRIOR_PRACTICE",
                                "prior practice commit verification requires a Git repository",
                            )
                        )
                    elif not _git_commit_exists(repo, commit_sha):
                        issues.append(
                            NotebookIssue(
                                1,
                                "PRIOR_PRACTICE",
                                f"prior practice commit does not exist: {commit_sha}",
                            )
                        )
                    else:
                        changed_paths = _git_commit_changed_paths(repo, commit_sha)
                        if changed_paths != [relative]:
                            issues.append(
                                NotebookIssue(
                                    1,
                                    "PRIOR_PRACTICE",
                                    "prior practice completion commit must change exactly "
                                    f"that one notebook path: {relative}",
                                )
                            )
                        committed_bytes = _git_show_file_bytes(repo, commit_sha, relative)
                        if committed_bytes is None:
                            issues.append(
                                NotebookIssue(
                                    1,
                                    "PRIOR_PRACTICE",
                                    f"prior practice path is absent from commit {commit_sha}: {relative}",
                                )
                            )
                        else:
                            committed_sha256 = hashlib.sha256(committed_bytes).hexdigest()
                            if prior.get("sha256") != committed_sha256:
                                issues.append(
                                    NotebookIssue(
                                        1,
                                        "PRIOR_PRACTICE_DRIFT",
                                        f"prior practice committed bytes do not match declared sha256: {relative}",
                                    )
                                )
                try:
                    prior_payload = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                    prior_payload = None
                prior_metadata = None
                if isinstance(prior_payload, dict):
                    prior_root_metadata = prior_payload.get("metadata")
                    if isinstance(prior_root_metadata, dict):
                        prior_lab = prior_root_metadata.get("llm_research_lab")
                        if isinstance(prior_lab, dict) and isinstance(prior_lab.get("practice"), dict):
                            prior_metadata = prior_lab["practice"]
                if not isinstance(prior_metadata, dict) or prior_metadata.get("schema_version") != 5:
                    issues.append(
                        NotebookIssue(
                            1,
                            "PRIOR_PRACTICE",
                            f"prior practice is not a metadata-v5 artifact: {relative}",
                        )
                    )
                else:
                    for field in ("practice_layer", "implementation_depth", "milestone_id"):
                        if prior.get(field) != prior_metadata.get(field):
                            issues.append(
                                NotebookIssue(
                                    1,
                                    "PRIOR_PRACTICE",
                                    f"prior practice {field} differs from artifact metadata: {relative}",
                                )
                            )
                    if prior_metadata.get("practice_layer") == "MODULE_ASSIGNMENT":
                        prior_validation = validate_notebook_v3(
                            path,
                            repo,
                            learner_state=True,
                            completion_ready=True,
                        )
                        if prior_validation.issues:
                            issues.append(
                                NotebookIssue(
                                    1,
                                    "PRIOR_PRACTICE",
                                    f"prior module artifact is not completion-ready with interpreted results: {relative}",
                                )
                            )
            if COMMIT_RE.fullmatch(str(prior.get("commit_sha", ""))) is None:
                issues.append(NotebookIssue(1, "PRIOR_PRACTICE", "prior practice needs an exact commit SHA"))
            prior_layer = prior.get("practice_layer")
            prior_depth = prior.get("implementation_depth")
            if prior_layer not in PRACTICE_LAYERS or prior_depth not in IMPLEMENTATION_DEPTHS:
                issues.append(NotebookIssue(1, "PRIOR_PRACTICE", "prior practice needs a valid layer and depth"))
            if practice_layer == "PHASE_CAPSTONE" and prior_layer != "MODULE_ASSIGNMENT":
                issues.append(NotebookIssue(1, "PRIOR_PRACTICE", "capstone prior evidence must come from module assignments"))
        if len(prior_paths) != len(set(prior_paths)):
            issues.append(NotebookIssue(1, "PRIOR_PRACTICE", "prior practice paths must be unique"))
        if practice_layer == "PRE_LAB" and raw_prior:
            issues.append(NotebookIssue(1, "PRIOR_PRACTICE", "PRE_LAB cannot claim cumulative prior-practice evidence"))
        if practice_layer == "PHASE_CAPSTONE" and len(raw_prior) < 2:
            issues.append(NotebookIssue(1, "PRIOR_PRACTICE", "PHASE_CAPSTONE needs at least two prior module artifacts"))

        raw_result_cells = practice.get("result_cell_ids")
        if (
            not isinstance(raw_result_cells, list)
            or not all(isinstance(cell_id, str) for cell_id in raw_result_cells)
            or len(raw_result_cells) != len(set(raw_result_cells))
        ):
            issues.append(NotebookIssue(1, "RESULT_EVIDENCE", "result_cell_ids must be a unique list"))
            raw_result_cells = []
        if practice_layer in {"MODULE_ASSIGNMENT", "PHASE_CAPSTONE"} and not raw_result_cells:
            issues.append(NotebookIssue(1, "RESULT_EVIDENCE", f"{practice_layer} needs result_cell_ids"))
        for cell_id in raw_result_cells:
            cell_record = cells_by_id.get(cell_id) if isinstance(cell_id, str) else None
            if cell_record is None or cell_record[2].get("role") not in {"fixture", "check"}:
                issues.append(NotebookIssue(1, "RESULT_EVIDENCE", f"invalid result cell: {cell_id}"))

    raw_exercises = practice.get("exercises")
    exercise_profiles: dict[str, dict[str, object]] = {}
    exercise_order: list[str] = []
    if not isinstance(raw_exercises, list):
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "exercises must be a list"))
        raw_exercises = []
    for item in raw_exercises:
        if not isinstance(item, dict):
            issues.append(NotebookIssue(1, "AUDIT_METADATA", "each exercise profile must be an object"))
            continue
        exercise_id = item.get("id")
        if not isinstance(exercise_id, str) or exercise_id in exercise_profiles:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"invalid or duplicate exercise profile: {exercise_id}"))
            continue
        exercise_profiles[exercise_id] = item
        exercise_order.append(exercise_id)
        primary = item.get("primary_outcome_id")
        supporting = item.get("supporting_outcome_ids")
        if primary not in outcomes:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{exercise_id} needs one known primary_outcome_id"))
        if not isinstance(supporting, list) or not all(isinstance(value, str) for value in supporting):
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{exercise_id} supporting_outcome_ids must be a list"))
            supporting = []
        unknown_supporting = sorted(set(supporting) - set(outcomes))
        if unknown_supporting or primary in supporting:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{exercise_id} has invalid supporting outcomes"))
        if item.get("scaffold_stage") not in SCAFFOLD_STAGES:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{exercise_id} has invalid scaffold_stage"))
        target_ids = item.get("learner_target_ids")
        if not isinstance(target_ids, list) or not target_ids or not all(isinstance(value, str) for value in target_ids):
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{exercise_id} needs learner_target_ids"))
        elif len(target_ids) > 3 or len(set(target_ids)) != len(target_ids):
            issues.append(NotebookIssue(1, "TARGET_SCOPE", f"{exercise_id} may have at most three unique learner targets"))
    if exercise_order != exercise_ids:
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "exercise profiles must match contiguous learner-flow exercises"))

    raw_requirements = practice.get("requirements")
    requirements: dict[str, dict[str, object]] = {}
    requirement_order: dict[str, list[str]] = {}
    if not isinstance(raw_requirements, list):
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "requirements must be a list"))
        raw_requirements = []
    source_text_cache: dict[str, str] = {}
    for item in raw_requirements:
        if not isinstance(item, dict):
            issues.append(NotebookIssue(1, "AUDIT_METADATA", "each requirement must be an object"))
            continue
        requirement_id = item.get("id")
        exercise_id = item.get("exercise_id")
        match = REQUIREMENT_ID_RE.fullmatch(requirement_id) if isinstance(requirement_id, str) else None
        if match is None or match.group(1) != exercise_id:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"invalid or cross-exercise requirement id: {requirement_id}"))
            continue
        if requirement_id in requirements:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"duplicate requirement id: {requirement_id}"))
            continue
        requirements[requirement_id] = item
        requirement_order.setdefault(exercise_id, []).append(requirement_id)
        kind = item.get("kind")
        owner = item.get("owner")
        if kind not in REQUIREMENT_KINDS:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{requirement_id} has invalid kind"))
        if owner not in REQUIREMENT_OWNERS:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{requirement_id} has invalid owner"))
        claim = item.get("claim")
        if not isinstance(claim, str) or len(_normalized(claim)) < 12:
            issues.append(NotebookIssue(1, "SPEC_DISCLOSURE", f"{requirement_id} needs one complete learner-visible claim"))
        if kind == "practice-given" and (
            not isinstance(item.get("rationale"), str) or not item["rationale"].strip()
        ):
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{requirement_id} needs a local-rule rationale"))
        locations = item.get("source_locations", [])
        if not isinstance(locations, list):
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{requirement_id} source_locations must be a list"))
            locations = []
        if kind == "source-given" and not locations:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{requirement_id} needs source_locations"))
        for location in locations:
            if not isinstance(location, dict):
                issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{requirement_id} has invalid source location"))
                continue
            source_id = location.get("source_id")
            if not isinstance(source_id, str) or source_id not in source_by_id:
                issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{requirement_id} source location is not a listed stable source ID"))
                continue
            if not isinstance(location.get("locator"), str) or not location["locator"].strip():
                issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{requirement_id} source location needs locator"))
            anchor = location.get("anchor")
            if not isinstance(anchor, str) or not anchor.strip():
                issues.append(NotebookIssue(1, "SOURCE_ANCHOR", f"{requirement_id} source location needs anchor"))
            else:
                source_record = source_by_id[source_id]
                raw_path = source_record.get("path")
                source_file: Path | None = None
                if isinstance(raw_path, str):
                    source_file = repo / raw_path
                elif source_record.get("kind") == "external-reference":
                    source_file = cached_external_paths.get(source_id)
                if source_file is None:
                    continue
                if source_id not in source_text_cache:
                    try:
                        source_text_cache[source_id] = _normalized(source_file.read_text(encoding="utf-8"))
                    except (OSError, UnicodeDecodeError):
                        source_text_cache[source_id] = ""
                if _normalized(anchor) not in source_text_cache[source_id]:
                    issues.append(NotebookIssue(1, "SOURCE_ANCHOR", f"{requirement_id} anchor does not occur in {source_id}"))
        visible_cell_id = item.get("visible_cell_id")
        if not isinstance(visible_cell_id, str) or visible_cell_id not in cells_by_id:
            issues.append(NotebookIssue(1, "SPEC_DISCLOSURE", f"{requirement_id} has no visible brief cell"))
        else:
            cell_index, visible_cell, cell_audit = cells_by_id[visible_cell_id]
            if cell_audit.get("role") != "brief" or cell_audit.get("exercise_id") != exercise_id:
                issues.append(NotebookIssue(1, "SPEC_DISCLOSURE", f"{requirement_id} must point to its exercise brief"))
            implementation = exercise_roles.get(exercise_id, {}).get("implementation", [])
            if implementation and cell_index >= implementation[0][0]:
                issues.append(NotebookIssue(1, "SPEC_DISCLOSURE", f"{requirement_id} is disclosed after implementation"))
            if isinstance(claim, str) and _normalized(claim) not in _normalized(_cell_text(visible_cell)):
                issues.append(NotebookIssue(1, "SPEC_DISCLOSURE", f"{requirement_id} full learner-visible claim is missing"))
        target_ids = item.get("target_ids")
        if not isinstance(target_ids, list) or not all(isinstance(value, str) for value in target_ids):
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{requirement_id} target_ids must be a list"))
        elif owner == "provided" and target_ids:
            issues.append(NotebookIssue(1, "TARGET_OWNERSHIP", f"{requirement_id} is provided and cannot own learner targets"))
        elif owner == "learner" and not target_ids:
            issues.append(NotebookIssue(1, "TARGET_OWNERSHIP", f"{requirement_id} is learner-owned and needs target_ids"))
        if kind == "practice-given" and owner == "learner":
            learner_outcomes = item.get("learner_outcome_ids")
            if not isinstance(learner_outcomes, list) or not learner_outcomes or not all(
                isinstance(value, str) and value in outcomes for value in learner_outcomes
            ):
                issues.append(NotebookIssue(1, "TARGET_OWNERSHIP", f"{requirement_id} needs direct learner_outcome_ids"))
    for exercise_id, observed_ids in requirement_order.items():
        expected_ids = [f"C-{exercise_id}-{index:02d}" for index in range(1, len(observed_ids) + 1)]
        if observed_ids != expected_ids:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{exercise_id} requirement IDs must be contiguous"))
    if set(requirement_order) != set(exercise_ids):
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "every exercise needs audited requirements"))

    raw_targets = practice.get("learner_targets")
    targets: dict[str, dict[str, object]] = {}
    target_order: dict[str, list[str]] = {}
    if not isinstance(raw_targets, list):
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "learner_targets must be a list"))
        raw_targets = []
    for item in raw_targets:
        if not isinstance(item, dict):
            issues.append(NotebookIssue(1, "AUDIT_METADATA", "each learner target must be an object"))
            continue
        target_id = item.get("id")
        exercise_id = item.get("exercise_id")
        match = TARGET_ID_RE.fullmatch(target_id) if isinstance(target_id, str) else None
        if match is None or match.group(1) != exercise_id:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"invalid or cross-exercise learner target id: {target_id}"))
            continue
        if target_id in targets:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"duplicate learner target id: {target_id}"))
            continue
        targets[target_id] = item
        target_order.setdefault(exercise_id, []).append(target_id)
        if item.get("kind") not in TARGET_KINDS:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{target_id} has invalid kind"))
        cell_id = item.get("cell_id")
        target_cell: dict[str, object] | None = None
        target_text = ""
        target_audit: dict[str, object] = {}
        if not isinstance(cell_id, str) or cell_id not in cells_by_id:
            issues.append(NotebookIssue(1, "TARGET_TRACE", f"{target_id} has no target cell"))
        else:
            _, target_cell, target_audit = cells_by_id[cell_id]
            target_text = _cell_text(target_cell)
            if target_audit.get("role") not in TARGET_ROLES or target_audit.get("exercise_id") != exercise_id:
                issues.append(NotebookIssue(1, "TARGET_TRACE", f"{target_id} must point to a same-exercise implementation or reflection"))
        marker = item.get("marker")
        placeholder = item.get("placeholder")
        if not isinstance(marker, str) or not marker.strip() or marker not in target_text:
            issues.append(NotebookIssue(1, "TARGET_TRACE", f"{target_id} marker is missing from its learner cell"))
        if not isinstance(placeholder, str) or not placeholder.strip():
            issues.append(NotebookIssue(1, "TARGET_TRACE", f"{target_id} needs an exact placeholder"))
        elif not learner_state and placeholder not in target_text:
            issues.append(NotebookIssue(1, "PREFILLED_CORE", f"{target_id} learner target is already resolved"))
        symbol = item.get("symbol")
        if symbol is not None:
            if not isinstance(symbol, str) or not symbol.strip() or target_cell is None or target_cell.get("cell_type") != "code":
                issues.append(NotebookIssue(1, "TARGET_TRACE", f"{target_id} has an invalid symbol target"))
            else:
                try:
                    tree = ast.parse(target_text)
                except SyntaxError:
                    tree = None
                if tree is not None:
                    node = _symbol_node(tree, symbol)
                    if node is None:
                        issues.append(NotebookIssue(1, "TARGET_TRACE", f"{target_id} symbol does not exist: {symbol}"))
                    elif isinstance(placeholder, str) and placeholder in target_text:
                        segment = ast.get_source_segment(target_text, node) or ""
                        if placeholder not in segment:
                            issues.append(NotebookIssue(1, "TARGET_TRACE", f"{target_id} placeholder is outside symbol {symbol}"))
        linked_outcomes = item.get("outcome_ids")
        if not isinstance(linked_outcomes, list) or not linked_outcomes or not all(
            isinstance(value, str) and value in outcomes for value in linked_outcomes
        ):
            issues.append(NotebookIssue(1, "TARGET_TRACE", f"{target_id} needs known outcome_ids"))
        else:
            for outcome_id in linked_outcomes:
                linked_exercises = outcomes[outcome_id].get("exercise_ids", [])
                if exercise_id not in linked_exercises:
                    issues.append(NotebookIssue(1, "TARGET_TRACE", f"{target_id} outcome {outcome_id} does not cover {exercise_id}"))
        linked_requirements = item.get("requirement_ids")
        if not isinstance(linked_requirements, list) or not all(isinstance(value, str) for value in linked_requirements):
            issues.append(NotebookIssue(1, "TARGET_TRACE", f"{target_id} requirement_ids must be a list"))
        else:
            for requirement_id in linked_requirements:
                if requirement_id not in requirements or requirements[requirement_id].get("exercise_id") != exercise_id:
                    issues.append(NotebookIssue(1, "TARGET_TRACE", f"{target_id} references an unknown or cross-exercise requirement"))
                else:
                    requirement_targets = requirements[requirement_id].get("target_ids", [])
                    if not isinstance(requirement_targets, list) or target_id not in requirement_targets:
                        issues.append(NotebookIssue(1, "TARGET_OWNERSHIP", f"{target_id} and {requirement_id} must reference each other"))
    for exercise_id, observed_ids in target_order.items():
        expected_ids = [f"T-{exercise_id}-{index:02d}" for index in range(1, len(observed_ids) + 1)]
        if observed_ids != expected_ids:
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{exercise_id} learner target IDs must be contiguous"))
    if set(target_order) != set(exercise_ids):
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "every exercise needs at least one learner target"))

    if schema_version == 5 and practice_layer in {"MODULE_ASSIGNMENT", "PHASE_CAPSTONE"}:
        declared_results = practice.get("result_cell_ids")
        result_set = set(declared_results) if isinstance(declared_results, list) else set()
        workflow = practice.get("workflow_contract")
        workflow_field_map = {
            "data": "data_contract",
            "model": "component_contract",
            "loss": "loss_contract",
            "train": "training_contract",
            "evaluation": "evaluation_contract",
        }
        if isinstance(workflow, dict):
            stage_cells = workflow.get("stage_cell_ids")
            if isinstance(stage_cells, dict):
                semantic_stage_target_ids: dict[str, set[str]] = {}
                stage_sets = {
                    stage: {
                        cell_id
                        for cell_id in stage_cells.get(stage, [])
                        if isinstance(cell_id, str)
                    }
                    for stage in workflow_field_map
                    if isinstance(stage_cells.get(stage), list)
                }
                if set(stage_sets) == set(workflow_field_map):
                    for stage, linked_cells in stage_sets.items():
                        other_cells = set().union(
                            *(
                                cells
                                for other_stage, cells in stage_sets.items()
                                if other_stage != stage
                            )
                        )
                        if not linked_cells - other_cells:
                            issues.append(
                                NotebookIssue(
                                    1,
                                    "WORKFLOW_CONTRACT",
                                    f"workflow stage {stage} needs a stage-exclusive learner-visible code cell",
                                )
                            )
                for stage, field in workflow_field_map.items():
                    contract_text = workflow.get(field)
                    linked_cells = stage_cells.get(stage)
                    if not isinstance(contract_text, str) or not contract_text.strip():
                        continue
                    if not isinstance(linked_cells, list):
                        continue
                    linked_cell_ids = {
                        cell_id for cell_id in linked_cells if isinstance(cell_id, str)
                    }
                    exercise_scope = {
                        cells_by_id[cell_id][2].get("exercise_id")
                        for cell_id in linked_cell_ids
                        if cell_id in cells_by_id
                    }
                    if stage == "data" and not any(
                        cell_id in cells_by_id
                        and cells_by_id[cell_id][2].get("role") == "fixture"
                        for cell_id in linked_cell_ids
                    ):
                        issues.append(
                            NotebookIssue(
                                1,
                                "WORKFLOW_CONTRACT",
                                "workflow data stage must include a deterministic fixture cell",
                            )
                        )
                    if stage == "data" and not any(
                        cell_id in cells_by_id
                        and cells_by_id[cell_id][2].get("role") == "check"
                        for cell_id in linked_cell_ids
                    ):
                        issues.append(
                            NotebookIssue(
                                1,
                                "WORKFLOW_CONTRACT",
                                "workflow data stage must include deterministic check evidence",
                            )
                        )
                    if stage in {"model", "loss", "train"} and not any(
                        cell_id in cells_by_id
                        and cells_by_id[cell_id][2].get("role") == "implementation"
                        for cell_id in linked_cell_ids
                    ):
                        issues.append(
                            NotebookIssue(
                                1,
                                "WORKFLOW_CONTRACT",
                                f"workflow stage {stage} must include an implementation cell",
                            )
                        )
                    if stage in {"model", "loss", "train"}:
                        matched_targets: list[tuple[str, dict[str, object]]] = []
                        for target_id, target in targets.items():
                            if (
                                target.get("kind") != "code"
                                or target.get("cell_id") not in linked_cell_ids
                            ):
                                continue
                            requirement_ids = target.get("requirement_ids")
                            if not isinstance(requirement_ids, list):
                                continue
                            if any(
                                isinstance(requirement_id, str)
                                and requirement_id in requirements
                                and requirements[requirement_id].get("owner") == "learner"
                                and _matches_contract_text(
                                    requirements[requirement_id].get("claim"),
                                    contract_text,
                                )
                                for requirement_id in requirement_ids
                            ):
                                matched_targets.append((target_id, target))
                        semantic_stage_target_ids[stage] = {
                            target_id for target_id, _ in matched_targets
                        }
                        if not matched_targets:
                            issues.append(
                                NotebookIssue(
                                    1,
                                    "WORKFLOW_CONTRACT",
                                    f"workflow stage {stage} needs a learner-owned code target whose requirement matches its contract",
                                )
                            )
                        elif not any(
                            isinstance(target.get("cell_id"), str)
                            and target["cell_id"] in cells_by_id
                            and _stage_target_exposes_semantics(
                                stage,
                                cell=cells_by_id[target["cell_id"]][1],
                                target=target,
                            )
                            for _, target in matched_targets
                        ):
                            issues.append(
                                NotebookIssue(
                                    1,
                                    "WORKFLOW_CONTRACT",
                                    f"workflow stage {stage} code scaffold does not expose its required API or data-flow semantics",
                                )
                            )
                    if stage == "evaluation" and not any(
                        cell_id in cells_by_id
                        and cells_by_id[cell_id][2].get("role") in {"fixture", "check"}
                        for cell_id in linked_cell_ids
                    ):
                        issues.append(
                            NotebookIssue(
                                1,
                                "WORKFLOW_CONTRACT",
                                "workflow evaluation stage must include a fixture or check cell",
                            )
                        )
                    visible_briefs = [
                        _cell_text(cells_by_id[cell_id][1])
                        for cell_id, (_, _, audit) in cells_by_id.items()
                        if audit.get("role") == "brief"
                        and audit.get("exercise_id") in exercise_scope
                    ]
                    if not any(
                        _matches_contract_text(brief_text, contract_text)
                        for brief_text in visible_briefs
                    ):
                        issues.append(
                            NotebookIssue(
                                1,
                                "WORKFLOW_CONTRACT",
                                f"workflow {field} must be disclosed in a learner-visible brief for its stage cells",
                            )
                        )
                if set(semantic_stage_target_ids) == {"model", "loss", "train"}:
                    all_semantic_targets = set().union(
                        *semantic_stage_target_ids.values()
                    )
                    if len(all_semantic_targets) != sum(
                        len(target_ids)
                        for target_ids in semantic_stage_target_ids.values()
                    ):
                        issues.append(
                            NotebookIssue(
                                1,
                                "WORKFLOW_CONTRACT",
                                "model, loss, and train must use distinct learner-owned code targets",
                            )
                        )
                if set(stage_sets) == set(workflow_field_map):
                    train_results = result_set.intersection(stage_sets["train"])
                    evaluation_results = result_set.intersection(
                        stage_sets["evaluation"]
                    )
                    if (
                        not train_results
                        or not evaluation_results
                        or not train_results.isdisjoint(evaluation_results)
                    ):
                        issues.append(
                            NotebookIssue(
                                1,
                                "RESULT_EVIDENCE",
                                "workflow needs distinct declared result cells for training and evaluation",
                            )
                        )
                    interpreted_results = set().union(
                        *(
                            _target_result_links(target, result_set)
                            for target in targets.values()
                            if target.get("kind") == "interpretation"
                        )
                    )
                    workflow_results = train_results.union(evaluation_results)
                    if workflow_results and not workflow_results.issubset(
                        interpreted_results
                    ):
                        issues.append(
                            NotebookIssue(
                                1,
                                "RESULT_EVIDENCE",
                                "the distinct training and evaluation result cells must be linked by learner interpretation targets",
                            )
                        )
        research = practice.get("research_contract")
        if practice_layer == "PHASE_CAPSTONE" and isinstance(research, dict):
            research_fields = (
                "hypothesis",
                "baseline",
                "control_or_ablation",
                "error_analysis",
                "reproducibility",
                "limitations",
            )
            research_result_links: dict[str, set[str]] = {}
            for field in research_fields:
                contract_text = research.get(field)
                if not isinstance(contract_text, str) or not contract_text.strip():
                    continue
                matches = _find_contract_requirements(requirements, contract_text)
                surfaced = False
                field_results: set[str] = set()
                for requirement_id, requirement in matches:
                    target_ids = requirement.get("target_ids")
                    if (
                        requirement.get("owner") != "learner"
                        or not isinstance(target_ids, list)
                        or not target_ids
                    ):
                        continue
                    for target_id in target_ids:
                        if (
                            isinstance(target_id, str)
                            and target_id in targets
                            and targets[target_id].get("kind")
                            in {"design", "interpretation"}
                        ):
                            linked_results = _target_result_links(
                                targets[target_id], result_set
                            )
                            if linked_results:
                                surfaced = True
                                field_results.update(linked_results)
                research_result_links[field] = field_results
                if not surfaced:
                    issues.append(
                        NotebookIssue(
                            1,
                            "RESEARCH_CONTRACT",
                            f"research field {field} must map to learner-visible requirements, targets, and result cells",
                        )
                    )
            evidence_fields = ("baseline", "control_or_ablation", "error_analysis")
            if all(field in research_result_links for field in evidence_fields):
                exclusive_results: dict[str, set[str]] = {}
                for field in evidence_fields:
                    other_results = set().union(
                        *(
                            research_result_links[other]
                            for other in evidence_fields
                            if other != field
                        )
                    )
                    exclusive_results[field] = (
                        research_result_links[field] - other_results
                    )
                if any(not cells for cells in exclusive_results.values()):
                    issues.append(
                        NotebookIssue(
                            1,
                            "RESEARCH_CONTRACT",
                            "baseline, control or ablation, and error analysis need structurally distinct result evidence",
                        )
                    )
                else:
                    evidence_exercises = {
                        field: {
                            cells_by_id[cell_id][2].get("exercise_id")
                            for cell_id in cell_ids
                            if cell_id in cells_by_id
                        }
                        for field, cell_ids in exclusive_results.items()
                    }
                    if len(
                        {
                            exercise_id
                            for exercise_ids in evidence_exercises.values()
                            for exercise_id in exercise_ids
                            if isinstance(exercise_id, str)
                        }
                    ) < len(evidence_fields):
                        issues.append(
                            NotebookIssue(
                                1,
                                "RESEARCH_CONTRACT",
                                "capstone research evidence must be learner-visible in distinct exercise result cells",
                            )
                        )
        grounded_interpretations = 0
        for target in targets.values():
            if target.get("kind") != "interpretation":
                continue
            linked_results = target.get("result_cell_ids")
            if (
                isinstance(linked_results, list)
                and linked_results
                and set(linked_results).issubset(result_set)
            ):
                grounded_interpretations += 1
            else:
                issues.append(
                    NotebookIssue(
                        1,
                        "RESULT_EVIDENCE",
                        f"{target.get('id')} interpretation must reference declared result_cell_ids",
                    )
                )
        if grounded_interpretations == 0:
            issues.append(
                NotebookIssue(
                    1,
                    "RESULT_EVIDENCE",
                    f"{practice_layer} needs a learner interpretation grounded in observed result cells",
                )
            )

    reflection_target_cells = {
        item.get("cell_id")
        for item in targets.values()
        if isinstance(item.get("cell_id"), str)
        and item["cell_id"] in cells_by_id
        and cells_by_id[item["cell_id"]][2].get("role") == "reflection"
    }
    for exercise_id in exercise_ids:
        reflection_matches = exercise_roles.get(exercise_id, {}).get("reflection", [])
        if len(reflection_matches) != 1:
            continue
        _, cell_id, cell, _ = reflection_matches[0]
        if cell_id not in reflection_target_cells and OPTIONAL_REFLECTION_RE.search(_cell_text(cell)) is None:
            issues.append(
                NotebookIssue(
                    1,
                    "TARGET_TRACE",
                    f"{exercise_id} reflection has no learner target and must say that it is optional, not a completion condition",
                )
            )

    for exercise_id, profile in exercise_profiles.items():
        declared = profile.get("learner_target_ids")
        if isinstance(declared, list) and declared != target_order.get(exercise_id, []):
            issues.append(NotebookIssue(1, "TARGET_TRACE", f"{exercise_id} profile learner_target_ids do not match target records"))
    for requirement_id, requirement in requirements.items():
        exercise_id = requirement["exercise_id"]
        target_ids = requirement.get("target_ids", [])
        if not isinstance(target_ids, list):
            continue
        for target_id in target_ids:
            if target_id not in targets or targets[target_id].get("exercise_id") != exercise_id:
                issues.append(NotebookIssue(1, "TARGET_OWNERSHIP", f"{requirement_id} references an unknown or cross-exercise target"))
            else:
                target_requirements = targets[target_id].get("requirement_ids", [])
                if not isinstance(target_requirements, list) or requirement_id not in target_requirements:
                    issues.append(NotebookIssue(1, "TARGET_OWNERSHIP", f"{requirement_id} and {target_id} must reference each other"))
        if requirement.get("kind") == "practice-given" and requirement.get("owner") == "learner":
            learner_outcomes = requirement.get("learner_outcome_ids", [])
            if isinstance(learner_outcomes, list):
                for target_id in target_ids:
                    target_outcomes = targets.get(target_id, {}).get("outcome_ids", [])
                    if not set(learner_outcomes).issubset(set(target_outcomes) if isinstance(target_outcomes, list) else set()):
                        issues.append(NotebookIssue(1, "TARGET_OWNERSHIP", f"{requirement_id} learner outcomes are not shared by target {target_id}"))

    used_requirements: set[str] = set()
    for exercise_id in exercise_ids:
        implementation_matches = exercise_roles.get(exercise_id, {}).get("implementation", [])
        implementation_code = ""
        if len(implementation_matches) == 1:
            _, cell_id, cell, _ = implementation_matches[0]
            implementation_code = _cell_text(cell)
            if re.search(r"\b(?:subprocess|pytest|importlib\.reload|sys\.path|PYTHONPATH)\b", implementation_code):
                issues.append(NotebookIssue(1, "NOTEBOOK_SETUP", f"implementation cell {cell_id} contains bundle machinery"))
        check_matches = exercise_roles.get(exercise_id, {}).get("check", [])
        if len(check_matches) != 1:
            continue
        _, cell_id, cell, audit = check_matches[0]
        code = _cell_text(cell)
        check_name = f"check_{exercise_id.lower()}"
        if not re.search(rf"^def {check_name}\s*\(", code, re.MULTILINE):
            issues.append(NotebookIssue(1, "EXERCISE_TEST", f"{exercise_id} check cell must define {check_name}()"))
        if len(re.findall(rf"\b{check_name}\s*\(\s*\)", code)) < 2:
            issues.append(NotebookIssue(1, "EXERCISE_TEST", f"{exercise_id} check cell must call {check_name}()"))
        try:
            tree = ast.parse(code)
        except SyntaxError:
            tree = None
        if tree is not None and any(isinstance(node, ast.Assert) for node in ast.walk(tree)):
            issues.append(NotebookIssue(1, "TEST_CONTRACT", f"{exercise_id} checks must use numpy.testing or torch.testing, not plain assert"))
        if re.search(r"\bpytest\b", code):
            issues.append(NotebookIssue(1, "TEST_CONTRACT", f"{exercise_id} check cell must not use pytest"))
        observed, syntax_error = collect_observables(code)
        if syntax_error is not None:
            continue
        learner_attributes, learner_instances = _learner_class_api(implementation_code, code)
        declared = audit.get("observables")
        if not isinstance(declared, list):
            issues.append(NotebookIssue(1, "CHECK_TRACE", f"{exercise_id} check cell needs observables metadata"))
            declared = []
        expected_ordinals = list(range(1, len(observed) + 1))
        declared_ordinals = [item.get("ordinal") for item in declared if isinstance(item, dict)]
        if declared_ordinals != expected_ordinals or len(declared) != len(observed):
            issues.append(NotebookIssue(1, "CHECK_TRACE", f"{exercise_id} observable ordinals must match AST order"))
        categories: set[str] = set()
        for expected, item in zip(observed, declared):
            if not isinstance(item, dict):
                issues.append(NotebookIssue(1, "CHECK_TRACE", f"{exercise_id} observable metadata must be objects"))
                continue
            if item.get("kind") != expected.kind or item.get("fingerprint") != expected.fingerprint:
                issues.append(NotebookIssue(1, "CHECK_TRACE", f"{exercise_id} observable {expected.ordinal} fingerprint or kind does not match code"))
            category = item.get("category")
            if category not in CHECK_CATEGORIES:
                issues.append(NotebookIssue(1, "CHECK_TRACE", f"{exercise_id} observable {expected.ordinal} has invalid category"))
            else:
                categories.add(category)
            linked = item.get("requirement_ids")
            if not isinstance(linked, list) or len(linked) != 1 or not isinstance(linked[0], str):
                issues.append(NotebookIssue(1, "CHECK_TRACE", f"{exercise_id} observable {expected.ordinal} must map to exactly one atomic requirement"))
                continue
            requirement_id = linked[0]
            match = REQUIREMENT_ID_RE.fullmatch(requirement_id)
            if match is None or match.group(1) != exercise_id:
                issues.append(NotebookIssue(1, "CHECK_TRACE", f"{exercise_id} observable {expected.ordinal} has a cross-exercise requirement"))
            elif requirement_id not in requirements:
                issues.append(NotebookIssue(1, "CHECK_TRACE", f"{exercise_id} observable {expected.ordinal} references an undefined requirement"))
            else:
                used_requirements.add(requirement_id)
                claim = requirements[requirement_id].get("claim")
                required_names = {
                    attribute
                    for instance, attribute in expected.direct_members
                    if instance in learner_instances and attribute in learner_attributes
                }
                if isinstance(claim, str):
                    missing_names = sorted(
                        name
                        for name in required_names
                        if re.search(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])", claim) is None
                    )
                    if missing_names:
                        issues.append(
                            NotebookIssue(
                                1,
                                "SPEC_DISCLOSURE",
                                f"{requirement_id} does not disclose public checked API name(s): {', '.join(missing_names)}",
                            )
                        )
            if expected.kind == "exception" and category != "failure":
                issues.append(NotebookIssue(1, "CHECK_TRACE", f"{exercise_id} expected exception must use failure category"))
        if "normal" not in categories:
            issues.append(NotebookIssue(1, "CHECK_TRACE", f"{exercise_id} checks need at least one normal observable"))
    def is_reflection_only(requirement_id: str) -> bool:
        """Allow prose evidence without inventing a machine-testable API.

        A Requirement may omit a public assertion only when it is learner-owned
        and every linked target is an interpretation or design response in the
        same Exercise's reflection cell. Code-facing Requirements still need an
        observable trace.
        """

        requirement = requirements[requirement_id]
        target_ids = requirement.get("target_ids", [])
        if requirement.get("owner") != "learner" or not isinstance(target_ids, list) or not target_ids:
            return False
        for target_id in target_ids:
            target = targets.get(target_id)
            if target is None or target.get("kind") not in {"design", "interpretation"}:
                return False
            cell_id = target.get("cell_id")
            cell_record = cells_by_id.get(cell_id) if isinstance(cell_id, str) else None
            if cell_record is None:
                return False
            _, _, cell_audit = cell_record
            if (
                cell_audit.get("role") != "reflection"
                or cell_audit.get("exercise_id") != requirement.get("exercise_id")
            ):
                return False
        return True

    unused = sorted(
        requirement_id
        for requirement_id in set(requirements) - used_requirements
        if not is_reflection_only(requirement_id)
    )
    if unused:
        issues.append(NotebookIssue(1, "CHECK_TRACE", f"requirements without a mapped check: {', '.join(unused)}"))

    if len(setup_cells) == 1:
        _, setup_code = setup_cells[0]
        if re.search(r"\b(?:refresh_core|run_exercise_tests)\s*\(|\bsys\.path\b|\bimportlib\.reload\b|\bsubprocess\b|PYTHONPATH", setup_code):
            issues.append(NotebookIssue(1, "NOTEBOOK_SETUP", "setup cell contains bundle path, reload, subprocess, or pytest helpers"))
        if "NotImplementedError" in setup_code:
            issues.append(NotebookIssue(1, "NOTEBOOK_SETUP", "setup cell must not contain learner implementation placeholders"))
        if re.search(r"\bglobals\s*\(", setup_code):
            issues.append(NotebookIssue(1, "DYNAMIC_GLOBALS", "setup cell must not create learner callables through globals()"))

    if completion_ready:
        for target_id, target in targets.items():
            cell_id = target.get("cell_id")
            placeholder = target.get("placeholder")
            cell_record = cells_by_id.get(cell_id) if isinstance(cell_id, str) else None
            if (
                cell_record is not None
                and isinstance(placeholder, str)
                and placeholder in _cell_text(cell_record[1])
            ):
                issues.append(
                    NotebookIssue(
                        1,
                        "COMPLETION_INCOMPLETE",
                        f"{target_id} still contains its learner placeholder",
                    )
                )

        executed_roles = ("setup", "implementation", "fixture", "check")
        for role in executed_roles:
            for _, cell_id, cell, _ in role_cells.get(role, []):
                execution_count = cell.get("execution_count")
                if not isinstance(execution_count, int) or execution_count <= 0:
                    issues.append(
                        NotebookIssue(
                            1,
                            "COMPLETION_UNEXECUTED",
                            f"{cell_id} ({role}) has not been actually executed",
                        )
                    )
                outputs = cell.get("outputs", [])
                if isinstance(outputs, list):
                    for output in outputs:
                        if not isinstance(output, dict):
                            continue
                        if output.get("output_type") == "error" or (
                            output.get("output_type") == "stream"
                            and output.get("name") == "stderr"
                            and bool(output.get("text"))
                        ):
                            issues.append(
                                NotebookIssue(
                                    1,
                                    "COMPLETION_ERROR_OUTPUT",
                                    f"{cell_id} contains an error output",
                                )
                            )

        for exercise_id in exercise_ids:
            roles = exercise_roles.get(exercise_id, {})
            implementation = roles.get("implementation", [])
            fixture = roles.get("fixture", [])
            check = roles.get("check", [])
            if not (len(implementation) == len(fixture) == len(check) == 1):
                continue
            implementation_count = implementation[0][2].get("execution_count")
            fixture_count = fixture[0][2].get("execution_count")
            check_count = check[0][2].get("execution_count")
            if all(isinstance(value, int) for value in (implementation_count, fixture_count, check_count)) and not (
                check_count > implementation_count and check_count > fixture_count
            ):
                issues.append(
                    NotebookIssue(
                        1,
                        "COMPLETION_STALE_CHECK",
                        f"{exercise_id} checker must run after its latest implementation and fixture",
                    )
                )

        if schema_version == 5:
            raw_result_cells = practice.get("result_cell_ids")
            for cell_id in raw_result_cells if isinstance(raw_result_cells, list) else []:
                cell_record = cells_by_id.get(cell_id) if isinstance(cell_id, str) else None
                if cell_record is None:
                    continue
                outputs = cell_record[1].get("outputs")
                has_observed_result = False
                if isinstance(outputs, list):
                    for output in outputs:
                        if not isinstance(output, dict) or output.get("output_type") == "error":
                            continue
                        if output.get("output_type") == "stream":
                            if output.get("name") == "stdout" and bool(output.get("text")):
                                has_observed_result = True
                        elif output.get("output_type") in {"display_data", "execute_result"}:
                            has_observed_result = bool(output.get("data"))
                if not has_observed_result:
                    issues.append(
                        NotebookIssue(
                            1,
                            "COMPLETION_RESULT_MISSING",
                            f"{cell_id} has no actual observed result output",
                        )
                    )

    return NotebookValidation(issues, source_links, setup_cells, warnings)


# Import compatibility for callers that have not yet renamed the function.
validate_notebook_v2 = validate_notebook_v3
