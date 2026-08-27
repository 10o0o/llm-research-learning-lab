from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
SCRIPT = SKILL / "scripts/inspect_target_graph.py"

SPEC = importlib.util.spec_from_file_location("inspect_target_graph_under_test", SCRIPT)
assert SPEC and SPEC.loader
graph = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = graph
SPEC.loader.exec_module(graph)


def test_roadmap_endpoints_resolve_and_have_valid_closures() -> None:
    report = graph.inspect_target_graph(REPO / "ROADMAP.md", REPO / "CURRICULUM.md")
    assert [
        (row["priority"], row["stage"], row["target_id"])
        for row in report["endpoints"]
    ] == [
        (1, "1A", "TR-SYS-03"),
        (1, "1B", "TR-SYS-04"),
        (2, "2A", "TR-MOD-03"),
        (2, "2B", "TR-EVAL-02"),
        (2, "2C", "TR-EVAL-04"),
    ]
    assert report["targets"]["TR-SYS-03"]["prerequisites"] == ["CC-SYS-03"]
    assert "CC-DL-01" in report["targets"]["TR-SYS-03"]["prerequisite_closure"]
    assert report["targets"]["TR-SYS-03"]["required_evidence"] == [
        "calculate", "implement", "debug", "interpret", "design", "transfer"
    ]


def test_route_edges_downstream_counts_and_endpoint_membership_are_static() -> None:
    report = graph.inspect_target_graph(REPO / "ROADMAP.md", REPO / "CURRICULUM.md")
    route = report["routes"]["TR-SYS-04"]
    assert route["route_nodes"][-1] == "TR-SYS-04"
    assert {"prerequisite": "TR-SYS-03", "target": "TR-SYS-04"} in route["edges"]
    assert route["downstream_count"]["TR-SYS-03"] == 1
    assert route["downstream_count"]["TR-SYS-04"] == 0
    assert report["endpoint_membership"]["TR-SYS-03"] == [
        "TR-SYS-03",
        "TR-SYS-04",
    ]
    assert report["endpoint_membership"]["TR-DATA-01"] == []


def test_ephemeral_states_expose_frontier_without_inventing_missing_evidence() -> None:
    initial = graph.inspect_target_graph(REPO / "ROADMAP.md", REPO / "CURRICULUM.md")
    route_nodes = initial["routes"]["TR-SYS-03"]["route_nodes"]
    states = {target_id: "satisfied" for target_id in route_nodes}
    states["CC-SYS-03"] = "blocking"
    states["TR-SYS-03"] = "unknown"
    states["CC-SYS-01"] = "bridgeable"
    report = graph.inspect_target_graph(
        REPO / "ROADMAP.md",
        REPO / "CURRICULUM.md",
        target_states=states,
    )
    route = report["routes"]["TR-SYS-03"]
    candidates = {item["target_id"]: item for item in route["frontier_candidates"]}
    assert candidates["CC-SYS-03"]["state"] == "blocking"
    assert candidates["CC-SYS-03"]["prerequisite_states"]["CC-SYS-01"] == "bridgeable"
    assert "TR-SYS-03" not in candidates
    assert route["unclassified_nodes"] == []

    partial = graph.inspect_target_graph(
        REPO / "ROADMAP.md",
        REPO / "CURRICULUM.md",
        target_states={"CC-MATH-01": "satisfied"},
    )
    partial_route = partial["routes"]["TR-SYS-03"]
    assert "CC-DL-01" in partial_route["unclassified_nodes"]
    assert partial_route["target_states"]["CC-DL-01"] == "unknown"
    assert partial_route["target_states"]["CC-MATH-01"] == "satisfied"
    assert any(
        item["state"] == "unknown"
        for item in partial_route["frontier_candidates"]
    )


def test_snapshot_exposes_planner_fields_and_direct_source_state() -> None:
    report = graph.inspect_target_graph(
        REPO / "ROADMAP.md", REPO / "CURRICULUM.md", ["CC-PROB-01"]
    )
    target = report["targets"]["CC-PROB-01"]
    assert target["depth"] == "D2"
    assert target["prerequisites"] == ["CC-MATH-01"]
    assert target["required_evidence"] == [
        "explain", "calculate", "implement", "interpret"
    ]
    assert target["direct_source_ids"] == ["SRC-HARV-STAT110-2E-00-01"]


def test_json_cli_can_inspect_one_target() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--json", "--target", "TR-EVAL-02"],
        check=False,
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert set(payload["targets"]) == {"TR-EVAL-02"}
    assert payload["targets"]["TR-EVAL-02"]["coverage"] == "없음"


def test_json_cli_accepts_repeatable_ephemeral_states() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--json",
            "--state",
            "CC-MATH-01=satisfied",
            "--state",
            "CC-DL-01=unknown",
        ],
        check=False,
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert "CC-DL-01" not in payload["routes"]["TR-SYS-03"]["unclassified_nodes"]


def test_invalid_roadmap_endpoint_fails_without_writing_state(tmp_path: Path) -> None:
    roadmap = tmp_path / "ROADMAP.md"
    roadmap.write_text(
        "# Roadmap\n\n## 정적 목표 endpoint\n\n"
        "| 우선순위 | 단계 | 방향 | Endpoint |\n|---:|---:|---|---|\n"
        "| 1 | `1A` | Systems | `TR-SYS-99` |\n",
        encoding="utf-8",
    )
    try:
        graph.inspect_target_graph(roadmap, REPO / "CURRICULUM.md")
    except ValueError as error:
        assert "absent from CURRICULUM" in str(error)
    else:
        raise AssertionError("invalid endpoint must fail")
    assert list(tmp_path.iterdir()) == [roadmap]


def test_endpoint_stage_format_order_and_uniqueness_are_enforced() -> None:
    prefix = (
        "# Roadmap\n\n## 정적 목표 endpoint\n\n"
        "| 우선순위 | 단계 | 방향 | Endpoint |\n|---:|---:|---|---|\n"
    )
    invalid_rows = (
        "| 1 | `2A` | Systems | `TR-SYS-03` |\n",
        "| 1 | `1B` | Systems | `TR-SYS-03` |\n| 1 | `1A` | Systems | `TR-SYS-04` |\n",
        "| 1 | `1A` | Systems | `TR-SYS-03` |\n| 1 | `1B` | Systems | `TR-SYS-03` |\n",
    )
    for rows in invalid_rows:
        try:
            graph.parse_roadmap_endpoints(prefix + rows)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid endpoint rows passed: {rows}")
