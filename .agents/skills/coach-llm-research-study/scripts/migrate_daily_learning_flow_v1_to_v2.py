#!/usr/bin/env python3
"""Atomically and idempotently migrate the daily cursor from schema v1 to v2."""

from __future__ import annotations

import argparse

from daily_learning_flow import DEFAULT_CURSOR_PATH, main as flow_main


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cursor", default=DEFAULT_CURSOR_PATH)
    args = parser.parse_args(argv)
    return flow_main(["--cursor", args.cursor, "migrate-v1-to-v2"])


if __name__ == "__main__":
    raise SystemExit(main())
