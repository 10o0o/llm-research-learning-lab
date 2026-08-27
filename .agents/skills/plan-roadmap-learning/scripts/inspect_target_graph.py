#!/usr/bin/env python3
"""Inspect static ROADMAP endpoints and their CURRICULUM prerequisite closure."""

from __future__ import annotations

import argparse
import importlib.util
import json
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
COACH_SCRIPTS = CURRICULUM_VALIDATOR.parent
if str(COACH_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(COACH_SCRIPTS))

from target_graph import (  # noqa: E402
    PREREQUISITE_STATES,
    build_endpoint_graph,
    parse_roadmap_endpoints,
    prerequisite_closure,
)


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


def inspect_target_graph(
    roadmap_path: Path,
    curriculum_path: Path,
    requested_targets: list[str] | None = None,
    target_states: dict[str, str] | None = None,
) -> dict[str, Any]:
    validator = _load_curriculum_validator()
    findings = validator.validate_curriculum(curriculum_path)
    if findings:
        rendered = "; ".join(finding.render() for finding in findings[:5])
        raise ValueError(f"CURRICULUM validation failed: {rendered}")

    snapshot = validator.curriculum_snapshot_from_text(
        curriculum_path.read_text(encoding="utf-8")
    )
    endpoints = parse_roadmap_endpoints(roadmap_path.read_text(encoding="utf-8"))
    endpoint_ids = [row["target_id"] for row in endpoints]
    routes, endpoint_membership = build_endpoint_graph(
        endpoints, snapshot.targets, target_states
    )

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
            "prerequisite_closure": prerequisite_closure(target_id, snapshot.targets),
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
        "routes": routes,
        "endpoint_membership": endpoint_membership,
        "targets": target_details,
    }


def render_text(report: dict[str, Any]) -> str:
    lines = ["Static ROADMAP endpoints"]
    for row in report["endpoints"]:
        lines.append(
            f"{row['stage']} {row['direction']}: {row['target_id']}"
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
    lines.append("")
    lines.append("Endpoint routes")
    for endpoint_id, route in report["routes"].items():
        candidates = route["frontier_candidates"]
        rendered_candidates = (
            "not computed"
            if candidates is None
            else ", ".join(
                f"{item['target_id']}[{item['state']}; downstream={item['downstream_count']}]"
                for item in candidates
            )
            or "none"
        )
        lines.extend(
            (
                f"{route['stage']} {endpoint_id}",
                f"  route nodes: {', '.join(route['route_nodes'])}",
                f"  frontier candidates: {rendered_candidates}",
                f"  unclassified: {', '.join(route['unclassified_nodes']) or 'none'}",
            )
        )
    return "\n".join(lines)


def _parse_states(values: list[str]) -> dict[str, str] | None:
    if not values:
        return None
    parsed: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError("--state must use TARGET=STATE")
        target_id, state = value.split("=", 1)
        if target_id in parsed:
            raise ValueError(f"duplicate --state target: {target_id}")
        if state not in PREREQUISITE_STATES:
            raise ValueError(f"invalid prerequisite state: {value}")
        parsed[target_id] = state
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roadmap", type=Path, default=DEFAULT_ROADMAP)
    parser.add_argument("--curriculum", type=Path, default=DEFAULT_CURRICULUM)
    parser.add_argument(
        "--target", action="append", default=[], help="inspect only this target (repeatable)"
    )
    parser.add_argument(
        "--state",
        action="append",
        default=[],
        metavar="TARGET=STATE",
        help="supply an ephemeral prerequisite state (repeatable)",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = inspect_target_graph(
            args.roadmap,
            args.curriculum,
            args.target or None,
            _parse_states(args.state),
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
