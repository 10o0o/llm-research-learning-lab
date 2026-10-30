# 현재 학습

## 재개 위치

| 항목 | 현재 확인된 상태 |
|---|---|
| 목표 | 단기 AX / AI 애플리케이션 → 장기 LLM Research Engineer |
| 운영 경로 | 2026-10-30 [첫 12주 경로](ROADMAP.md#첫-집중-구간-12주)를 채택했다. 주 30시간 이상을 기준으로 현재 Monitoring 실습 → 자기 데이터 RAG → 필요한 모델 기반 → 단일 추론 실험으로 연결한다. 실제 주차·시작일은 아직 기록하지 않았으며, 첫 프로젝트의 제품·데이터·실습 공간과 후속 모델·장비는 미정이다. 문서 반영은 수강·프로젝트 착수·완료가 아니다. |
| 활성 자료 | **LLM Zoomcamp 2026** — [Module 5: Monitoring](https://github.com/DataTalksClub/llm-zoomcamp/tree/main/05-monitoring). 사용자가 선택한 과정의 공식 순서를 이어가며 main의 단원 원문을 확인한다. |
| 실제 강의 위치 | Module 5 / 3강 완료를 학습자가 보고했다. app.py의 질문 입력·Ask 버튼·spinner·RAG 응답 출력과 Makefile chat target·Streamlit 의존성을 확인했다. 실제 브라우저 응답은 이번에 직접 확인하지 않았으며 수행 완료는 학습자 보고로 기록한다. 공식 [4. Capturing Metrics](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/05-monitoring/04-metrics.md)를 재개한다. 2026-10-28 metrics.py의 LLMCallRecord dataclass 작성을 직접 확인했다. RAGWithMetrics·앱 지표 연결과 4강 실행·완료는 아직 미확인이다. |
| 외부 실습 저장소 | Module 1·4 실습의 실제 경로가 `/home/jake/workspace/learning/llm-zoomcamp-studies/llm-zoomcamp-2026`으로 이동한 것을 확인했다. 기존 원격 연결 기록은 [10o0o/llm-zoomcamp-2026](https://github.com/10o0o/llm-zoomcamp-2026)이며 이번에 push하지 않았다. 현재 별도 AGENTS·CLAUDE는 없다. 기존 Module 3는 `/home/jake/workspace/learning/llm-zoomcamp-studies/03-orchestration`이며 Git·원격 미연결이다. 공식 checkout `/home/jake/workspace/learning/llm-zoomcamp`는 출처다. Module 2 ONNX: `/home/jake/workspace/learning/llm-zoomcamp-studies/llm-zoomcamp-onnx`, 기존 벡터 검색: `/home/jake/workspace/learning/llm-zoomcamp-code`다. |
| 실습 파일·폴더 | metrics.py에 LLMCallRecord dataclass가 있고 RAGWithMetrics는 아직 없다. assistant.py는 RAGBase를 반환하며 app.py는 답변까지만 표시한다. 기존 Makefile run·chat, Streamlit 의존성과 helper·평가 산출물·Git 변경을 보존했다. |
| 다음 행동 | 같은 외부 실습 레포에서 공식 4강의 Instrumented RAG부터 이어가며 metrics.py의 기존 LLMCallRecord를 사용해 RAGWithMetrics로 LLM 호출 시간·토큰·비용을 기록하고 assistant.py가 새 클래스를 반환하도록 연결한다. app.py에서 last_call 지표를 표시한 뒤 make chat으로 질문 한 건과 지표를 확인한다. 비용은 현재 Luna에 맞는 기존 evaluation_utils.calc_price의 total_cost를 재사용하도록 안내한다. 4강의 gpt-5.4-mini 전용 분기를 그대로 쓰면 Luna 비용이 0이 되는 점을 짚는다. |

[외부 실습 안내](docs/external-practice.md)에 따라 실제 실습 위치를 연결했다.
Module 1은 사용자가 만든 `llm-zoomcamp-2026`에서 수행했고, Module 2는 별도 `llm-zoomcamp-code`로 연결했다.
외부 공간에 AGENTS·CLAUDE 파일은 없으며, 이 허브의 지침이 새 외부 세션에 자동 적용된다고 가정하지 않는다.
키 값은 STATE나 공개 저장소에 저장하지 않는다.
URL·시청 위치·구현 결과를 추정해서 채우지 않는다. 자료 안내와 저장소 준비는 수강 완료가 아니다.

## 확인된 수행과 남은 문제

2026-10-26 사용자가 학습 북마크를 초기화했다. 이후 AI가 입력→모델→출력의 역할을 설명하고,
내부 한 문장 요약 실습을 제안했다. 제안 파일 `practice/ai-apps/summarize.py`는 생성되지 않았고,
재시작 후 학습자의 구현·실행·첫 해석은 확인되지 않았다.

같은 날 사용자가 허브에서 자료·진도를 안내하고 외부 저장소에서 수행하는 방식으로 전환을 요청했다.
내부 자체 실습 제안은 현재 시작 경로에서 제외했다. 전환 시점에는 강의 선택, 외부 실습 생성·이전,
실제 학습 완료는 아직 확인되지 않았다. 이번 문서·구조 변경은 학습 진도에 포함하지 않는다.

이후 같은 날 사용자가 LLM Zoomcamp를 주자료로 선택했다. AI는 2026년판 Module 1의 공식 순서,
소개·환경 안내와 공식 AI 사용·프로젝트 정책을 확인했다.

학습자는 소개 안내를 다 읽었다고 보고했다. AI는 LLM의 역할과 한계, RAG의 검색→프롬프트→모델
흐름, 자료 준비와 질문 처리, RAG에서 agent로의 확장을 설명했다. 안내 읽음은 학습자 보고이며,
소개 영상 시청이나 독립 구현·실행·숙달을 확인한 것은 아니다.

학습자는 기존 OpenAI API 키 사용을 선택했고 환경 설정을 마쳤다고 보고했다(키 값 미수집).
AI가 현재 WSL의 `uv 0.12.5`, Python 3.14와 실제 외부 저장소를 확인했다.
외부 `.venv`에서 requests·minsearch·openai·jupyter·python-dotenv·ipykernel 설치를 확인했고,
`.env` 파일의 존재와 Git 제외·미추적 상태를 확인했다. 키 내용은 읽지 않았다.

학습자는 3. RAG에서 FAQ 문맥을 넣는 단계까지 완료했다고 보고했다. AI는 영어 FAQ 네 항목을
한국어로 설명하고 `question`·`context`·`prompt`의 역할을 안내했다.

7번까지 확인한 저장본에서 `load_dotenv()`·`OpenAI()` 준비 셀의 실행과
`클라이언트 준비 완료` 출력을 확인했다. 학습자 코드의 모델은 `gpt-6-luna`이며,
`llm(question)` 응답에는 등록 가능 여부를 확인하고 강의 페이지나 주최 측에 문의하라는
일반적인 안내가 저장되어 있다. FAQ 네 항목과 이를 포함한 프롬프트도 작성되어 있다.

추가 저장본에서 `answer = llm(prompt)`·`print(answer)` 셀의 실행 번호 7과 응답을 확인했다.
FAQ를 제공한 응답은 지금 참여할 수 있으며 수료증을 원하면 접수 기간 안에 프로젝트를 제출해야
한다는 내용이다. 두 호출의 저장된 응답 차이를 AI가 한국어로 설명했다.
학습자 자신의 첫 해석은 아직 제시되지 않았으며, 독립 구현·숙달로 판정하지 않는다.

7번의 `search`·`build_prompt`·새 인자의 `llm`과 세 함수를 연결하는 `rag` 구현·출력을
당시 notebook에서 확인했다. 이후 AI가 `01-rag-through-07.ipynb`로 복사했으나 현재 파일 목록에는
보존본이 없다. 삭제 경위는 미확인이고 복구하거나 사용자 변경을 덮어쓰지 않았다.
`01-rag.ipynb`는 학습자가 초기화한 뒤 분리 모듈의 준비·호출 코드를 작성하던 공간이다.

학습자가 4. The Course FAQ Dataset까지 완료했다고 보고했다. 저장본에서 과정 목록을 가져오고
각 과정의 FAQ JSON을 `documents.extend(course_data)`로 합치는 코드, `len(documents)`의
출력 1,427과 `documents[0]` 출력을 확인했다. 첫 항목에는 `id`·`course`·`section`·
`question`·`answer`가 있고 과정은 `stock-markets-analytics-zoomcamp`다.
이는 저장된 데이터 수집 결과이며, 학습자 자신의 해석은 아직 제시되지 않았다.

학습자가 5. Search까지 완료했다고 보고했다. 저장본에서 `question`·`answer`·`section`을
텍스트 필드로, `course`를 키워드 필드로 지정한 minsearch 인덱스 구성과 `fit(documents)`를
확인했다. 질문 가중치 2.0·section 가중치 0.5, 과정 필터와 상위 5개 반환을 적용한
`search(question, course="llm-zoomcamp")` 함수 및 호출 출력도 확인했다.
LLM 과정의 참여 질문에서는 첫 결과가 참여 가능 여부 FAQ이며, 저장된 다섯 결과 모두
LLM 과정이다. MLOps 과정의 수료증 질문에서도 다섯 결과 모두 과정 필터를 따르지만,
네 번째 Grafana 문서와 다섯 번째 Kinesis 문서는 질문과 관련성이 낮다.
AI가 과정 필터의 동작과 결과별 관련성 차이를 설명했으며, 학습자 자신의 첫 해석과
별도 가중치 변경 실험은 아직 확인되지 않았다. 검색 결과 생성과 검색 품질을 구분한다.
5번 마지막 `results` 변수에는 MLOps 수료증 질문의 결과가 있다. 6번에서는 LLM 과정의
`search_results`를 현재 참여 질문과 함께 전달하여 질문·검색 결과가 맞는 것을 확인했다.

학습자가 6. Building the Prompt까지 완료했다고 보고했다. 저장본에서 `INSTRUCTIONS`,
`USER_PROMPT_TEMPLATE`, `build_context`·`build_prompt` 코드와 실행 번호 22의 프롬프트 출력을
확인했다. 출력에는 참여 질문과 LLM 과정 FAQ 다섯 개의 section·질문·답변이 포함되며,
첫 FAQ는 참여 가능 여부다. 6번 확인 시 미기록이었던 `INSTRUCTIONS` 실행은
7번 추가 저장본의 실행 번호 38로 확인했다. AI는 학습자 코드를 수정하거나 재실행하지 않았다.
7번의 가격 계산은 강의 예제 모델 대신 학습자 코드의 `gpt-6-luna` 공식 단가를 사용한다.

학습자는 7번 진행을 완료했다고 보고했다.
현재 저장본에는 `gpt-6-luna`로 프롬프트를 전송한 코드와 응답 객체,
입력 490·출력 77·총 567 토큰의 사용량이 있다. 출력 토큰 중 reasoning 토큰은 26이다.
`response.output[0]`은 답변 메시지가 아닌 `ResponseReasoningItem`이며,
응답 텍스트는 `response.output_text`로 확인하는 경로를 사용한다.

새 `llm(instructions, user_prompt, model="gpt-6-luna")`에는 developer·user 메시지 구성과
`response.output_text` 반환이 작성되어 있다. 추가 저장본에서 불필요한 `response.history`가
제거되었고 정의 셀의 실행 번호 63과 인사 응답을 확인했다. 이 수정에는 AI의 한 줄 제거 안내가 있었다.

`rag(query, model="gpt-6-luna")` 정의 셀의 실행 번호 65와 참여 질문 호출의 실행 번호 66,
생성 응답을 확인했다. 답변은 지금 참여할 수 있으며 수료증을 원하면 라이브 기수의 접수 기간에
프로젝트 제출과 필수 동료 평가를 완료해야 한다는 내용이다. 검색→프롬프트→고정 지시를 포함한
모델 호출의 전체 연결을 저장본으로 확인했다. 별도 수료증 질문과 가격 계산 결과는 아직
미확인으로 남긴다. 학습자 자신의 첫 해석은 아직 제시되지 않았으며 독립 숙달로 판정하지 않는다.

8번에서 `ingest.py`의 데이터 수집·인덱스 구성 함수와 `rag_helper.py`의 `RAGBase`를 확인했다.
파일명 오타 `rag_helpter.py`는 AI가 지적한 뒤 학습자가 `rag_helper.py`로 수정했다.
8번 확인 당시 notebook은 한 셀이며 필요한 import, `.env` 로딩, 데이터·인덱스 준비와 객체 생성,
참여 질문에 대한 `assistant.rag(...)` 호출이 작성되어 있다. 실행 번호 1과 생성 응답을 확인했다.
응답에는 지금 참여할 수 있고 수료증을 원하면 라이브 기수 접수 기간에 프로젝트 제출과 필수
동료 평가를 마쳐야 한다는 조건이 포함된다. 학습자가 클래스 기본 모델을 `gpt-6-luna`로 바꾼
것도 확인했다. 모듈 분리 후의 전체 실행을 저장본으로 확인했으며, AI가 대신 실행하지 않았다.

초기화로 지워진 이전 실행 기록은 VS Code 로컬 히스토리에서 7번 확인 당시의 원본을 찾아
`01-rag-through-07.ipynb`로 복사했다. 당시 27개 셀과 원본과 동일한 바이트를 확인했으며,
작업 중인 notebook은 덮어쓰거나 재실행하지 않았다. 보존은 AI가 수행했고 새 학습 진도는 아니다.

자동완성 막힘을 조사하며 실습 `.venv`에서 `dotenv.load_dotenv`가 존재하고, Pylance가 같은
인터프리터로 인덱싱했으며 자동 import 설정도 켜져 있음을 확인했다. 학습자는 명시적
`from dotenv import load_`에서도 제안이 없었다가 VS Code reload 후 복구됐다고 보고했다.
UI 복구는 학습자 보고이며 내부 원인은 확정하지 않았다. 편집기 설정·패키지는 변경하지 않았다.

학습자가 9번 수행을 완료했다고 보고했다. 실제 파일 이름은 강의 참고 notebook과 같은
`persistent_rag_ingest.ipynb`와 `persinsent_rag.ipynb`다. `sqlitesearch>=0.3.0` 의존성 추가,
전체 FAQ 1,456개를 불러온 출력과 LLM 과정 필터·SQLite 적재 코드를 확인했다.
조회 notebook에는 같은 `faq.db`를 여는 코드, 개수 161과 검색된 질문 다섯 개가 저장되어 있다.
AI의 읽기 전용 DB 검사에서도 문서와 FTS 인덱스가 각각 161개, 고유 FAQ ID가 161개이며
모두 `llm-zoomcamp`인 것을 확인했다. 적재 중 개수가 증가하는 과정 자체는 확인하지 않았다.

추가 저장본에서 조회용 `persinsent_rag.ipynb`의 실행 번호 7과 RAG 응답을 확인했다.
조회 notebook 자체에서 `load_dotenv()` 후 클라이언트를 생성하고, 기존 DB를 여는
`sqlite_index`를 `RAGBase`에 전달한다. FAQ 다운로드나 `fit` 없이 검색→프롬프트→모델 응답으로
연결되어 있다. 응답에는 시작 후 참여 가능 여부와 라이브 기수의 프로젝트·동료 평가 조건이
포함된다. 이 마지막 연결에는 AI가 기존 호출 코드를 조회 notebook용으로 제시한 도움이 있었고,
학습자가 실행·저장했다. AI는 코드를 수정하거나 재실행하지 않았고 DB는 읽기 전용으로 확인했다.
학습자 자신의 첫 해석은 아직 제시되지 않았으며, 동시 적재 중 개수 변화·영상 시청이나
독립 숙달을 확인한 것으로 확대하지 않는다.

학습자는 10. Wrap-up of Part 1을 읽었다고 보고했다. 정리글 읽음만 기록하며 확장 제안의
추가 구현이나 독립 숙달을 수행한 것으로 보지 않는다.
현재 코드는 검색을 한 번 실행한 뒤 프롬프트와 모델 호출로 이어지며, Part 2에서는 LLM이
도구와 다음 행동을 선택하는 흐름으로 확장한다. 11번은 소개 범위이고 에이전트 구현은 아직
확인되지 않았다. 학습자는 이후 11번 소개도 읽었다고 보고했다. 12번은 Part 1 복습용 선택
단원이며, 이미 수행한 RAG를 처음부터 반복하지 않고 13. Function Calling으로 연결한다.
새 자체 과제나 반복 시험은 추가하지 않는다.

13번 공식 원문과 설치된 OpenAI SDK의 함수 호출 타입, 공식 API 안내를 확인했다.
이번 직접 수행 범위는 도구 정의부터 도구 실행 결과를 모델에 전달해 최종 답변을 받는
한 차례 왕복이다. 도구 없는 일반 응답은 앞선 저장 결과를 참고하고, 반복 에이전트 루프는
다음 14번에서 다룬다. 안내 당시 `function-calling.ipynb`의 생성과 새 응답은 미확인이었으며,
이후 아래 저장본 리뷰에서 확인했다. 기존 `faq.db`·검색 코드와 `gpt-6-luna`를 재사용한다.

공식 예제의 검색 인덱스 변수는 실제 준비한 SQLite 객체에 맞춘다. 함수 호출은
`response.output[0]`으로 가정하지 않고 `type == "function_call"`인 항목을 찾는다.
이전 저장본에서 reasoning 항목이 먼저 오는 것을 확인했으며, 다음 요청에는
`response.output` 전체와 `call_id`가 일치하는 도구 결과를 포함한다. 두 API 요청의
토큰 사용량은 각각 기록하고 가격 계산은 현재 모델의 공식 단가를 적용한다.


학습자가 13강 완료를 보고했다. `function-calling.ipynb`의 실행 번호 1–13과 저장 출력을
확인했다. 도구 없는 첫 응답은 등록 여부를 강의 페이지나 주최 측에 확인하라는 일반 안내다.
이후 `search_tool`을 전달한 응답에는 `search` 함수 호출과 모델이 확장한 참여 관련 검색어가
있다. Python이 JSON 인자를 읽어 기존 `faq.db`를 검색했고, 첫 결과는 참여 가능 여부 FAQ다.
`messages.extend(response.output)`와 같은 `call_id`의 `function_call_output`을 전달한 뒤,
지금 참여할 수 있으며 수료증에는 접수 기간 안의 프로젝트 제출이 필요하다는 답변이 저장되어 있다.
AI는 학습자 코드·notebook을 수정하거나 재실행하지 않았다. 학습자의 첫 해석과 독립 숙달은
미확인이다. 두 도구 관련 API 요청의 사용량·비용 계산 출력도 저장본에는 없어 미확인으로 남긴다.

현재 코드는 공식 13번처럼 `call = response.output[0]`을 사용한다. 이번 저장 응답의 첫 항목은
실제로 함수 호출이므로 성공했으나, reasoning 등 다른 항목이 먼저 오는 경우에는 취약하다.
14번 공식 원문 `main`을 확인했으며, 응답 항목을 `type`으로 나누어 모든 함수 호출을 처리하는
공식 반복 구조로 이어간다. `make_call`·`agent_loop`, 함수 호출 없는 턴의 종료, 전체 응답과
도구 결과의 누적이 이번 범위다. 기존 notebook에서 이어 쓰며 현재 모델을 유지한다.
공식 오타 `Olama`·참여 질문과 다중 검색·주제 제한 지시 변경을 실행해 실제 호출 로그를 본다.
검색 횟수나 오타 교정 성공을 미리 보장하지 않았으며, 이후 아래 저장본 리뷰에서 14번 구현·실행을 확인했다.

학습자가 14번 수행 완료를 보고했다. `function-calling.ipynb`의 추가 셀에서 `instructions`,
`make_call`, 직접 반복문과 `agent_loop` 정의(실행 번호 31–34), 네 호출의 저장 출력(35–38)을
확인했다. 함수는 매 질문에 developer·user 메시지를 새로 구성하고 전체 모델 출력과 도구 결과를
누적하며, `item.type`으로 분기하고 함수 호출 없는 턴에 종료한다. 모델은 `gpt-6-luna`다.
`Olama` 질문은 2회 반복 후 Ollama 실행 안내, 참여 질문은 3회 후 참여·수료 조건 안내가 있다.
FAQ 범위로 제한한 체스 질문은 3회 후 FAQ로 답할 수 없다고 했으며, 이후 다중 검색 지시의
참여 질문도 3회 후 답변이 저장되어 있다. 반복 횟수는 모델 호출 횟수이며 검색 횟수와 같지 않다.
`agent_loop`에는 함수 이름·인자 출력이 없어 검색어 변화, 정확한 검색 횟수와 `Olama`→`Ollama`
재검색 경로는 미확인이다. 최종 문장의 철자 교정만으로 재검색 성공을 인정하지 않는다.

독립된 반복문 초안에는 `elif item.type == "messWage"` 오타가 있고 이전 13번 메시지를 재사용해
실행 출력이 `iteration #1...`만 남았다. 실제 사용한 `agent_loop`는 `message`로 올바르게 분기한다.
학습자에게 초안의 오타 수정과 함수 호출 분기의 이름·인자 로그 추가를 안내하며, 핵심 반복
실행이 확인되었으므로 전체 재구현·반복 시험을 요구하지 않는다. 학습자의 첫 해석·독립 숙달과
토큰·비용은 미확인이다. AI는 학습자 코드·notebook을 수정하거나 재실행하지 않았다.

15번 공식 원문 `main`을 확인했다. 다음은 기존 검색 함수를 ToyAIKit에 등록하고 수동/자동
스키마, runner, callback 표시, `LoopResult`의 대화·사용량·비용, `previous_messages`를 통한
후속 질문과 대화 입력을 살펴보는 공식 범위다. 안내 당시 설치·15번 구현·실행은 미확인이었으며,
이후 아래 저장본 리뷰에서 수행 범위를 확인했다.
기존 DB·모델을 재사용하고, 프레임워크가 14번의 반복·메시지 관리를 맡는 흐름으로 연결한다.

학습자가 15번 완료를 보고했다. 외부 `pyproject.toml`에 `toyaikit>=0.0.11`이 있으며,
`function-calling.ipynb` 추가 셀의 실행 번호 24–35에서 수동 스키마 등록, 타입 힌트·docstring을
이용한 자동 도구 등록과 `get_tools()`의 JSON 스키마 출력, runner·callback 구성을 확인했다.
현재 모델 `gpt-6-luna`, 기존 SQLite 검색을 유지한다. `result = runner.loop(...)`의 저장 HTML과
`result.all_messages`에는 첫 검색, 결과 반환, 두 번째 검색과 최종 답변이 있다.
첫 검색어부터 `Olama`와 올바른 철자 `Ollama`를 함께 사용해 설치 FAQ를 찾았고, 이후
`ollama serve`, `localhost 11434`, Python 등의 키워드를 확장했다. 이는 실제 다중 검색의
근거이며, 첫 검색 실패 후 철자를 고친 경로라고 해석하지 않는다.

`result2 = runner.loop(prompt="How do I run a different model?", previous_messages=result.all_messages,
callback=callback)`와 HTML 출력을 확인했다. 후속 검색어는 Ollama의 다른 모델 실행을 명시하고,
답변에는 모델 이름을 바꾸는 `ollama run qwen2.5` 등의 안내가 있어 이전 대화 맥락 연결이
확인된다. 이는 모델의 생성 답변이며 Ollama 설치·명령 실행을 학습자가 수행했다는 근거는 아니다.
비용 출력 `result.cost`와 대화형 `runner.run()` 코드는 당시 30개 셀의 저장본에 없어 미확인이었다.
첫 질문·후속 질문을 다시 구현하거나 반복 실행시키지 않고 이 두 공식 항목만 다음 행동으로 둔다.
학습자 자신의 첫 해석과 독립 숙달은 미확인이며, AI는 notebook을 수정하거나 재실행하지 않았다.

16. Other Frameworks 공식 `main`도 확인했다. 프레임워크의 공통 도구·반복 구조와 에이전트의
추가 호출·시간·비용을 정리하는 다음 읽기 범위다. AI가 확인한 것이며 학습자가 읽었다는 뜻은
아니다. 여러 프레임워크 설치나 별도 구현 과제를 새로 추가하지 않는다.

학습자가 남은 비용 확인·대화형 실행도 완료했다고 보고했다. 추가 저장본은 32개 셀이며,
`result.cost` 셀의 실행 번호 36과 `CostInfo`를 확인했다. input_cost 0.0004389,
output_cost 0.0002225, total_cost 0.0006614는 ToyAIKit이 첫 `result`에 계산한 값이며,
후속 `result2`나 모든 학습 실행의 총비용 또는 공급자 실제 청구액으로 확대하지 않는다.
`runner.run()` 셀은 존재하지만 execution_count가 null이고 출력이 없어, 대화 입력·답변·stop
종료는 학습자 완료 보고로만 기록한다. 저장 출력 부재만으로 미수행이라 단정하거나 반복 실행을
요구하지 않는다. 15번에서 확인한 핵심 연결을 유지하고 다음 16번 읽기로 진행한다.
AI는 notebook 수정·재실행이나 유료 API 호출을 하지 않았다.

학습자가 16. Other Frameworks를 다 읽었다고 보고했다. 읽음만 확인하며 프레임워크 추가
설치·실행, 전체 영상 시청·독립 숙달이나 공식 과제 제출을 수행한 것으로 확대하지 않는다.
공식 Module 1 목차와 Module 2 / `01-intro.md`의 현재 `main` 원문을 확인했다.
16번의 다음 링크와 소개의 이전 링크가 서로 연결되므로 공식 순서대로 Vector Search 소개로
이어간다. 현재 범위는 소개 읽기이며 Module 2 구현·실행은 아직 없다.
소개는 기존 FAQ를 embedding으로 변환해 인덱싱하고 질문도 같은 모델로 변환해 유사도를 찾는
흐름과 minsearch·sqlitesearch·PGVector 적용 순서를 다룬다. 새 실습 환경 권고는 무거운
sentence-transformers/PyTorch 설치를 분리하기 위한 것이며, 후속 실습 진입 때 기존 외부
저장소 구조·지침을 확인해 연결한다. 새 프로젝트·notebook·패키지는 AI가 만들거나 설치하지 않았다.
이전 도움·사용량 계산 범위·대화형 실행의 보고/출력 구분과 선택 복습 미수행은 그대로 보존한다.

사용자가 Module 2용 `llm-zoomcamp-code`를 직접 만들었다고 보고하고 원격 연결을 요청했다.
실제 새 폴더와 기존 Git 초기화, 미커밋 초기 파일 6개, 원격 미설정 상태를 확인했다.
인증된 GitHub 계정은 `10o0o`이며 같은 이름의 원격 저장소가 없어 비공개로 생성했다.
사용자가 만든 초기 프로젝트에 `.env`·`.env.*`와 notebook checkpoint 제외 규칙을 추가하고,
`.env.example`은 예외로 뒀다. 가상환경 제외는 유지했다. 초기 파일의 비밀키 형태 검사에서
후보가 없었으며 `.env`·가상환경의 Git 제외를 확인했다. 비밀키 파일 내용을 읽거나 올리지 않았다.

초기 파일 6개를 커밋 `f8838705f07c8d2f3c63ecff7d3ca8e698e211cd`로 만들고 새 원격 `master`에
push했다. 로컬 HEAD·upstream·`git ls-remote`의 SHA 일치, private 설정, 깨끗한 실습 worktree와
`origin/master` 추적을 확인했다. 연결·초기 커밋은 AI의 관리 작업이며 Module 2 학습 구현이 아니다.
`pyproject.toml`의 sentence-transformers 등 의존성 선언을 확인했으나 설치 성공·임베딩 실행은
아직 검증하지 않았다. 새 공간에는 AGENTS·CLAUDE가 없고 지침 파일을 추가하지 않았다.
현재 허브 세션에서는 학습자가 핵심 구현·실행·첫 해석을 담당하는 규칙으로 계속 돕는다.
Module 1 폴더·원격은 변경하지 않았다. 허브 STATE는 로컬 갱신이며 이번 요청으로 허브를
커밋·push한 것은 아니다. 연결 당시 Module 2 소개 완료는 아직 보고되지 않았었다.

사용자가 새 원격을 공개로 바꾸라고 명시적으로 요청했다. GitHub 저장소 설정을 변경한 뒤
`gh repo view`의 `visibility: PUBLIC`으로 반영을 확인했다. 커밋·브랜치·실습 코드는 변경하지 않았다.
사용자는 이어 Module 2의 1강도 다 봤다고 보고했다. 소개 완료는 학습자 보고이며 임베딩 구현·실행과
구분한다. 다음 공식 `02-embeddings.md` 원문을 확인했다.

2번은 sentence-transformers의 CPU PyTorch 설정, `all-MiniLM-L6-v2`, 문장 인코딩과 유사도
비교, 정규화된 벡터의 내적과 cosine 연결을 다룬다. 새 실습의 pyproject에는 이미
sentence-transformers가 선언되어 있지만 CPU 전용 torch index 설정은 없어 공식 설치 안내부터
확인하도록 연결한다. AI가 환경 설정·설치나 모델 다운로드를 대신 수행하지 않았다.
`embeddings.ipynb`는 사용할 파일명 제안이며 생성·학습자 실행은 아직 미확인이다.
공식 예제의 384차원과 유사도 수치는 참고값이며 실제 학습자 출력과 해석을 기다린다.
허브 STATE는 로컬 갱신이며 이번 요청으로 허브를 commit·push하지 않았다.

학습자가 2번도 다 했다고 보고하고 다음 진행을 요청했다. 실제 `embeddings.ipynb`는 코드 셀
4개이며 실행 번호 1–3에서 `SentenceTransformer("all-MiniLM-L6-v2")`, 참여 질문 인코딩과
`v1.shape: (384,)` 출력이 확인됐다. 마지막 셀은 비어 있고 문서 `d`·`dv`, Docker 질문 `q2`·`v2`,
두 내적 결과는 현재 저장본에 없다. 미저장 작업 가능성을 열어 두고 비교까지 작성했다면
저장본을 갱신하도록 안내한다. 로딩·참여 질문을 다시 구현하거나 재실행할 필요는 없다.
pyproject의 CPU PyTorch index 추가도 확인했으나 실제 설치된 torch 빌드는 미확인이다.
학습자의 비교 결과·첫 해석과 독립 숙달은 아직 미확인이다. AI는 notebook을 수정·재실행하지 않았다.
공식 다음 3번 원문도 확인했으며, FAQ 전체를 질문+답변 텍스트로 만들고 배치 임베딩하는
후속 범위다. 당시 유사도 비교 저장을 다음 행동으로 안내했으나, 아래 학습자의 명시적 요청에 따라
완료 보고로 반영하고 3번으로 진행한다.

학습자가 유사도 비교는 했다고 기록하고 넘어가자고 명시적으로 요청했다. 2번 비교는
학습자 완료 보고로 기록하고 저장 출력 직접 확인과 구분한다. 출력 저장·재실행·반복 확인을
진행 조건으로 요구하지 않는다. 비교 수치·자신의 해석이나 독립 숙달을 새로 추정하지 않는다.
다음은 공식 3번 전체 FAQ 임베딩이다. Module 1의 실제 `ingest.py`에 `load_faq_data()`가 있는
것을 읽어 확인했으므로 자기 코드를 새 폴더로 복사해 재사용하도록 안내한다. AI는 파일을
복사하거나 notebook·모델을 실행하지 않았다. 같은 모델과 notebook을 이어 쓰고, 문서당
질문+답변 텍스트 하나, 50개 단위 배치, NumPy 행렬의 `(N, 384)` 연결을 다룬다.
강의의 1208개는 예시이며 실제 FAQ 수 `N`을 기준으로 한다. 안내 당시 3번 구현·실행은 미확인이었으며
이후 아래 저장본으로 확인했다.

학습자가 3번 완료를 보고했다. Module 2에 `ingest.py`가 있고 `embeddings.ipynb`의
실행 번호 4–10에서 FAQ 로딩, 각 문서의 질문+답변 연결, `len(texts): 1456`, 50개씩 인코딩하는
배치 반복, `len(vectors)` 1456과 `X.shape` `(1456, 384)`를 확인했다. 저장된 진행바는 0%지만
후속 벡터 개수와 행렬 출력이 있어 전체 인코딩 결과를 확인한 것으로 기록한다.

추가 실행 번호 12–13에는 참여 질문을 정규화해 인코딩하고, 각 문서 행을 정규화한
`X_normalized @ q`, `np.argsort(scores)[::-1][:5]`와 검색된 질문 다섯 개가 저장되어 있다.
최상위는 참여 가능 여부 FAQ이며 점수는 0.7784726, 나머지도 참여 관련 질문이다.
4번 공식 원문과 비교해 핵심 수동 벡터 검색이 이미 구현·실행된 것을 확인했으므로 반복 구현을
요구하지 않고 5번으로 이어간다. 문서 과정·답변은 이 검색 출력에 없고 과정 필터는 아직 없다.
4번 영상 시청·글 전체 읽음이나 학습자 첫 해석·독립 숙달은 추정하지 않는다.
2번의 두 유사도 비교는 기존 학습자 완료 보고 구분을 유지한다.

공식 5번 원문을 확인했다. 기존 행렬과 문서를 같은 순서로 `VectorSearch`에 넣고, 질문
인코딩과 검색, 과정 필터를 연결하는 범위다. 데이터를 다시 수집·임베딩하는 과제를 추가하지
않는다. 6번 RAG 연결은 아직 다음 범위이며 현재는 5번 검색 결과까지다.
AI는 학습자 파일·출력을 수정하거나 재실행하지 않았다. 외부 `pyproject.toml` 수정과 새
notebook·ingest 파일은 미커밋 상태로 보존했고 commit·push하지 않았다.

학습자가 5번 완료를 보고했다. `embeddings.ipynb` 실행 번호 14–19에서 course 키워드 필드의
`VectorSearch`, `fit(X, documents)`, 질문 인코딩, 필터 없는 상위 5개 검색과 이후
`filter_dict={"course": "llm-zoomcamp"}` 검색을 확인했다. 필터 없는 저장 결과에는 LLM·ML·MLOps·
Data Engineering 과정이 섞여 있다. 필터 후 저장된 질문/답변은 참여, 라이브 기수 수료 조건,
로컬 환경, 인증서 시간, OpenAI 대체 제공자 순이다. 과정 필터 적용 코드와 실행·답변 출력은
확인했으나 후자의 출력에는 course 필드가 없으므로 필드 자체를 직접 확인했다고 확대하지 않는다.
상위 두 결과는 참여·수료 조건에 직접 연결되고 나머지는 강의 관련이지만 참여 질문과 관련성이
낮다. 필터 적용과 검색 관련성을 구분하며 추가 출력·재실행을 진급 조건으로 요구하지 않는다.
학습자의 첫 해석·독립 숙달은 미확인이며, AI는 notebook을 수정하거나 재실행하지 않았다.

6번 공식 원문과 학습자가 작성한 Module 1의 실제 `rag_helper.py`를 읽었다.
`RAGBase`의 build_prompt·llm·rag를 재사용하고, `RAGVector`의 생성자에 embedder를 받으며
search에서 질문을 벡터로 바꾸고 course 필터를 적용하는 공식 범위다. 기본 생성 모델은 기존
`gpt-6-luna`를 유지하고 임베딩 모델은 기존 SentenceTransformer 객체를 사용한다.
기존 X·vindex를 재사용하며 키워드 RAG를 다시 처음부터 구현하거나 데이터를 재임베딩하지 않는다.
새 폴더에 `rag_helper.py`를 재사용하고 OpenAI 클라이언트를 준비하는 것은 학습자가 수행한다.
6번 새 클래스·호출·응답, .env 연결은 아직 미확인이다. 실습 파일 commit·push는 하지 않았다.

학습자가 6번 완료를 보고했다. 새 파일의 실제 이름은 `rag_helper.py`가 아닌 `reg_helper.py`이며
notebook도 `from reg_helper import RAGVector`를 사용하므로 파일명 불일치는 없다.
파일에 RAGBase의 기존 프롬프트·Responses 호출과 RAGVector의 embedder 초기화·검색 재정의가
작성되어 있다. 검색은 질문을 encode한 벡터, 과정 필터, num_results를 인덱스로 전달한다.
생성 모델은 `gpt-6-luna`다. notebook의 OpenAI 준비 셀 실행 번호 20은 확인했다.
후속 객체 생성·rag 호출 셀은 execution_count null이고 출력이 없어 최종 응답은 저장본으로
직접 확인하지 못했다. 완료는 학습자 보고로 기록하고 실행·응답을 검증한 것으로 확대하지 않으며,
저장 출력 부재를 이유로 반복 실행을 요구하지 않고 7번으로 진행한다.

7번 공식 원문을 확인했다. 기존 문서 벡터를 SQLite에 영구 저장하고, 다른 notebook에서
모델·DB를 열어 질문만 인코딩한 뒤 검색·RAG를 수행하는 범위다. 공식 `mode="ivf"`,
`faq_vectors2.db`, course 필터와 close/reopen 흐름을 따른다. 조회 notebook에는 문서 재수집·
재임베딩·fit을 넣지 않는다. 기존 `reg_helper.py`에서 RAGVector를 import해 재사용한다.
`persistent-vector-rag.ipynb`는 새 조회 notebook 이름 제안이며 생성·DB 적재·7번 실행은 미확인이다.
AI는 파일을 수정·복사하거나 notebook·API를 실행하지 않았고 commit·push도 하지 않았다.

2026-10-27 학습 재개 시 `embeddings.ipynb`의 최신 저장본에서 OpenAI 준비 셀 실행 번호 16,
RAGVector 객체 생성 17, `assistant.rag(...)` 호출 18과 응답을 확인했다. 응답은 지금 참여할 수
있으며 과제 접수 중에는 과제를 제출할 수 있고, 수료증에는 프로젝트 접수 기간 안의 제출이
필요하다는 내용이다. 위 6번 최종 응답의 미확인은 이 저장본 확인으로 해소했다.
학습자의 첫 해석·독립 숙달을 새로 판정하지 않으며 AI는 notebook을 수정·재실행하지 않았다.
7번 공식 `main` 원문을 다시 확인했다. 현재 파일 목록에는 벡터 DB와 별도 조회 notebook이
없고 `pyproject.toml`에 sqlitesearch 의존성 선언도 없어, 기존 다음 행동을 유지한다.

같은 날 학습자가 7번 완료를 보고하고 저장본 리뷰와 다음 단원 진행을 요청했다.
`pyproject.toml`의 `sqlitesearch>=0.3.0`, 실제 `faq_vector2.db` 파일과 notebook의 실행 번호
31–33·35–37에서 `mode="ivf"` 인덱스 생성, `fit(X, documents)`, 검색·course 필터·close를
확인했다. 필터 없는 결과에는 여러 과정이 섞이며, 필터 후 저장된 5개 결과의 course는 모두
`llm-zoomcamp`다. 최상위는 참여 가능 여부 FAQ다. 필터 없는 결과 표시 셀은 실행 번호가
null이지만 출력은 저장되어 있으며, notebook 전체 저장 출력에는 오류 항목이 없다.

별도 조회는 제안한 새 notebook 대신 `new_session.py`로 구현했다. 같은 DB와 임베딩 모델을
열고 문서 재수집·재임베딩·fit 없이 질문 인코딩과 RAG·close를 수행하는 코드다. 기존 RAGBase를
import하고 RAGVector는 스크립트 안에 다시 정의했다. 기존 `reg_helper.py`의 RAGVector와 같은
구조이므로 이후 재사용할 수 있다. 스크립트 실행 로그·최종 응답은 저장본에서 확인하지 못했으며
학습자의 완료 보고로 구분한다. 출력 부재를 이유로 반복 실행을 요구하지 않는다.
학습자의 첫 해석·독립 숙달은 새로 판정하지 않았고, AI는 실습 파일을 수정하거나 실행하지 않았다.

공식 8번 `main` 원문을 확인했다. Docker의 `pgvector/pgvector:pg17`, psycopg v3,
vector(384) 테이블·벡터 적재, cosine distance `<=>` 검색·course 필터, HNSW 인덱스와
RAGPgVector 연결이 다음 범위다. 살아 있는 기존 커널의 문서·벡터·모델은 재사용한다.
현재 WSL에서 `docker --version`과 컨테이너 목록 조회는 Docker 명령을 사용할 수 없다는
WSL 통합 안내로 실패했다. Docker Desktop의 실제 실행·설정 상태는 미확인이며
[공식 WSL 안내](https://docs.docker.com/desktop/features/wsl/)에 따라 연결 확인부터 진행한다.
8번 컨테이너 시작·설치·테이블 생성·검색은 아직 수행하지 않았다. AI는 commit·push하지 않았다.

2026-10-27 학습자가 현재 진행 중이던 8번 강의 완료를 보고했다. 최신 `embeddings.ipynb`의
실행 번호 26–29에서 psycopg 연결·vector 확장, vector(384) 테이블 생성, 기존 문서·벡터
적재와 commit을 확인했다. 33번의 course 필터 검색 출력은 5개 모두 `llm-zoomcamp`이며,
최상위 참여 FAQ의 cosine similarity는 0.8365다. 38번에서 HNSW 인덱스 생성 성공 응답,
41번 검색 함수 정의, 50번 검색 함수 호출과 문서 결과도 확인했다.

`reg_helper.py`에는 vec_to_str와 RAGPgVector가 있으며, 기존 RAGBase를 상속하고 DB 연결로
course 필터·거리순 검색을 수행한다. `new_session_pg.ipynb`의 실행 번호 1–5에서 클라이언트·
같은 임베딩 모델·별도 DB 연결을 준비하고 이 클래스를 import해 RAG를 호출했다.
저장 응답은 지금 참여할 수 있으며 수료증에는 접수 기간 안의 프로젝트 제출이 필요하다는
내용이다. 별도 조회 notebook에는 문서 재적재·재임베딩이 없고 저장 오류도 없다.
PGVector 접속·실행은 저장본으로 확인했으나 Docker Desktop 설정이나 컨테이너 상태를
직접 재확인한 것은 아니다. 학습자의 첫 해석·독립 숙달도 새로 판정하지 않았다.

HNSW 생성 응답은 INTRANS이며 이후 commit은 저장본에 없었으나, 학습자가 별도로 커밋을
완료했다고 추가 보고했다. 생성 실행의 직접 확인과 커밋 수행 보고를 구분하며 커밋을 남은
과제로 두거나 반복 실행을 요구하지 않는다. 실제 쿼리에서의 인덱스 사용 여부는 별도로
확인하지 않았다. 기존 SQLite fit 셀에는 이미 문서가 있는 인덱스라는 ValueError가 남아
있으나 이번 PGVector 검색·RAG의 성공과 구분한다.
AI는 DB 초기화·학습자 코드 수정·notebook 재실행·API 호출을 하지 않았다.

공식 9번 `main`과 연결된 download.py·embedder.py를 확인했다. 강의는 PyTorch 의존성과
환경 크기를 분리하기 위해 별도 프로젝트를 사용한다. ONNX 모델 다운로드·모델 폴더 Git 제외,
토큰화·추론·attention mask를 반영한 mean pooling·L2 정규화를 거치는 Embedder,
두 문장의 유사도 비교·FAQ 배치 임베딩·검색이 다음 범위다. 원문의 환경 크기 비교 수치를
학습자 환경의 실측값으로 취급하지 않는다. 실제 형제 폴더는 아직 없으며 AI가 프로젝트나
모델 파일을 생성·설치·다운로드하지 않았다. 허브 STATE는 로컬 갱신이며 commit·push하지 않았다.

2026-10-27 학습자가 ONNX 프로젝트를 만들었다고 보고하고 이전 학습 저장소처럼 공개 원격
동기화를 요청했다. 실제 위치는 제안했던 learning 바로 아래가 아니라
`/home/jake/workspace/learning/llm-zoomcamp-studies/llm-zoomcamp-onnx`다. 사용자 초기 Git은
커밋 없는 master였고 원격이 없었다. 새 공간과 상위 studies 폴더에 AGENTS·CLAUDE는 없었다.
기존 Module 1·2 폴더와 원격도 읽기 전용으로 확인했으며 이동·변경하지 않았다.

사용자 초기 프로젝트·의존성 선언과 작업 중 추가된 download.py를 보존했다. AI는 .gitignore에
`.env`·`.env.*` 제외와 `.env.example` 예외, models/·ONNX 모델 파일·notebook checkpoint
제외를 추가했다. 기존 .venv 제외는 유지했다. 게시할 7개 파일과 staged 내용의 비밀키 형태
검사에서 후보가 없었으며, 환경·모델 파일이 제외되는 것을 확인했다. 키 내용은 읽지 않았다.

GitHub에 공개 `10o0o/llm-zoomcamp-onnx`를 생성하고 초기 커밋
`318c8294823dddb636e6619590d61cafece5f320`을 master로 push했다. 로컬 HEAD·origin/master·
git ls-remote의 SHA 일치, `visibility: PUBLIC`, upstream 추적과 깨끗한 worktree를 확인했다.
확인 시점에 models/ 폴더는 있었으나 가중치 내용·다운로드 성공·추론 실행은 확인하지 않았다.
프로젝트 생성·download.py 작성은 사용자 수행이고, AI의 ignore 정리·커밋·원격 연결은 관리
작업이다. 의존성 설치·커널 등록·9번 실행·완료나 숙달로 확대하지 않는다.
AI는 모델·notebook을 실행하지 않았고 허브 STATE는 로컬만 갱신하며 commit·push하지 않았다.

2026-10-27 학습자가 현재 진행 중이던 9번 완료를 보고했다. 실제 ONNX 프로젝트에
download.py·embedder.py·ingest.py와 `embedding.ipynb`가 있다. Embedder는 ONNX CPU 실행,
토큰화·attention mask 기반 mean pooling·L2 정규화를 수행하고 encode·encode_batch를
제공한다. 모델·tokenizer 파일의 존재·크기와 Git 제외를 확인했으며 가중치 내용은 읽지 않았다.

notebook은 코드 셀 7개다. 실행 번호 1에서 Embedder 생성과 세 문장의 encode,
3·4에서 참여 질문과 등록 안내의 내적 0.32332391095966817, Docker 질문과 같은 안내의
내적 0.019730407140850777을 확인했다. 5·7에서 FAQ 로딩과 질문+답변 연결,
8에서 50개 단위 배치 임베딩·NumPy 변환, 9에서 질문 인코딩·내적·argmax와 최상위 문서를
확인했다. 진행바는 0%로 저장됐으나 후속 벡터 검색 결과가 있어 배치 결과를 사용한 검색을
확인한다. 최상위는 data-engineering-zoomcamp의 시작 후 참여 가능 여부 FAQ다.
과정 필터 없는 전체 FAQ 검색이므로 다른 과정의 결과 자체를 오류로 판단하지 않는다.
저장된 오류 항목은 없다. 벡터 행렬 shape·PyTorch와의 직접 수치 대조·환경 크기 비교는
이번 저장본에서 확인하지 못했으며 이를 추가 진급 조건으로 요구하지 않는다.

앞선 질문에는 사전학습 모델 로딩·encode 추론·검색 인덱스 fit과 모델 가중치 학습의 차이를
AI가 설명했다. 설명을 제공한 것과 학습자의 첫 해석·독립 숙달을 구분한다.
이번 리뷰에서 학습자 파일·출력을 수정하거나 재실행하지 않았다. download.py 수정과
신규 embedder.py·ingest.py·notebook은 미커밋 상태로 보존했고 commit·push하지 않았다.

공식 9번과 다음 10번 `main` 원문을 확인했다. 10번은 Module 2 요약과 검색 도입 기준을
읽는 범위다. text search에서 시작해 검색 품질 평가로 vector search의 추가 비용을 판단하고,
hybrid search·reranking은 후속 Best Practices 단원과 연결한다. 원문의 추가 모델·데이터셋·
벡터 DB 실험 제안을 새로운 필수 과제로 만들지 않는다. 10번 읽음과 Module 2 전체 완료는
아직 보고되지 않았으며 다음 Module 3를 자동 시작하지 않는다.

2026-10-27 학습자가 Module 2 / 10. Next Steps를 다 읽었다고 보고했다. 읽음은 학습자
보고로 기록하며 모든 영상 시청·선택 실험·공식 과제 제출·독립 숙달까지 확대하지 않는다.
앞서 확인한 구현·출력과 도움 이력, HNSW commit 수행 보고와 직접 수치 대조 등의 미확인
구분을 유지한다. 추가 모델·대규모 데이터·다른 벡터 DB 실험을 새 필수 과제로 요구하지 않는다.

단계 전환에 필요한 ROADMAP·CURRICULUM의 해당 부분과 공식 Module 2 / 10번,
Module 3 README·01-intro의 현재 main 원문을 확인했다. 10번의 next_url과 소개의 prev_url이
서로 연결되므로 선택한 과정의 공식 순서대로 Module 3 소개 읽기를 다음 행동으로 둔다.
이번 범위는 Kestra 기반 AI 작업 흐름과 모듈 목표를 읽는 것이며 새 flow 구현이 아니다.
공식 순서는 Introduction → Context Engineering → Setting up Kestra → AI Copilot →
RAG → AI Agents → Multi-Agent Systems → Best Practices → Next Steps다.
예제는 Gemini를 사용하지만 소개에서 다른 주요 제공자도 지원한다고 명시한다. 현재 소개
읽기를 위해 새 계정·키·환경을 요구하지 않으며, 실제 제공자 선택·설치·실습 공간 연결은
설정 단원에서 기존 공간·환경과 함께 확인한다. Module 3 파일·저장소·환경은 생성하지 않았다.
소개 읽음·Kestra 설치·flow 실행은 아직 보고되지 않았다. 허브 STATE는 로컬 저장이며
이번 요청으로 기존 실습이나 허브를 commit·push하지 않았다.

2026-10-27 학습자가 Module 3 / 1. AI Orchestration 소개를 다 읽었다고 보고했다.
읽음은 학습자 보고로 기록하며 영상 시청·Kestra 설치·flow 구현·독립 숙달로 확대하지 않는다.
공식 1번과 2. Context Engineering의 main 원문을 확인했다. 서로 next_url·prev_url로
연결되므로 다음 행동은 2번 읽기와 원문의 무문맥 생성 실험이다.

2번은 기존 문맥이 없는 ChatGPT 대화에서 NYC taxi CSV를 추출하고 GCS에 올린 뒤
BigQuery에 적재하는 Kestra flow를 생성해 task 종류·속성 등의 오류 가능성을 관찰한다.
실제 결과는 모델·제공된 문맥 등에 따라 달라질 수 있으며 오류를 미리 확정하지 않는다.
최신 문맥은 코드 정확성을 돕지만 생성 코드의 검증을 대체한다고 단정하지 않는다.
이번 범위는 생성된 YAML 관찰이며 실제 GCS·BigQuery 적재나 새 클라우드 계정·키 준비를
추가하지 않는다. 환경 설정은 공식 3번에서 기존 환경·실습 공간과 함께 확인한다.
2번 읽음·실험 수행·생성 YAML·학습자 해석은 아직 미확인이다. AI는 새 대화·실습 파일·
환경을 생성하거나 실행하지 않았고, 허브 STATE만 로컬 저장하며 commit·push하지 않았다.

2026-10-27 학습자가 2번을 읽고 실험도 따로 시도했다고 보고하며 다음 진행을 요청했다.
읽기·실험 수행은 학습자 보고로 기록하며 생성 YAML·오류 종류·실행 결과나 학습자 해석을
직접 확인한 것으로 확대하지 않는다. 결과 제출·재실험을 다음 진행의 조건으로 요구하지 않는다.

공식 2번과 다음 3. Setting up Kestra의 main 원문, 공식 Compose를 확인했다.
3번 전체 범위는 Compose로 Kestra 실행, API 키 준비·secret 설정, 제공 flow import와
첫 에이전트 및 웹 검색·다중 에이전트 예제 실행이다. 이번 안내의 첫 작업은 자기 실습 공간에
제공 설정을 준비하고 Kestra UI 접속을 확인하는 것까지다. 공식 예제의 Gemini 설정과
flow별 OpenAI·Tavily 요구는 후속 키 설정 시 확인하며, 기존 키는 재사용하고 값은 수집하지 않는다.

현재 Docker CLI와 Docker Desktop 서버의 연결 및 Docker Compose 버전 조회가 모두 성공했다.
이전 WSL의 Docker 명령 사용 불가 상태와 구분한다. 공식 로컬 checkout의 origin은
DataTalksClub/llm-zoomcamp이며 03-orchestration 경로에 변경이 없다. Compose와 제공 YAML
6개가 실제 존재하고 root·해당 단원에 AGENTS·CLAUDE가 없음을 확인했다.
자기 실습 위치로 제안한 studies/03-orchestration 폴더는 아직 없다. 공식 checkout을
학습자 원격 저장소로 바꾸거나 허브에 실습을 만들지 않는다. AI는 파일 복사·컨테이너 시작·
API 호출을 하지 않았다. Kestra UI·키 설정·flow import·실행은 아직 미확인이다.
허브 STATE만 로컬 저장하며 이번 요청으로 commit·push하지 않았다.

2026-10-27 학습자가 폴더 준비·Compose 실행·Kestra UI 접속을 완료했다고 보고했다.
실제 studies/03-orchestration 폴더의 Compose·제공 flow YAML 6개와 .env 존재를 확인했다.
이 공간은 Git 저장소가 아니며 AGENTS·CLAUDE도 없다. 공식 원문과 실제 실습 공간을 기준으로
핵심 실행·첫 해석은 학습자가 수행하는 현재 허브의 튜터 규칙으로 계속 돕는다.
Docker 조회에서 Kestra v1.3.21 컨테이너의 실행·8080/8081 포트 공개와 PostgreSQL 18의
healthy 상태를 직접 확인했다. UI 접속 자체는 학습자 완료 보고로 구분한다.

키 설정을 중복 요구하지 않기 위해 값은 출력·저장하지 않고 이름과 비어 있지 않은지만
확인했다. 실제 실행 중 컨테이너에는 Gemini·OpenAI·Tavily secret 환경변수와 Copilot용
API key 설정이 비어 있지 않다. 이는 주입 확인이며 유효한 키인지나 API 호출 성공까지
검증한 것은 아니다. .env에는 변수 선언이 없고 이번 도구 세션의 Compose 설정 해석에서는
키 변수가 비어 있어, 기존 컨테이너의 설정과 재생성 시의 설정을 혼동하지 않는다.
AI는 컨테이너 재시작·키 변경·API 호출을 하지 않았다.

공식 3번 설정 안내·Compose·4_simple_agent 원문과 로컬 4·5·6번 flow의 secret 참조를
확인했다. 4번 flow에는 Gemini, 5·6번에는 Gemini·Tavily가 사용된다. 다음은 제공 flow
등록과 4_simple_agent의 기본 입력 1회 실행이다. 첫 요약 → 영어 한 문장 요약 → 두 agent의
토큰 사용량 로그를 살펴보며, 실제 생성 결과·인증 성공·학습자 해석은 실행 후에 확인한다.
3강 전체 완료나 4강 AI Copilot 수행으로 자동 기록하지 않는다. AI는 flow import·실행이나
실습 파일 수정을 하지 않았고 허브 STATE만 로컬 저장하며 commit·push하지 않았다.

2026-10-27 학습자가 공식 curl import 명령 6개를 수행했으나 응답이 [][][][][][]로
나와 등록되지 않은 것 같다고 보고했다. bug-triage·systematic-debugging으로 현재 상태와
실행 버전의 원문을 확인했다. 읽기 전용 GET /api/v1/flows/search와 /api/v1/main/flows/search는
모두 HTTP 200·total 6이며, namespace zoomcamp에 제공 flow 1–6번이 각각 revision 1로 있다.
4_simple_agent 개별 GET도 HTTP 200으로 등록된 정의를 확인했다.

Kestra v1.3.21 FlowController의 importFlows는 실패 항목을 wrongFiles에 모아 반환한다.
따라서 이번 [] 응답은 실패 항목 없음이며 등록 성공 상태와 일치한다. curl 응답마다 줄바꿈이
없어 빈 배열 여섯 개가 붙어 보인 것이다. 제품 회귀나 등록 실패로 판단하지 않으며 코드·
설정 변경·재등록은 필요하지 않다. UI에서 Flows의 zoomcamp를 확인하고 4_simple_agent를
직접 Execute하는 다음 단계로 안내한다. import는 정의 등록이며 flow 실행과 구분한다.
AI는 GET 조회만 했고 flow 생성·수정·재등록·실행이나 LLM API 호출을 하지 않았다.
실제 flow 출력·토큰 사용량·LLM 인증 성공은 아직 미확인이다. 허브 STATE만 로컬 저장하며
이번 요청으로 commit·push하지 않았다.

2026-10-27 학습자가 Gemini 2.5 Flash 미지원 오류를 보고하며 YAML별 모델 교체안을 요청했다.
로컬 YAML 6개·Compose, Kestra 등록본과 실행 중 Copilot 설정, 실패 실행의 오류 로그를
읽기 전용으로 확인했다. 이전 revision의 1·4번 실행 로그에는 HTTP 404와 신규 사용자에게
gemini-2.5-flash를 더 제공하지 않으며 gemini-3.8-flash로 변경하라는 메시지가 있다.
Google 공식 모델·지원 종료 안내도 기존 사용자의 2.5 서비스는 유지하고 신규 프로젝트에는
3.8 Flash 또는 3.5 Flash-Lite를 쓰도록 한다. 전체 서비스 종료로 확대하지 않는다.

검토 중 최신 로컬 파일·Kestra 등록본은 1·2번의 생성 모델, 4번 AIAgent 기본 provider,
5번 provider, 6번 상위·하위 agent의 공통 provider가 모두 gemini-3.8-flash로 갱신된 것을
확인했다. 2번의 적재·검색 embeddingProvider는 둘 다 gemini-embedding-001이며 이 모델은
공식 문서에서 텍스트 임베딩용으로 계속 지원된다. 3번은 Gemini 오류와 무관한 gpt-5-mini로
유지한다. Compose와 실제 실행 중 Copilot의 model-name도 gemini-3.8-flash다.
확인 당시 등록 revision은 1번 4, 나머지 2–6번 3이며 최근 실패 기록은 이전 revision 1이다.
이전 실패 기록을 최신 모델의 실패로 해석하지 않고 최신 flow에서 새 실행하도록 안내한다.

컨테이너의 plugin-ai는 1.12.6이다. 해당 버전 GoogleGemini 구현은 modelName을 SDK에
전달하며 function-call thought signature 보존을 포함한다. 다만 thinkingEnabled가 false이고
budget이 없으면 thinking budget 0을 전송한다. Gemini 3.8의 thinking 비활성화 미지원과
충돌할 수 있어 Gemini 생성 task에는 thinkingEnabled: true를 명시하는 호환성 보완을
안내한다. 일반 ChatCompletion·AIAgent는 configuration, 2번 RAG ChatCompletion은
chatConfiguration에 둔다. 4번은 두 task 또는 AIAgent pluginDefaults에 적용하고, 6번은
상위·하위 agent 각각의 configuration을 확인한다. 이는 정적 검토이며 해당 새 오류를
직접 재현하거나 3.8 호출 성공을 검증한 것은 아니다.
AI는 학습자 YAML·Compose 수정, flow 갱신·재실행, 키 값 수집이나 LLM API 호출을 하지 않았다.
검토 결과·막힘·다음 행동을 허브 STATE에만 로컬 저장하며 commit·push하지 않았다.

2026-10-27 학습자가 앞서 검토한 thinking 설정을 AI가 직접 수정·적용하도록 명시했다.
설정 변경에 맞는 비례 검증을 선택했다. 변경 전 로컬 YAML과 등록본 source의 의미상 일치,
현재 revision을 확인하고 기존 내용을 보존했다. 1번 일반 ChatCompletion, 4번의 두 요약
agent, 5번 research agent, 6번 상위·하위 agent의 configuration에 thinkingEnabled: true를
추가했다. 2번 RAG의 생성 task에는 chatConfiguration.thinkingEnabled: true를 추가했다.
총 5개 파일·7개 생성 호출 위치이며 임베딩·OpenAI 모델과 다른 설정·프롬프트는 보존했다.

변경 전후 YAML을 파싱해 허용한 thinking 설정 외 의미 변화가 없음을 확인했다.
실행 중 Kestra의 validate API에 6개 YAML을 보내 모두 HTTP 200·constraints 없음으로
확인한 뒤 개별 PUT으로 1·2·4·5·6번 등록본을 갱신했다. 새 revision은 1번 5, 2·4·5·6번 4다.
3번은 revision 3을 유지했다. 각 갱신 뒤 GET source를 다시 읽고 마지막으로 6개 모두
로컬 YAML과 일치함을 확인했다. 3번 YAML·Compose는 바이트 비교로 무변경을 확인했다.
전체 공백 검사에서 3번 6행의 기존 공백이 발견됐지만 변경 전에도 동일해 보존했으며,
이번 변경에서 새로 생긴 공백은 없다. 모든 YAML은 파싱됐다.

이 작업은 AI가 맡은 설정 보완이며 학습자의 독립 구현·실행으로 기록하지 않는다.
AI는 flow를 실행하거나 LLM API를 호출하지 않았다. 실제 3.8 응답·토큰 사용량·성공 여부는
학습자가 최신 revision으로 새 실행한 뒤 확인한다. 컨테이너 재시작이나 키 변경 없이 적용했고,
실습 공간은 여전히 로컬 Git 미연결이다. 허브 STATE는 로컬 저장이며 commit·push하지 않았다.

2026-10-27 학습자가 english_brevity가 4분 넘게 실행 중이라며 정상 진행 여부 확인을
요청했다. 해당 실행 `14jfwBVJ11o5iOHGRE4PNm`은 4_simple_agent revision 4다.
API 조회에서 multilingual_agent가 54.6초 후 SUCCESS이며 실제 요약 응답·STOP과
inputTokenCount 281, outputTokenCount 96, totalTokenCount 978을 확인했다.
이는 첫 task의 저장 사용량이며 전체 flow 비용이나 실패한 다음 호출의 사용량으로 확대하지 않는다.

english_brevity는 처음 RUNNING·출력 없음으로 보였지만 서버 로그에서 Gemini HTTP 503과
수요 과다 메시지, SDK의 남은 재시도 2회·1회, request timed out을 확인했다.
Kestra task attempt는 1개여도 SDK 내부 요청 재시도는 별도로 진행됐음을 구분한다.
후속 API와 서버 로그 조회에서 이 task는 314.7초 후 FAILED, 전체 flow는 370.2초 후
2026-10-27 12:51:10 KST에 FAILED로 종료한 것을 확인했다. 두 번째 요약·사용량과 마지막
토큰 로그 task의 완료는 확인되지 않았다. 이전 2.5 접근 제한 오류와 다른 API 가용성 실패다.

Kestra·PostgreSQL 컨테이너는 실행 중이고 PostgreSQL은 healthy였다. 조회 당시 Kestra
CPU 약 1.5%, 메모리 약 1.79GiB/25.44GiB로 로컬 자원 고갈의 근거는 없었다.
이번 로그는 서비스 수요 과다와 응답 지연을 직접 보여주지만 전체 Gemini 서비스 장애나
영구적인 모델 미지원으로 확대하지 않는다. 학습자의 첫 해석·독립 숙달도 새로 판정하지 않았다.
AI는 읽기 전용 조회만 했으며 실행 취소·재시작·재실행·설정 변경·LLM 호출은 하지 않았다.
부분 성공과 새 막힘을 허브 STATE에 로컬 저장하며 commit·push하지 않았다.

2026-10-27 학습자가 반복되는 503 때문에 강의 실행이 어렵다며 reasoning·모델을 낮추는
방안을 물었다. 새 실행 4nzA86rBLtsLFEuUK8CX1R은 revision 4이며 13:19:37 KST에 시작했다.
13:24 KST 조회 시 첫 multilingual_agent가 RUNNING이고 출력은 아직 없다. 서버 로그에서
13:21:37·13:23:38 KST의 request timed out과 SDK 내부 재시도를 확인했다. 새 실행에서
503을 직접 확인한 것으로 확대하지 않으며, 앞선 실행의 503 수요 과다 근거와 구분한다.

Google 공식 모델·thinking 문서에서 gemini-3.5-flash-lite의 함수 호출·구조화 출력 지원과
기본 thinking level minimal을 확인했다. 3.8 Flash의 기본은 medium이다. 설치된 plugin-ai
1.12.6의 ChatConfiguration에는 thinkingLevel 필드가 없다. thinkingEnabled: true는
high reasoning 지정이 아니며 budget을 생략하면 모델 기본 동작을 사용한다. 따라서 4번의
공통 provider 모델명만 Lite로 바꾸고 기존 true를 유지하는 시험을 먼저 추천했다.
낮은 reasoning은 지연을 줄일 수 있지만 서버 수요 과다인 503 해소는 보장하지 않는다.

현재 등록본 source를 메모리에서 복사해 모델명 하나만 바꾼 후보를 validate API에 보냈다.
HTTP 200·제약 오류·경고 없음으로 확인했으며 모델 존재·접근 권한·생성 성공을 검증한 것은
아니다. 로컬 YAML·등록본·실행 중 작업은 변경하지 않았고 LLM 호출도 하지 않았다.
Lite 전환은 AI의 제안이며 학습자의 선택·적용·실행 결과로 기록하지 않는다.
새 막힘과 제안을 허브 STATE에 로컬 저장하며 commit·push하지 않았다.

2026-10-27 학습자가 제안한 Lite 전환의 수정·적용과 실제 검증을 명시적으로 맡겼다.
실습 공간의 별도 지침 부재와 로컬 YAML·Kestra 등록본 6개의 일치를 먼저 확인하고,
변경 전 파일·등록 revision을 저장소 밖 임시 경로에 보존했다. 앞선 실행
4nzA86rBLtsLFEuUK8CX1R은 첫 multilingual_agent에서 FAILED로 끝난 것을 추가 확인했다.

먼저 4번의 공통 provider modelName 하나만 gemini-3.5-flash-lite로 변경했다.
validate 통과 뒤 Kestra revision 5로 적용하고 GET으로 로컬과 일치함을 확인했다.
강의의 기본 입력으로 검증 실행 4o7VxGS4tOO9piAmK1lQPB를 한 번 생성했다.
2026-10-27 13:26:24–13:26:28 KST에 전체 SUCCESS, 총 3.27948초로 완료했다.
multilingual_agent는 약 1.59초, english_brevity는 약 1.44초, log_token_usage도 SUCCESS다.
두 실제 요약 textOutput이 비어 있지 않고 finishReason STOP인 것을 확인했다.
english_brevity 출력은 영어 한 문장이다. 두 task의 토큰 로그는 각각 입력 281·출력 119·총 400,
입력 134·출력 46·총 180이며, 해당 실행의 ERROR 로그는 0개였다.

4번 성공 뒤 1·2·5·6번도 생성 모델명만 Lite로 바꾸고 등록본에 적용했다.
최종 revision은 1번 6, 2·4·5·6번 5이며 3번은 3을 유지한다. 6개 YAML의 후보 검증이
모두 통과했고 최종 GET source가 로컬과 의미상 일치한다. 백업과의 바이트 비교에서
변경은 5개 파일의 modelName 각 한 줄뿐이며, thinking 설정·임베딩·OpenAI 모델·프롬프트·
로그·secret 참조를 보존했다. 6번은 공통 provider를 쓰는 상위·하위 agent 모두에 적용된다.
3번 파일과 Compose는 무변경이며 컨테이너 재시작·키 변경은 하지 않았다.

실제 모델 응답 검증은 4번의 두 호출에 한했다. 다른 flow의 검색·임베딩 적재·외부 도구·
파일 출력 전체 성공까지 확대하지 않으며 이후의 503 재발 가능성도 배제하지 않는다.
이번 실행은 AI가 수행한 검증 도움이며 학습자의 독립 수행·3강 전체 완료로 기록하지 않는다.
허브 STATE는 로컬 저장이며 commit·push하지 않았다.

2026-10-27 학습자가 공식 4강 Copilot 예제 프롬프트를 새 flow 생성 창에 입력했지만
"I can only assist with creating Kestra flows."라는 빨간 오류가 뜬다고 보고했다.
공식 04-ai-copilot.md 원문과 동일한 요청임을 확인했고, API access 로그에서
POST /api/v1/main/ai/generate/flow가 약 83.945초 뒤 HTTP 422로 끝난 것을 확인했다.
Copilot은 앞서 수정한 flow provider와 별개이며 Compose·실제 런타임은 여전히 3.8 Flash였다.
Copilot의 plain key가 비어 있지 않고, 성공한 flow용 base64 key를 복호화한 값과 같음을
메모리 내 비교로 확인했다. 키 값은 도구 출력·저장소·임시 파일에 쓰지 않았다.

Kestra 공식 이슈 #17041은 1.3.21에서 정상 flow 요청의 생성 실패에도 같은 모호한 문구가
표시되는 문제를 보고한다. 해당 버전의 copilot 라이브러리 0.2.4 소스에서도 플러그인 선택·
스키마 준비 중 발생한 예외를 이 문구의 AiException으로 바꾸는 것을 확인했다.
따라서 이 문구만으로 프롬프트 범위 위반·잘못된 키·503 중 하나를 확정하지 않는다.
이번 Copilot 실패의 숨겨진 원래 예외는 로그에 없어 확정하지 못했다.

진행 중인 execution 0개를 확인한 뒤 Compose의 Copilot model-name 한 줄만
gemini-3.5-flash-lite로 바꿨다. 현재 컨테이너의 기존 환경을 메모리에서 재사용하고
Compose 결과를 비교해 모델명 외 설정·인증 값이 유지됨을 확인했다. 같은 image로 Kestra만
재생성했고 기존 저장 볼륨·PostgreSQL은 유지했다. 재시작 후 API 응답과 키·설정 보존,
PostgreSQL healthy 및 6개 flow의 revision·로컬 YAML 일치를 확인했다.

AI가 사용자의 원래 프롬프트로 Copilot 생성 API를 검증했다. 처음 진단 요청은 Accept
헤더 불일치로 모델 호출 전에 HTTP 406이었고, application/yaml로 바로잡은 실제 생성
요청은 약 4.31초에 HTTP 200이었다. 다운로드·GCS Upload·BigQuery Load 3개 task를
포함한 YAML을 받았으며 validate API는 제약 오류·경고 없이 HTTP 200이었다.
생성본은 저장소 밖 임시 경로에만 두었고 flow 등록·GCS 업로드·BigQuery 실제 적재는
실행하지 않았다. 검증 생성 성공은 AI 도움이며 학습자의 수행 완료로 확대하지 않는다.
이후 학습자의 화면 재시도·YAML 검토·후속 refinement는 아직 미확인이다.
허브 STATE는 로컬 저장이며 commit·push하지 않았다.

2026-10-27 학습자가 Copilot이 이제 정상 동작하며 4강을 완료했다고 보고하고 다음 강의를
요청했다. 정상 동작과 수강 완료는 학습자 보고로 저장하며, 새 화면·생성본·후속 refinement나
GCS·BigQuery 실제 실행을 직접 확인한 것으로 확대하지 않는다. 앞선 AI 설정·검증 도움은 유지한다.

공식 main의 05-rag.md와 현재 실습 YAML 1·2·3번을 확인해 공식 5강으로 연결했다.
이번 범위는 RAG의 적재·질의 단계, 문맥 없는 답변과 문서 RAG 비교, 웹 검색 retriever다.
기존 등록 flow를 1 → 2 → 3 순서로 학습자가 실행하며 새 코드나 재등록은 요구하지 않는다.
1·2번 생성 모델은 Lite, 2번 적재·검색 임베딩은 gemini-embedding-001이고 KV Store를 쓴다.
3번은 기존 OpenAI·Tavily 구성을 유지한다. 답변 정확도는 릴리스 원문과 비교해 확인하도록
안내하며 RAG 사용이나 성공 로그만으로 보장하지 않는다. 5강 읽기·실행·해석은 아직 미확인이다.
AI는 이번 턴에 실습 코드·설정 변경이나 flow 재실행을 하지 않았다.
허브 STATE는 로컬 저장이며 commit·push하지 않았다.

2026-10-27 학습자가 Kestra에서 execute는 성공하지만 result를 어디서 보는지 질문했다.
읽기 전용 API 조회에서 1_chat_without_rag 실행 3mCYUgT6R34Xfz0sWPeyhI의 두 task가
SUCCESS이고 chat_without_rag.textOutput이 비어 있지 않으며 log_results의 INFO 메시지가
저장돼 있음을 확인했다. 응답 전문·정확도·학습자의 해석은 이번 요청에서 검토하지 않았다.
Kestra 1.3.21 UI 소스의 Logs·Outputs 구성을 확인하고 실행 상세의 Logs → log_results,
또는 Outputs → chat_without_rag → textOutput 경로를 안내했다. INFO 로그 필터도 짚었다.
AI는 새 실행·기존 출력 수정이나 설정 변경을 하지 않았다. 허브 STATE만 로컬 저장했다.

2026-10-27 학습자가 현재 gpt-5-mini 설정을 모두 gpt-6-luna로 변경·적용하도록 요청했다.
현재 Module 3 실습 폴더와 Kestra 등록 flow 16개를 조회해 대상이 로컬
flows/3_rag_with_websearch.yaml 및 zoomcamp.3_rag_with_websearch 한 곳임을 확인했다.
다른 저장소의 과거 자료나 공식 원본은 수정하지 않았다. 변경 전 파일·등록본을 임시 경로에
보존하고 최신 revision 3·로컬 일치를 확인한 뒤 modelName 한 줄만 변경했다.
validate API는 제약 오류·경고 없이 통과했고 revision 4로 적용 후 GET source 일치를 확인했다.
로컬 실습 폴더와 등록 flow 16개 재검색에서 gpt-5-mini가 남아 있지 않음을 확인했다.

공식 OpenAI 문서에서 gpt-6-luna의 Chat Completions 지원을 확인했으며, 기존 키로
GET /v1/models/gpt-6-luna가 HTTP 200·동일 모델 ID를 반환했다. 이는 메타데이터 조회이며
모델 생성·Tavily 검색·3번 전체 flow 성공을 검증한 것은 아니다. 해당 실행은 학습자가 이어간다.
키 값은 출력·저장하지 않았고 다른 flow·프롬프트·검색 설정·Compose는 수정하지 않았다.
이번 변경은 AI 설정 도움이며 강의 완료·독립 수행으로 기록하지 않는다.
허브 STATE는 로컬 저장이며 commit·push하지 않았다.

2026-10-27 학습자가 3번 flow 실행 뒤 output이 보이지 않는다고 질문했다.
최신 실행 3oX255U0WVDs2WCysgRCdP는 revision 4이며 약 5.27286초에 SUCCESS다.
유일한 task chat_with_rag_and_websearch_content_retriever에 비어 있지 않은 textOutput,
finishReason STOP, 검색 sources 3개와 입력 882·출력 134·총 1,016 토큰이 저장돼 있다.
바로 이전 revision 4 실행도 SUCCESS·응답 저장 상태다. 실제 응답 전문·정확도는 검토하지 않았다.

3번 YAML은 RAG task 하나로 끝나며 1·2번처럼 log_results가 없다. API의 INFO 이상 Logs도
빈 배열이므로 로그가 비어 있는 것을 생성 출력 부재로 해석하지 않는다. 실행 상세의 Outputs에서
해당 task → textOutput으로 답변을, sources로 검색 출처를 확인하도록 안내했다.
실행 root의 flow outputs는 별도로 선언돼 있지 않으며 task outputs와 구분한다.
AI는 읽기 전용 확인만 했고 코드 수정·재실행은 하지 않았다. 허브 STATE만 로컬 저장했다.

2026-10-27 학습자가 3번 출력 확인과 5강 완료를 보고하고 다음 강의를 요청했다.
수강 완료·화면에서의 출력 확인은 학습자 보고로 저장한다. 2번 개별 실행·응답 정확도·
학습자의 첫 해석을 새로 직접 확인하거나 독립 숙달로 판정한 것은 아니다.

공식 main의 06-agents.md와 현재 5_web_research_agent.yaml을 확인해 6강으로 연결했다.
Module 1에서 작성한 LLM → 도구 실행 → 결과 전달의 반복을 Kestra AIAgent가 관리하는
방식, 고정 task 순서와 agent의 도구 선택, prompt·systemMessage·provider·tools,
실제 toolExecutions·토큰·파일 출력을 보는 것이 이번 범위다. 이미 성공한 4번은 구조를
참고하고 5번 웹 연구 agent를 학습자가 실행하도록 안내한다. 기존 Lite 설정을 사용한다.

현재 5번 YAML의 Tavily는 contentRetrievers이고 tools에는 filesystem Docker MCP만 있다.
따라서 강의 설명이나 log_report 문구만으로 모델이 반복 웹 검색을 선택했다고 인정하지 않는다.
실제 toolExecutions와 research_report.md 저장 여부를 확인하도록 안내하며, 아직 실행·
파일 존재·도구 호출 성공은 미확인이다. 7강 multi-agent나 새 자체 실습은 시작하지 않았다.
AI는 이번 턴에 실습 파일 수정·flow 재실행을 하지 않았다. 허브 STATE만 로컬 저장했다.

2026-10-27 학습자가 5번 flow를 실행해 SUCCESS가 나왔고 파일 위치를 질문했다.
읽기 전용 조회에서 실행 57Jtfp0BxhaHCCtGcxEfmk는 revision 5이며 전체 약 27.725603초,
research_agent·log_report 모두 SUCCESS다. textOutput과 finishReason STOP,
입력 8,391·출력 996·총 9,387 토큰, toolExecutions의 write_file 호출 1개를 확인했다.
outputFiles에는 research_report.md의 Kestra 내부 저장소 URI가 있고 로그에도 그 URI가 있다.

해당 파일 metadata API는 HTTP 200·size 4,764바이트였고 다운로드 API도 HTTP 200으로
비어 있지 않은 응답과 research_report.md 첨부 파일명을 확인했다. 보고서 본문을 읽거나
정확도를 평가하지 않았으며 학습자 PC나 실습 저장소로 파일을 내려받지는 않았다.
Outputs → research_agent → outputFiles → research_report.md의 Download 경로와
현재 실행 파일 다운로드 링크를 안내했다. 보고서는 Kestra의 실행 결과 파일로 보관된다.
AI는 코드·설정 수정·새 실행 없이 확인했고, 6강 완료나 보고서 해석을 추정하지 않았다.
허브 STATE만 로컬 저장했다.

2026-10-27 학습자가 보고서 파일을 확인했고 6강을 완료했다고 보고하며 다음 강의를 요청했다.
파일 열람·수강 완료는 학습자 보고로 저장하며 보고서 본문·정확도·첫 해석을 직접 검토한
것으로 확대하지 않는다. 이전 실행·파일 저장을 직접 확인한 근거와 AI 도움을 유지한다.

공식 main의 07-multi-agent.md와 현재 6_multi_agent_research.yaml을 확인해 7강으로 연결했다.
핵심은 상위 analysis agent가 tools의 하위 AIAgent를 호출해 조사를 맡기고 최종 JSON으로
정리하는 구조다. 하위 agent는 Tavily contentRetrievers를 사용한다. 공통 provider는 기존
gemini-3.5-flash-lite이며 새 모델·파일·별도 실습 환경은 필요하지 않다.
학습자가 등록된 6번을 기본 company_name=kestra.io로 실행하고 analysis.textOutput의 JSON,
toolExecutions의 실제 위임 호출, parse_results 로그를 확인하도록 안내한다.
현재 예제는 메인 agent에게 부족한 정보를 추론으로 보완하도록 지시하므로 뉴스의 사실성은
출처와 구분해 확인한다. 실행 성공이나 JSON 형식만으로 사실 정확성을 인정하지 않는다.
7강 원문의 영상 링크는 6강과 같으며 같은 영상의 반복 시청을 새 과제로 요구하지 않는다.
AI는 이번 턴에 실습 파일 수정·flow 실행을 하지 않았고 허브 STATE만 로컬 저장했다.

2026-10-27 학습자가 6번 flow 실행·출력 확인과 7강 완료를 보고했다.
최신 실행 IvMGjFyMCuqwXI9uffO1Q는 revision 5·약 9.243313초·SUCCESS이며
analysis와 parse_results가 모두 성공했다. analysis.textOutput은 company·summary·
recent_news·competitors를 가진 유효 JSON이고 toolExecutions에는 kestra_agent_tool
호출 1개가 있다. 실제 출력 내용의 사실성·하위 검색 경로·학습자의 첫 해석은 검토하지 않았다.

공식 main의 08-best-practices.md를 확인해 8강으로 연결했다. 도구 선택 기준, 비용·secret,
실행 관찰과 실패 대응을 정리하는 읽기 범위다. 본문의 Gemini 2.5/3.5 Flash 가격표와 현재
Lite·Luna 모델은 구분하며 모델 변경·추가 실습·운영 배포를 요구하지 않는다.
8강 읽기 완료는 아직 미확인이다. AI는 실습 설정 수정·재실행 없이 확인하고 STATE만 로컬 저장했다.

2026-10-27 학습자가 8강을 다 읽었다고 보고하고 다음 강의를 요청했다.
읽음은 학습자 보고로 저장하며 보안·비용·재시도 설정의 신규 구현이나 운영 배포를 한 것으로
확대하지 않는다. 공식 main의 09-next-steps.md를 확인해 Module 3의 마지막 9강으로 연결했다.
이번 범위는 모듈 요약과 후속 자료 안내 읽기다. 모델 제공자 비교·자체 agent·Blueprints·
커뮤니티 참여는 원문의 확장 제안이며 새 필수 과제·외부 게시로 바꾸지 않는다.
next_url은 ../04-evaluation/01-intro.md다. 9강 완료 보고 전에 Module 3를 완료 처리하거나
Module 4를 시작하지 않았다. 실습 변경·재실행 없이 STATE만 로컬 저장했다.

2026-10-27 학습자가 9강 안내 뒤 다음으로 진행하도록 요청했다. 9강을 다 읽었다는 명시 보고는
없어 미확인으로 보존하고, 공식 next_url을 따라 Module 4 소개 읽기로 연결했다.
현재 main의 04-evaluation/README.md와 01-intro.md를 확인했다. 이번 범위는 오프라인 평가의
목적, 정답 FAQ에서 시험 질문을 만드는 A → Q* → A′ 구조, 검색·RAG·agent 평가의 차이다.
검색은 Hit Rate·MRR, 답변 품질은 LLM-as-a-judge, agent는 최종 답변·도구 호출 경로로
이어진다. 이번에는 소개 읽기이며 데이터 생성·환경 구축·LLM 호출을 시작하지 않았다.
Module 4 외부 실습 공간은 구현 단원에서 연결하며 기존 실습 자료·모델 설정을 보존한다.
허브 STATE만 로컬 저장했다.

2026-10-27 학습자가 Module 4 소개 읽기 완료를 보고하고 다음 단원을 요청했다.
공식 main의 02-ground-truth.md를 확인했다. LLM 과정 FAQ 한 문서에서 질문 5개를
structured output으로 생성하고 원본 id와 연결하는 2강 전체 범위로 안내한다.
기존 Module 1 레포의 load_faq_data·RAGBase와 설치된 OpenAI 환경을 확인해 재사용하도록
연결했다. 새 notebook evaluation.ipynb는 생성 안내이며 AI가 만들지 않았다.

원문의 cohorts/2026 다운로드 URL 세 개는 현재 HTTP 404였다. 기존 ingest.py·rag_helper.py를
재사용하고 evaluation_utils.py는 main/04-evaluation/code/evaluation_utils.py의 HTTP 200
주소를 안내한다. helper와 tqdm은 실습 공간에 아직 없으며 준비 명령만 안내한다.
현재 helper의 기본 모델 gpt-5.4-mini와 하드코딩 단가를 확인했다. 기존 gpt-6-luna로
호출할 때 모델을 명시하고, 비용 계산은 2026-10-27 확인한 표준 단가인 100만 토큰당
입력 $0.10·출력 $0.50에 맞추도록 안내한다. 공식 모델 문서에서 structured outputs 지원도
확인했다. 데이터 생성·유료 API 호출·핵심 구현·파일 수정은 AI가 대신 하지 않았다.
1강 읽음은 학습자 보고이며 2강 수행·완료·독립 숙달은 아직 미확인이다. STATE만 로컬 저장했다.

2026-10-27 학습자가 2강 실습 완료를 보고하고 저장 notebook 리뷰와 다음 안내를 요청했다.
기존 경로는 사라졌고 studies 아래 이동한 레포의 evalutaion.ipynb를 찾았다. 저장본의
실행 번호 1–16에서 LLM 과정 필터, 문서 ID 74eb249bbf와 참여·수료 기한 FAQ,
Questions 구조·responses.parse(model=gpt-6-luna), 두 번의 질문 5개 출력을 확인했다.
직접 작성한 evalutaion_utils.llm_structured도 Luna 기본값이며 마지막 출력은 입력 207·
출력 136토큰이다. 저장된 오류는 없고 생성 질문은 해당 FAQ의 참여·수료 조건 범위다.
calc_price·비용 결과와 question/document 레코드 생성 셀은 없어 2강 전부를 직접 확인한
것으로 확대하지 않는다. 학습자의 별도 해석·독립 숙달도 미확인이다.

공식 main의 03-ground-truth-batch.md를 확인했다. 남은 레코드·비용 연결을 마무리한 뒤
문서별 처리·재시도, 첫 5문서, 병렬 처리, 사용량 합산과 CSV 저장으로 이어가도록 안내한다.
현재 helper에는 llm_structured만 있으므로 필요한 재시도·가격·진행률 함수를 이어 붙이는
과정에서 기존 사용자 함수를 보존한다. 강의의 79문서·395질문은 과거 실행 예시이며 현재
문서 개수와 동일하다고 가정하지 않는다. AI는 코드 수정·이름 변경·notebook 재실행·LLM
호출·commit·push를 하지 않았다. 실제 위치와 확인 범위·남은 수행을 STATE에 로컬 저장했다.

2026-10-27 학습자가 calc_price 구성 방법을 질문했다. 현재 helper에는 아직 해당 함수가 없다.
AI가 사용자의 요청에 따라 Luna 표준 입력·출력 단가를 곱해 input_cost·output_cost·total_cost를
반환하는 함수 예시와 모듈 reload 후 기존 usage를 사용하는 호출 방법을 설명했다.
입력 207·출력 136토큰의 캐시 할인 없는 계산 예시는 총 $0.0000887이다. 이는 AI의 산술
예시이며 학습자 notebook의 계산 출력이나 실제 청구액 확인이 아니다. 사용자 파일 수정·
notebook 재실행·API 호출은 하지 않았고 함수 추가·실행·레코드 변환은 아직 미확인이다.

2026-10-27 학습자가 비용 계산 오류를 보고했다. 최신 notebook의 실행 15에 ResponseUsage의
output_tokesn 속성이 없다는 AttributeError가 저장돼 있고 실제 helper 27행과 일치한다.
올바른 속성명 output_tokens로 고친 뒤 reload하고 모듈의 calc_price로 기존 usage를
계산하도록 안내했다. 최신 사용량은 입력 207·출력 131토큰이다. 코드·저장 출력 수정이나
LLM 재호출은 AI가 하지 않았고 수정 후 성공은 아직 미확인이다. STATE만 로컬 저장했다.

2026-10-27 학습자가 오타를 수정했고 비용 계산도 성공했다고 보고하며 다음을 요청했다.
helper의 output_tokens 수정은 직접 확인했다. notebook 저장본의 마지막 비용 셀에는
이전 output_token AttributeError가 남아 있으므로 현재 계산 성공은 학습자 보고로 구분한다.
오류를 재발한 것으로 단정하거나 LLM 호출을 다시 요구하지 않는다.
공식 03-ground-truth-batch.md를 다시 확인해 같은 notebook에서 문서별 처리·재시도,
첫 5문서, 병렬 처리, 비용 합산·CSV 저장으로 연결한다. 질문·원본 ID 연결은 이 처리 함수에서
마무리한다. 3강 helper의 모델·import를 현재 Luna·evalutaion_utils와 맞추도록 안내한다.
AI는 실습 파일·환경 수정·재실행 없이 확인했고 STATE만 로컬 저장했다.

2026-10-27 학습자가 CSV 저장 오류가 폴더 부재 때문인지, 상위 폴더 자동 생성이 가능한지
질문했다. 저장본의 마지막 셀은 to_csv("data/ground_truth-new.csv", index=False)이며
Cannot save file into a non-existent directory: 'data' OSError를 확인했다.
실습 폴더의 data·CSV가 없는 상태와 직전 DataFrame 생성 셀의 실행 번호 27을 확인했다.
AI는 Path의 parent.mkdir(parents=True, exist_ok=True) 뒤 같은 DataFrame을 저장하는
예시와 옵션 의미를 안내했다. 코드 수정·폴더 생성·notebook/LLM 재실행은 대신 하지 않았고
저장 성공·3강 전체 완료는 아직 미확인이다. STATE만 로컬 저장했다.

2026-10-27 학습자가 CSV 저장과 3강 완료를 보고하며 저장 notebook 리뷰·다음 안내를 요청했다.
단일 문서 생성과 6 worker 병렬 처리, 재시도 helper의 Luna 유지, 문서 ID 연결을 확인했다.
저장된 집계 비용은 직접 합산과 calc_total_price 모두 $0.017958800000000004로 일치한다.
이는 usages를 병렬 결과로 다시 구성한 전체 배치 한 번의 집계이며 앞선 단건·5문서 샘플·
실패 재시도까지 포함한 전체 실제 청구액으로 확대하지 않는다.

실제 CSV는 72,028바이트·805행·문서 ID 161개이며 ID별 질문이 모두 5개다. question/document
두 열에 빈 값과 중복 쌍이 없고, notebook의 전체 ground_truth 저장 출력과 행·순서가 일치한다.
마지막 저장 셀에는 이전 OSError 출력이 남아 있지만 파일을 직접 읽어 정상 저장을 확인했다.
생성된 모든 질문의 의미적 정확도나 독립 숙달은 검증하지 않았다.
공식 main의 04-search-evaluation.md를 확인해 4강으로 연결했다. 새 검색 평가 notebook에서
같은 CSV·FAQ 로더·인덱스를 재사용하고 relevance 리스트를 수집한다. 5강 지표 계산을
앞당기거나 새 LLM 호출·기존 notebook 재실행·코드 수정을 하지 않았다. STATE만 로컬 저장했다.

2026-10-27 학습자가 4강 완료를 보고하고 search-evaluation.ipynb 리뷰·다음 안내를 요청했다.
저장본에서 기존 CSV 로딩, LLM 과정만 인덱싱, question 3.0·section 0.5 가중치의 상위 5개
검색, 정답 ID 일치 여부를 0/1로 변환하는 로직과 검색 함수를 받는 일반화를 확인했다.
첫 질문 출력은 [1,0,0,0,0]이고 특정 함수·일반 함수의 첫 15질문 결과가 일치한다.
리스트는 모두 길이 5·0/1 값이며 저장된 오류는 없다. 전체 805행 CSV도 그대로다.
마지막 호출은 ground_truth_sample을 사용하므로 4강 마지막 전체 질문 실행은 미확인으로
구분한다. 이를 5강 evaluate(ground_truth, text_search)의 전체 평가에서 이어가도록 안내했다.
공식 main의 05-search-metrics.md를 확인해 Hit Rate·MRR·evaluate 구현으로 연결했다.
현재 샘플의 지표 계산이나 학습자의 첫 해석을 AI가 대신 수행하지 않았고 사용자 notebook·
출력 수정·재실행 없이 STATE만 로컬 저장했다.

2026-10-27 학습자가 5강 완료를 보고하며 저장 notebook 리뷰와 다음 안내를 요청했다.
hit_rate·mrr·evaluate 정의와 실행 번호 16–21을 확인했고, example 15건의 Hit Rate
0.9333333333333333·MRR 0.8222222222222222가 저장돼 있다. 구현은 공식 정의와 맞는다.
마지막 evaluate(ground_truth,text_search) 셀은 실행 번호·출력이 없어 전체 기준값은
확인되지 않았다. 이는 저장본의 확인 범위이며 학습자가 실행하지 않았다고 단정하지 않는다.

공식 main의 06-search-tuning.md를 확인했다. 먼저 전체 기준값을 남긴 뒤 같은 데이터에서
question boost 후보 비교, 세 필드 가중치 grid search·MRR 정렬·설정 선택으로 이어가도록
안내한다. 강의 example의 점수·최적 설정을 현재 데이터의 실측값으로 쓰지 않는다.
AI는 전체 검색·지표 계산·튜닝을 대신 실행하거나 notebook을 수정하지 않았고 STATE만 저장했다.

2026-10-27 학습자가 6강 완료를 보고하며 저장 notebook 리뷰와 다음 안내를 요청했다.
기준 평가 셀 실행 22의 전체 805질문 점수는 Hit Rate 0.7975155279503106·MRR
0.647018633540372다. question boost만 비교한 5개 후보 중 0.5가 가장 높았고,
세 필드의 36개 조합 탐색·MRR 정렬 후 최상위 행은 question=1.0·answer=4.0·section=0.2,
표시값 Hit Rate 약 0.940373·MRR 약 0.836832다. 동일 평가셋에서의 개선이며 별도 검증셋
성능으로 확대하지 않는다. 최종 text_search 재정의 코드는 해당 값을 쓰지만 실행 번호가
없어 적용은 미확인이다. 재정의 셀만 실행·저장하도록 안내하고 전체 탐색 반복은 요구하지 않는다.

공식 main의 11-evaluation-intro.md와 목차를 확인했다. 공식 순서가 6강 다음 Part 2의
11강으로 이어지므로 RAG·agent 평가 소개 읽기로 연결한다. 원본 답변과 생성 답변의 의미
비교, 질문·정답·생성 답변을 입력으로 받는 LLM judge, 도구 호출 경로를 보는 범위다.
11강 읽기·12강 생성 실습·사용자 자신의 결과 해석·독립 숙달은 아직 미확인이다.
AI는 notebook 수정·재실행·모델 호출 없이 확인했고 STATE만 로컬 저장했다.

2026-10-27 학습자가 마지막 셀의 실행 기록이 있다며 재확인을 요청했다. 최신 notebook에서
셀 26의 text_search 재정의 실행 번호 28과 question=1.0·answer=4.0·section=0.2 설정을
직접 확인했다. 현재 위치의 미확인 표시를 갱신하고 재실행 요구를 없앴다. 이전 튜닝 결과는
유지하며 다음 행동은 공식 11강 소개 읽기다. 사용자 파일 수정·재실행 없이 STATE만 저장했다.

2026-10-27 학습자가 11강 소개를 다 읽었다고 보고하고 다음 단원을 요청했다.
공식 main의 12-rag-answers.md와 현재 RAGBase·RAGWithUsage를 확인했다. 기존 실습 공간에서
새 RAG 평가 notebook으로 CSV 질문·문서 ID lookup·인덱스를 연결하고 한 질문부터 답변을
생성하는 범위다. 원본 답변과 생성 답변을 question·answer_llm·answer_orig·document로
묶은 뒤 전체 질문을 처리하고 CSV로 저장한다. usage 초기화와 배치 비용 확인도 포함한다.

현재 helper의 RAGWithUsage.search는 강의 예제 가중치 1.0·2.0·0.1을 사용하고 있으므로
학습자가 측정·선택한 1.0·4.0·0.2에 맞추도록 짚었다. RAGBase 모델은 기존 Luna이며
import는 실제 파일명 evalutaion_utils를 사용한다. 이번 실습은 질문마다 LLM 호출이 있으므로
한 건 결과를 먼저 확인하고 전체 805건으로 이어가도록 안내한다. 실행·CSV 저장·평가 완료는
아직 미확인이다. AI는 코드 수정·notebook 생성·API 호출 없이 STATE만 로컬 저장했다.

2026-10-27 학습자가 12강 완료를 보고하며 rag-evaluation.ipynb 리뷰와 다음 안내를 요청했다.
FAQ lookup·한 건 RAG·원본 답변 연결·처리 함수·reset_usage·6 worker 병렬 처리·CSV 저장의
실행 1–17을 확인했다. 첫 예시는 표현이 달라도 참여 가능·수료를 위한 제출 기간 조건을 담고
있다. 배치 집계 비용은 $0.10985690000000002이며 테스트 호출과 분리된 사용량 기준이다.
현재 RAGWithUsage는 question=1.0·answer=4.0·section=0.2이고 기본 모델은 Luna다.

답변 CSV는 833,605바이트·805행·4열이며 원본 ground truth와 질문·ID·순서가 모두 일치한다.
문서 ID 161개, ID별 원본 답변 일관성, 각 열의 빈 값 없음·중복 질문/ID 쌍 없음도 확인했다.
805개 생성 답변의 의미적 정확도를 전수 검증하거나 채점을 대신한 것은 아니다.
파일명이 evaluation.ipynb·evaluation_utils.py로 바뀌었고 새 notebook의 import도 일치한다.

공식 main의 13-llm-as-judge.md를 확인했다. 저장된 답변에 good/bad·판정 근거를 붙이는
구조화 채점, 전체 비율·비용 확인·판정 일부를 직접 검토하고 CSV 저장하는 범위로 연결한다.
원문의 evaluate_aqa 기본 모델은 gpt-5.4-mini이므로 현재 Luna 단가 helper와 맞게 모델을
유지하도록 짚었다. 판정이 절대 정답인 것으로 간주하거나 Streamlit 앱 제작을 새 필수
과제로 추가하지 않는다. AI는 코드 수정·재실행·API 채점 없이 STATE만 로컬 저장했다.

2026-10-27 학습자가 13강 실습 중 실행 오류의 원인 파악을 요청했다. 저장된 notebook의
AnswerEvaluation 정의(실행 20)에서 from openai import BaseModel을 확인했고, 첫 채점
호출(실행 27)에 additionalProperties=false 요구를 위반한 400 오류가 저장되어 있다.
helper의 responses.parse까지 호출 경로를 확인했다. 설치된 OpenAI 3.37.0·Pydantic 2.14.1에서
별도 최소 클래스의 스키마를 비교하니 SDK BaseModel의 extra=allow 때문에 true가 남으며,
Pydantic BaseModel을 사용하면 SDK가 false를 붙이는 것을 확인했다. API 호출 없는 진단이다.
학습자에게 import 교체 후 클래스 정의와 실패한 채점 셀만 다시 실행하도록 안내한다.
수정·재실행·채점 성공은 아직 미확인이며 학습자 파일을 변경하지 않았다.

2026-10-27 학습자가 13강 완료를 보고하고 다음 강의를 요청했다. 최신 저장본에서
Pydantic BaseModel import 수정 실행 28과 첫 채점 성공 29, Luna를 기본으로 한 evaluate_aqa,
6 worker 전체 채점·사용량 집계·good 비율·bad 예시 출력을 확인했다. 배치 집계 비용은
$0.0820532999999998이다. 실제 rag-evaluations-new.csv는 805행이며 good 748·bad 57,
빈 값 없음·원본 답변 CSV와 질문/문서 ID 순서 일치를 확인했다. 마지막 저장 셀의 실행 번호는
없지만 실제 CSV가 있어 저장을 미완료로 되돌리거나 재실행을 요구하지 않는다.
판정 일부를 학습자가 직접 검토한 내용과 자신의 해석은 아직 제시되지 않았다.

공식 main의 목차와 14-agent-evaluation.md를 직접 확인했다. 같은 질문·원본 답변에 대해
Module 1 ToyAIKit agent의 최종 답변과 function_call 이름·인자를 저장하고, 답변과 도구 호출
trajectory를 별도로 good/bad 채점하는 범위다. 공식 예제는 한 건 확인 후 첫 50건을 처리하며
agent-answers.csv·agent-evaluations.csv로 저장한다. 기존 function-calling.ipynb의
OpenAIResponsesRunner·Luna 사용과 ToyAIKit 설치 파일을 확인했다. agent/judge 모델은 Luna,
검색 가중치는 이전 선택값을 유지하고 json을 첫 사용 전에 import하도록 안내한다.
14강 구현·실행은 아직 미확인이다. AI는 학습자 파일 수정·재실행·API 호출 없이 STATE만 저장했다.

2026-10-27 학습자가 14강 완료를 보고하고 다음 단원을 요청했다. 이번에는 14강 실습 파일·
실행·CSV를 직접 검토하지 않았으므로 학습자 보고로 기록한다. 공식 main의 15-next-steps.md를
읽고 마지막 정리 단원으로 연결했다. 검색·RAG·agent 평가 복습, 합성 질문에서 실제 질문과
사람의 라벨로 평가 데이터를 개선하는 흐름, 반복 평가와 배포 후 monitoring을 다룬다.
Ragas·DeepEval·TruLens는 소개 자료이며 설치·추가 프로젝트를 필수 수행으로 추가하지 않는다.
15강 읽기나 Module 4 전체 완료는 아직 미확인이다. AI는 실습 파일 수정·재실행·API 호출 없이
STATE만 로컬 저장했다.

2026-10-27 학습자가 Module 4 / 15강을 다 봤다고 보고하고 다음을 요청했다. 강의 학습 구간을
마친 것으로 기록하고 Module 5 / 1강 소개로 연결했다. Module 4의 기존 확인·도움 이력과
14강의 보고 범위를 유지하며 공식 과제 제출이나 독립 숙달로 확대하지 않는다.

공식 main의 05-monitoring README와 01-intro.md를 확인했다. 기존 RAG를 재사용하며 실제
질문의 응답 시간·사용량·비용·피드백·관련성을 기록하고 Streamlit·PostgreSQL·Grafana로
확인하는 모듈이다. 현재는 소개 글·영상 범위만 안내하며, 다음 공식 단원은
02-assistant-setup.md다. 실습 환경 생성·설치·실행을 대신하거나 agent monitoring 과제를
선택한 것으로 기록하지 않았다. Module 5 소개 완료·구현은 아직 미확인이다.
AI는 사용자 실습 파일 수정·재실행·API 호출 없이 STATE만 로컬 저장했다.

2026-10-27 학습자가 Module 5 / 1강 소개 읽기 완료를 보고하고 다음을 요청했다.
공식 main의 02-assistant-setup.md를 확인하고 기존 실습 레포에서 2강으로 연결했다.
실제 ingest.py·rag_helper.py와 python-dotenv 의존성이 있어 공식 재다운로드·재설치 단계를
반복할 필요는 없다. RAGBase 기본 모델은 Luna로 확인했다. 학습자가 assistant.py에서
생성 함수와 CLI 실행을 연결하고 Makefile run target·터미널 응답을 확인하는 범위다.

RAGBase의 검색 가중치는 question=3.0·section=0.5이며, 이전 튜닝값 1.0·4.0·0.2는
RAGWithUsage에만 있다. 이전 값을 이어 쓰려면 RAGBase.search에도 맞추도록 짚는다.
2강 작성·실행·출력은 아직 미확인이다. AI는 실습 파일 수정·재실행·API 호출 없이
STATE만 로컬 저장했다.

2026-10-27 학습자가 Makefile 생성 위치를 물었다. AI는 외부 레포 최상위의 확장자 없는
Makefile과 run target·명령 앞 Tab을 안내했다. 이후 학습자가 2강 완료를 보고하며 다음을
요청했다. 실제 assistant.py 생성 함수·CLI main guard와 Makefile의 Tab·run 명령을 확인했다.
터미널 실행 결과는 직접 읽거나 재실행하지 않았으며 수행 완료는 학습자 보고로 기록한다.

공식 main의 03-chat-app.md를 확인했다. 기존 assistant를 Streamlit 질문 입력·버튼·처리
표시·답변 출력에 연결하고 기존 Makefile에 chat target을 추가하는 범위다. app.py는 아직
없고 pyproject.toml에 Streamlit도 없어 학습자가 공식 설치·작성 단계부터 진행한다.
레이아웃 개선·metrics·DB를 이번 필수 작업에 추가하지 않는다. 3강 작성·실행은 아직
미확인이며 AI는 실습 파일 수정·설치·재실행·API 호출 없이 STATE만 로컬 저장했다.

2026-10-27 학습자가 Module 5 / 3강 완료를 보고하고 다음을 요청했다. app.py의 입력·버튼·
spinner·답변 출력, Makefile chat target과 Streamlit 의존성 추가를 직접 확인했다.
브라우저 실행·실제 답변은 이번에 직접 확인하지 않았으며 학습자 보고로 기록한다.

공식 main의 04-metrics.md를 확인했다. metrics.py에 호출 기록 dataclass와 RAGBase를
상속하는 RAGWithMetrics를 만들고 LLM 호출 시간을 측정하며 usage·비용·시각을 last_call에
저장한다. assistant.py에서 새 클래스를 사용하고 app.py에 지표를 표시하는 범위다.
원문의 calculate_cost는 gpt-5.4-mini 조건만 있어 Luna로 그대로 쓰면 0을 반환한다.
기존 evaluation_utils.calc_price의 total_cost를 재사용하도록 안내한다. 이 단원의
response_time은 LLM 호출 구간이며 검색까지 포함한 RAG 전체 시간과 구분한다.
4강 작성·실행은 아직 미확인이다. AI는 실습 파일 수정·재실행·API 호출 없이 STATE만 저장했다.

2026-10-28 학습 시작 요청으로 Module 5 / 4강을 재개했다. 외부 metrics.py에서
LLMCallRecord의 필드·timestamp 기본값을 직접 확인했다. RAGWithMetrics는 아직 없고
assistant.py는 RAGBase, app.py는 답변 표시까지이므로 공식 Instrumented RAG부터
이어간다. 기존 calc_price는 비용 딕셔너리를 반환하므로 total_cost를 사용하도록 안내한다.
학습자 코드 수정·재실행·API 호출 없이 시작 위치만 갱신하며 4강 완료로 기록하지 않는다.

## 이전 작업으로 돌아갈 때

- [전환 직전 STATE](https://github.com/10o0o/llm-research-learning-lab/blob/211b6b510c83c39930b3cb2b6796e3a83c405144/STATE.md): 요약 실습 제안, 환경 확인 범위, 문의 앱의 수행·도움·미완료.
- [기존 코드·노트북·기록](archive/README.md): 문의 앱, micrograd·makemore 등 과거 작업.

문의 앱의 과거 이력 호환성, 거절 동작의 실행 확인, 근거 없는 추정과 오분류 등
남은 문제는 위 원본에 보존되어 있다. 과거 작업을 다시 선택할 때 해당 근거에서 이어가며,
현재 과제나 필수 선수조건으로 자동 전환하지 않는다.
