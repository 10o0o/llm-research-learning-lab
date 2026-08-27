#!/usr/bin/env python3
"""Mechanically migrate practice audit metadata v2 to v3 without changing cells."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import tempfile
from pathlib import Path


CURRICULUM_ID_RE = re.compile(r"(?:CC|TR)-[A-Z]+-\d{2}\Z")
PRACTICE_MODES = {"NOTEBOOK", "BENCHMARK", "DATASET_PROJECT"}


def parse_outcome_target(raw: str) -> tuple[str, list[str]]:
    if "=" not in raw:
        raise ValueError("outcome mapping must use O##=CC-AREA-NN[,CC-AREA-NN]")
    outcome_id, raw_targets = (part.strip() for part in raw.split("=", 1))
    targets = [item.strip() for item in raw_targets.split(",") if item.strip()]
    if not re.fullmatch(r"O\d{2}", outcome_id):
        raise ValueError(f"invalid Outcome ID: {outcome_id}")
    if not targets or len(targets) != len(set(targets)) or any(
        CURRICULUM_ID_RE.fullmatch(target) is None for target in targets
    ):
        raise ValueError(f"invalid curriculum targets for {outcome_id}")
    return outcome_id, targets


def migrate_payload(
    payload: dict[str, object],
    *,
    practice_mode: str,
    outcome_targets: dict[str, list[str]],
) -> dict[str, object]:
    if practice_mode not in PRACTICE_MODES:
        raise ValueError(f"invalid local practice mode: {practice_mode}")
    before_cells = copy.deepcopy(payload.get("cells"))
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError("Notebook metadata is missing")
    lab = metadata.get("llm_research_lab")
    if not isinstance(lab, dict) or not isinstance(lab.get("practice"), dict):
        raise ValueError("metadata.llm_research_lab.practice is missing")
    practice: dict[str, object] = lab["practice"]
    if practice.get("schema_version") != 2:
        raise ValueError("only practice schema v2 can be migrated by this script")

    outcomes = practice.get("outcomes")
    if not isinstance(outcomes, list) or not all(isinstance(item, dict) for item in outcomes):
        raise ValueError("v2 outcomes must be a list of objects")
    observed_outcomes = [str(item.get("id")) for item in outcomes]
    if set(observed_outcomes) != set(outcome_targets):
        missing = sorted(set(observed_outcomes) - set(outcome_targets))
        extra = sorted(set(outcome_targets) - set(observed_outcomes))
        raise ValueError(
            "outcome target mapping mismatch"
            + (f"; missing {', '.join(missing)}" if missing else "")
            + (f"; unknown {', '.join(extra)}" if extra else "")
        )

    sources = practice.get("sources")
    if not isinstance(sources, list) or not all(isinstance(item, dict) for item in sources):
        raise ValueError("v2 sources must be a list of objects")
    source_id_by_path: dict[str, str] = {}
    for index, source in enumerate(sources, start=1):
        source_id = f"S{index:03d}"
        path = source.get("path")
        if not isinstance(path, str) or path in source_id_by_path:
            raise ValueError(f"source[{index - 1}] has a missing or duplicate path")
        source_id_by_path[path] = source_id
        source["id"] = source_id

    requirements = practice.get("requirements")
    if not isinstance(requirements, list) or not all(isinstance(item, dict) for item in requirements):
        raise ValueError("v2 requirements must be a list of objects")
    for requirement in requirements:
        locations = requirement.get("source_locations")
        if not isinstance(locations, list):
            raise ValueError(f"{requirement.get('id')} source_locations must be a list")
        for location in locations:
            if not isinstance(location, dict):
                raise ValueError(f"{requirement.get('id')} has an invalid source location")
            path = location.pop("path", None)
            source_id = source_id_by_path.get(path) if isinstance(path, str) else None
            if source_id is None:
                raise ValueError(f"{requirement.get('id')} references an unlisted source path: {path}")
            location["source_id"] = source_id

    artifact_targets: list[str] = []
    for outcome in outcomes:
        outcome_id = str(outcome["id"])
        targets = list(outcome_targets[outcome_id])
        outcome["curriculum_target_ids"] = targets
        for target in targets:
            if target not in artifact_targets:
                artifact_targets.append(target)

    practice["schema_version"] = 3
    practice["practice_mode"] = practice_mode
    practice["curriculum_targets"] = artifact_targets
    if payload.get("cells") != before_cells:
        raise AssertionError("migration changed Notebook cells")
    return payload


def _atomic_write(path: Path, payload: dict[str, object]) -> None:
    serialized = (json.dumps(payload, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".practice-v3-", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--practice-mode", choices=sorted(PRACTICE_MODES), required=True)
    parser.add_argument(
        "--outcome-target",
        action="append",
        required=True,
        help="O##=CC-AREA-NN[,CC-AREA-NN] (repeat for every Outcome)",
    )
    parser.add_argument("--write", action="store_true", help="atomically replace only metadata in the Notebook JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        mappings = dict(parse_outcome_target(item) for item in args.outcome_target)
        if len(mappings) != len(args.outcome_target):
            raise ValueError("duplicate Outcome mapping")
        payload = json.loads(args.notebook.read_text(encoding="utf-8"))
        migrated = migrate_payload(
            payload,
            practice_mode=args.practice_mode,
            outcome_targets=mappings,
        )
        if args.write:
            _atomic_write(args.notebook, migrated)
    except (OSError, ValueError, json.JSONDecodeError, AssertionError) as error:
        print(f"ERROR: {error}")
        return 1
    action = "migrated" if args.write else "validated migration for"
    print(f"OK: {action} {args.notebook}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
