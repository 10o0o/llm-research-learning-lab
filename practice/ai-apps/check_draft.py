"""가상 문의와 계정 자료로 초안 생성의 정상·오류 동작을 확인합니다."""

import json

from inquiry.storage import load_inquiries
from inquiry.tools import build_lock_review_draft, get_account_status


def main():
    inquiry = next(
        (item for item in load_inquiries() if item["id"] == "demo-001"), None
    )
    if inquiry is None:
        raise ValueError("확인에 사용할 문의를 찾을 수 없습니다: demo-001")

    locked_id = "demo-account-001"
    active_id = "demo-account-002"
    locked_status = get_account_status(locked_id)
    active_status = get_account_status(active_id)
    text = inquiry["text"]

    cases = [
        ("잠김 계정", locked_id, locked_status, text, False),
        ("활성 계정", active_id, active_status, text, False),
        ("조회 결과 없음", locked_id, None, text, True),
        ("빈 문의 본문", locked_id, locked_status, "   ", True),
    ]

    for label, account_id, account_status, inquiry_text, expect_error in cases:
        print(f"\n[{label}]")
        try:
            draft = build_lock_review_draft(account_id, account_status, inquiry_text)
        except ValueError as error:
            if not expect_error:
                raise
            print(f"예상한 입력 오류: {error}")
        else:
            assert not expect_error, "잘못된 입력이 거절되지 않았습니다."
            assert draft == {
                "account_id": account_id,
                "account_status": account_status,
                "inquiry_text": inquiry_text,
                "request_status": "draft",
            }
            print(json.dumps(draft, ensure_ascii=False, indent=2))

    print("\n초안 생성 확인 통과")


if __name__ == "__main__":
    main()
