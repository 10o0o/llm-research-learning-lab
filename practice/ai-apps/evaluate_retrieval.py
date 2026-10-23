"""개발 질의의 1위 적중·빈 결과·Recall을 문서 선택 개수별로 평가합니다."""

import argparse
from pathlib import Path

from inquiry.config import DEV_QUERIES_PATH, DOCUMENTS_PATH
from inquiry.retrieval import search_idf
from inquiry.storage import load_dev_queries


def evaluate_query(query, documents):
    relevant_ids = set(query["relevant_ids"])
    retrieved_ids = [document["id"] for document in documents]

    if relevant_ids:
        passed = bool(retrieved_ids) and retrieved_ids[0] in relevant_ids
    else:
        passed = not retrieved_ids

    both = relevant_ids & set(retrieved_ids)
    recall = len(both) / len(relevant_ids) if relevant_ids else None

    return {**query, "retrieved_ids": retrieved_ids, "passed": passed, "recall": recall}


def print_result(result):
    label = "성공" if result["passed"] else "실패"
    criterion = "1위 적중" if result["relevant_ids"] else "빈 결과"
    expected = ", ".join(result["relevant_ids"]) or "없음"
    retrieved = " → ".join(result["retrieved_ids"]) or "없음"
    recall = result["recall"]
    recall_text = f"{recall:.1%}" if recall is not None else "N/A (관련 문서 없음)"

    print(f"[{criterion}: {label}] {result['id']} ({result['group']})")
    print(f"  질문: {result['query']}")
    print(f"  예상 문서: {expected}")
    print(f"  검색 순서: {retrieved}")
    print(f"  Recall: {recall_text}")
    print()


def print_summary(results):
    for has_relevant, label in (
        (True, "관련 문서 있음 — 1위 적중"),
        (False, "관련 문서 없음 — 빈 결과"),
    ):
        selected = [
            result for result in results if bool(result["relevant_ids"]) == has_relevant
        ]
        passed = sum(result["passed"] for result in selected)
        print(f"{label}: {passed} / {len(selected)}")

    recalls = [result["recall"] for result in results if result["recall"] is not None]
    average_recall = f"{sum(recalls) / len(recalls):.1%}" if recalls else "N/A"
    print(f"관련 문서 있음 — 평균 Recall: {average_recall} ({len(recalls)}개 질의)")


def main(argv=None):
    parser = argparse.ArgumentParser(description="개발 질의의 검색 결과를 평가합니다.")
    parser.add_argument(
        "--queries", help="질의 파일 경로", default=DEV_QUERIES_PATH, type=Path
    )
    parser.add_argument(
        "--documents", help="규정 파일 경로", default=DOCUMENTS_PATH, type=Path
    )
    args = parser.parse_args(argv)

    queries = load_dev_queries(args.queries)
    print("개발용 검색 평가 — IDF 검색")

    for k in (1, 2):
        print(f"\n상위 {k}개 문서 선택\n")
        results = []
        for query in queries:
            documents = search_idf(path=args.documents, query_text=query["query"], k=k)
            result = evaluate_query(query, documents)
            results.append(result)
            print_result(result)

        print_summary(results)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
