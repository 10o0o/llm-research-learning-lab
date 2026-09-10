"""Copy saved notebook bytes; reset only against an existing verified copy.

This does not execute code, assess learning, write notes, change STATE, or use Git.
The caller must finish note validation before invoking --reset. Close/save the
notebook before reset: filesystem checks cannot lock a Jupyter editor's kernel.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile


def _digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _notebook(raw: bytes) -> dict:
    try:
        notebook = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise ValueError("Invalid notebook JSON") from exc
    if not isinstance(notebook, dict) or notebook.get("nbformat") != 4:
        raise ValueError("Expected a version 4 notebook object")
    if (not isinstance(notebook.get("metadata"), dict)
            or not isinstance(notebook.get("cells"), list)
            or type(notebook.get("nbformat_minor")) is not int):
        raise ValueError("Invalid notebook metadata, cells, or version")
    for cell in notebook["cells"]:
        if not isinstance(cell, dict) or cell.get("cell_type") not in {"code", "markdown", "raw"}:
            raise ValueError("Invalid notebook cell")
        source = cell.get("source")
        if not (isinstance(source, str) or
                isinstance(source, list) and all(isinstance(line, str) for line in source)):
            raise ValueError("Invalid cell source")
        if not isinstance(cell.get("metadata"), dict):
            raise ValueError("Invalid cell metadata")
        if cell["cell_type"] == "code":
            if not isinstance(cell.get("outputs"), list) or "execution_count" not in cell:
                raise ValueError("Invalid code cell outputs or execution count")
            count = cell["execution_count"]
            if count is not None and type(count) is not int:
                raise ValueError("Invalid execution count")
    return notebook


def _empty(notebook: dict) -> bool:
    return all(
        not "".join(cell["source"]).strip()
        and not cell.get("outputs") and not cell.get("attachments")
        and cell.get("execution_count") is None
        for cell in notebook["cells"]
    )


def _blank_bytes(notebook: dict) -> bytes:
    blank = dict(notebook)
    blank["cells"] = [{
        "cell_type": "code", "id": "workspace", "metadata": {},
        "source": [], "outputs": [], "execution_count": None,
    }]
    return (json.dumps(blank, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def archive_notebook(source: Path, archive: Path, expected_sha256: str, *, reset: bool = False) -> str:
    if not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise ValueError("Expected a lowercase SHA-256 of the inspected source")
    if source.suffix != ".ipynb" or archive.suffix != ".ipynb":
        raise ValueError("Source and archive must be .ipynb files")
    if source.is_symlink() or archive.is_symlink():
        raise ValueError("Source and archive must not be symlinks")
    if source.resolve() == archive.resolve() or archive.exists() and source.samefile(archive):
        raise ValueError("Source and archive must be different files")
    raw = source.read_bytes()
    notebook = _notebook(raw)

    if reset:
        if not archive.is_file():
            raise ValueError("Reset requires an existing verified archive")
        archived = archive.read_bytes()
        original = _notebook(archived)
        if _digest(archived) != expected_sha256:
            raise ValueError("The archive does not match the expected original")
        if _empty(notebook):
            if raw == _blank_bytes(original):
                return "already_reset"
            raise ValueError("Source changed; empty workspace does not match this archive")
    if _digest(raw) != expected_sha256:
        raise ValueError("Source changed since inspection; inspect it again before continuing")
    if _empty(notebook):
        return "empty_source"

    if reset:
        if archived != raw:
            raise ValueError("Source and archive differ")
        payload = _blank_bytes(notebook)
        destination = source
    else:
        if archive.exists():
            if archive.read_bytes() == raw:
                return "already_archived"
            raise ValueError("Archive has different content; refusing to overwrite it")
        payload = raw
        destination = archive

    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=".chapter-", delete=False) as f:
            temp_path = Path(f.name)
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(temp_path, stat.S_IMODE(source.stat().st_mode))
        if temp_path.read_bytes() != payload:
            raise OSError("Temporary copy verification failed")
        if source.read_bytes() != raw:
            raise ValueError("Source changed while preparing the operation")
        if reset:
            if archive.read_bytes() != raw:
                raise ValueError("Verified archive changed before reset")
            os.replace(temp_path, source)
            return "reset"
        # Publishing a complete file with link() fails if the target appeared
        # concurrently. Unlike replace(), it cannot overwrite an older chapter.
        os.link(temp_path, archive)
        if archive.read_bytes() != raw:
            raise OSError("Archive verification failed; source was preserved")
        return "archived"
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--reset", action="store_true", help="Reset only after notes are validated")
    args = parser.parse_args()
    try:
        result = archive_notebook(args.source, args.archive, args.expected_sha256, reset=args.reset)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Not completed: {exc}\n")
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
