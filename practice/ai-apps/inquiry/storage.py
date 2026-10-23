import json

from inquiry.config import DEV_QUERIES_PATH, INPUT_PATH, RUNS_PATH


def load_inquiries(path=INPUT_PATH, text_key="text"):
    with path.open("r", encoding="utf-8") as file:
        inquiries = json.load(file)

    if type(inquiries) != list:
        raise TypeError("리스트 타입이 아님")

    for inquiry in inquiries:
        if type(inquiry) != dict:
            raise TypeError("문의 하나가 딕셔너리 타입이 아님")
        if not inquiry.get("id") or not inquiry.get(text_key):
            raise ValueError("문의에 id, text 둘 중 하나가 없다")
        if type(inquiry["id"]) != str or type(inquiry[text_key]) != str:
            raise TypeError("문의 id, text 둘 중 하나가 string이 아니다")
        if not inquiry["id"].strip() or not inquiry[text_key].strip():
            raise ValueError("문의 id혹은 text에 공백이 있다")

    return [{"id": inquiry["id"], "text": inquiry[text_key]} for inquiry in inquiries]


def save_runs(runs, path=RUNS_PATH):
    """기존 기록을 유지하면서 실행 결과를 한 줄씩 추가합니다."""
    if not runs:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        for run in runs:
            file.write(json.dumps(run, ensure_ascii=False) + "\n")


def read_runs(path=RUNS_PATH):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def latest_runs(runs):
    """문의별로 파일에서 마지막에 저장된 실행 기록을 선택합니다."""
    latest_by_id = {}
    for run in runs:
        latest_by_id[run["inquiry_id"]] = run
    return list(latest_by_id.values())


def load_dev_queries(path=DEV_QUERIES_PATH):
    with path.open(mode="r", encoding="utf-8") as file:
        queries = json.load(file)

    return queries
