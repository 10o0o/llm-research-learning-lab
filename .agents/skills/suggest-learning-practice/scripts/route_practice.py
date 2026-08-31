#!/usr/bin/env python3
"""Return the target-linked practice action and modality for a typed outcome."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


PRACTICE_ACTIONS = {
    "SESSION_REPAIR_REQUIRED",
    "TIL_REPAIR_REQUIRED",
    "CONTINUE_EXISTING_PRACTICE",
    "CREATE_LOCAL_PRACTICE",
    "PROPOSE_EXTERNAL_PRACTICE",
    "DEFER_TO_MILESTONE",
    "NO_EXTRA_PRACTICE",
}
PRACTICE_MODES = {
    "NOTEBOOK",
    "BENCHMARK",
    "DATASET_PROJECT",
    "EXTERNAL_CHALLENGE",
    "EXTERNAL_COMPETITION",
    "NONE",
}
PRACTICE_LAYERS = {
    "PRE_LAB",
    "MODULE_ASSIGNMENT",
    "PHASE_CAPSTONE",
    "NONE",
}
IMPLEMENTATION_DEPTHS = {
    "I0_NONE": 0,
    "I1_MECHANISM": 1,
    "I2_COMPONENT": 2,
    "I3_WORKFLOW": 3,
    "I4_EXPERIMENT": 4,
    "I5_RESEARCH": 5,
}
PROFILES = {
    "math-tensor-mechanism": "NOTEBOOK",
    "inference-performance": "BENCHMARK",
    "evaluation-data": "DATASET_PROJECT",
    "short-algorithm-api": "NOTEBOOK",
    "valuable-competition": "DATASET_PROJECT",
    "no-practice-capable-outcome": "NONE",
}
EXTERNAL_MODES = {
    "short-algorithm-api": "EXTERNAL_CHALLENGE",
    "valuable-competition": "EXTERNAL_COMPETITION",
}
MILESTONE_ID_RE = re.compile(r"(?:MA|PC)-[A-Z0-9][A-Z0-9-]{2,95}\Z")
MILESTONE_TABLE_COLUMNS = (
    "Milestone ID",
    "Practice layer",
    "Module IDs",
    "구현 깊이",
    "선수 Milestone ID",
    "Endpoint closure",
    "요구 산출물",
)


def _markdown_cells(line: str) -> tuple[str, ...] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return tuple(cell.strip().strip("`") for cell in stripped[1:-1].split("|"))


def _curriculum_milestone_rows(lines: list[str]) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for index, line in enumerate(lines):
        if _markdown_cells(line) != MILESTONE_TABLE_COLUMNS:
            continue
        if index + 1 >= len(lines):
            continue
        separator = _markdown_cells(lines[index + 1])
        if (
            separator is None
            or len(separator) != len(MILESTONE_TABLE_COLUMNS)
            or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator)
        ):
            continue
        for candidate in lines[index + 2 :]:
            cells = _markdown_cells(candidate)
            if cells is None or len(cells) != len(MILESTONE_TABLE_COLUMNS):
                break
            milestone_id, practice_layer = cells[:2]
            if MILESTONE_ID_RE.fullmatch(milestone_id) is not None:
                rows.append((milestone_id, practice_layer))
    return rows


def _require_curriculum_milestone(
    repo_root: Path | str,
    milestone_id: str,
    *,
    argument_name: str,
    expected_prefix: str | None = None,
) -> None:
    """Require one exact, well-formed milestone row in the current Curriculum."""

    if (
        MILESTONE_ID_RE.fullmatch(milestone_id) is None
        or (expected_prefix is not None and not milestone_id.startswith(expected_prefix))
    ):
        expected = f"a well-formed {expected_prefix}* ID" if expected_prefix else "a well-formed MA-* or PC-* ID"
        raise ValueError(
            f"{argument_name} must be {expected}"
        )
    curriculum = Path(repo_root).resolve() / "CURRICULUM.md"
    try:
        lines = curriculum.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as error:
        raise ValueError(
            f"{argument_name} requires a readable current CURRICULUM.md"
        ) from error
    expected_layer = (
        "MODULE_ASSIGNMENT" if milestone_id.startswith("MA-") else "PHASE_CAPSTONE"
    )
    matches = [
        row
        for row in _curriculum_milestone_rows(lines)
        if row == (milestone_id, expected_layer)
    ]
    if len(matches) != 1:
        raise ValueError(
            f"{argument_name} must name exactly one current Curriculum milestone"
        )


@dataclass(frozen=True)
class PracticeDecision:
    practice_action: str
    practice_mode: str
    practice_layer: str
    implementation_depth: str
    milestone_id: str | None
    reason: str
    approval_required: bool
    approval_scope: str


def route_practice(
    profile: str,
    *,
    learning_input_kind: str = "captured-cycle",
    learning_input_ready: bool = True,
    til_ready: bool | None = None,
    equivalent_evidence: bool = False,
    existing_direct_artifact: bool = False,
    existing_required_execution: bool = True,
    existing_cost_effective: bool = True,
    existing_paused: bool = False,
    conceptual_blocker: bool = False,
    external_item_verified_current: bool = False,
    external_item_valuable: bool = False,
    required_implementation_depth: str = "I1_MECHANISM",
    equivalent_implementation_depth: str | None = None,
    prelab_required: bool = False,
    module_assignment_id: str | None = None,
    module_assignment_ready: bool = False,
    module_assignment_depth: str = "I3_WORKFLOW",
    phase_capstone_id: str | None = None,
    phase_capstone_ready: bool = False,
    defer_to_milestone_id: str | None = None,
    repo_root: Path | str = ".",
) -> PracticeDecision:
    if til_ready is not None:
        learning_input_kind = "finalized-til"
        learning_input_ready = til_ready
    if learning_input_kind == "lesson-session":
        # Compatibility for v4 callers. New v5 decisions use captured-cycle.
        learning_input_kind = "captured-cycle"
    if learning_input_kind not in {"captured-cycle", "finalized-til"}:
        raise ValueError("learning_input_kind must be captured-cycle or finalized-til")
    if not learning_input_ready:
        action = (
            "SESSION_REPAIR_REQUIRED"
            if learning_input_kind == "captured-cycle"
            else "TIL_REPAIR_REQUIRED"
        )
        return PracticeDecision(
            action,
            "NONE",
            "NONE",
            "I0_NONE",
            None,
            "The exact lesson session is not current."
            if learning_input_kind == "captured-cycle"
            else "The exact finalized TIL is not ready.",
            False,
            "NONE",
        )
    if profile not in PROFILES:
        raise ValueError(f"unknown practice outcome profile: {profile}")
    if required_implementation_depth not in IMPLEMENTATION_DEPTHS:
        raise ValueError("required_implementation_depth is invalid")
    if equivalent_implementation_depth is not None and (
        equivalent_implementation_depth not in IMPLEMENTATION_DEPTHS
    ):
        raise ValueError("equivalent_implementation_depth is invalid")
    if module_assignment_depth not in IMPLEMENTATION_DEPTHS or (
        IMPLEMENTATION_DEPTHS[module_assignment_depth]
        < IMPLEMENTATION_DEPTHS["I3_WORKFLOW"]
    ):
        raise ValueError("module_assignment_depth must be I3_WORKFLOW or deeper")
    if phase_capstone_ready and not phase_capstone_id:
        raise ValueError("a ready phase capstone requires phase_capstone_id")
    if phase_capstone_id is not None:
        _require_curriculum_milestone(
            repo_root,
            phase_capstone_id,
            argument_name="phase_capstone_id",
            expected_prefix="PC-",
        )
    if module_assignment_ready and not module_assignment_id:
        raise ValueError("a ready module assignment requires module_assignment_id")
    if module_assignment_id is not None:
        _require_curriculum_milestone(
            repo_root,
            module_assignment_id,
            argument_name="module_assignment_id",
            expected_prefix="MA-",
        )
    if defer_to_milestone_id is not None:
        _require_curriculum_milestone(
            repo_root,
            defer_to_milestone_id,
            argument_name="defer_to_milestone_id",
        )

    evidence_is_equivalent = equivalent_evidence
    if evidence_is_equivalent or PROFILES[profile] == "NONE":
        return PracticeDecision(
            "NO_EXTRA_PRACTICE",
            "NONE",
            "NONE",
            "I0_NONE",
            None,
            "Equivalent implementation, execution, and interpretation evidence exists or no practice-capable outcome remains.",
            False,
            "NONE",
        )
    local_mode = PROFILES[profile]
    if phase_capstone_ready:
        selected_layer = "PHASE_CAPSTONE"
        selected_depth = "I5_RESEARCH"
        selected_milestone = phase_capstone_id
    elif module_assignment_ready:
        selected_layer = "MODULE_ASSIGNMENT"
        selected_depth = module_assignment_depth
        selected_milestone = module_assignment_id
    elif prelab_required or conceptual_blocker:
        selected_layer = "PRE_LAB"
        selected_depth = "I1_MECHANISM"
        selected_milestone = None
    elif defer_to_milestone_id:
        return PracticeDecision(
            "DEFER_TO_MILESTONE",
            "NONE",
            "NONE",
            "I0_NONE",
            defer_to_milestone_id,
            "No pre-lab blocker remains; preserve this session for the named cumulative milestone instead of creating another micro-practice.",
            False,
            "NONE",
        )
    else:
        selected_layer = "NONE"
        selected_depth = "I0_NONE"
        selected_milestone = None
    if (
        existing_direct_artifact
        and existing_required_execution
        and existing_cost_effective
        and not existing_paused
        and not conceptual_blocker
    ):
        return PracticeDecision(
            "CONTINUE_EXISTING_PRACTICE",
            local_mode,
            selected_layer,
            selected_depth,
            selected_milestone,
            "A directly target-linked artifact still needs the selected evidence.",
            False,
            "NONE",
        )
    external_mode = EXTERNAL_MODES.get(profile)
    if (
        external_mode is not None
        and external_item_verified_current
        and external_item_valuable
    ):
        return PracticeDecision(
            "PROPOSE_EXTERNAL_PRACTICE",
            external_mode,
            selected_layer,
            selected_depth,
            selected_milestone,
            "Propose the exact current, valuable external item; account access, participation, and submission remain unapproved.",
            True,
            "ACCOUNT_ACCESS_PARTICIPATION_SUBMISSION",
        )
    if selected_layer == "NONE":
        raise ValueError(
            "practice routing needs an explicit blocker, a ready module/capstone, "
            "or defer_to_milestone_id; blockerless work must not create a micro-practice"
        )
    return PracticeDecision(
        "CREATE_LOCAL_PRACTICE",
        local_mode,
        selected_layer,
        selected_depth,
        selected_milestone,
        "Create one unexecuted local Notebook; no exact current external item with material value has been verified.",
        False,
        "NONE",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", choices=sorted(PROFILES))
    parser.add_argument(
        "--learning-input-kind",
        choices=("captured-cycle", "finalized-til", "lesson-session"),
        default="captured-cycle",
    )
    parser.add_argument("--learning-input-not-ready", action="store_true")
    parser.add_argument("--til-not-ready", action="store_true")
    parser.add_argument("--equivalent-evidence", action="store_true")
    parser.add_argument("--existing-direct-artifact", action="store_true")
    parser.add_argument("--existing-evidence-complete", action="store_true")
    parser.add_argument("--existing-low-value", action="store_true")
    parser.add_argument("--existing-paused", action="store_true")
    parser.add_argument("--conceptual-blocker", action="store_true")
    parser.add_argument("--external-item-verified-current", action="store_true")
    parser.add_argument("--external-item-valuable", action="store_true")
    parser.add_argument(
        "--required-implementation-depth",
        choices=sorted(IMPLEMENTATION_DEPTHS),
        default="I1_MECHANISM",
    )
    parser.add_argument(
        "--equivalent-implementation-depth",
        choices=sorted(IMPLEMENTATION_DEPTHS),
    )
    parser.add_argument("--prelab-required", action="store_true")
    parser.add_argument(
        "--no-prelab-required",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument("--module-assignment-id")
    parser.add_argument("--module-assignment-ready", action="store_true")
    parser.add_argument(
        "--module-assignment-depth",
        choices=sorted(IMPLEMENTATION_DEPTHS),
        default="I3_WORKFLOW",
    )
    parser.add_argument("--phase-capstone-id")
    parser.add_argument("--phase-capstone-ready", action="store_true")
    parser.add_argument("--defer-to-milestone-id")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        decision = route_practice(
            args.profile,
            learning_input_kind=args.learning_input_kind,
            learning_input_ready=not (
                args.learning_input_not_ready or args.til_not_ready
            ),
            equivalent_evidence=args.equivalent_evidence,
            existing_direct_artifact=args.existing_direct_artifact,
            existing_required_execution=not args.existing_evidence_complete,
            existing_cost_effective=not args.existing_low_value,
            existing_paused=args.existing_paused,
            conceptual_blocker=args.conceptual_blocker,
            external_item_verified_current=args.external_item_verified_current,
            external_item_valuable=args.external_item_valuable,
            required_implementation_depth=args.required_implementation_depth,
            equivalent_implementation_depth=args.equivalent_implementation_depth,
            prelab_required=args.prelab_required and not args.no_prelab_required,
            module_assignment_id=args.module_assignment_id,
            module_assignment_ready=args.module_assignment_ready,
            module_assignment_depth=args.module_assignment_depth,
            phase_capstone_id=args.phase_capstone_id,
            phase_capstone_ready=args.phase_capstone_ready,
            defer_to_milestone_id=args.defer_to_milestone_id,
            repo_root=args.repo_root,
        )
    except ValueError as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps(asdict(decision), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
