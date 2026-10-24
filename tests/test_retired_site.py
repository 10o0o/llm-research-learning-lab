"""Verify the small retirement artifact, not learner mastery or external uptime."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import pytest

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://github.com/10o0o/llm-research-learning-lab'
HISTORY = '5f0fccb96894e75805430ad194282319d6e44c4c'

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags = []
        self.hrefs = []
        self.attrs = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        self.attrs.append((tag, attrs))
        if tag == 'a':
            self.hrefs.append(attrs.get('href', ''))

@pytest.mark.parametrize('name', ['index.html', '404.html'])
def test_retirement_notice_is_accessible_static_and_links_to_real_repo_paths(name):
    source = (ROOT / 'web/public' / name).read_text()
    page = Page(source)
    assert '<!doctype html>' in source
    assert ('html', {'lang': 'ko'}) in page.attrs
    assert any(tag == 'meta' and attrs.get('name') == 'viewport'
               and attrs.get('content') == 'width=device-width, initial-scale=1'
               for tag, attrs in page.attrs)
    assert page.tags.count('h1') == 1
    assert 'main' in page.tags
    assert 'script' not in page.tags and 'iframe' not in page.tags
    assert page.hrefs == [BASE, BASE+'/blob/main/STATE.md',
                          BASE+'/blob/main/CURRICULUM.md', BASE+'/tree/'+HISTORY+'/knowledge']
    assert all(urlparse(link).scheme == 'https' for link in page.hrefs)
    for name in ['STATE.md', 'CURRICULUM.md']:
        assert (ROOT/name).is_file()
    assert 'overflow-wrap: anywhere' in source
    assert ':focus-visible' in source
    assert '운영하지 않습니다' in source or '정리되었습니다' in source


def test_only_two_notice_pages_are_published_without_old_search_assets():
    assert sorted(p.name for p in (ROOT/'web/public').iterdir()) == ['404.html', 'index.html']
    assert not (ROOT/'web/package.json').exists()
    assert not (ROOT/'web/src/content.config.ts').exists()
    workflow = (ROOT/'.github/workflows/validate.yml').read_text()
    assert 'path: web/public' in workflow
    assert 'web/dist' not in workflow
    assert 'npm' not in workflow
    assert 'validate_knowledge' not in workflow
    assert "github.ref == 'refs/heads/main'" in workflow
    assert 'needs: [validate, pages-artifact]' in workflow
