# 문의 보조 Python 실습

같은 업무 문의 서비스에서 검색 근거·모델 응답 검사·계정 조회를 연결하는 실습입니다.
현재 학습 위치와 다음 행동은 [STATE](../../STATE.md), 승인 범위는 [ROADMAP](../../ROADMAP.md)이
정합니다. 이 문서는 저장된 코드의 실행·파일 안내이며 새 과제나 품질 평가 결과가 아닙니다.

## 실행 조건

lab 루트에서 uv 환경을 사용합니다. 의존성과 Python 버전은
[pyproject.toml](../../pyproject.toml)·[.python-version](../../.python-version)을 따릅니다.
모델 생성에는 실행 중인 로컬 Ollama와 [설정된 모델](inquiry/config.py)이 별도로 필요합니다.
이 안내만으로 모델 설치·다운로드·유료 실행이 수행되거나 허용된 것은 아닙니다.

기본 입력은 ignored `materials/private/` 아래의 가상 문의·규정·계정 상태·개발 평가 질의이며
공개 clone에는 없습니다. 실제 경로는 `inquiry/config.py`가 관리합니다. 이력은 ignored
`tmp/ax-inquiry-runs.jsonl`에 추가됩니다. 원자료·정답·개인/고객 자료를 공개 Git에 넣지 않습니다.
공개 clone에서 `--help`는 실행할 수 있지만, 입력·모델 준비 없이 전체 실행을 재현할 수는 없습니다.

## CLI

아래 두 명령은 입력을 읽거나 모델을 호출하지 않고 옵션만 보여줍니다.

```bash
uv run --frozen python practice/ai-apps/inquiry_assistant.py --help
uv run --frozen python practice/ai-apps/evaluate_retrieval.py --help
```

`inquiry_assistant.py`는 다음 동작 중 정확히 하나를 선택합니다.

| 동작 | 현재 코드의 결과·조건 |
|---|---|
| `--id <문의-ID>` | 문의 한 건 검색·모델 응답 검사 후 이력에 추가; 입력과 모델 필요 |
| `--all` | 입력의 모든 문의를 각각 실행·기록; 문의마다 모델 호출 |
| `--history` | 저장 이력 조회; 모델 호출 없음 |
| `--latest` | 문의별 마지막 저장 응답 조회; 모델 호출 없음 |
| `--search <검색어>` | 규정 검색 결과의 순서·ID·제목만 출력; 규정 입력 필요, 모델 호출 없음 |
| `--account-status <계정-ID>` | 설정된 계정 파일에서 상태 조회; 모델 호출·상태 변경 없음 |

| 선택 인자 | 적용 범위 |
|---|---|
| `--account-id <계정-ID>` | `--id`/`--all` 실행 전에 계정을 조회해 모델 근거와 실행 기록에 전달 |
| `--top-k <양의 정수>` | 검색·문의 실행의 최대 선택 문서 수, 기본 1 |
| `--queries <파일>` | 문의 실행 입력 교체; 각 항목의 `query`를 문의 본문으로 사용. 기본 문의 파일은 `text` 사용 |
| `--documents <파일>` | 검색·문의 실행에 사용하는 규정 파일 교체 |

`evaluate_retrieval.py`는 `--queries`와 `--documents`로 개발 평가 입력을 교체할 수 있습니다.
IDF 검색의 상위 1개·2개 결과를 비교하며 관련 문서가 있으면 1위 적중·Recall, 없으면 빈
결과를 확인합니다. 모델은 호출하지 않습니다. 본문 생성 품질이나 운영 유용성을 측정하는
검사가 아니며, 이미 수정에 사용한 질의의 재실행은 개발 검토입니다.

## 파일과 데이터 흐름

| 파일 | 책임 |
|---|---|
| [inquiry_assistant.py](inquiry_assistant.py) | 인자 분기·보기 좋은 출력·실행 이력 저장 |
| [evaluate_retrieval.py](evaluate_retrieval.py) | 개발 질의 검색 평가·요약 |
| [inquiry/config.py](inquiry/config.py) | 입력·기록 경로와 모델 이름 |
| [inquiry/storage.py](inquiry/storage.py) | 입력 로드·검증, JSONL 이력 저장/조회 |
| [inquiry/retrieval.py](inquiry/retrieval.py) | 규정 로드와 검색 |
| [inquiry/prompts.py](inquiry/prompts.py) | 규정·조회 사실과 모델 지시문 구성 |
| [inquiry/service.py](inquiry/service.py) | 문의 선택→검색→모델 요청→응답 검사·실행 결과 구성 |
| [inquiry/validation.py](inquiry/validation.py) | 출력 형식·출처 ID 검사; 내용 정확성을 보장하지 않음 |
| [inquiry/tools.py](inquiry/tools.py) | 로컬 계정 상태 조회와 이미 조회한 값으로 초안을 만드는 helper |
| [check_draft.py](check_draft.py) | 튜터가 제공한 초안 helper 확인 코드; 서비스 연결 완료 증거 아님 |

문의 실행은 CLI 입력→선택적 계정 조회→문의 선택→규정 검색→지시문/메시지 구성→모델 요청→
형식·출처 검사→출력·이력 저장으로 이어집니다. 계정/검색 조회 전용 경로는 모델을 거치지 않습니다.

초안 helper는 이미 조회한 ID·상태와 문의 본문으로 초안 값을 반환하며 재조회·계정 변경·
접수를 하지 않습니다. 현재 문의 흐름에는 아직 연결되지 않았고 초안 CLI 옵션도 없습니다.
고정 Python 함수 호출은 모델이 도구를 선택하는 agent 구현과 다릅니다. 향후 연결에서도
모델의 원인 추정과 실제 조회 상태, 미리보기와 실제 접수를 구별합니다.

학습은 현재 중지 상태이며 이 문서 정비로 재개하지 않습니다. 재개하면 STATE의 한 기능 안에서
정상·초안 미요청·조회값 부재를 관찰합니다. 기존 보조 수행을 새 독립 성공으로 바꾸지 않습니다.
