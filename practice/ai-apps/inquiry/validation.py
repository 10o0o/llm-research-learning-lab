import json


def parse_and_validate_output(content, documents):
    """모델 본문을 JSON으로 파싱하고 필수 출력 항목과 자료형을 검사합니다."""
    if not isinstance(content, str):
        raise TypeError("모델 응답 본문은 문자열이어야 합니다.")

    converted = json.loads(content)
    if not isinstance(converted, dict):
        raise TypeError("모델 출력 전체는 JSON 객체여야 합니다.")

    for field in (
        "summary",
        "facts",
        "missing_information",
        "scope",
        "answer",
        "sources",
    ):
        if field not in converted:
            raise ValueError(f"필수 출력 항목이 없습니다: {field}")

    if converted["scope"] not in ("in_scope", "out_of_scope"):
        raise ValueError("scope 출력이 in_scope, out_of_scope가 아닙니다.")

    for field in ("summary", "answer"):
        if not isinstance(converted[field], str):
            raise TypeError(f"{field}는 문자열이어야 합니다.")

        if field == "answer":  # noqa: SIM102
            if converted[field].strip() == "":
                raise ValueError(f"{field}는 빈 문자열이면 안됩니다.")

    if not converted["summary"].strip():
        raise ValueError("summary는 공백뿐이거나 빈 문자열일 수 없습니다.")

    for field in ("facts", "missing_information", "sources"):
        values = converted[field]
        if not isinstance(values, list):
            raise TypeError(f"{field}는 목록이어야 합니다.")
        for index, value in enumerate(values):
            if not isinstance(value, str):
                raise TypeError(f"{field}[{index}]는 문자열이어야 합니다.")

    documents_ids = {document["id"] for document in documents}
    unknown_doc_source_ids = set(converted["sources"]) - documents_ids
    if unknown_doc_source_ids:
        raise ValueError("제공하지 않은 문서를 인용했습니다.")

    return converted


RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "facts": {"type": "array", "items": {"type": "string"}},
        "missing_information": {"type": "array", "items": {"type": "string"}},
        "scope": {"type": "string", "enum": ["in_scope", "out_of_scope"]},
        "answer": {"type": "string"},
        "sources": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "summary",
        "facts",
        "missing_information",
        "scope",
        "answer",
        "sources",
    ],
}
