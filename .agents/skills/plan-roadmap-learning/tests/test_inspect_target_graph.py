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
    assert [row["target_ids"] for row in report["endpoints"]] == [
        ["TR-SYS-03", "TR-SYS-04"],
        ["TR-MOD-03", "TR-EVAL-02", "TR-EVAL-04"],
    ]
    assert report["targets"]["TR-SYS-03"]["prerequisites"] == ["CC-SYS-03"]
    assert "CC-DL-01" in report["targets"]["TR-SYS-03"]["prerequisite_closure"]
    assert report["targets"]["TR-SYS-03"]["required_evidence"] == [
        "calculate", "implement", "debug", "interpret", "design", "transfer"
    ]


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


def test_invalid_roadmap_endpoint_fails_without_writing_state(tmp_path: Path) -> None:
    roadmap = tmp_path / "ROADMAP.md"
    roadmap.write_text(
        "# Roadmap\n\n## 정적 목표 endpoint\n\n"
        "| 우선순위 | 방향 | Endpoint |\n|---:|---|---|\n"
        "| 1 | Systems | `TR-SYS-99` |\n",
        encoding="utf-8",
    )
    try:
        graph.inspect_target_graph(roadmap, REPO / "CURRICULUM.md")
    except ValueError as error:
        assert "absent from CURRICULUM" in str(error)
    else:
        raise AssertionError("invalid endpoint must fail")
    assert list(tmp_path.iterdir()) == [roadmap]
