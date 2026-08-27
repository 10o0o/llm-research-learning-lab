from __future__ import annotations

import importlib.util
import json
import sys
from email.message import Message
from pathlib import Path
from urllib.error import HTTPError


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/cache_external_source.py"
SPEC = importlib.util.spec_from_file_location("cache_external_source_under_test", SCRIPT)
assert SPEC and SPEC.loader
cache = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = cache
SPEC.loader.exec_module(cache)


def public_resolver(host: str, port: int, *, type: int):
    del host, port, type
    return [(2, 1, 6, "", ("93.184.216.34", 443))]


class FakeResponse:
    def __init__(self, body: bytes, *, url: str, media_type: str) -> None:
        self.body = body
        self.offset = 0
        self.url = url
        self.headers = Message()
        self.headers["Content-Type"] = media_type
        self.headers["Content-Length"] = str(len(body))

    def read(self, size: int = -1) -> bytes:
        if size < 0:
            size = len(self.body) - self.offset
        chunk = self.body[self.offset : self.offset + size]
        self.offset += len(chunk)
        return chunk

    def geturl(self) -> str:
        return self.url

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None


class FakeOpener:
    def __init__(self, response=None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error
        self.request = None

    def open(self, request, timeout: int):
        self.request = request
        assert timeout == 30
        if self.error is not None:
            raise self.error
        return self.response


def test_caches_html_bytes_and_receipt_atomically(tmp_path: Path) -> None:
    body = b"<html><body><p>Exact external excerpt.</p></body></html>"
    opener = FakeOpener(
        FakeResponse(
            body,
            url="https://docs.example.edu/course/lesson.html",
            media_type="text/html; charset=utf-8",
        )
    )
    result = cache.cache_external_source(
        lesson_id="external-lesson",
        url="https://docs.example.edu/course/lesson",
        official_hosts=["example.edu"],
        repo_root=tmp_path,
        opener=opener,
        resolver=public_resolver,
        retrieved_at="2026-08-27T01:02:03Z",
    )
    assert result["status"] == "CACHED"
    assert (tmp_path / result["path"]).read_bytes() == body
    receipt = json.loads((tmp_path / result["receipt_path"]).read_text(encoding="utf-8"))
    assert receipt == result
    assert opener.request.get_header("Cookie") is None
    assert result["path"].startswith("tmp/active-lesson-sources/external-lesson/")


def test_redirect_must_remain_https_and_on_official_host(tmp_path: Path) -> None:
    for final_url in (
        "http://docs.example.edu/course/lesson",
        "https://unrelated.example.com/course/lesson",
    ):
        result = cache.cache_external_source(
            lesson_id="external-lesson",
            url="https://docs.example.edu/course/lesson",
            official_hosts=["example.edu"],
            repo_root=tmp_path,
            opener=FakeOpener(
                FakeResponse(b"text", url=final_url, media_type="text/plain")
            ),
            resolver=public_resolver,
        )
        assert result["status"] == "AWAIT_SOURCE_APPROVAL"
    assert not (tmp_path / "tmp").exists()


def test_limits_media_kind_size_and_authenticated_access(tmp_path: Path) -> None:
    image = FakeResponse(
        b"image", url="https://docs.example.edu/image.png", media_type="image/png"
    )
    wrong_kind = cache.cache_external_source(
        lesson_id="external-lesson",
        url="https://docs.example.edu/image.png",
        official_hosts=["example.edu"],
        repo_root=tmp_path,
        opener=FakeOpener(image),
        resolver=public_resolver,
    )
    assert wrong_kind["status"] == "AWAIT_SOURCE_APPROVAL"

    too_large = cache.cache_external_source(
        lesson_id="external-lesson",
        url="https://docs.example.edu/lesson.txt",
        official_hosts=["example.edu"],
        repo_root=tmp_path,
        max_bytes=3,
        opener=FakeOpener(
            FakeResponse(b"four", url="https://docs.example.edu/lesson.txt", media_type="text/plain")
        ),
        resolver=public_resolver,
    )
    assert too_large["status"] == "AWAIT_SOURCE_APPROVAL"

    auth_error = HTTPError(
        "https://docs.example.edu/private", 401, "Unauthorized", {}, None
    )
    auth = cache.cache_external_source(
        lesson_id="external-lesson",
        url="https://docs.example.edu/private",
        official_hosts=["example.edu"],
        repo_root=tmp_path,
        opener=FakeOpener(error=auth_error),
        resolver=public_resolver,
    )
    assert auth["status"] == "AWAIT_SOURCE_APPROVAL"


def test_direct_image_asset_is_allowed_only_as_asset(tmp_path: Path) -> None:
    body = b"png-bytes"
    result = cache.cache_external_source(
        lesson_id="external-lesson",
        url="https://docs.example.edu/image.png",
        official_hosts=["example.edu"],
        kind="asset",
        repo_root=tmp_path,
        opener=FakeOpener(
            FakeResponse(
                body,
                url="https://docs.example.edu/image.png",
                media_type="image/png",
            )
        ),
        resolver=public_resolver,
        retrieved_at="2026-08-27T01:02:03Z",
    )
    assert result["status"] == "CACHED"
    assert result["kind"] == "asset"
    assert (tmp_path / result["path"]).read_bytes() == body


def test_credentials_and_archives_are_never_cached_automatically(tmp_path: Path) -> None:
    credential = cache.cache_external_source(
        lesson_id="external-lesson",
        url="https://docs.example.edu/file?token=secret",
        official_hosts=["example.edu"],
        repo_root=tmp_path,
        opener=FakeOpener(),
        resolver=public_resolver,
    )
    assert credential["status"] == "AWAIT_SOURCE_APPROVAL"

    archive = cache.cache_external_source(
        lesson_id="external-lesson",
        url="https://docs.example.edu/course.zip",
        official_hosts=["example.edu"],
        repo_root=tmp_path,
        opener=FakeOpener(
            FakeResponse(
                b"archive",
                url="https://docs.example.edu/course.zip",
                media_type="application/zip",
            )
        ),
        resolver=public_resolver,
    )
    assert archive["status"] == "AWAIT_SOURCE_APPROVAL"


def test_private_or_local_network_hosts_are_never_opened(tmp_path: Path) -> None:
    def private_resolver(host: str, port: int, *, type: int):
        del host, port, type
        return [(2, 1, 6, "", ("127.0.0.1", 443))]

    opener = FakeOpener(
        FakeResponse(b"text", url="https://docs.example.edu/lesson", media_type="text/plain")
    )
    result = cache.cache_external_source(
        lesson_id="external-lesson",
        url="https://docs.example.edu/lesson",
        official_hosts=["example.edu"],
        repo_root=tmp_path,
        opener=opener,
        resolver=private_resolver,
    )
    assert result["status"] == "AWAIT_SOURCE_APPROVAL"
    assert opener.request is None
