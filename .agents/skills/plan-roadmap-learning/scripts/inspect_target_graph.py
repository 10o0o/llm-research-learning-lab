#!/usr/bin/env python3
"""Inspect static ROADMAP endpoints and their CURRICULUM prerequisite closure."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_ROADMAP = REPO_ROOT / "ROADMAP.md"
DEFAULT_CURRICULUM = REPO_ROOT / "CURRICULUM.md"
CURRICULUM_VALIDATOR = (
    REPO_ROOT
    / ".agents/skills/coach-llm-research-study/scripts/validate_curriculum.py"
)
ENDPOINT_HEADING = "## 정적 목표 endpoint"
ENDPOINT_HEADER = ("우선순위", "방향", "Endpoint")
TARGET_RE = re.compile(r"(?:CC|TR)-[A-Z]+-\d{2}\Z")


def _load_curriculum_validator():
    spec = importlib.util.spec_from_file_location(
        "target_graph_curriculum_validator", CURRICULUM_VALIDATOR
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load curriculum validator: {CURRICULUM_VALIDATOR}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _split_row(line: str) -> tuple[str, ...] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return tuple(cell.strip() for cell in stripped[1:-1].split("|"))


def _unwrap_code(value: str) -> str:
    stripped = value.strip()
    if stripped.startswith("`") and stripped.endswith("`"):
        return stripped[1:-1].strip()
    return stripped


def parse_endpoints(text: str) -> list[dict[str, Any]]:
    """Parse the one normative endpoint table from ROADMAP text."""
    lines = text.splitlines()
    heading_indexes = [i for i, line in enumerate(lines) if line == ENDPOINT_HEADING]
    if len(heading_indexes) != 1:
        raise ValueError(
            f"{ENDPOINT_HEADING!r} must appear exactly once; found {len(heading_indexes)}"
        )

    heading_index = heading_indexes[0]
    header_indexes = [
        i
        for i in range(heading_index + 1, len(lines))
        if _split_row(lines[i]) == ENDPOINT_HEADER
    ]
    header_indexes = [i for i in header_indexes if not lines[i].startswith("## ")]
    if not header_indexes:
        raise ValueError("endpoint table is missing")
    header_index = header_indexes[0]
    if header_index + 1 >= len(lines):
        raise ValueError("endpoint table separator is missing")

    endpoints: list[dict[str, Any]] = []
    cursor = header_index + 2
    while cursor < len(lines):
        cells = _split_row(lines[cursor])
        if cells is None:
            break
        if len(cells) != 3:
            raise ValueError(f"endpoint row {cursor + 1} must have 3 cells")
        try:
            priority = int(cells[0])
        except ValueError as error:
            raise ValueError(
                f"endpoint row {cursor + 1} has invalid priority {cells[0]!r}"
            ) from error
        target_ids = tuple(
            _unwrap_code(item) for item in cells[2].split(",") if item.strip()
        )
        if not target_ids or any(not TARGET_RE.fullmatch(item) for item in target_ids):
            raise ValueError(f"endpoint row {cursor + 1} has invalid target IDs")
        endpoints.append(
            {
                "priority": priority,
                "direction": cells[1],
                "target_ids": list(target_ids),
                "roadmap_line": cursor + 1,
            }
        )
        cursor += 1

    if not endpoints:
        raise ValueError("endpoint table has no data rows")
    flattened = [target for row in endpoints for target in row["target_ids"]]
    if len(flattened) != len(set(flattened)):
        raise ValueError("an endpoint target appears more than once")
    return endpoints


def _closure(
    target_id: str,
    targets: dict[str, Any],
    *,
    visiting: tuple[str, ...] = (),
) -> list[str]:
    if target_id in visiting:
        chain = " -> ".join((*visiting, target_id))
        raise ValueError(f"prerequisite cycle: {chain}")
    target = targets[target_id]
    ordered: list[str] = []
    for prerequisite in target.prerequisites:
        if prerequisite not in targets:
            raise ValueError(f"{target_id} has unknown prerequisite {prerequisite}")
        for ancestor in _closure(
            prerequisite, targets, visiting=(*visiting, target_id)
        ):
            if ancestor not in ordered:
                ordered.append(ancestor)
        if prerequisite not in ordered:
            ordered.append(prerequisite)
    return ordered


def inspect_target_graph(
    roadmap_path: Path,
    curriculum_path: Path,
    requested_targets: list[str] | None = None,
) -> dict[str, Any]:
    validator = _load_curriculum_validator()
    findings = validator.validate_curriculum(curriculum_path)
    if findings:
        rendered = "; ".join(finding.render() for finding in findings[:5])
        raise ValueError(f"CURRICULUM validation failed: {rendered}")

    snapshot = validator.curriculum_snapshot_from_text(
        curriculum_path.read_text(encoding="utf-8")
    )
    endpoints = parse_endpoints(roadmap_path.read_text(encoding="utf-8"))
    endpoint_ids = [target for row in endpoints for target in row["target_ids"]]
    missing = [target for target in endpoint_ids if target not in snapshot.targets]
    if missing:
        raise ValueError(f"ROADMAP endpoint is absent from CURRICULUM: {', '.join(missing)}")

    selected_ids = requested_targets or endpoint_ids
    unknown = [target for target in selected_ids if target not in snapshot.targets]
    if unknown:
        raise ValueError(f"unknown target: {', '.join(unknown)}")

    target_details: dict[str, Any] = {}
    for target_id in selected_ids:
        target = snapshot.targets[target_id]
        target_details[target_id] = {
            "depth": target.depth,
            "prerequisites": list(target.prerequisites),
            "prerequisite_closure": _closure(target_id, snapshot.targets),
            "required_evidence": list(target.required_evidence),
            "coverage": target.coverage,
            "gap_action": target.gap_action,
            "direct_source_ids": list(target.direct_source_ids),
            "direct_source_paths": sorted(target.direct_source_paths),
            "curriculum_line": target.line,
        }

    return {
        "roadmap": str(roadmap_path),
        "curriculum": str(curriculum_path),
        "endpoints": endpoints,
        "targets": target_details,
    }


def render_text(report: dict[str, Any]) -> str:
    lines = ["Static ROADMAP endpoints"]
    for row in report["endpoints"]:
        lines.append(
            f"P{row['priority']} {row['direction']}: {', '.join(row['target_ids'])}"
        )
    lines.append("")
    for target_id, target in report["targets"].items():
        lines.extend(
            (
                f"{target_id} ({target['depth']})",
                f"  prerequisites: {', '.join(target['prerequisites']) or 'none'}",
                f"  closure: {', '.join(target['prerequisite_closure']) or 'none'}",
                f"  required evidence: {', '.join(target['required_evidence'])}",
                f"  source state: coverage={target['coverage']}; gap={target['gap_action']}",
                f"  direct sources: {', '.join(target['direct_source_ids']) or 'none'}",
            )
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roadmap", type=Path, default=DEFAULT_ROADMAP)
    parser.add_argument("--curriculum", type=Path, default=DEFAULT_CURRICULUM)
    parser.add_argument(
        "--target", action="append", default=[], help="inspect only this target (repeatable)"
    )
    parser.add_argument("--json", action="store_true", help="emit JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = inspect_target_graph(
            args.roadmap, args.curriculum, args.target or None
        )
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
