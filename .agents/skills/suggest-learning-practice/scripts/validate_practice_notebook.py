#!/usr/bin/env python3
"""Validate guided-fading Notebook practice backed by audit metadata v2."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote


ACTIONS = {"implement", "test", "debug", "interpret", "design"}
REQUIREMENT_KINDS = {"source-given", "practice-given", "derive"}
REQUIREMENT_OWNERS = {"provided", "learner"}
TARGET_KINDS = {"code", "debug", "prediction", "design", "interpretation"}
SCAFFOLD_STAGES = {"guided", "partial", "independent"}
SOURCE_KINDS = {"course-index", "lesson", "instructor-practice", "reference"}
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
EXERCISE_ID_RE = re.compile(r"E\d{2}\Z")
REQUIREMENT_ID_RE = re.compile(r"C-(E\d{2})-(\d{2})\Z")
TARGET_ID_RE = re.compile(r"T-(E\d{2})-(\d{2})\Z")
CELL_ID_RE = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
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


def validate_notebook_v2(
    notebook: Path,
    repo: Path,
    *,
    learner_state: bool = False,
) -> NotebookValidation:
    issues: list[NotebookIssue] = []
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
    if schema_version != 2:
        message = (
            "practice schema v1 must be deliberately migrated to v2; token lists cannot be reused as claims"
            if schema_version == 1
            else "practice schema_version must be 2"
        )
        return NotebookValidation([NotebookIssue(1, "SCHEMA_MIGRATION", message)], set(), [])
    if practice.get("artifact_kind") != "standalone-practice":
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "artifact_kind must be standalone-practice"))
    if practice.get("scaffold_mode") != "guided-fading":
        issues.append(NotebookIssue(1, "AUDIT_METADATA", "scaffold_mode must be guided-fading"))

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

    til_path = _validate_hash_record(issues, record=practice.get("til"), repo=repo, label="til")
    if til_path is not None:
        source_links.add(til_path)
        if TIL_RE.fullmatch(til_path) is None:
            issues.append(NotebookIssue(1, "SOURCE_AUDIT", "til path must name one finalized dated TIL"))

    raw_sources = practice.get("sources")
    if not isinstance(raw_sources, list):
        issues.append(NotebookIssue(1, "SOURCE_AUDIT", "sources must be a list"))
        raw_sources = []
    source_records = [item for item in raw_sources if isinstance(item, dict)]
    listed_source_paths = {
        item.get("path") for item in source_records if isinstance(item.get("path"), str)
    }
    valid_source_paths: set[str] = set()
    for index, record in enumerate(raw_sources):
        path = _validate_hash_record(issues, record=record, repo=repo, label=f"source[{index}]")
        if path is not None:
            if path in valid_source_paths:
                issues.append(NotebookIssue(1, "SOURCE_AUDIT", f"duplicate source path: {path}"))
            valid_source_paths.add(path)
            source_links.add(path)
        if not isinstance(record, dict):
            continue
        kind = record.get("kind")
        if kind not in SOURCE_KINDS:
            issues.append(NotebookIssue(1, "SOURCE_AUDIT", f"source[{index}] has invalid kind: {kind}"))
        if kind == "instructor-practice":
            if record.get("variant") not in {"basic", "advanced", "single"}:
                issues.append(NotebookIssue(1, "SOURCE_AUDIT", f"source[{index}] needs a valid practice variant"))
            related = record.get("related_lesson")
            if not isinstance(related, str) or related not in listed_source_paths:
                issues.append(NotebookIssue(1, "SOURCE_AUDIT", f"source[{index}] needs a listed related_lesson"))

    raw_outcomes = practice.get("outcomes")
    outcomes: dict[str, dict[str, object]] = {}
    outcome_order: list[str] = []
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
        if not isinstance(item.get("til_location"), str) or not item["til_location"].strip():
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{outcome_id} needs til_location"))
        if not isinstance(item.get("required_evidence"), str) or not item["required_evidence"].strip():
            issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{outcome_id} needs required_evidence"))
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
            raw_path = location.get("path")
            if raw_path not in valid_source_paths:
                issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{requirement_id} source location is not a listed source"))
                continue
            if not isinstance(location.get("locator"), str) or not location["locator"].strip():
                issues.append(NotebookIssue(1, "AUDIT_METADATA", f"{requirement_id} source location needs locator"))
            anchor = location.get("anchor")
            if not isinstance(anchor, str) or not anchor.strip():
                issues.append(NotebookIssue(1, "SOURCE_ANCHOR", f"{requirement_id} source location needs anchor"))
            elif isinstance(raw_path, str):
                if raw_path not in source_text_cache:
                    try:
                        source_text_cache[raw_path] = _normalized((repo / raw_path).read_text(encoding="utf-8"))
                    except (OSError, UnicodeDecodeError):
                        source_text_cache[raw_path] = ""
                if _normalized(anchor) not in source_text_cache[raw_path]:
                    issues.append(NotebookIssue(1, "SOURCE_ANCHOR", f"{requirement_id} anchor does not occur in {raw_path}"))
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

    return NotebookValidation(issues, source_links, setup_cells)
