#!/usr/bin/env python3
"""Notebook을 토큰 낭비 없이 읽기 위한 뷰어.

Notebook을 파일로 직접 읽으면 저장된 그림이 base64로 딸려 온다. 이 저장소의
보관본 하나는 그것만으로 17만 토큰이 넘는다. 이 스크립트는 셀 source와 텍스트
출력만 보여 주고 그림은 자리 표시자로 줄인다.

    python3 scripts/nbpeek.py main.ipynb                 # 전체 개요
    python3 scripts/nbpeek.py main.ipynb --cells 3-7,12  # 해당 셀만
    python3 scripts/nbpeek.py main.ipynb --list          # 셀 목록 한 줄씩
    python3 scripts/nbpeek.py main.ipynb --no-output     # source만
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MAX_OUTPUT_CHARS = 2000


def parse_cell_spec(spec: str) -> set[int]:
    """`3-7,12` 같은 문자열을 셀 번호 집합으로 바꾼다."""
    wanted: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, _, end = part.partition("-")
            wanted.update(range(int(start), int(end) + 1))
        else:
            wanted.add(int(part))
    return wanted


def join(value) -> str:
    return "".join(value) if isinstance(value, list) else str(value)


def clip(text: str, limit: int = MAX_OUTPUT_CHARS) -> str:
    if len(text) <= limit:
        return text
    return f"{text[:limit]}\n... [{len(text) - limit} chars 생략]"


def render_outputs(cell: dict) -> list[str]:
    lines: list[str] = []
    for output in cell.get("outputs", []):
        kind = output.get("output_type")
        if kind == "stream":
            lines.append(clip(join(output.get("text", ""))))
        elif kind == "error":
            name = output.get("ename", "Error")
            value = output.get("evalue", "")
            lines.append(f"{name}: {value}")
            traceback = output.get("traceback") or []
            if traceback:
                lines.append(clip("\n".join(traceback)))
        elif kind in {"execute_result", "display_data"}:
            data = output.get("data", {})
            if "text/plain" in data:
                lines.append(clip(join(data["text/plain"])))
            for mime, payload in data.items():
                if mime.startswith("image/"):
                    size = len(join(payload))
                    lines.append(f"[{mime} 출력 생략, base64 {size // 1000}KB]")
    return lines


def summarize(path: Path) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = notebook.get("cells", [])
    print(f"{path}  cells={len(cells)}")
    for index, cell in enumerate(cells):
        source = "".join(cell.get("source", []))
        first = next((line for line in source.splitlines() if line.strip()), "")
        marker = "*" if cell.get("outputs") else " "
        print(f"[{index:>3}]{marker} {cell.get('cell_type', '?'):<8} {first[:88]}")
    print("\n* = 저장된 출력 있음.  --cells 로 필요한 셀만 열어 보세요.")


def show(path: Path, wanted: set[int] | None, with_output: bool) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = notebook.get("cells", [])
    for index, cell in enumerate(cells):
        if wanted is not None and index not in wanted:
            continue
        source = "".join(cell.get("source", []))
        print(f"\n===== cell [{index}] {cell.get('cell_type', '?')} =====")
        print(source.rstrip() or "(비어 있음)")
        if not with_output:
            continue
        rendered = render_outputs(cell)
        if rendered:
            print("--- output ---")
            for line in rendered:
                print(line.rstrip())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("notebook", type=Path)
    parser.add_argument("--cells", help="예: 3-7,12. 생략하면 전체")
    parser.add_argument("--list", action="store_true", help="셀 목록만 한 줄씩")
    parser.add_argument("--no-output", action="store_true", help="source만 보기")
    args = parser.parse_args(argv)

    if not args.notebook.is_file():
        parser.error(f"파일이 없습니다: {args.notebook}")

    if args.list:
        summarize(args.notebook)
        return 0

    wanted = parse_cell_spec(args.cells) if args.cells else None
    show(args.notebook, wanted, with_output=not args.no_output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
