#!/usr/bin/env python3
"""Supersede one current cycle with exact archive and preserved-practice receipts."""

from __future__ import annotations

import argparse

from daily_learning_flow import (
    DEFAULT_CURSOR_PATH,
    main as flow_main,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cursor", default=DEFAULT_CURSOR_PATH)
    parser.add_argument("--cycle-id")
    parser.add_argument("--reason", required=True)
    parser.add_argument("--replacement-cycle-id", required=True)
    parser.add_argument("--archive-path", required=True)
    parser.add_argument("--archive-sha256", required=True)
    parser.add_argument("--practice-path", required=True)
    parser.add_argument("--practice-sha256", required=True)
    parser.add_argument("--practice-layer", choices=("PRE_LAB",), required=True)
    parser.add_argument(
        "--implementation-depth",
        choices=("I1_MECHANISM",),
        required=True,
    )
    args = parser.parse_args(argv)
    command = [
        "--cursor",
        args.cursor,
        "supersede",
        "--reason",
        args.reason,
        "--replacement-cycle-id",
        args.replacement_cycle_id,
        "--archive-path",
        args.archive_path,
        "--archive-sha256",
        args.archive_sha256,
        "--practice-path",
        args.practice_path,
        "--practice-sha256",
        args.practice_sha256,
        "--practice-layer",
        args.practice_layer,
        "--implementation-depth",
        args.implementation_depth,
    ]
    if args.cycle_id:
        command.extend(["--cycle-id", args.cycle_id])
    return flow_main(command)


if __name__ == "__main__":
    raise SystemExit(main())
