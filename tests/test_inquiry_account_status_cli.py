import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "practice/ai-apps/inquiry_assistant.py"


@pytest.mark.parametrize("account_id", ["", "   "], ids=["empty", "whitespace"])
def test_account_status_rejects_blank_id_without_traceback(account_id):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--account-status", account_id],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert "Traceback" not in result.stderr
    assert result.returncode == 2
    assert "error:" in result.stderr
    assert "account_id" in result.stderr
    assert result.stdout == ""


@pytest.mark.parametrize(
    ("error_type", "message"),
    [
        (ValueError, "테스트 계정을 찾을 수 없습니다."),
        (OSError, "테스트 계정 자료를 읽을 수 없습니다."),
    ],
    ids=["invalid-account", "unreadable-data"],
)
def test_inquiry_execution_reports_error_without_saving_run(
    monkeypatch, tmp_path, capsys, error_type, message
):
    monkeypatch.syspath_prepend(str(SCRIPT.parent))
    cli = importlib.import_module("inquiry_assistant")
    inquiries_path = tmp_path / "inquiries.json"
    inquiries_path.write_text(
        json.dumps([{"id": "test-inquiry", "text": "계정 상태를 확인해 주세요."}]),
        encoding="utf-8",
    )
    runs_path = tmp_path / "runs.jsonl"
    monkeypatch.setattr(cli, "INPUT_PATH", inquiries_path)
    monkeypatch.setattr(cli, "RUNS_PATH", runs_path)
    monkeypatch.setattr(cli, "Client", lambda: object())

    def fail_inquiry(*args, **kwargs):
        raise error_type(message)

    monkeypatch.setattr(cli, "run_inquiry", fail_inquiry)

    with pytest.raises(SystemExit) as stopped:
        cli.main(["--id", "test-inquiry", "--account-id", "test-account"])

    captured = capsys.readouterr()
    assert stopped.value.code == 2
    assert "error:" in captured.err
    assert message in captured.err
    assert "Traceback" not in captured.err
    assert captured.out == ""
    assert not runs_path.exists()
