#!/usr/bin/env python3
"""Validate creation-ready or learner-state single-Notebook practice.

Legacy bundles can be reviewed only with an explicit compatibility flag.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from validate_practice_index import validate as validate_index
from validate_practice_notebook import validate_notebook_v2


ACTIONS = {"implement", "test", "debug", "interpret", "design"}
COVERAGE_COLUMNS = ("Outcome ID", "TIL location", "Practice action", "Artifact/Exercise", "Required evidence")
EXERCISE_SECTIONS = (
    "실제 사용 맥락",
    "실행 전 회상·예측",
    "작은 유사 사례와 계약",
    "구현",
    "테스트와 실패 진단",
    "결과 해석",
)
TIL_RE = re.compile(r"til/\d{4}/\d{2}/\d{4}-\d{2}-\d{2}\.md\Z")

@dataclass(frozen=True)
class Problem:
    path: Path
    line: int
    code: str
    message: str

    def render(self) -> str:
        return f"ERROR {self.path.as_posix()}:{self.line} [{self.code}] {self.message}"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _line(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _table_rows(markdown: str) -> tuple[list[tuple[int, list[str]]], list[Problem]]:
    problems: list[Problem] = []
    heading = re.search(r"^## Practice Coverage Map[ \t]*$", markdown, re.MULTILINE)
    if heading is None:
        return [], problems
    region = markdown[heading.end() :]
    next_heading = re.search(r"^## ", region, re.MULTILINE)
    if next_heading:
        region = region[: next_heading.start()]
    lines = region.splitlines()
    header_index = next((index for index, raw in enumerate(lines) if raw.strip().startswith("|")), None)
    if header_index is None:
        return [], problems
    header = [part.strip() for part in lines[header_index].strip()[1:-1].split("|")]
    if tuple(header) != COVERAGE_COLUMNS:
        return [], problems
    rows: list[tuple[int, list[str]]] = []
    base = _line(markdown, heading.end())
    for index, raw in enumerate(lines[header_index + 2 :], start=header_index + 2):
        stripped = raw.strip()
        if not stripped:
            continue
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [part.strip().strip("`") for part in stripped[1:-1].split("|")]
        rows.append((base + index, cells))
    return rows, problems


def _cell_text(cell: dict[str, object]) -> str:
    source = cell.get("source", [])
    if isinstance(source, str):
        return source
    if isinstance(source, list) and all(isinstance(item, str) for item in source):
        return "".join(source)
    return ""


def _resolve_link(notebook: Path, target: str, repo: Path) -> tuple[Path | None, str | None]:
    target = unquote(target.split("#", 1)[0].strip())
    if not target or target.startswith(("http://", "https://", "mailto:")) or "<" in target or ">" in target:
        return None, None
    candidate = notebook.parent / target
    try:
        resolved = candidate.resolve(strict=False)
        resolved.relative_to(repo)
    except (OSError, ValueError):
        return None, "link escapes the repository"
    if not candidate.exists():
        return resolved, "link target does not exist"
    return resolved, None


def _validate_notebook(
    notebook: Path,
    repo: Path,
) -> tuple[list[Problem], set[str], list[tuple[int, str]], dict[str, set[str]]]:
    problems: list[Problem] = []
    try:
        payload = json.loads(notebook.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [Problem(notebook, getattr(exc, "lineno", 1), "NOTEBOOK_JSON", f"invalid Notebook JSON: {exc}")], set(), [], {}
    if payload.get("nbformat") != 4 or not isinstance(payload.get("cells"), list):
        return [Problem(notebook, 1, "NOTEBOOK_JSON", "Notebook must use nbformat 4 and contain cells")], set(), [], {}

    cells: list[dict[str, object]] = payload["cells"]
    markdown_cells: list[tuple[int, str]] = []
    setup_cells: list[tuple[int, str]] = []
    todo_cell_indexes: list[int] = []
    previous_markdown = ""
    for index, cell in enumerate(cells):
        if not isinstance(cell, dict):
            problems.append(Problem(notebook, 1, "NOTEBOOK_JSON", f"cell {index} is not an object"))
            continue
        text = _cell_text(cell)
        if cell.get("cell_type") == "markdown":
            markdown_cells.append((index, text))
            previous_markdown = text
        elif cell.get("cell_type") == "code":
            if cell.get("execution_count") is not None or cell.get("outputs") not in ([], None):
                problems.append(Problem(notebook, 1, "EXECUTED", f"code cell {index} contains execution state or output"))
            todo_ids = re.findall(r"TODO:\s*(E\d{2})", text)
            if todo_ids:
                todo_cell_indexes.append(index)
            if re.search(r"^# setup-check(?:\s|:|$)", text, re.MULTILINE):
                setup_cells.append((index, text))
            for exercise_id in todo_ids:
                if f"<summary>힌트 1" not in previous_markdown or f"<summary>힌트 2" not in previous_markdown:
                    problems.append(
                        Problem(notebook, 1, "HINT_ADJACENCY", f"{exercise_id} implementation cell needs Hint 1 and Hint 2 in the immediately preceding Markdown cell")
                    )

    if setup_cells and todo_cell_indexes and setup_cells[0][0] > min(todo_cell_indexes):
        problems.append(Problem(notebook, 1, "IMPORT_SETUP", "setup-check cell must precede every learner TODO"))

    markdown = "\n".join(text for _, text in markdown_cells)
    if re.search(r"^#{1,6} (?:전역 |점진적 )?힌트", markdown, re.MULTILINE):
        problems.append(Problem(notebook, 1, "GLOBAL_HINT", "global hint sections are not allowed; put folded hints beside each TODO"))
    if re.search(r"^#{1,6}\s+.*(?:모범답안|완성 답안|Solution|Answer)\b", markdown, re.MULTILINE | re.IGNORECASE):
        problems.append(Problem(notebook, 1, "SOLUTION", "learner-facing solution or answer section is not allowed"))

    links = re.findall(r"\[[^\]]+\]\((?:<([^>]+)>|([^\s)]+))\)", markdown)
    resolved_links: set[Path] = set()
    for wrapped, bare in links:
        target = wrapped or bare
        resolved, error = _resolve_link(notebook, target, repo)
        if error:
            problems.append(Problem(notebook, 1, "BROKEN_LINK", f"{error}: {target}"))
        elif resolved is not None:
            resolved_links.add(resolved)
    til_links = [path for path in resolved_links if TIL_RE.fullmatch(path.relative_to(repo).as_posix())]
    if len(til_links) != 1:
        problems.append(Problem(notebook, 1, "TIL_LINK", "Notebook must link exactly one finalized dated TIL"))

    coverage_rows, _ = _table_rows(markdown)
    coverage_heading = "## Practice Coverage Map" in markdown
    if not coverage_heading:
        problems.append(Problem(notebook, 1, "COVERAGE", "missing Practice Coverage Map"))
    table_header = f"| {' | '.join(COVERAGE_COLUMNS)} |"
    if coverage_heading and table_header not in markdown:
        problems.append(Problem(notebook, 1, "COVERAGE", f"coverage columns must be: {' | '.join(COVERAGE_COLUMNS)}"))
    if not coverage_rows:
        problems.append(Problem(notebook, 1, "COVERAGE", "Practice Coverage Map must contain at least one outcome"))
    outcome_ids: list[str] = []
    referenced_exercises: set[str] = set()
    for line_no, row in coverage_rows:
        if len(row) != 5:
            problems.append(Problem(notebook, line_no, "COVERAGE", "coverage row must have five cells"))
            continue
        outcome_id, til_location, action, artifact, evidence = row
        outcome_ids.append(outcome_id)
        if not til_location or not evidence:
            problems.append(Problem(notebook, line_no, "COVERAGE", f"{outcome_id} needs a TIL location and required evidence"))
        if action not in ACTIONS:
            problems.append(Problem(notebook, line_no, "COVERAGE", f"invalid practice action: {action}"))
        exercise_ids = set(re.findall(r"E\d{2}", artifact))
        if not exercise_ids:
            problems.append(Problem(notebook, line_no, "COVERAGE", f"{outcome_id} must name at least one exercise ID"))
        referenced_exercises.update(exercise_ids)
    expected_outcomes = [f"O{index:02d}" for index in range(1, len(outcome_ids) + 1)]
    if outcome_ids != expected_outcomes:
        problems.append(Problem(notebook, 1, "COVERAGE", "Outcome IDs must be contiguous O01, O02, ..."))

    exercise_matches = list(re.finditer(r"^## (E\d{2})\.\s+.+$", markdown, re.MULTILINE))
    exercise_ids = [match.group(1) for match in exercise_matches]
    if exercise_ids != [f"E{index:02d}" for index in range(1, len(exercise_ids) + 1)] or not exercise_ids:
        problems.append(Problem(notebook, 1, "EXERCISE", "exercise IDs must be contiguous headings: ## E01. ..."))
    if set(exercise_ids) != referenced_exercises:
        problems.append(Problem(notebook, 1, "COVERAGE", "coverage map and exercise headings must reference the same exercise set"))
    for index, match in enumerate(exercise_matches):
        exercise_id = match.group(1)
        end = exercise_matches[index + 1].start() if index + 1 < len(exercise_matches) else len(markdown)
        body = markdown[match.end() : end]
        positions = [body.find(f"### {heading}") for heading in EXERCISE_SECTIONS]
        if any(position < 0 for position in positions) or positions != sorted(positions):
            problems.append(Problem(notebook, _line(markdown, match.start()), "EXERCISE", f"{match.group(1)} needs the ordered authentic-task sections"))
        else:
            for section_index, heading in enumerate(EXERCISE_SECTIONS):
                content_start = positions[section_index] + len(f"### {heading}")
                content_end = positions[section_index + 1] if section_index + 1 < len(positions) else len(body)
                content = body[content_start:content_end].strip()
                if not content:
                    problems.append(Problem(notebook, _line(markdown, match.start()), "EXERCISE", f"{match.group(1)} section is empty: {heading}"))
        exercise_line = _line(markdown, match.start())
        if body.count("<summary>힌트 1") != 1 or body.count("<summary>힌트 2") != 1:
            problems.append(Problem(notebook, exercise_line, "HINT_ADJACENCY", f"{exercise_id} needs exactly one folded Hint 1 and Hint 2"))
        if f"TODO: {exercise_id}" not in "\n".join(_cell_text(cell) for cell in cells if cell.get("cell_type") == "code"):
            problems.append(Problem(notebook, exercise_line, "STARTER", f"{exercise_id} needs a learner TODO code cell"))

    return problems, {path.relative_to(repo).as_posix() for path in resolved_links}, setup_cells, {}


def _validate_notebook_setup(
    notebook: Path,
    setup_cells: list[tuple[int, str]],
    *,
    repo: Path,
) -> list[Problem]:
    if len(setup_cells) != 1:
        return [Problem(notebook, 1, "IMPORT_SETUP", "practice Notebook needs exactly one # setup-check code cell")]
    cell_index, setup_code = setup_cells[0]
    if "TODO:" in setup_code:
        return [Problem(notebook, 1, "IMPORT_SETUP", "setup-check cell must not contain a learner TODO")]
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    command = [sys.executable, "-c", setup_code]
    if (repo / "pyproject.toml").is_file():
        command = ["uv", "run", "python", "-c", setup_code]
    try:
        result = subprocess.run(
            command,
            cwd=repo,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [Problem(notebook, 1, "IMPORT_SETUP", f"setup-check cell could not run: {exc}")]
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().splitlines()
        summary = detail[-1] if detail else f"exit {result.returncode}"
        return [Problem(notebook, 1, "IMPORT_SETUP", f"setup-check cell {cell_index} failed from repository root: {summary}")]
    return []


def _validate_bundle_notebook_ergonomics(
    notebook: Path,
    setup_cells: list[tuple[int, str]],
) -> list[Problem]:
    problems: list[Problem] = []
    try:
        payload = json.loads(notebook.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return problems
    cells = payload.get("cells", [])
    if not isinstance(cells, list):
        return problems

    if len(setup_cells) == 1:
        _, setup_code = setup_cells[0]
        if re.search(r"\bglobals\s*\(", setup_code):
            problems.append(
                Problem(
                    notebook,
                    1,
                    "DYNAMIC_GLOBALS",
                    "bundle setup must use an explicit module alias instead of globals()",
                )
            )
        if not re.search(r"^def refresh_core\s*\(", setup_code, re.MULTILINE):
            problems.append(
                Problem(notebook, 1, "BUNDLE_REFRESH", "setup-check must define refresh_core()")
            )
        if not re.search(r"^def run_exercise_tests\s*\(", setup_code, re.MULTILINE):
            problems.append(
                Problem(
                    notebook,
                    1,
                    "EXERCISE_TEST",
                    "setup-check must define run_exercise_tests(exercise_id)",
                )
            )

    todo_cells: dict[str, list[tuple[int, str]]] = {}
    test_cells: dict[str, list[tuple[int, str]]] = {}
    for index, cell in enumerate(cells):
        if not isinstance(cell, dict) or cell.get("cell_type") != "code":
            continue
        text = _cell_text(cell)
        for exercise_id in re.findall(r"TODO:\s*(E\d{2})", text):
            todo_cells.setdefault(exercise_id, []).append((index, text))
        for exercise_id in re.findall(
            r"^# test-check:\s*(E\d{2})\s*$", text, re.MULTILINE
        ):
            test_cells.setdefault(exercise_id, []).append((index, text))

    for exercise_id, matches in sorted(todo_cells.items()):
        if len(matches) != 1:
            problems.append(
                Problem(
                    notebook,
                    1,
                    "EXERCISE_FIXTURE",
                    f"{exercise_id} needs exactly one learner TODO cell",
                )
            )
            continue
        _, todo_code = matches[0]
        fixture_marker = rf"^# provided-fixture:\s*{re.escape(exercise_id)}\s*$"
        if not re.search(fixture_marker, todo_code, re.MULTILINE):
            problems.append(
                Problem(
                    notebook,
                    1,
                    "EXERCISE_FIXTURE",
                    f"{exercise_id} TODO must include # provided-fixture: {exercise_id}",
                )
            )
        if not re.search(r"\brefresh_core\s*\(\s*\)", todo_code):
            problems.append(
                Problem(
                    notebook,
                    1,
                    "BUNDLE_REFRESH",
                    f"{exercise_id} TODO must call refresh_core() before using the fixture",
                )
            )

        focused = test_cells.get(exercise_id, [])
        if len(focused) != 1:
            problems.append(
                Problem(
                    notebook,
                    1,
                    "EXERCISE_TEST",
                    f"{exercise_id} needs exactly one # test-check: {exercise_id} cell",
                )
            )
        else:
            _, test_code = focused[0]
            focused_call = rf"\brun_exercise_tests\s*\(\s*['\"]{re.escape(exercise_id)}['\"]\s*\)"
            if not re.search(focused_call, test_code):
                problems.append(
                    Problem(
                        notebook,
                        1,
                        "EXERCISE_TEST",
                        f"{exercise_id} test-check must call run_exercise_tests(\"{exercise_id}\")",
                    )
                )

    for exercise_id in sorted(set(test_cells) - set(todo_cells)):
        problems.append(
            Problem(
                notebook,
                1,
                "EXERCISE_TEST",
                f"test-check references an exercise without a TODO: {exercise_id}",
            )
        )

    test_class_ids: set[str] = set()
    for test_file in sorted((notebook.parent / "tests").glob("test_*.py")):
        try:
            test_text = test_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        test_class_ids.update(
            re.findall(r"^class Test(E\d{2})\b", test_text, re.MULTILINE)
        )
    for exercise_id in sorted(set(todo_cells) - test_class_ids):
        problems.append(
            Problem(
                notebook,
                1,
                "EXERCISE_TEST",
                f"{exercise_id} needs a focused pytest class named Test{exercise_id}",
            )
        )
    return problems


def _public_functions(tree: ast.Module) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    functions = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_")
    ]
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        functions.extend(
            child
            for child in node.body
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
            and child.name != "__init__"
            and not child.name.startswith("_")
        )
    return functions


def _is_stub(function: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    meaningful = [node for node in function.body if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str))]
    return len(meaningful) == 1 and isinstance(meaningful[0], ast.Raise) and isinstance(meaningful[0].exc, ast.Call) and isinstance(meaningful[0].exc.func, ast.Name) and meaningful[0].exc.func.id == "NotImplementedError"


def _validate_python_bundle(bundle: Path, *, repo: Path, check_collection: bool) -> list[Problem]:
    problems: list[Problem] = []
    source_files = sorted((bundle / "src").rglob("*.py")) if (bundle / "src").is_dir() else []
    test_files = sorted((bundle / "tests").glob("test_*.py")) if (bundle / "tests").is_dir() else []
    if not source_files:
        problems.append(Problem(bundle, 1, "BUNDLE", "bundle needs at least one Python file under src/"))
    if not test_files:
        problems.append(Problem(bundle, 1, "BUNDLE", "bundle needs at least one tests/test_*.py file"))
    public_count = 0
    for path in source_files + test_files:
        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text, filename=path.as_posix())
        except (UnicodeDecodeError, SyntaxError) as exc:
            problems.append(Problem(path, getattr(exc, "lineno", 1) or 1, "PYTHON_SYNTAX", str(exc)))
            continue
        if path in source_files and path.name != "__init__.py":
            for function in _public_functions(tree):
                public_count += 1
                if not _is_stub(function):
                    problems.append(Problem(path, function.lineno, "PREFILLED_CORE", f"public learner function must remain a NotImplementedError stub: {function.name}"))
        if path in test_files:
            test_names = {node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_")}
            for category in ("normal", "edge", "failure"):
                if not any(name.startswith(f"test_{category}_") for name in test_names):
                    problems.append(Problem(path, 1, "TEST_CONTRACT", f"tests need a test_{category}_* contract"))
    if source_files and public_count == 0:
        problems.append(Problem(bundle, 1, "STARTER", "bundle has no public learner function to implement"))
    hidden = [path for path in bundle.rglob("*") if path.is_file() and re.search(r"(?:solution|answer|정답)", path.name, re.IGNORECASE)]
    for path in hidden:
        problems.append(Problem(path, 1, "SOLUTION", "solution or answer artifact is not allowed"))
    if check_collection and source_files and test_files and not any(
        problem.code == "PYTHON_SYNTAX" for problem in problems
    ):
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(bundle / "src")
        try:
            result = subprocess.run(
                ["uv", "run", "pytest", "--collect-only", "-q", str(bundle / "tests")],
                cwd=repo,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
                timeout=60,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            problems.append(Problem(bundle, 1, "IMPORT_COLLECTION", f"pytest collection could not run: {exc}"))
        else:
            if result.returncode != 0:
                detail = (result.stderr or result.stdout).strip().splitlines()
                summary = detail[-1] if detail else f"exit {result.returncode}"
                problems.append(Problem(bundle, 1, "IMPORT_COLLECTION", f"pytest collection failed: {summary}"))
    return problems


def validate(
    artifact: Path | str,
    *,
    repo_root: Path | str | None = None,
    check_collection: bool = True,
    allow_legacy_bundle: bool = False,
    learner_state: bool = False,
) -> list[Problem]:
    repo = Path(repo_root).resolve() if repo_root is not None else _repo_root()
    target = Path(artifact)
    if not target.is_absolute():
        target = repo / target
    try:
        resolved = target.resolve(strict=False)
        relative = resolved.relative_to(repo)
    except (OSError, ValueError):
        return [Problem(target, 1, "PATH", "artifact escapes the repository")]
    if not relative.parts or relative.parts[0] != "practice":
        return [Problem(target, 1, "PATH", "artifact must be under practice/")]
    if not target.exists():
        return [Problem(target, 1, "SOURCE_MISSING", "artifact does not exist")]
    if target.is_dir():
        if not allow_legacy_bundle:
            return [
                Problem(
                    target,
                    1,
                    "NOTEBOOK_ONLY",
                    "new practice must be one .ipynb file; pass --allow-legacy-bundle only to review an existing bundle",
                )
            ]
        notebook = target / "workbook.ipynb"
        if not notebook.is_file():
            return [Problem(target, 1, "BUNDLE", "bundle must contain workbook.ipynb")]
        problems, links, setup_cells, _ = _validate_notebook(
            notebook,
            repo,
        )
        problems.extend(_validate_notebook_setup(notebook, setup_cells, repo=repo))
        problems.extend(_validate_bundle_notebook_ergonomics(notebook, setup_cells))
        problems.extend(_validate_python_bundle(target, repo=repo, check_collection=check_collection))
    elif target.suffix == ".ipynb":
        notebook = target
        notebook_validation = validate_notebook_v2(
            notebook,
            repo,
            learner_state=learner_state,
        )
        problems = [
            Problem(notebook, issue.line, issue.code, issue.message)
            for issue in notebook_validation.issues
        ]
        links = notebook_validation.source_links
        setup_cells = notebook_validation.setup_cells
        if not any(problem.code == "SCHEMA_MIGRATION" for problem in problems):
            problems.extend(_validate_notebook_setup(notebook, setup_cells, repo=repo))
    else:
        return [Problem(target, 1, "PATH", "artifact must be a .ipynb file or bundle directory")]

    course_practice_links = [link for link in links if "/course-provided-practice/" in f"/{link}"]
    checked_indexes: set[Path] = set()
    for link in course_practice_links:
        absolute = repo / link
        course = absolute.parent.parent
        index = course / "INDEX.md"
        if not index.is_file():
            problems.append(Problem(notebook, 1, "PRACTICE_MAPPING", f"mapped course INDEX is missing for {link}"))
            continue
        if index not in checked_indexes:
            checked_indexes.add(index)
            for issue in validate_index(index):
                problems.append(Problem(index, issue.line, "PRACTICE_MAPPING", f"[{issue.code}] {issue.message}"))
        index_text = index.read_text(encoding="utf-8")
        relative_practice = absolute.relative_to(course).as_posix()
        matching = [raw for raw in index_text.splitlines() if f"`{relative_practice}`" in raw]
        if len(matching) != 1:
            problems.append(Problem(notebook, 1, "PRACTICE_MAPPING", f"course practice must have one explicit INDEX mapping: {link}"))
            continue
        cells = [part.strip().strip("`") for part in matching[0].strip()[1:-1].split("|")]
        if len(cells) >= 2:
            lesson_link = (course / cells[1]).relative_to(repo).as_posix()
            if lesson_link not in links:
                problems.append(Problem(notebook, 1, "PRACTICE_MAPPING", f"Notebook must also link the mapped lesson: {lesson_link}"))
    return problems


class ContractParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.exit(2, f"ERROR <cli>:1 [ARTIFACT_SCHEMA] {message}\n")


def main(argv: list[str] | None = None) -> int:
    parser = ContractParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument(
        "--allow-legacy-bundle",
        action="store_true",
        help="review an existing multi-file bundle without allowing it as a new practice artifact",
    )
    parser.add_argument(
        "--learner-state",
        action="store_true",
        help="validate a learner-worked Notebook without requiring unresolved targets or empty execution state",
    )
    args = parser.parse_args(argv)
    try:
        problems = validate(
            args.artifact,
            allow_legacy_bundle=args.allow_legacy_bundle,
            learner_state=args.learner_state,
        )
    except Exception as exc:  # pragma: no cover
        print(f"ERROR {args.artifact}:1 [ARTIFACT_SCHEMA] internal error: {exc}", file=sys.stderr)
        return 2
    for problem in problems:
        print(problem.render(), file=sys.stderr)
    if problems:
        return 2 if any(
            problem.code in {
                "ARTIFACT_SCHEMA",
                "AUDIT_METADATA",
                "SCHEMA_MIGRATION",
                "NOTEBOOK_JSON",
                "PYTHON_SYNTAX",
            }
            for problem in problems
        ) else 1
    print(f"OK {args.artifact.as_posix()} [practice-artifact]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
