"""문의 반복 실행 도구.

노트북의 입력 검사, find, 지시문, 모델 요청, 출력 검사를 재사용한다.
튜터가 실행 편의를 위한 함수 구성, CLI, 실행 기록 저장을 추가했다.
"""

import argparse
import json
from pathlib import Path

from inquiry.config import DOCUMENTS_PATH, INPUT_PATH, RUNS_PATH
from inquiry.retrieval import search_idf
from inquiry.service import run_inquiry
from inquiry.storage import latest_runs, load_inquiries, read_runs, save_runs
from inquiry.tools import get_account_status
from ollama import Client


def print_run(run):
    print(f"문의 {run['inquiry_id']}: {run['inquiry_text']}")
    if run["format_error"] is None:
        print("출력 형식 검사 통과")
        if (
            run["output"].get("scope") is not None
            and run["output"]["scope"] == "out_of_scope"
        ):
            print("업무 포털 관련 문의만 처리합니다.")

        print(json.dumps(run["output"], ensure_ascii=False, indent=2))
    else:
        print(f"출력 형식 검사 실패: {run['format_error']}")
        print(run["raw_content"])


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="문의를 실행하거나 저장된 응답을 조회합니다."
    )
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--all", action="store_true", help="모든 문의를 한 번씩 실행")
    action.add_argument("--id", help="실행할 문의 식별자")
    action.add_argument(
        "--history", action="store_true", help="이 도구로 저장한 실행 결과 조회"
    )
    action.add_argument("--latest", action="store_true", help="문의별 최신 응답만 조회")
    action.add_argument("--search", help="검색 결과만 조회")
    action.add_argument("--account-status", help="계정 상태 조회")
    parser.add_argument("--account-id", help="계정 ID")
    parser.add_argument(
        "--top-k", type=int, default=1, help="검색에 사용할 최대 문서 수"
    )
    parser.add_argument("--queries", help="질의 파일 경로", default=None, type=Path)
    parser.add_argument(
        "--documents", help="규정 파일 경로", default=DOCUMENTS_PATH, type=Path
    )

    args = parser.parse_args(argv)

    if args.top_k < 1:
        parser.error("--top-k는 1 이상의 정수여야 합니다.")

    if args.history or args.latest:
        runs = read_runs(RUNS_PATH)
        if args.latest:
            runs = latest_runs(runs)
        if not runs:
            print("저장된 실행 기록이 없습니다.")
            return 0
        for number, run in enumerate(runs, start=1):
            print(f"\n실행 {number}")
            print_run(run)
        return 0

    if args.search is not None:
        if args.search.strip() == "":
            print("검색어는 빈 문자열이 아니여야 합니다.")
            return 0

        documents = search_idf(
            path=args.documents, query_text=args.search, k=args.top_k
        )
        converted = [
            {"order": i, "id": document["id"], "title": document["title"]}
            for i, document in enumerate(documents)
        ]
        if len(documents) == 0:
            print("검색 결과가 없습니다.")
        else:
            print(*converted, sep="\n")

        return 0

    if args.account_status is not None:
        try:
            account = get_account_status(account_id=args.account_status)
        except ValueError as error:
            parser.error(str(error))

        if account is None:
            print("계정이 없습니다.")
        else:
            print(f"계정 ID: {args.account_status}, 계정 상태: {account}")

        return 0

    inquiries = load_inquiries(
        path=args.queries if args.queries is not None else INPUT_PATH,
        text_key="query" if args.queries is not None else "text",
    )
    inquiry_ids = [inquiry["id"] for inquiry in inquiries] if args.all else [args.id]
    client = Client()
    exit_code = 0

    for inquiry_id in inquiry_ids:
        try:
            run = run_inquiry(
                inquiries,
                inquiry_id,
                client,
                account_id=args.account_id,
                top_k=args.top_k,
                document_path=args.documents,
            )
        except (ValueError, OSError) as error:
            parser.error(str(error))

        print_run(run)
        save_runs([run], RUNS_PATH)
        print(f"실행 기록 저장: {RUNS_PATH}")
        if run["format_error"] is not None:
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
