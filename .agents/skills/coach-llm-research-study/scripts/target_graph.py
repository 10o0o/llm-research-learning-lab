"""Pure helpers for ROADMAP endpoint and Curriculum prerequisite graphs."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any


ENDPOINT_HEADING = "## 정적 목표 endpoint"
ENDPOINT_HEADER = ("우선순위", "단계", "방향", "Endpoint")
TARGET_RE = re.compile(r"(?:CC|TR)-[A-Z]+-\d{2}\Z")
STAGE_RE = re.compile(r"([1-9]\d*)([A-Z])\Z")
PREREQUISITE_STATES = {"satisfied", "bridgeable", "blocking", "unknown"}


def _split_row(line: str) -> tuple[str, ...] | None:
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


def _unwrap_code(value: str) -> str:
    stripped = value.strip()
    if stripped.startswith("`") and stripped.endswith("`"):
        return stripped[1:-1].strip()
    return stripped


def parse_roadmap_endpoints(text: str) -> list[dict[str, Any]]:
    """Parse the sole ordered endpoint table from ROADMAP Markdown."""
    lines = text.splitlines()
    headings = [index for index, line in enumerate(lines) if line == ENDPOINT_HEADING]
    if len(headings) != 1:
        raise ValueError(
            f"{ENDPOINT_HEADING!r} must appear exactly once; found {len(headings)}"
        )
    section_start = headings[0] + 1
    section_end = next(
        (
            index
            for index in range(section_start, len(lines))
            if lines[index].startswith("## ")
        ),
        len(lines),
    )
    header_indexes = [
        index
        for index in range(section_start, section_end)
        if _split_row(lines[index]) == ENDPOINT_HEADER
    ]
    if len(header_indexes) != 1:
        raise ValueError(
            f"endpoint table header must appear exactly once; found {len(header_indexes)}"
        )
    header_index = header_indexes[0]
    if header_index + 1 >= section_end or not _is_separator(
        _split_row(lines[header_index + 1]), len(ENDPOINT_HEADER)
    ):
        raise ValueError("endpoint table separator is missing or invalid")

    endpoints: list[dict[str, Any]] = []
    cursor = header_index + 2
    previous_order: tuple[int, str] | None = None
    seen_stages: set[str] = set()
    seen_targets: set[str] = set()
    while cursor < section_end:
        cells = _split_row(lines[cursor])
        if cells is None:
            break
        if len(cells) != len(ENDPOINT_HEADER):
            raise ValueError(f"endpoint row {cursor + 1} must have 4 cells")
        try:
            priority = int(cells[0])
        except ValueError as error:
            raise ValueError(
                f"endpoint row {cursor + 1} has invalid priority {cells[0]!r}"
            ) from error
        stage = _unwrap_code(cells[1])
        stage_match = STAGE_RE.fullmatch(stage)
        if priority <= 0 or stage_match is None or int(stage_match.group(1)) != priority:
            raise ValueError(
                f"endpoint row {cursor + 1} has invalid stage {stage!r} for priority {priority}"
            )
        order = (priority, stage_match.group(2))
        if previous_order is not None and order <= previous_order:
            raise ValueError("endpoint stages must be strictly ordered by priority and letter")
        previous_order = order
        if stage in seen_stages:
            raise ValueError(f"duplicate endpoint stage: {stage}")
        seen_stages.add(stage)
        direction = cells[2].strip()
        if not direction:
            raise ValueError(f"endpoint row {cursor + 1} has an empty direction")
        target_id = _unwrap_code(cells[3])
        if TARGET_RE.fullmatch(target_id) is None:
            raise ValueError(f"endpoint row {cursor + 1} has invalid target ID")
        if target_id in seen_targets:
            raise ValueError(f"an endpoint target appears more than once: {target_id}")
        seen_targets.add(target_id)
        endpoints.append(
            {
                "priority": priority,
                "stage": stage,
                "direction": direction,
                "target_id": target_id,
                "roadmap_line": cursor + 1,
            }
        )
        cursor += 1

    if not endpoints:
        raise ValueError("endpoint table has no data rows")
    return endpoints


def prerequisite_closure(
    target_id: str,
    targets: Mapping[str, Any],
    *,
    visiting: tuple[str, ...] = (),
) -> list[str]:
    """Return prerequisites in stable ancestor-before-dependent order."""
    if target_id in visiting:
        chain = " -> ".join((*visiting, target_id))
        raise ValueError(f"prerequisite cycle: {chain}")
    if target_id not in targets:
        raise ValueError(f"unknown target: {target_id}")
    ordered: list[str] = []
    for prerequisite in targets[target_id].prerequisites:
        if prerequisite not in targets:
            raise ValueError(f"{target_id} has unknown prerequisite {prerequisite}")
        for ancestor in prerequisite_closure(
            prerequisite,
            targets,
            visiting=(*visiting, target_id),
        ):
            if ancestor not in ordered:
                ordered.append(ancestor)
        if prerequisite not in ordered:
            ordered.append(prerequisite)
    return ordered


def _downstream_counts(
    route_nodes: list[str],
    edges: list[dict[str, str]],
) -> dict[str, int]:
    dependents: dict[str, set[str]] = {target_id: set() for target_id in route_nodes}
    for edge in edges:
        dependents[edge["prerequisite"]].add(edge["target"])

    def descendants(target_id: str) -> set[str]:
        result: set[str] = set()
        frontier = list(dependents[target_id])
        while frontier:
            dependent = frontier.pop()
            if dependent in result:
                continue
            result.add(dependent)
            frontier.extend(dependents[dependent])
        return result

    return {target_id: len(descendants(target_id)) for target_id in route_nodes}


def build_endpoint_graph(
    endpoints: list[dict[str, Any]],
    targets: Mapping[str, Any],
    target_states: Mapping[str, str] | None = None,
) -> tuple[dict[str, dict[str, Any]], dict[str, list[str]]]:
    """Build deterministic route facts and optional evidence-state frontiers."""
    if target_states is not None:
        unknown_ids = sorted(set(target_states) - set(targets))
        if unknown_ids:
            raise ValueError(f"state has unknown target: {', '.join(unknown_ids)}")
        invalid_states = sorted(
            f"{target_id}={state}"
            for target_id, state in target_states.items()
            if state not in PREREQUISITE_STATES
        )
        if invalid_states:
            raise ValueError(f"invalid prerequisite state: {', '.join(invalid_states)}")

    routes: dict[str, dict[str, Any]] = {}
    membership: dict[str, list[str]] = {target_id: [] for target_id in targets}
    for endpoint in endpoints:
        endpoint_id = endpoint["target_id"]
        if endpoint_id not in targets:
            raise ValueError(f"ROADMAP endpoint is absent from CURRICULUM: {endpoint_id}")
        route_nodes = [*prerequisite_closure(endpoint_id, targets), endpoint_id]
        route_set = set(route_nodes)
        edges = [
            {"prerequisite": prerequisite, "target": target_id}
            for target_id in route_nodes
            for prerequisite in targets[target_id].prerequisites
            if prerequisite in route_set
        ]
        downstream_count = _downstream_counts(route_nodes, edges)
        for target_id in route_nodes:
            membership[target_id].append(endpoint_id)

        if target_states is None:
            effective_states = {target_id: "unknown" for target_id in route_nodes}
            unclassified_nodes = route_nodes.copy()
            frontier_candidates: list[dict[str, Any]] | None = None
        else:
            unclassified_nodes = [
                target_id for target_id in route_nodes if target_id not in target_states
            ]
            effective_states = {
                target_id: target_states.get(target_id, "unknown")
                for target_id in route_nodes
            }
            frontier_candidates = []
            for target_id in route_nodes:
                state = effective_states[target_id]
                if state == "satisfied":
                    continue
                prerequisite_states = {
                    prerequisite: effective_states[prerequisite]
                    for prerequisite in targets[target_id].prerequisites
                }
                if all(
                    prerequisite_state in {"satisfied", "bridgeable"}
                    for prerequisite_state in prerequisite_states.values()
                ):
                    frontier_candidates.append(
                        {
                            "target_id": target_id,
                            "state": state,
                            "downstream_count": downstream_count[target_id],
                            "prerequisite_states": prerequisite_states,
                        }
                    )
            frontier_candidates.sort(
                key=lambda item: (
                    -item["downstream_count"],
                    targets[item["target_id"]].line,
                )
            )

        routes[endpoint_id] = {
            "priority": endpoint["priority"],
            "stage": endpoint["stage"],
            "direction": endpoint["direction"],
            "route_nodes": route_nodes,
            "edges": edges,
            "downstream_count": downstream_count,
            "target_states": effective_states,
            "frontier_candidates": frontier_candidates,
            "unclassified_nodes": unclassified_nodes,
        }

    return routes, membership
