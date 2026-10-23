import json
import math

from inquiry.config import DOCUMENTS_PATH


def load_documents(inquiry_text, path=DOCUMENTS_PATH):
    """공통 단어가 있는 문서를 점수 내림차순으로 반환합니다."""
    with path.open(mode="r", encoding="utf-8") as file:
        documents = json.load(file)

    query_words = set(inquiry_text.split())
    scored_documents = [
        (
            len(query_words & set(f"{document['title']} {document['text']}".split())),
            document,
        )
        for document in documents
    ]
    scored_documents.sort(key=lambda item: item[0], reverse=True)

    return [document for score, document in scored_documents if score > 0]


def search_idf(query_text, path, k=None):
    with path.open(mode="r", encoding="utf-8") as file:
        documents = json.load(file)

    query_words = set(query_text.split())
    words_weight = [0.0] * len(query_words)

    for i, word in enumerate(query_words):
        counts = 0

        for document in documents:
            document_words = set(f"{document['title']} {document['text']}".split())
            if word in document_words:
                counts += 1

        words_weight[i] = math.log(len(documents) / counts) if counts != 0 else 0

    documents_score = [0.0] * len(documents)

    for di, document in enumerate(documents):
        document_words = set(f"{document['title']} {document['text']}".split())

        for wi, word in enumerate(query_words):
            if word in document_words:
                documents_score[di] += words_weight[wi]

    ranked = sorted(
        zip(documents, documents_score), key=lambda pair: pair[1], reverse=True
    )
    result = [document for document, score in ranked if score > 0]
    return result[:k]
