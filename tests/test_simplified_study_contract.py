"""Structural checks for the learning hub, not a test of learner mastery."""
from __future__ import annotations
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote
import pytest

REPO = Path(__file__).resolve().parents[1]
def _extract_link_targets(line: str) -> list[str]:
    targets: list[str] = []
    cursor = 0
    while True:
        start = line.find("](", cursor)
        if start == -1:
            return targets
        index = start + 2
        depth = 1
        escaped = False
        while index < len(line):
            character = line[index]
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    targets.append(line[start + 2 : index])
                    cursor = index + 1
                    break
            index += 1
        else:
            return targets


# All active tracked Markdown, including preserved learner notes; historical archive is immutable.
OPERATING_DOCS = tuple(path for path in subprocess.check_output(
    ["git", "ls-files", "*.md"], cwd=REPO, text=True
).splitlines() if (REPO / path).is_file() and not path.startswith("archive/"))

def _doc_lines(path: Path) -> list[tuple[int, str]]:
    """Markdown lines outside fenced/inline examples; never execute examples."""
    visible = []
    fence = ""
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = ""
            continue
        if marker:
            fence = marker[1]
            continue
        visible.append((number, line))
    return visible


def _doc_heading_ids(path: Path) -> set[str]:
    """GitHub-style ATX heading IDs used by this repository, including duplicates."""
    ids: set[str] = set()
    for _, line in _doc_lines(path):
        heading = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*$", line)
        if not heading:
            continue
        text = re.sub(r"<[^>]+>", "", heading[1])
        text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
        slug = re.sub(r"[^\w\s-]", "", text.lower())
        slug = re.sub(r"\s", "-", slug.strip())
        candidate, suffix = slug, 0
        while candidate in ids:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        ids.add(candidate)
    return ids


def _doc_link_errors(path: Path) -> list[str]:
    """Check local inline link files/headings; external URLs and templates are inert."""
    if not path.is_file():
        return [f"{path}: document missing"]
    errors = []
    for number, line in _doc_lines(path):
        line = re.sub(r"`+[^`]*`+", "", line)
        for raw in _extract_link_targets(line):
            target = raw.strip()
            if target.startswith("<") and ">" in target:
                target = target[1:target.index(">")]
            else:
                target = target.split(maxsplit=1)[0] if target else ""
            if re.match(r"[a-zA-Z][\w+.-]*:", target) or target.startswith("//"):
                continue
            file_part, _, fragment = target.partition("#")
            file_part = re.sub(r"\\([\\()])", r"\1", unquote(file_part))
            fragment = unquote(fragment)
            if re.search(r"[<>{}]", file_part):
                continue  # e.g. notes/<area>/<concept>.md, not a real file.
            linked = (path.parent / file_part).resolve() if file_part else path.resolve()
            prefix = f"{path}:{number}: {raw}"
            if not linked.exists():
                errors.append(f"{prefix}: target missing")
                continue
            if linked.is_dir():
                linked = linked / "README.md"
            if fragment and linked.suffix.lower() == ".md":
                if not linked.is_file() or fragment not in _doc_heading_ids(linked):
                    errors.append(f"{prefix}: heading missing")
    return errors


def test_doc_link_errors_handle_real_and_example_targets(tmp_path: Path) -> None:
    target = tmp_path / "참고 문서(1).md"
    target.write_text("## 절 하나\n", encoding="utf-8")
    page = tmp_path / "guide.md"
    page.write_text(
        "[정상](<참고 문서(1).md#절-하나>)\n\n"
        "```md\n[예시](missing-example.md)\n```\n",
        encoding="utf-8",
    )
    assert _doc_link_errors(page) == []
    page.write_text("[누락](missing.md)\n", encoding="utf-8")
    assert any("missing.md" in error for error in _doc_link_errors(page))
    page.write_text("[없는 절](<참고 문서(1).md#없는-절>)\n", encoding="utf-8")
    assert any("없는-절" in error for error in _doc_link_errors(page))


@pytest.mark.parametrize("relative", OPERATING_DOCS)
def test_operating_doc_links_resolve(relative: str) -> None:
    assert _doc_link_errors(REPO / relative) == []


def test_doc_links_normalize_escapes_fragments_and_duplicate_headings(tmp_path: Path) -> None:
    target = tmp_path / "한 글(1).md"
    target.write_text("## API `find` / Set\n## API `find` / Set\n", encoding="utf-8")
    page = tmp_path / "guide.md"
    page.write_text(
        "# Local\n"
        "[self](#local)\n"
        "[encoded](%ED%95%9C%20%EA%B8%80%281%29.md#api-find--set-1)\n"
        "[escaped](<한 글\\(1\\).md#api-find--set>)\n",
        encoding="utf-8",
    )
    assert _doc_link_errors(page) == []
    page.write_text("[missing self](#absent)\n", encoding="utf-8")
    assert any("#absent" in error for error in _doc_link_errors(page))


def test_doc_links_ignore_urls_templates_and_nested_fenced_examples(tmp_path: Path) -> None:
    page = tmp_path / "guide.md"
    page.write_text(
        "[web](https://example.invalid/doc#missing)\n"
        "[email](mailto:example@example.invalid)\n"
        "[template](notes/<area>/<concept>.md)\n"
        "`[inline example](absent-inline.md)`\n"
        "~~~~md\n[example](absent-tilde.md)\n~~~~\n"
        "````md\n```md\n[example](absent-nested.md)\n```\n````\n",
        encoding="utf-8",
    )
    assert _doc_link_errors(page) == []



def test_shared_agent_entrypoint() -> None:
    assert (REPO / "CLAUDE.md").is_symlink()
    assert (REPO / "CLAUDE.md").resolve() == REPO / "AGENTS.md"


def test_removed_management_is_not_an_active_dependency() -> None:
    for relative in ("knowledge", ".agents/skills/update-learning-knowledge", "til/README.md", "USAGE.md", "DEFERRED.md",
                     ".agents/skills/finish-chapter/SKILL.md",
                     ".agents/skills/save-today-til/SKILL.md", ".specify/README.md"):
        assert not (REPO / relative).exists()
    for relative in ("README.md", "AGENTS.md", "STATE.md", "ROADMAP.md", "CURRICULUM.md"):
        assert (REPO / relative).stat().st_size > 0
    assert (REPO / "docs/migration-20261024.md").is_file()


def test_private_material_paths_remain_ignored() -> None:
    paths = ["materials/private/example.txt", "practice/private/example.txt"]
    result = subprocess.run(["git", "check-ignore", "--stdin"], input="\n".join(paths)+"\n",
                            cwd=REPO, text=True, capture_output=True, check=True)
    assert result.stdout.splitlines() == paths


def test_no_progress_database() -> None:
    assert not (REPO / "progress.db").exists()


def test_new_migration_links_resolve() -> None:
    assert _doc_link_errors(REPO / "docs/migration-20261024.md") == []
