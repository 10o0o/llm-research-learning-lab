#!/usr/bin/env python3
"""Atomically classify one metadata-v4 Notebook as preserved v5 PRE_LAB work.

The migration is intentionally conservative: it never grants a milestone,
never invents a creation review, and never changes ``.cells``. A v4 lesson
session is replaced only by the matching immutable cursor-v2 capture; the live
lesson handoff is not opened.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
import tempfile
from pathlib import Path

from validate_practice_notebook import (
    CAPTURED_SESSION_FIELDS,
    CYCLE_ID_RE,
    EXTERNAL_CACHE_RE,
    SHA256_RE,
    captured_session_projection_hash,
)


def _canonical_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _cells_sha256(payload: dict[str, object]) -> str:
    return hashlib.sha256(_canonical_bytes(payload.get("cells"))).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _practice_metadata(payload: dict[str, object]) -> dict[str, object]:
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError("Notebook metadata is missing")
    lab = metadata.get("llm_research_lab")
    if not isinstance(lab, dict) or not isinstance(lab.get("practice"), dict):
        raise ValueError("metadata.llm_research_lab.practice is missing")
    return lab["practice"]


def _captured_session(
    cursor: dict[str, object], cycle_id: object
) -> dict[str, object]:
    if cursor.get("schema_version") != 2:
        raise ValueError("captured-cycle migration requires cursor schema v2")
    cycles = cursor.get("cycles")
    if not isinstance(cycles, list):
        raise ValueError("cursor cycles must be a list")
    matches = [
        cycle
        for cycle in cycles
        if isinstance(cycle, dict) and cycle.get("cycle_id") == cycle_id
    ]
    if len(matches) != 1:
        raise ValueError(f"cursor must contain exactly one cycle: {cycle_id}")
    captured = matches[0].get("captured_session")
    if not isinstance(captured, dict):
        raise ValueError(f"cycle has no immutable captured_session: {cycle_id}")
    if set(captured) != set(CAPTURED_SESSION_FIELDS):
        raise ValueError("captured_session fields differ from projection schema")
    if captured.get("schema_version") not in {9, 10}:
        raise ValueError("captured_session schema_version must be 9 or 10")
    if captured.get("projection_sha256") != captured_session_projection_hash(captured):
        raise ValueError("captured_session projection_sha256 is invalid")
    evidence = captured.get("learner_evidence")
    if (
        not isinstance(evidence, list)
        or captured.get("learner_evidence_sha256")
        != hashlib.sha256(_canonical_bytes(evidence)).hexdigest()
    ):
        raise ValueError("captured_session learner_evidence_sha256 is invalid")
    return captured


def _migrate_learning_input(
    old: dict[str, object], cursor: dict[str, object] | None
) -> tuple[dict[str, object], str | None]:
    kind = old.get("kind")
    if kind == "finalized-til":
        path = old.get("path")
        sha256 = old.get("sha256")
        if not isinstance(path, str) or not isinstance(sha256, str):
            raise ValueError("finalized-til learning_input is incomplete")
        return {
            "id": "L001",
            "role": "primary",
            "kind": "finalized-til",
            "path": path,
            "sha256": sha256,
        }, None
    if kind != "lesson-session":
        raise ValueError("v4 learning_input.kind must be lesson-session or finalized-til")
    if cursor is None:
        raise ValueError("lesson-session migration requires the cursor-v2 payload")
    captured = _captured_session(cursor, old.get("cycle_id"))
    concepts = captured.get("concepts")
    evidence = captured.get("learner_evidence")
    concept_ids = [
        item.get("concept_id")
        for item in (concepts if isinstance(concepts, list) else [])
        if isinstance(item, dict) and isinstance(item.get("concept_id"), str)
    ]
    evidence_ids = [
        item.get("evidence_id")
        for item in (evidence if isinstance(evidence, list) else [])
        if isinstance(item, dict) and isinstance(item.get("evidence_id"), str)
    ]
    comparisons = {
        "cycle_id": captured.get("cycle_id"),
        "lesson_id": captured.get("lesson_id"),
        "primary_target": captured.get("primary_target"),
        "bridge_target": captured.get("bridge_target"),
        "handoff_sha256": captured.get("handoff_sha256"),
        "concept_ids": concept_ids,
        "evidence_ids": evidence_ids,
        "learner_evidence_sha256": captured.get("learner_evidence_sha256"),
    }
    mismatches = [key for key, expected in comparisons.items() if old.get(key) != expected]
    if mismatches:
        raise ValueError(
            "v4 lesson-session differs from immutable captured_session: "
            + ", ".join(mismatches)
        )
    return {
        "id": "L001",
        "role": "primary",
        "kind": "captured-cycle",
        "cycle_id": captured["cycle_id"],
        "lesson_id": captured["lesson_id"],
        "primary_target": captured["primary_target"],
        "bridge_target": captured["bridge_target"],
        "concept_ids": concept_ids,
        "evidence_ids": evidence_ids,
        "captured_session_sha256": captured["projection_sha256"],
    }, "L001"


def migrate_payload(
    payload: dict[str, object], *, cursor: dict[str, object] | None = None
) -> dict[str, object]:
    """Return a v5 payload while preserving the complete ``cells`` value."""

    migrated = copy.deepcopy(payload)
    practice = _practice_metadata(migrated)
    schema_version = practice.get("schema_version")
    if schema_version == 5:
        return migrated
    if schema_version != 4:
        raise ValueError("only practice schema v4 can be migrated to v5")
    before_cells = copy.deepcopy(migrated.get("cells"))
    before_cells_hash = _cells_sha256(migrated)
    old_input = practice.get("learning_input")
    if not isinstance(old_input, dict):
        raise ValueError("schema v4 requires learning_input")
    new_input, captured_prefix = _migrate_learning_input(old_input, cursor)

    outcomes = practice.get("outcomes")
    if not isinstance(outcomes, list):
        raise ValueError("practice outcomes must be a list")
    if captured_prefix is not None:
        for outcome in outcomes:
            if not isinstance(outcome, dict):
                continue
            for field in ("concept_ids", "evidence_ids"):
                values = outcome.get(field)
                if isinstance(values, list):
                    outcome[field] = [f"{captured_prefix}:{value}" for value in values]

    practice["schema_version"] = 5
    practice.pop("learning_input", None)
    practice["practice_layer"] = "PRE_LAB"
    practice["implementation_depth"] = "I1_MECHANISM"
    practice["lifecycle"] = "preserved_attempt"
    practice["milestone_id"] = None
    practice["milestone_definition_sha256"] = None
    practice["learning_inputs"] = [new_input]
    practice["prior_practice_evidence"] = []
    practice["creation_reviews"] = []
    practice["result_cell_ids"] = []

    if migrated.get("cells") != before_cells or _cells_sha256(migrated) != before_cells_hash:
        raise AssertionError("migration changed Notebook cells")
    return migrated


def _repo_relative_file(path: Path, repo_root: Path, *, label: str) -> str:
    resolved_repo = repo_root.resolve()
    lexical = path.absolute()
    try:
        lexical_relative = lexical.relative_to(resolved_repo)
    except ValueError as error:
        raise ValueError(f"{label} must stay inside the repository") from error
    current = resolved_repo
    for part in lexical_relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"{label} cannot use symbolic links")
    resolved = path.resolve(strict=True)
    try:
        relative = resolved.relative_to(resolved_repo)
    except ValueError as error:
        raise ValueError(f"{label} must stay inside the repository") from error
    if not resolved.is_file():
        raise ValueError(f"{label} must be a file: {relative.as_posix()}")
    return relative.as_posix()


def _archived_external_record(
    source: dict[str, object],
    *,
    archive_root: Path,
    repo_root: Path,
) -> dict[str, object] | None:
    captured_path = source.get("path")
    digest = source.get("sha256")
    cache_match = (
        EXTERNAL_CACHE_RE.fullmatch(captured_path)
        if isinstance(captured_path, str)
        else None
    )
    if cache_match is None:
        return None
    if not isinstance(digest, str) or SHA256_RE.fullmatch(digest) is None:
        raise ValueError("captured external source needs a lowercase SHA-256")
    if cache_match.group(2) != digest:
        raise ValueError("captured external source path differs from its SHA-256")
    captured_receipt_path = source.get("receipt_path")
    expected_captured_receipt = (
        f"tmp/active-lesson-sources/{cache_match.group(1)}/{digest}.receipt.json"
    )
    if captured_receipt_path != expected_captured_receipt:
        raise ValueError("captured external source receipt path is invalid")

    cache_path = archive_root / "source-cache" / Path(captured_path).name
    receipt_path = archive_root / "source-cache" / Path(captured_receipt_path).name
    cache_relative = _repo_relative_file(
        cache_path, repo_root, label="archived external source"
    )
    receipt_relative = _repo_relative_file(
        receipt_path, repo_root, label="archived external receipt"
    )
    if _file_sha256(cache_path) != digest:
        raise ValueError(f"archived external source hash does not match: {cache_relative}")
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"archived external receipt is unreadable: {receipt_relative}") from error
    if not isinstance(receipt, dict):
        raise ValueError(f"archived external receipt must be an object: {receipt_relative}")
    receipt_expected = {
        "status": "CACHED",
        "lesson_id": cache_match.group(1),
        "kind": "primary",
        "original_url": source.get("official_url"),
        "final_url": source.get("final_url"),
        "sha256": digest,
        "path": captured_path,
        "receipt_path": captured_receipt_path,
    }
    mismatches = [
        key for key, expected in receipt_expected.items() if receipt.get(key) != expected
    ]
    if receipt.get("byte_count") != cache_path.stat().st_size:
        mismatches.append("byte_count")
    if mismatches:
        raise ValueError(
            "archived external receipt differs from captured provenance: "
            + ", ".join(sorted(set(mismatches)))
        )
    required_source_fields = (
        "provider",
        "course",
        "offering_or_edition",
        "artifact",
        "scope",
    )
    missing = [
        key
        for key in required_source_fields
        if not isinstance(source.get(key), str) or not str(source[key]).strip()
    ]
    if missing:
        raise ValueError(
            "captured external source is incomplete: " + ", ".join(missing)
        )
    for key in ("media_type", "retrieved_at"):
        if not isinstance(receipt.get(key), str) or not str(receipt[key]).strip():
            raise ValueError(f"archived external receipt needs {key}")
    return {
        "kind": "external-reference",
        "provider": source["provider"],
        "course": source["course"],
        "offering_or_edition": source["offering_or_edition"],
        "artifact": source["artifact"],
        "url": source["official_url"],
        "final_url": source["final_url"],
        "media_type": receipt["media_type"],
        "scope": source["scope"],
        "cache_path": cache_relative,
        "receipt_path": receipt_relative,
        "captured_path": captured_path,
        "captured_receipt_path": captured_receipt_path,
        "retrieved_at": receipt["retrieved_at"],
        "sha256": digest,
    }


def _repair_preserved_archive_bindings(
    payload: dict[str, object],
    *,
    cursor: dict[str, object],
    repo_root: Path,
) -> dict[str, object]:
    """Bind one migrated captured attempt to its immutable archived bytes."""

    repaired = copy.deepcopy(payload)
    practice = _practice_metadata(repaired)
    if (
        practice.get("schema_version") != 5
        or practice.get("lifecycle") != "preserved_attempt"
    ):
        return repaired
    raw_inputs = practice.get("learning_inputs")
    captured_inputs = [
        item
        for item in (raw_inputs if isinstance(raw_inputs, list) else [])
        if isinstance(item, dict) and item.get("kind") == "captured-cycle"
    ]
    if not captured_inputs:
        return repaired
    if len(captured_inputs) != 1:
        raise ValueError("preserved-attempt archive repair requires one captured cycle")
    input_record = captured_inputs[0]
    captured = _captured_session(cursor, input_record.get("cycle_id"))
    expected_input = {
        "cycle_id": captured.get("cycle_id"),
        "lesson_id": captured.get("lesson_id"),
        "primary_target": captured.get("primary_target"),
        "bridge_target": captured.get("bridge_target"),
        "captured_session_sha256": captured.get("projection_sha256"),
    }
    mismatches = [
        key for key, expected in expected_input.items() if input_record.get(key) != expected
    ]
    if mismatches:
        raise ValueError(
            "v5 captured-cycle input differs from immutable captured_session: "
            + ", ".join(mismatches)
        )
    cycle_id = captured.get("cycle_id")
    if (
        not isinstance(cycle_id, str)
        or CYCLE_ID_RE.fullmatch(cycle_id) is None
        or Path(cycle_id).name != cycle_id
    ):
        raise ValueError("captured cycle_id cannot identify an archive directory")
    archive_root = repo_root / "tmp/lesson-attempts" / cycle_id
    _repo_relative_file(
        archive_root / "active-lesson-handoff.md",
        repo_root,
        label="archived lesson handoff",
    )

    raw_sources = practice.get("sources")
    if not isinstance(raw_sources, list) or not all(
        isinstance(item, dict) for item in raw_sources
    ):
        raise ValueError("preserved-attempt sources must be a list of objects")
    sources = copy.deepcopy(raw_sources)
    handoff_digest = captured.get("handoff_sha256")
    handoff_matches = [
        source
        for source in sources
        if source.get("kind") == "lesson" and source.get("sha256") == handoff_digest
    ]
    if len(handoff_matches) != 1:
        raise ValueError("preserved attempt must have exactly one captured lesson handoff source")
    archived_handoff = archive_root / "active-lesson-handoff.md"
    archived_handoff_relative = _repo_relative_file(
        archived_handoff, repo_root, label="archived lesson handoff"
    )
    if _file_sha256(archived_handoff) != handoff_digest:
        raise ValueError("archived lesson handoff hash differs from captured_session")
    handoff_matches[0]["path"] = archived_handoff_relative

    captured_sources = captured.get("source_provenance")
    if not isinstance(captured_sources, list):
        raise ValueError("captured_session source_provenance must be a list")
    next_source_number = len(sources) + 1
    for captured_source in captured_sources:
        if not isinstance(captured_source, dict):
            raise ValueError("captured source provenance must contain objects")
        archived_record = _archived_external_record(
            captured_source,
            archive_root=archive_root,
            repo_root=repo_root,
        )
        if archived_record is None:
            continue
        digest = archived_record["sha256"]
        captured_path = archived_record["captured_path"]
        archive_path = archived_record["cache_path"]
        matches = [
            source
            for source in sources
            if source.get("kind") == "external-reference"
            and source.get("sha256") == digest
            and (
                source.get("captured_path") == captured_path
                or source.get("cache_path") in {captured_path, archive_path}
            )
        ]
        if len(matches) > 1:
            raise ValueError("duplicate source records for captured external provenance")
        if matches:
            source_id = matches[0].get("id")
            if not isinstance(source_id, str):
                raise ValueError("captured external source has no stable source ID")
            replacement = {"id": source_id, **archived_record}
            sources[sources.index(matches[0])] = replacement
        else:
            sources.append({"id": f"S{next_source_number:03d}", **archived_record})
            next_source_number += 1
    practice["sources"] = sources
    return repaired


def migrate_file(
    notebook: Path,
    *,
    repo_root: Path,
    cursor_path: Path | None = None,
) -> tuple[bool, str]:
    """Atomically migrate ``notebook`` and return ``(changed, cells_sha256)``."""

    resolved_repo = repo_root.resolve()
    resolved_notebook = notebook.resolve(strict=True)
    try:
        relative = resolved_notebook.relative_to(resolved_repo)
    except ValueError as error:
        raise ValueError("Notebook must stay inside the repository") from error
    if not relative.parts or relative.parts[0] != "practice" or resolved_notebook.suffix != ".ipynb":
        raise ValueError("migration target must be one practice/*.ipynb file")

    payload = json.loads(resolved_notebook.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Notebook root must be an object")
    practice = _practice_metadata(payload)
    cells_hash = _cells_sha256(payload)
    schema_version = practice.get("schema_version")
    needs_captured_cursor = False
    if schema_version == 4:
        input_record = practice.get("learning_input")
        needs_captured_cursor = (
            isinstance(input_record, dict)
            and input_record.get("kind") == "lesson-session"
        )
    elif schema_version == 5:
        raw_inputs = practice.get("learning_inputs")
        needs_captured_cursor = (
            practice.get("lifecycle") == "preserved_attempt"
            and isinstance(raw_inputs, list)
            and any(
                isinstance(item, dict) and item.get("kind") == "captured-cycle"
                for item in raw_inputs
            )
        )
        if not needs_captured_cursor:
            return False, cells_hash
    else:
        raise ValueError("only practice schema v4 or preserved-attempt v5 can be migrated")

    if schema_version == 5 and not needs_captured_cursor:
        return False, cells_hash

    cursor: dict[str, object] | None = None
    if needs_captured_cursor:
        selected_cursor = cursor_path or resolved_repo / "tmp/active-learning-flow.json"
        loaded_cursor = json.loads(selected_cursor.read_text(encoding="utf-8"))
        if not isinstance(loaded_cursor, dict):
            raise ValueError("cursor root must be an object")
        cursor = loaded_cursor
    migrated = migrate_payload(payload, cursor=cursor)
    if cursor is not None:
        migrated = _repair_preserved_archive_bindings(
            migrated,
            cursor=cursor,
            repo_root=resolved_repo,
        )
    if migrated == payload:
        return False, cells_hash

    mode = stat.S_IMODE(resolved_notebook.stat().st_mode)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{resolved_notebook.name}.",
        suffix=".tmp",
        dir=resolved_notebook.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(migrated, stream, ensure_ascii=False, indent=1)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, resolved_notebook)
        directory_fd = os.open(resolved_notebook.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()
    rewritten = json.loads(resolved_notebook.read_text(encoding="utf-8"))
    if _cells_sha256(rewritten) != cells_hash:
        raise AssertionError("atomic migration did not preserve Notebook cells")
    return True, cells_hash


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--cursor", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    notebook = args.notebook
    if not notebook.is_absolute():
        notebook = args.repo_root / notebook
    cursor = args.cursor
    if cursor is not None and not cursor.is_absolute():
        cursor = args.repo_root / cursor
    try:
        changed, cells_hash = migrate_file(
            notebook,
            repo_root=args.repo_root,
            cursor_path=cursor,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "ERROR", "error": str(error)}, ensure_ascii=False))
        return 1
    print(
        json.dumps(
            {
                "status": "MIGRATED" if changed else "UNCHANGED",
                "path": notebook.resolve().relative_to(args.repo_root.resolve()).as_posix(),
                "cells_sha256": cells_hash,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
