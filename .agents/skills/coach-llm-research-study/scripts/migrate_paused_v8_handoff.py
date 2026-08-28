#!/usr/bin/env python3
"""Replace one legacy v8 handoff with an independently prepared paused v9 handoff.

The helper does not invent a v9 Module Plan.  It verifies a supplied current
contract, preserves every learner-content byte and evidence verdict, and then
atomically replaces the ignored operational handoff.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_lesson_handoff import validate_handoff  # noqa: E402


class MigrationError(RuntimeError):
    """Raised when a legacy handoff cannot be replaced without evidence drift."""


def _single_field(data: bytes, name: bytes) -> bytes:
    matches = re.findall(rb"(?m)^- " + re.escape(name) + rb": ([^\r\n]+)$", data)
    if len(matches) != 1:
        raise MigrationError(f"legacy handoff must contain exactly one {name.decode()} field")
    return matches[0]


def _learner_blocks(data: bytes) -> tuple[bytes, ...]:
    opening = b"<!-- learner-content:start -->\n"
    closing = b"\n<!-- learner-content:end -->"
    blocks: list[bytes] = []
    cursor = 0
    while True:
        start = data.find(opening, cursor)
        if start < 0:
            break
        body_start = start + len(opening)
        end = data.find(closing, body_start)
        if end < 0:
            raise MigrationError("learner-content markers are unbalanced")
        blocks.append(data[body_start:end])
        cursor = end + len(closing)
    return tuple(blocks)


def _evidence_verdicts(data: bytes) -> tuple[tuple[bytes, bytes], ...]:
    blocks = re.findall(
        rb"(?ms)^<!-- learner-evidence:(E\d{3,}):start -->\n(.*?)^<!-- learner-evidence:\1:end -->$",
        data,
    )
    result: list[tuple[bytes, bytes]] = []
    for evidence_id, body in blocks:
        verdicts = re.findall(rb"(?m)^- verdict: ([^\r\n]+)$", body)
        if len(verdicts) != 1:
            raise MigrationError(f"{evidence_id.decode()} must have one verdict")
        result.append((evidence_id, verdicts[0]))
    return tuple(result)


def _atomic_write(path: Path, payload: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        old_mode = path.stat().st_mode & 0o777 if path.exists() else 0o600
        os.fchmod(descriptor, old_mode)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def migrate_paused_v8_handoff(
    legacy_path: Path | str,
    replacement_path: Path | str,
    *,
    repo_root: Path | str,
) -> None:
    root = Path(repo_root).resolve()
    legacy = Path(legacy_path)
    replacement = Path(replacement_path)
    if not legacy.is_absolute():
        legacy = root / legacy
    if not replacement.is_absolute():
        replacement = root / replacement
    old = legacy.read_bytes()
    new = replacement.read_bytes()
    if _single_field(old, b"schema_version") != b"8":
        raise MigrationError("migration source must be schema v8")
    if _single_field(new, b"schema_version") != b"9":
        raise MigrationError("replacement must be schema v9")
    if _single_field(old, b"lesson_id") != _single_field(new, b"lesson_id"):
        raise MigrationError("replacement lesson_id differs from the legacy handoff")
    if _single_field(new, b"status") != b"paused":
        raise MigrationError("replacement must preserve unresolved learning as paused")
    old_blocks = _learner_blocks(old)
    new_blocks = _learner_blocks(new)
    if old_blocks != new_blocks:
        raise MigrationError("replacement changes learner-content bytes or their order")
    if _evidence_verdicts(old) != _evidence_verdicts(new):
        raise MigrationError("replacement changes learner evidence verdicts")
    report = validate_handoff(replacement, repo_root=root)
    if not report.ok:
        detail = "; ".join(f"{item.code}: {item.message}" for item in report.errors)
        raise MigrationError("replacement v9 handoff is invalid: " + detail)
    _atomic_write(legacy, new)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("legacy", type=Path)
    parser.add_argument("replacement", type=Path)
    args = parser.parse_args(argv)
    try:
        root = next(
            candidate
            for candidate in Path(__file__).resolve().parents
            if (candidate / "AGENTS.md").is_file()
        )
        migrate_paused_v8_handoff(args.legacy, args.replacement, repo_root=root)
    except (OSError, StopIteration, MigrationError) as error:
        print(f"ERROR {args.legacy}:1 [MIGRATION] {error}", file=sys.stderr)
        return 1
    print(f"OK {args.legacy} [v8-to-v9-paused]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
