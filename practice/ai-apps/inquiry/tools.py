import json

from inquiry.config import ACCOUNT_STATUS_PATH


def get_account_status(account_id, path=ACCOUNT_STATUS_PATH):
    if account_id.strip() == "":
        raise ValueError("account_id는 공백이 아니여야 합니다.")

    with path.open(mode="r", encoding="utf-8") as file:
        accounts_dict = json.load(file)

    account_status = accounts_dict.get(account_id, None)

    return account_status


def build_lock_review_draft(
    account_id: str, account_status: str | None, inquiry_text: str
) -> dict[str, str]:
    """이미 조회한 계정 상태와 문의 본문으로 접수 전 초안을 만듭니다."""
    if not account_id.strip():
        raise ValueError("계정 ID는 비어 있을 수 없습니다.")
    if account_status is None:
        raise ValueError("계정 조회 결과가 필요합니다.")
    if account_status not in {"locked", "active"}:
        raise ValueError(f"지원하지 않는 계정 상태입니다: {account_status}")
    if not inquiry_text.strip():
        raise ValueError("문의 본문은 비어 있을 수 없습니다.")

    return {
        "account_id": account_id,
        "account_status": account_status,
        "inquiry_text": inquiry_text,
        "request_status": "draft",
    }
