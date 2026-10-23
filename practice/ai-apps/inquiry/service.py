from inquiry.config import DOCUMENTS_PATH, MODEL_NAME
from inquiry.prompts import build_prompt
from inquiry.retrieval import search_idf
from inquiry.tools import get_account_status
from inquiry.validation import RESPONSE_SCHEMA, parse_and_validate_output


def find(items, predicate):
    """조건을 만족하는 첫 항목을 반환하고, 없으면 None을 반환합니다."""
    for item in items:
        if predicate(item):
            return item
    return None


def run_inquiry(
    inquiries,
    inquiry_id,
    client,
    account_id=None,
    top_k=None,
    document_path=DOCUMENTS_PATH,
):
    account_info = None

    if account_id is not None:
        account_status = get_account_status(account_id)

        if account_status is None:
            raise ValueError("계정이 없음")

        account_info = {"id": account_id, "status": account_status}

    inquiry = find(inquiries, lambda item: item["id"] == inquiry_id)
    if inquiry is None:
        raise ValueError(f"문의를 찾을 수 없습니다: {inquiry_id}")

    documents = search_idf(path=document_path, query_text=inquiry["text"], k=top_k)
    prompt = build_prompt(documents, account_info)

    messages = [
        {"role": "system", "content": prompt},
        {
            "role": "user",
            "content": f"""문의 식별자: {inquiry["id"]}
문의 본문:
{inquiry["text"]}
""",
        },
    ]

    response = client.chat(model=MODEL_NAME, messages=messages, format=RESPONSE_SCHEMA)
    run = {
        "inquiry_id": inquiry["id"],
        "inquiry_text": inquiry["text"],
        "model": MODEL_NAME,
        "messages": messages,
        "raw_content": response.message.content,
        "output": None,
        "format_error": None,
        "tool_result": {"account_info": account_info},
    }
    try:
        run["output"] = parse_and_validate_output(run["raw_content"], documents)
    except (ValueError, TypeError) as error:
        run["format_error"] = f"{type(error).__name__}: {error}"
    return run
