#!/usr/bin/env python3
"""Safely cache one public official HTTPS lesson source under ignored tmp/."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
import re
import socket
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_LIMIT = 100 * 1024 * 1024
LESSON_ID_RE = re.compile(r"[a-z0-9][a-z0-9-]{2,63}\Z")
CREDENTIAL_QUERY_KEYS = {
    "access_token",
    "api_key",
    "apikey",
    "auth",
    "authorization",
    "credential",
    "key",
    "password",
    "secret",
    "sig",
    "signature",
    "token",
}
PRIMARY_MEDIA = {
    "application/pdf": ".pdf",
    "text/html": ".html",
    "text/markdown": ".md",
    "text/plain": ".txt",
}
ASSET_MEDIA = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/webp": ".webp",
    "image/gif": ".gif",
    "image/svg+xml": ".svg",
}


class CachePolicyError(ValueError):
    """A source requires approval instead of automatic caching."""


def _host_allowed(host: str | None, allowed: tuple[str, ...]) -> bool:
    if host is None:
        return False
    normalized = host.lower().rstrip(".")
    return any(
        normalized == item or normalized.endswith("." + item)
        for item in allowed
    )


def _validate_public_host(host: str, resolver: Any) -> None:
    normalized = host.lower().rstrip(".")
    if normalized == "localhost" or normalized.endswith((".localhost", ".local")):
        raise CachePolicyError("local hostnames are not public source hosts")
    try:
        literal = ipaddress.ip_address(normalized)
        addresses = [literal]
    except ValueError:
        try:
            answers = resolver(normalized, 443, type=socket.SOCK_STREAM)
        except OSError as error:
            raise CachePolicyError(f"official host could not be resolved publicly: {normalized}") from error
        addresses = []
        for answer in answers:
            try:
                addresses.append(ipaddress.ip_address(answer[4][0]))
            except (IndexError, ValueError):
                continue
    if not addresses or any(not address.is_global for address in addresses):
        raise CachePolicyError("official host resolves to a non-public network address")


def _validate_url(url: str, allowed_hosts: tuple[str, ...], resolver: Any) -> None:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise CachePolicyError("only public HTTPS URLs may be cached automatically")
    if parsed.username or parsed.password:
        raise CachePolicyError("credential-bearing URLs require explicit approval")
    if not _host_allowed(parsed.hostname, allowed_hosts):
        raise CachePolicyError(f"host is not in the declared official host set: {parsed.hostname}")
    _validate_public_host(parsed.hostname, resolver)
    query_keys = {key.lower() for key, _ in parse_qsl(parsed.query, keep_blank_values=True)}
    if query_keys & CREDENTIAL_QUERY_KEYS:
        raise CachePolicyError("credential-like query parameters require explicit approval")


class _PublicRedirectHandler(HTTPRedirectHandler):
    def __init__(self, allowed_hosts: tuple[str, ...], resolver: Any) -> None:
        super().__init__()
        self.allowed_hosts = allowed_hosts
        self.resolver = resolver

    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        _validate_url(new_url, self.allowed_hosts, self.resolver)
        return super().redirect_request(
            request, file_pointer, code, message, headers, new_url
        )


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".cache-", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def _approval(reason: str, original_url: str) -> dict[str, Any]:
    return {
        "status": "AWAIT_SOURCE_APPROVAL",
        "reason": reason,
        "original_url": original_url,
    }


def cache_external_source(
    *,
    lesson_id: str,
    url: str,
    official_hosts: list[str],
    kind: str = "primary",
    repo_root: Path = REPO_ROOT,
    max_bytes: int = DEFAULT_LIMIT,
    opener: Any | None = None,
    resolver: Any = socket.getaddrinfo,
    retrieved_at: str | None = None,
) -> dict[str, Any]:
    """Cache one allowed source and return a receipt-shaped JSON object."""
    if not LESSON_ID_RE.fullmatch(lesson_id):
        raise ValueError("lesson_id has an invalid format")
    if kind not in {"primary", "asset"}:
        raise ValueError("kind must be primary or asset")
    if max_bytes <= 0:
        raise ValueError("max_bytes must be positive")
    allowed_hosts = tuple(
        sorted({host.lower().rstrip(".") for host in official_hosts if host.strip()})
    )
    if not allowed_hosts:
        raise ValueError("at least one official host is required")
    try:
        _validate_url(url, allowed_hosts, resolver)
    except CachePolicyError as error:
        return _approval(str(error), url)

    request = Request(
        url,
        headers={
            "Accept": "application/pdf,text/html,text/markdown,text/plain,image/*",
            "User-Agent": "llm-research-learning-lab-source-cache/1",
        },
        method="GET",
    )
    client = opener or build_opener(_PublicRedirectHandler(allowed_hosts, resolver))
    try:
        response = client.open(request, timeout=30)
    except CachePolicyError as error:
        return _approval(f"redirect rejected: {error}", url)
    except HTTPError as error:
        if error.code in {401, 402, 403, 407, 413}:
            return _approval(f"HTTP {error.code} requires access or scope approval", url)
        raise RuntimeError(f"source retrieval failed with HTTP {error.code}") from error
    except URLError as error:
        raise RuntimeError(f"source retrieval failed: {error.reason}") from error

    with response:
        final_url = response.geturl()
        try:
            _validate_url(final_url, allowed_hosts, resolver)
        except CachePolicyError as error:
            return _approval(f"redirect rejected: {error}", url)
        media_type = response.headers.get_content_type().lower()
        allowed_media = PRIMARY_MEDIA if kind == "primary" else ASSET_MEDIA
        suffix = allowed_media.get(media_type)
        if suffix is None:
            return _approval(
                f"unsupported {kind} media type {media_type!r}; archives, datasets, and weights are not cached automatically",
                url,
            )
        content_length = response.headers.get("Content-Length")
        if content_length is not None:
            try:
                declared_size = int(content_length)
            except ValueError:
                declared_size = -1
            if declared_size > max_bytes:
                return _approval(
                    f"declared size {declared_size} exceeds the {max_bytes}-byte limit",
                    url,
                )
        chunks: list[bytes] = []
        byte_count = 0
        while True:
            chunk = response.read(min(1024 * 1024, max_bytes + 1 - byte_count))
            if not chunk:
                break
            byte_count += len(chunk)
            if byte_count > max_bytes:
                return _approval(
                    f"download exceeds the {max_bytes}-byte limit", url
                )
            chunks.append(chunk)

    payload = b"".join(chunks)
    digest = hashlib.sha256(payload).hexdigest()
    cache_directory = repo_root / "tmp/active-lesson-sources" / lesson_id
    content_path = cache_directory / f"{digest}{suffix}"
    receipt_path = cache_directory / f"{digest}.receipt.json"
    _atomic_write(content_path, payload)

    timestamp = retrieved_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    relative_content = content_path.relative_to(repo_root).as_posix()
    relative_receipt = receipt_path.relative_to(repo_root).as_posix()
    receipt = {
        "status": "CACHED",
        "lesson_id": lesson_id,
        "kind": kind,
        "original_url": url,
        "final_url": final_url,
        "official_hosts": list(allowed_hosts),
        "media_type": media_type,
        "byte_count": byte_count,
        "sha256": digest,
        "path": relative_content,
        "receipt_path": relative_receipt,
        "retrieved_at": timestamp,
    }
    _atomic_write(
        receipt_path,
        (json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )
    return receipt


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lesson-id", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument(
        "--official-host",
        action="append",
        required=True,
        help="allowed official host or parent domain (repeatable)",
    )
    parser.add_argument("--kind", choices=("primary", "asset"), default="primary")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_LIMIT)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = cache_external_source(
            lesson_id=args.lesson_id,
            url=args.url,
            official_hosts=args.official_host,
            kind=args.kind,
            max_bytes=args.max_bytes,
        )
    except (OSError, RuntimeError, ValueError) as error:
        print(json.dumps({"status": "ERROR", "reason": str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "CACHED" else 3


if __name__ == "__main__":
    raise SystemExit(main())
