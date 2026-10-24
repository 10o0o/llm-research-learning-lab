"""Source/CI retirement contract, not a check of live GitHub Pages status."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_site_source_removed_and_learning_material_preserved():
    assert not (ROOT / 'web').exists()
    for name in ('STATE.md', 'CURRICULUM.md', 'ROADMAP.md', 'main.ipynb', 'practice'):
        assert (ROOT / name).exists()
    recovery = (ROOT / 'docs/migration-20261024.md').read_text()
    assert '9592b804f275ce4db68ca0ed702cfd64e302464f/web' in recovery


def test_general_ci_remains_without_pages_or_site_build():
    workflow = (ROOT / '.github/workflows/validate.yml').read_text()
    assert 'uv run --frozen pytest -q tests' in workflow
    assert 'uv lock --check' in workflow
    assert 'git diff --check' in workflow
    for retired in ('pages-artifact:', 'deploy:', 'upload-pages-artifact',
                    'deploy-pages', 'configure-pages', 'pages: write',
                    'id-token: write', 'web/public', 'web/dist', 'npm'):
        assert retired not in workflow
