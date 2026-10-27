import subprocess
import tempfile
import unittest
from pathlib import Path

from check_links import check


class CheckLinksTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def git(self, *arguments):
        subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            check=True,
            capture_output=True,
        )

    def init_repository(self):
        self.git("init", "--quiet")
        self.write(".gitignore", "/private/\n/til/today.md\n.venv/\n")

    def test_ignored_private_notes_and_dependencies_do_not_fail_public_links(self):
        self.init_repository()
        self.write("README.md", "[Guide](docs/guide.md#ready)\n")
        self.write("docs/guide.md", "# Ready\n")
        self.git("add", "README.md", "docs/guide.md")
        self.write("private/old.md", "[Old](missing.md)\n")
        self.write("til/today.md", "[Old](../../missing.md)\n")
        self.write(".venv/package/README.md", "[Old](missing.md)\n")

        pages, checked, errors = check(self.root)

        self.assertEqual(errors, [])
        self.assertEqual(checked, 1)
        self.assertEqual(
            [page.relative_to(self.root).as_posix() for page in pages],
            ["README.md", "docs/guide.md"],
        )

    def test_new_nonignored_documents_are_checked_before_staging(self):
        self.init_repository()
        self.write("draft.md", "[Missing](missing.md)\n")

        _, checked, errors = check(self.root)

        self.assertEqual(checked, 1)
        self.assertEqual(len(errors), 1)
        self.assertIn("draft.md -> missing.md: missing target", errors)

    def test_tracked_documents_are_checked_even_when_they_match_gitignore(self):
        self.init_repository()
        self.write("private/tracked.md", "[Missing](missing.md)\n")
        self.git("add", "--force", "private/tracked.md")

        _, checked, errors = check(self.root)

        self.assertEqual(checked, 1)
        self.assertEqual(len(errors), 1)
        self.assertIn("private/tracked.md -> missing.md: missing target", errors)

    def test_directories_without_git_still_validate_links_and_headings(self):
        self.write("README.md", "[Guide](guide.md#absent)\n")
        self.write("guide.md", "# Present\n")

        _, checked, errors = check(self.root)

        self.assertEqual(checked, 1)
        self.assertEqual(len(errors), 1)
        self.assertIn("README.md -> guide.md#absent: missing heading", errors)


if __name__ == "__main__":
    unittest.main()
