#!/usr/bin/env python3
"""Return the target-linked practice action and modality for a typed outcome."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


PRACTICE_ACTIONS = {
    "TIL_REPAIR_REQUIRED",
    "CONTINUE_EXISTING_PRACTICE",
    "CREATE_LOCAL_PRACTICE",
    "PROPOSE_EXTERNAL_PRACTICE",
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


@dataclass(frozen=True)
class PracticeDecision:
    practice_action: str
    practice_mode: str
    reason: str
    approval_required: bool
    approval_scope: str


def route_practice(
    profile: str,
    *,
    til_ready: bool = True,
    equivalent_evidence: bool = False,
    existing_direct_artifact: bool = False,
    existing_required_execution: bool = True,
    existing_cost_effective: bool = True,
    existing_paused: bool = False,
    conceptual_blocker: bool = False,
    external_item_verified_current: bool = False,
    external_item_valuable: bool = False,
) -> PracticeDecision:
    if not til_ready:
        return PracticeDecision(
            "TIL_REPAIR_REQUIRED",
            "NONE",
            "The exact finalized TIL is not ready.",
            False,
            "NONE",
        )
    if profile not in PROFILES:
        raise ValueError(f"unknown practice outcome profile: {profile}")
    if equivalent_evidence or PROFILES[profile] == "NONE":
        return PracticeDecision(
            "NO_EXTRA_PRACTICE",
            "NONE",
            "Equivalent implementation, execution, and interpretation evidence exists or no practice-capable outcome remains.",
            False,
            "NONE",
        )
    local_mode = PROFILES[profile]
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
            "Propose the exact current, valuable external item; account access, participation, and submission remain unapproved.",
            True,
            "ACCOUNT_ACCESS_PARTICIPATION_SUBMISSION",
        )
    return PracticeDecision(
        "CREATE_LOCAL_PRACTICE",
        local_mode,
        "Create one unexecuted local Notebook; no exact current external item with material value has been verified.",
        False,
        "NONE",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", choices=sorted(PROFILES))
    parser.add_argument("--til-not-ready", action="store_true")
    parser.add_argument("--equivalent-evidence", action="store_true")
    parser.add_argument("--existing-direct-artifact", action="store_true")
    parser.add_argument("--existing-evidence-complete", action="store_true")
    parser.add_argument("--existing-low-value", action="store_true")
    parser.add_argument("--existing-paused", action="store_true")
    parser.add_argument("--conceptual-blocker", action="store_true")
    parser.add_argument("--external-item-verified-current", action="store_true")
    parser.add_argument("--external-item-valuable", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        decision = route_practice(
            args.profile,
            til_ready=not args.til_not_ready,
            equivalent_evidence=args.equivalent_evidence,
            existing_direct_artifact=args.existing_direct_artifact,
            existing_required_execution=not args.existing_evidence_complete,
            existing_cost_effective=not args.existing_low_value,
            existing_paused=args.existing_paused,
            conceptual_blocker=args.conceptual_blocker,
            external_item_verified_current=args.external_item_verified_current,
            external_item_valuable=args.external_item_valuable,
        )
    except ValueError as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps(asdict(decision), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
