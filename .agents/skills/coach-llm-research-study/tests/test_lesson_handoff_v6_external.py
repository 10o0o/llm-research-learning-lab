from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

from handoff_fixture import CONTRACT, build_handoff, sha256


SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts/validate_lesson_handoff.py"
SPEC = importlib.util.spec_from_file_location("handoff_v6_external_under_test", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


EXTERNAL_BYTES = b"""<!doctype html><html><body>
<p>Identify the batch and feature axes.</p>
<p>Predict the output shape of a broadcast operation.</p>
<p>Review the course map only when it affects the current path.</p>
<h2>axes</h2><p>Tensor axes.</p>
<h2>shape-propagation</h2><p>Broadcast shapes.</p>
<h2>orientation</h2><p>Use the course map when navigation is needed.</p>
</body></html>"""
OFFICIAL_URL = "https://docs.example.edu/course/lesson"
FINAL_URL = "https://docs.example.edu/course/lesson.html"
RETRIEVED_AT = "2026-08-27T01:02:03Z"


def _write_curriculum(root: Path, *, local_path: str | None = None, related: bool = False) -> None:
    relation = "—"
    source_table = ""
    if local_path is not None:
        local_hash = sha256((root / local_path).read_bytes())
        relation = ("primary" if related else "context") + ":SRC-LOCAL-00-01"
        source_table = (
            "\n| Source ID | 정확한 경로 | 자료 형식 | SHA-256 | 무결성 | 감사 상태 | 감사일 | 비고 |\n"
            "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
            f"| SRC-LOCAL-00-01 | `{local_path}` | HTML 토글 펼침 Markdown | `{local_hash}` | complete | complete | 2026-08-27 | Fixture. |\n"
        )
    (root / "CURRICULUM.md").write_text(
        "# Curriculum\n\n"
        "| ID | 학습 성과 | 목표 깊이 | 선수 ID | 요구 근거 | 자료 연결 | 자료 충족도 | 공백 처리 | 비고 |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        f"| CC-DL-01 | Tensor contracts | D2 | — | explain | {relation} | 없음 | 별도 자료 확보 | Fixture row. |\n"
        "| TR-SYS-03 | Systems endpoint | D3 | CC-DL-01 | design | — | 없음 | 트랙 선택 시 확보 | Fixture endpoint. |\n"
        + source_table,
        encoding="utf-8",
    )


def _external_contract(
    external_path: str,
    receipt_path: str,
    *,
    mixed_local_path: str | None = None,
    objective_order: str = "O001, O002, O004",
) -> str:
    contract = CONTRACT.replace(
        "materials/lesson.md#", f"{external_path}#text: "
    )
    contract = contract.replace(
        "| CC-DL-01 | 충분 | 그대로 사용 | source-only | O001, O002 | The named source directly supports the selected tensor-shape target. |",
        "| CC-DL-01 | 없음 | 별도 자료 확보 | resolved-external | O001, O002 | The official external source resolves this lesson without changing durable Curriculum coverage. |",
    )
    contract = contract.replace(
        "| none | none | none | none | none | none | none | none | none | none | none |",
        f"| I001 | Example University | Tensor Systems | 2026 offering | Shape lesson | {OFFICIAL_URL} | {FINAL_URL} | {RETRIEVED_AT} | text/html | axes and broadcasting | {receipt_path} |",
        1,
    )
    contract = contract.replace(
        "| none | none | none | none | none |",
        "| CC-DL-01 | I001 | primary | O001, O002 | Full source-body audit against the selected target. |",
        1,
    )
    if mixed_local_path is not None:
        contract = contract.replace(
            "| CC-DL-01 | 없음 | 별도 자료 확보 | resolved-external | O001, O002 |",
            f"| CC-DL-01 | 없음 | 별도 자료 확보 | resolved-external | {objective_order} |",
        )
        contract = contract.replace(
            "| I001 | entire-source | none | entire-source | none | none |",
            "| I001 | entire-source | none | entire-source | none | none |\n"
            "| I002 | entire-source | none | entire-source | none | none |",
        )
        contract = contract.replace(
            "| I001 | D001, D002, D003 | O001, O002 | G001 |",
            "| I001 | D001, D002, D003 | O001, O002 | G001 |\n"
            "| I002 | none | O004 | none |",
        )
        objective_row = (
            f"| O004 | source-core | none | {mixed_local_path}#local-core | "
            "Relate the local shape rule to the same target. | C02 | C01 | full | "
            "Compare the local and external statements. | none |"
        )
        contract = contract.replace(
            "| O003 | optional-added | supplement | CURRICULUM.md#CC-DL-01 | Connect tensor axes to batch, token, and hidden axes. | C03 | C01, C02 | full | Map one small tensor to an attention input. | none |",
            "| O003 | optional-added | supplement | CURRICULUM.md#CC-DL-01 | Connect tensor axes to batch, token, and hidden axes. | C03 | C01, C02 | full | Map one small tensor to an attention input. | none |\n"
            + objective_row,
        )
        contract = contract.replace(
            "| X003 | Work one tensor broadcast | A 2 by 1 tensor combined with a 1 by 3 tensor. | O001, O002 |",
            "| X003 | Work one tensor broadcast | A 2 by 1 tensor combined with a 1 by 3 tensor. | O001, O002, O004 |",
        )
        contract = contract.replace(
            "| O001, O002, O003 |",
            "| O001, O002, O003, O004 |",
        )
        contract = contract.replace(
            "- objective_ids: O001, O002\n",
            "- objective_ids: O001, O002, O004\n",
        )
        contract = contract.replace(
            "- objective_ids: O001, O002, O003\n",
            "- objective_ids: O001, O002, O003, O004\n",
        )
    return contract


def _build_external(
    root: Path,
    *,
    mixed: bool = False,
    local_related: bool = False,
    objective_order: str = "O001, O002, O004",
    include_asset: bool = False,
):
    lesson_id = "external-shape-lesson"
    digest = sha256(EXTERNAL_BYTES)
    external_path = f"tmp/active-lesson-sources/{lesson_id}/{digest}.html"
    receipt_path = f"tmp/active-lesson-sources/{lesson_id}/{digest}.receipt.json"
    external_file = root / external_path
    external_file.parent.mkdir(parents=True, exist_ok=True)
    external_file.write_bytes(EXTERNAL_BYTES)
    receipt = {
        "status": "CACHED",
        "lesson_id": lesson_id,
        "kind": "primary",
        "original_url": OFFICIAL_URL,
        "final_url": FINAL_URL,
        "official_hosts": ["example.edu"],
        "media_type": "text/html",
        "byte_count": len(EXTERNAL_BYTES),
        "sha256": digest,
        "path": external_path,
        "receipt_path": receipt_path,
        "retrieved_at": RETRIEVED_AT,
    }
    (root / receipt_path).write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    additional: list[tuple[str, str, bytes]] = []
    local_path = None
    delivery = None
    if mixed:
        local_path = "materials/local.md"
        local_bytes = b"# Local\n\n## local-core\n\nLocal source core.\n"
        local_file = root / local_path
        local_file.parent.mkdir(parents=True, exist_ok=True)
        local_file.write_bytes(local_bytes)
        additional.append(("primary", local_path, local_bytes))
        delivery = [
            {"objective": objective, "state": "pending", "mode": "none", "note": "Awaiting instruction."}
            for objective in ("O001", "O002", "O003", "O004")
        ]
    _write_curriculum(root, local_path=local_path, related=local_related)
    asset_receipt: tuple[str, dict[str, object]] | None = None
    if include_asset:
        asset_bytes = b"image-bytes"
        asset_digest = sha256(asset_bytes)
        asset_path = f"tmp/active-lesson-sources/{lesson_id}/{asset_digest}.png"
        asset_receipt_path = (
            f"tmp/active-lesson-sources/{lesson_id}/{asset_digest}.receipt.json"
        )
        additional.append(("external-asset", asset_path, asset_bytes))
        asset_receipt = (
            asset_receipt_path,
            {
                "status": "CACHED",
                "lesson_id": lesson_id,
                "kind": "asset",
                "original_url": "https://docs.example.edu/course/diagram.png",
                "final_url": "https://docs.example.edu/course/diagram.png",
                "official_hosts": ["example.edu"],
                "media_type": "image/png",
                "byte_count": len(asset_bytes),
                "sha256": asset_digest,
                "path": asset_path,
                "receipt_path": asset_receipt_path,
                "retrieved_at": RETRIEVED_AT,
            },
        )
    curriculum_before = (root / "CURRICULUM.md").read_bytes()
    contract = _external_contract(
        external_path,
        receipt_path,
        mixed_local_path=local_path,
        objective_order=objective_order,
    )
    handoff, hashes = build_handoff(
        root,
        contract=contract,
        status="active",
        reviews=[("pass", "fresh-external-reviewer")],
        lesson_id=lesson_id,
        primary_role="external-primary",
        primary_path=external_path,
        primary_bytes=EXTERNAL_BYTES,
        additional_manifest_inputs=additional or None,
        delivery=delivery,
    )
    if asset_receipt is not None:
        asset_receipt_path, payload = asset_receipt
        (root / asset_receipt_path).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return handoff, hashes, curriculum_before, receipt_path


def _codes(report) -> set[str]:
    return {error.code for error in report.errors}


def test_remote_only_ready_and_html_exact_excerpt_locator() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        handoff, _, curriculum_before, _ = _build_external(root)
        report = validator.validate_handoff(handoff, repo_root=root, ready=True)
        assert report.ok, report.errors
        assert (root / "CURRICULUM.md").read_bytes() == curriculum_before
        assert report.document.curriculum_treatments["CC-DL-01"].lesson_treatment == "resolved-external"

        hidden = handoff.read_text(encoding="utf-8").replace(
            "text: Identify the batch and feature axes.",
            "text: hidden script objective",
            1,
        )
        external = next(
            root / item.path
            for item in report.document.manifest
            if item.role == "external-primary"
        )
        external.write_bytes(
            EXTERNAL_BYTES.replace(
                b"</body>", b"<script>hidden script objective</script></body>"
            )
        )
        handoff.write_text(hidden, encoding="utf-8")
        hidden_report = validator.validate_handoff(handoff, repo_root=root)
        assert "SOURCE_LOCATION" in _codes(hidden_report)


def test_mixed_lesson_requires_every_local_and_external_relation_regardless_of_order() -> None:
    for related in (True, False):
        for order in ("O001, O002, O004", "O004, O001, O002"):
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                handoff, _, _, _ = _build_external(
                    root, mixed=True, local_related=related, objective_order=order
                )
                report = validator.validate_handoff(handoff, repo_root=root, ready=True)
                if related:
                    assert report.ok, report.errors
                else:
                    assert "CURRICULUM_SOURCE_RELATION" in _codes(report)


def test_external_identity_https_cache_and_relation_are_blocking() -> None:
    mutations = {
        "non_https": ("https://docs.example.edu/course/lesson |", "http://docs.example.edu/course/lesson |", "EXTERNAL_IDENTITY"),
        "missing_relation": (
            "| CC-DL-01 | I001 | primary | O001, O002 | Full source-body audit against the selected target. |",
            "| none | none | none | none | none |",
            "EXTERNAL_SOURCE_RELATION",
        ),
    }
    for old, new, expected_code in mutations.values():
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            handoff, _, _, _ = _build_external(root)
            text = handoff.read_text(encoding="utf-8").replace(old, new)
            handoff.write_text(text, encoding="utf-8")
            report = validator.validate_handoff(handoff, repo_root=root, ready=True)
            assert expected_code in _codes(report), report.errors

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        handoff, _, _, receipt_path = _build_external(root)
        (root / receipt_path).unlink()
        report = validator.validate_handoff(handoff, repo_root=root, ready=True)
        assert "EXTERNAL_CACHE_MISSING" in _codes(report)


def test_external_identity_missing_and_duplicate_rows_are_blocking() -> None:
    identity_row = (
        f"| I001 | Example University | Tensor Systems | 2026 offering | Shape lesson | "
        f"{OFFICIAL_URL} | {FINAL_URL} | {RETRIEVED_AT} | text/html | axes and broadcasting |"
    )
    for duplicate in (False, True):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            handoff, _, _, _ = _build_external(root)
            text = handoff.read_text(encoding="utf-8")
            row = next(line for line in text.splitlines() if line.startswith(identity_row))
            replacement = f"{row}\n{row}" if duplicate else "| none | none | none | none | none | none | none | none | none | none | none |"
            handoff.write_text(text.replace(row, replacement, 1), encoding="utf-8")
            report = validator.validate_handoff(handoff, repo_root=root, ready=True)
            assert "EXTERNAL_IDENTITY" in _codes(report), report.errors


def test_external_hash_and_roadmap_drift_stale_the_review() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        handoff, _, _, _ = _build_external(root)
        external = next(
            root / entry.path
            for entry in validator.validate_handoff(handoff, repo_root=root).document.manifest
            if entry.role == "external-primary"
        )
        external.write_bytes(EXTERNAL_BYTES + b"changed")
        report = validator.validate_handoff(handoff, repo_root=root, ready=True)
        assert {"SOURCE_HASH", "REVIEW_STALE"} <= _codes(report)

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        handoff, _, _, _ = _build_external(root)
        (root / "ROADMAP.md").write_text("# Changed roadmap\n", encoding="utf-8")
        report = validator.validate_handoff(handoff, repo_root=root, ready=True)
        assert {"SOURCE_HASH", "REVIEW_STALE"} <= _codes(report)


def test_external_asset_receipt_is_required_and_identity_checked() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        handoff, _, _, _ = _build_external(root, include_asset=True)
        assert validator.validate_handoff(handoff, repo_root=root, ready=True).ok
        asset = next(
            item
            for item in validator.validate_handoff(handoff, repo_root=root).document.manifest
            if item.role == "external-asset"
        )
        receipt = (
            root
            / "tmp/active-lesson-sources/external-shape-lesson"
            / f"{asset.sha256}.receipt.json"
        )
        payload = json.loads(receipt.read_text(encoding="utf-8"))
        payload["kind"] = "primary"
        receipt.write_text(json.dumps(payload), encoding="utf-8")
        report = validator.validate_handoff(handoff, repo_root=root, ready=True)
        assert "EXTERNAL_CACHE_IDENTITY" in _codes(report)


def test_external_identity_is_separate_from_common_target_relation() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        handoff, _, _, _ = _build_external(root)
        report = validator.validate_handoff(handoff, repo_root=root)
        assert report.ok, report.errors
        document = report.document
        assert document is not None
        identity = document.external_identities["I001"]
        relation = document.external_relations[("CC-DL-01", "I001")]
        assert identity.official_url == OFFICIAL_URL
        assert identity.offering_or_edition == "2026 offering"
        assert identity.scope == "axes and broadcasting"
        assert relation.target_id == document.target_decision.primary_target
        assert relation.relation == "primary"
        assert relation.objective_ids == ["O001", "O002"]
