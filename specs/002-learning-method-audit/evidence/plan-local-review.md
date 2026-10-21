# 계획 단계의 현재 파일 확인

확인일: 2026-10-21. [기존 로컬 관찰](local-observations.md)과 원본 evidence를 보존한 추가 근거다. 사용자 불만·과거 요청·최신 판단은 승인 명세/이번 입력에서 받은 사실이며 별도 대화 로그를 재구성하지 않았다. 이 문서는 새 진도·학습 기록이 아니다.

## 직접 읽은 기준과 역할

| 대상 | 이번 읽기 범위 | 계획에서의 사용 |
| --- | --- | --- |
| [STATE](../../../STATE.md) | 현재 범위·근거·재확인·다음 독립 행동 | AX-01, 제공 CLI를 학습자가 실행·해석할 북마크. 새 사례/최종 평가·실제 CLI 모델 실행은 미확인. 보존. |
| [ROADMAP](../../../ROADMAP.md) | AX-01~04·RE-01~04 전체, 평가/지원/보존 | 현행 8단위의 기준. LangGraph/두 방식 고정과 한 서비스 발전의 구체 조건을 재검토. |
| [CURRICULUM](../../../CURRICULUM.md) | 현재 1~3절 | 선수/사용처/보강·자료 판본. 역사적 4~8절을 새 의무/숙달로 해석하지 않음. |
| [DEFERRED](../../../DEFERRED.md) | 보류·복귀 조건 전체 | 전권/전체 과제/기술 순회·자원 제한 보존. 조건이 자동 선택 권한은 아님. |
| [README](../../../README.md)·[USAGE](../../../USAGE.md) | 사용자 시작/재개/종료·공개·준비 안내 | 요약/링크 역할. 웹 안내를 읽었으나 `web/`에 진입하지 않음. |
| [AGENTS](../../../AGENTS.md) | 전체 | 단일 STATE·소유권·권한·보존·공식 과제·Spec Kit 승인 경계. |
| [study-session](../../../.agents/skills/study-session/SKILL.md) | Teach and review·확인 한 번 제한·실제 근거/평가·중지/종료 포함 전체 절차 | 이미 있는 충분한 답 수용/연결 진행은 운영 교정. 기능 작업 크기/충분성 기준은 보완 후보. 수업으로 발동하지 않음. |
| [learning-policies](../../../.agents/references/learning-policies.md) | 준비·소유권·평가·과정별 정책·기록/Git 전체 | 지원과 대상 대행을 구별하되 핵심 구현 금지/CS336 제한 유지. |
| [헌법](../../../.specify/memory/constitution.md) | 1.0.0 전체 | 취업 우선·직접 구현·맥락 선수·근거 보존·단순 운영. 수정 없음. |
| [001 조사](../../001-employment-project-curriculum/research.md)·[선택 매핑](../../001-employment-project-curriculum/research/decision-matrix.md)·[과정](../../001-employment-project-curriculum/research/reference-curricula.md)·[계약](../../001-employment-project-curriculum/contracts/learning-contract.md)·[명세](../../001-employment-project-curriculum/spec.md) | 목표/문제/기술 선택·학습 계약·선수/평가/공간/근거 보존 결정 | 이전 승인/구현과 이번 재감사를 구별. 옛 JD/기술 도구 사실을 현재 채용/호환 근거로 재사용하지 않음. |

001의 후보 공간과 실제 `practice/ai-apps/` 경로 차이만으로 구현 오류라 하지 않는다. 실제 선택의 권한·기여·평가·공개/재현을 본다. 현재 운영 파일을 이번 계획에 맞게 편집하지 않았다.

## 현재 산출물: 읽기와 실행의 경계

작업 노트북 (`practice/ai-apps/inquiry-assistant.ipynb`, 로컬 확인 자료)은 `scripts/nbpeek.py`의 `--list`, `--cells 1-5`로 관련 저장 셀/출력만 확인했다. 셀 0/6 본문·전체 JSON은 읽지 않았고 셀·kernel·모델은 실행하지 않았다. private 입력/기록도 열지 않았다.

| 위치 | 직접 확인한 사실 | 인정하지 않는 결론 |
| --- | --- | --- |
| 셀 1 | 문의 목록·항목/필드/문자열/공백 검사, 개발용 가상 입력 3건의 저장 출력 | 현재 3건이 독립 최종 평가·실제 고객 요구라는 결론 |
| 셀 2 | id 조건 find·메시지와 지원 표시, 이미 제공한 정보의 중복 추가 확인 금지 지시문 | 검색/메시지 구현이 학습자 무보조 코드라는 결론 |
| 셀 3/4 | 같은 개발 문의의 구조화 응답·본문 표시. 추가 확인 목록은 비어 있음 | 빈 목록이 모든 목적/새 사례에서 적절하거나 지시문의 전후 향상이 입증됐다는 결론 |
| 셀 5 | 튜터 작성 표시의 JSON 검사·형식 pass | 사실/업무 충분성·독립 숙달 pass |
| inquiry_assistant.py (`practice/ai-apps/inquiry_assistant.py`, 로컬 확인 자료) | 전체를 읽기만 함. 입력/선택/지시문/요청/형식 검사·표시·기록/조회와 튜터 지원 설명 | import·CLI 도움말·실제 모델·history를 실행/검증했다는 결론 |

노트북과 스크립트에는 비슷한 지시문·find·형식 검사 로직이 각각 있다. 이는 중복 관리가 필요하다는 관찰이며 전체 동등성을 테스트한 결과는 아니다. 저장된 요청 메타데이터가 있더라도 cold/warm·서버 수명·장치 조건을 통제한 확장자별 성능 비교로 쓰지 않는다. 변경 전 별도 응답과 새 사례의 비교는 만들지 않는다.

학습자의 지시문 추가·직접 실행/저장과 최신 내용 판단의 주체는 이번 사용자 입력/STATE에 따른 구분이다. 저장 셀만으로 독립 작성 여부를 판정하지 않는다. 제공 CLI의 모의 검증 이력은 인계된 사실이며 이번에 재실행한 사실이 아니다.

## 검사에서 확인한 의미와 고정 문구

[현재 운영 검사](../../../tests/test_simplified_study_contract.py)의 관련 함수/호출을 읽었다. 이 단계에서 테스트 파일을 수정하거나 학습자 코드를 실행하지 않았다.

| 함수/구간 | 현재 검사 | 후속 계획의 판단 |
| --- | --- | --- |
| `test_state_is_a_public_bookmark_with_one_next_action_and_preserved_original`, 550~568행 | 단일 필드/다음 절·금지 정보·과거 원문 hash 보존과 함께 `AX-01`, `식별자·본문`, `직접 작성·실행`, `준비`, `미실행`을 현재 STATE에 요구 | 단일 역할/과거 원문/금지 정보는 유지. 단위·행동 문구·현재 미실행 상태 고정은 스냅샷과 계약을 분리. 의미상 다음 행동 한 개도 검증. |
| `test_first_baseline_has_its_own_completion_boundary`, 152~158행 | AX-01 입력/정상·누락·범위 밖·baseline·모델 미접근 경계 | 핵심 평가/입력 경계 유지. R-02의 접수 목적과 맞게 대조. 현재 STATE의 첫 활동으로 강제하지 않음. |
| `test_tutoring_contract_distinguishes_support_progress_and_mastery`, 82~97행 | 관련 없는 API 예·target 답안 금지·후속 확인 한 번·다음 진행·독립 근거 분리 | 유지. 준비를 반복시키는 예외나 즉시 재시험으로 바꾸지 않음. |
| 준비 관련 331~396행 | 제공 starter/기존 복구/무보조 공간 구별, 준비 책임·출력/코드 보존·허용/제한 | 유지. 지원 유형의 명확화만 검토. 기존 세 시작 상태를 대체하지 않음. |
| 행동 관련 399~437행 | 사례 목록과 응답 비교 방법의 문구 검사 | 사례 존재/검증 방법일 뿐 실제 행동/교육 효과 증거 아님. 새 시나리오는 동일 입력으로 검토하되 이번에 agent/실제 수업을 실행하지 않음. |

현재 전체 suite의 통과 여부나 새 운영 계약 이행을 이 읽기로 주장하지 않는다. 새 계획 문서의 링크/표/추적/보존 검증과, 계획 승인 후의 운영 검사 실행을 구별한다.

## 설정·작업 경계

- 기존 작업 트리는 `main`이고 STATE·pyproject·uv.lock 변경 및 미추적 실습/002가 있었다. 시작 시 보존 대상 61파일의 bytes/크기와 Git branch·HEAD·staged 목록을 임시 비교 자료로 확보했다. 이 자료는 학습자 진도 기록이 아니다.
- 검증 중 이 command가 작성하지 않은 [pilot-purpose-decision.md](pilot-purpose-decision.md)가 추가된 것을 발견해 읽었다. 시작 baseline에는 없으므로 별도 추가 공급 근거로 분류하고 최초 확인 뒤 bytes/크기를 보존 비교에 추가했다. R-02의 접수 목적과 일치하며, R-05에는 초기 개발 저장소와 포트폴리오 주장 준비의 구분을 반영했다. 이 파일을 수정하지 않는다.
- `.python-version`은 3.14, pyproject는 Python 3.14 범위·uv 의존성/pytest를 선언한다. 선언을 실제 새 설치/호환 검증으로 보고하지 않는다.
- `setup-plan.sh --json`은 기존 feature 경로를 명시하고 feature pointer 저장을 끈 채 실행했다. plan template을 같은 feature에 준비했다. 반환 `BRANCH=002-learning-method-audit`는 스크립트의 feature 식별자 fallback이며 실제 Git branch는 `main`이다.
- 승인 명세·요구 체크리스트·기존 evidence·001·운영/실습·헌법·설정/lock은 보존한다. 추가 보호 파일의 비교와 새 문서 검증 결과는 [계획 검증 결과](plan-validation.md)에 기록한다.
- Run `94c571a9`의 review-spec 승인/completed는 최신 사용자/상위 인계 사실이다. 이 command 내부에서 중첩 도우미 check/run/resume·엔진 파일/로그 수정·status 대행을 하지 않는다. plan 작성 중 running과 반환 뒤 엔진의 paused/review-plan은 별도 사실이며 후자는 상위 도우미 확인 대상이다.
