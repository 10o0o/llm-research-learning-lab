---
description: "승인된 학습 방법 재감사의 문서·운영 규칙·기존 검사 반영 작업"
---

# Tasks: 전체 학습 경로와 실제 학습 방식 재감사

**Input**: [승인 명세](spec.md), [승인 계획·최신 인계](plan.md), [조사 결정](research.md), [문서 관계](data-model.md), [8단위 계약](contracts/unit-audit.md), [튜터 계약](contracts/tutoring-flow.md), [검증 안내](quickstart.md), [20제안 추적표](evidence/proposal-traceability.md).

**현재 권한**: 공식 Run `94c571a9`의 명세·최종 계획 검토가 모두 승인됐다. 기존 문서의 “plan만/승인 전/tasks는 아직”은 해당 작성 단계의 이력이다. 이번 tasks 호출은 작성·정합성 검토 후 반환하고 공식 dispatcher의 implement가 아래 작업을 실행한다. 학습은 중지 상태다. 엔진 상태/로그 수정·중첩 workflow 실행·CLI 경로 수리는 하지 않는다.

**Tests**: 사용자가 요청한 기존 검사 개선·회귀 검증을 포함한다. 새 앱·서비스 코드·학습 데이터·평가 정답·연습·학습자 실행은 작업이 아니다. V-A는 문서/보존, V-B는 합성 응답의 수동 검토이며 V-C 실제 학습 관찰과 효과는 이번에 미수행/미검증으로 남긴다.

**Organization**: spec의 시나리오 ID를 유지한다. P1인 US1·US2·US3·US4·US6 이후 P2인 US5를 배치한다. 모든 작업은 한 작성자가 순차 수행하며 완료 체크는 실제 반영·해당 검증 이후에만 한다.

**구현 현황**: T001~T033 반영·검토/명령 확인 완료. T034는 Git index byte 지문 불일치로 미해결이며 T035의 전체 완료 선언도 대기한다. staged 변경은 없고 보호 35파일·역사 구간·main·symlink는 동일하다. 상세는 [구현 검증](evidence/implementation-validation.md)에 남긴다. 승인 gate를 다시 열지 않는다.

## Format: `[ID] [Story] Description`

- 작업 ID는 T001~T035이며 사용자 시나리오 단계만 `[US1]`~`[US6]`을 붙인다.
- 이번 권한에서는 병렬 작업·추가 에이전트가 없으므로 `[P]` 표시도 없다.
- 모든 경로는 lab 루트 기준이다. 기준 문서가 상세 사실을 관리하고 README/USAGE/루트 지침은 필요한 요약·링크만 둔다.
- 아래 보고서 경로는 같은 feature의 추가 검증 근거다. 새 진도/성과 기록 시스템이 아니다.

## Phase 1: Setup — 현재 작업 트리와 보존 경계 확인

**목적**: 사용자 변경과 승인 원문을 보존한 구현 시작점을 확인한다. 설치·브랜치 전환·새 저장소 초기화는 없다.

- [X] T001 `/tmp/learning-method-implementation-preservation.json`의 35개 protected 파일·허용 운영 파일 지문과 `STATE.md`, `pyproject.toml`, `uv.lock`, `practice/ai-apps/`의 기존 bytes, `CURRICULUM.md` 역사 구간, Git index·main·`CLAUDE.md -> AGENTS.md`를 비교하고 시작 결과를 `specs/002-learning-method-audit/evidence/implementation-validation.md`에 기록한다. baseline을 새 값으로 덮어쓰지 않는다.
- [X] T002 `AGENTS.md`, `.specify/memory/constitution.md`, `specs/002-learning-method-audit/plan.md`의 최신 인계·F-01~F-14와 `tests/test_simplified_study_contract.py`의 관련 검사를 직접 대조해 기존 사용자 변경·바꿀 snapshot·유지할 보호 검사를 `specs/002-learning-method-audit/evidence/implementation-validation.md`에 구분한다. 운영 파일 편집 전에 V-B 8개의 동일 입력·제공 사실·사전 판정 기준과 기존 지침을 적용해 이번에 작성한 검토 응답을 `specs/002-learning-method-audit/evidence/behavior-review.md`에 남긴다. 기존 계획의 파일 확인 근거를 재사용하되 학습자 파일·모델을 실행하지 않는다.

## Phase 2: Foundational — 승인 계약과 작업 대응 확정

**목적**: 모든 시나리오의 공통 근거·권위·권한을 확인한다. Phase 1 이후 수행하고 이 단계 뒤에만 운영 파일을 편집한다.

- [X] T003 `specs/002-learning-method-audit/tasks.md` 아래 38 FR·20제안 대응을 `specs/002-learning-method-audit/evidence/tasks-analysis.md`와 대조해 누락/범위 확대가 없음을 재확인하고 `specs/002-learning-method-audit/evidence/implementation-validation.md`에 구현 기준을 남긴다. `specs/002-learning-method-audit/data-model.md`의 문서 제약인 “기존 8개와 1:1 대응. 변경/분할하더라도 원 ID 연결을 잃지 않음.”과 “확인/부분/미확인 구분, 기관 중복 집계 금지.”를 유지한다. 새 DB·모델·migration을 만들지 않는다.

**Checkpoint**: 두 승인 gate와 현재 반영 범위가 명확하고 보호 baseline을 확인했다. 새로운 명세/계획 승인 질문은 필요하지 않다.

## Phase 3: US1 — 전체 경로와 직접 할 일을 판단한다 (P1, MVP)

**목표**: AX 취업 우선·장기 RE, 8단위의 목적·입출력·선수·직접 작업·산출물·사전 평가·실패/미실행·연구 연결을 승인 계약대로 반영한다.

**독립 검증**: `ROADMAP.md`의 8개 ID와 E-01~08의 의미를 계약에 대조한다. 조건부 선택의 미수행과 과거 전체 계약 완료를 구별하고 현재 STATE를 건드리지 않아야 한다.

- [X] T004 [US1] `ROADMAP.md` 공통 원칙·첫 평가·지원 경계에 하나의 목적 있는 기능을 문제/입출력/앞뒤 흐름/직접 할 일/관찰·완료 기준/최소 선수 설명 뒤 작성→실행→첫 해석→실제 피드백으로 잇는 기준을 반영한다. 조기 공고 비교·주 서비스·연구 산출물과 여섯 설명을 유지하고 전권·전과목·전체 수학을 시작 gate로 만들지 않는다.
- [X] T005 [US1] `ROADMAP.md` AX-01을 학습용 문의 접수 정리로 명확히 하고 E-01의 형식/원문 사실/중복 질문/목적상 추가 확인/유용성을 구별한다. 실제 계정 해제·조직 정책 창작을 제외하고 “어디서/어떻게 로그인이 안되는지”와 충분한 현상 설명을 합리적 기준으로 인정한다. account ID 강요 없이 대체 문제·재검토 조건·지원/미실행 한계를 보존한다.
- [X] T006 [US1] `ROADMAP.md` AX-02에 sparse baseline 하나의 입력→근거→답변/기권·실패 분해와 E-02를 반영한다. dense/hybrid 추가 비교는 관찰한 오류 또는 사전 학습 질문에 따라 선택하고 corpus 색인과 평가 질의/qrels·개발/최종 용도를 구별한다. 미선택 비교를 수행/옛 계약 전체 완료로 세지 않는다.
- [X] T007 [US1] `ROADMAP.md` AX-03에 일반 Python 고정 흐름·도구 계약을 먼저 두고 E-03의 실제 모의 상태/오류/중복·거절·단계 제한을 유지한다. LangGraph는 상태 보존·중단/재개·승인이 필요할 때, bounded agent는 모델 주도 선택을 비교할 질문이 있을 때 선택하며 미선택을 미수행/근거 있는 제외로 남긴다.
- [X] T008 [US1] `ROADMAP.md` AX-04를 AX 초반부터 쌓는 작은 평가·권리·재현·오류·기여 설명 위에서 API/저장/서비스 경계·필요 회귀를 강화하는 단위로 조정한다. E-04의 정상/실패·상태 분리·실측/미계측·로컬/운영 경계를 보존하고 UI·클라우드·배포 완료를 필수화하지 않는다.
- [X] T009 [US1] `ROADMAP.md` RE-01~04를 `specs/002-learning-method-audit/contracts/unit-audit.md`의 네 계약·E-05~08과 대조해 필요한 작업 크기·사용 전 선수·보강·산출물/평가·연구 연결만 명확히 한다. 실제 학습/검증, 자체 LM 또는 공식 A1 대체, 전문화 한 비교, 실제 읽은 주장/실패의 제한 재현을 유지하고 현재 착수·성공·전체 공식 과제 완료를 만들지 않는다.
- [X] T010 [US1] `CURRICULUM.md` 현재 1~3절의 8단위 선수→의존 작업·실제 공백 보강·자료 사용처를 T004~T009와 동기화한다. sparse 이후 조건부 비교·고정 흐름 우선·최소 선수 시점을 반영하고 “## 역사적 참고 — 기존 4~8절 보존 경계”부터 끝까지 byte를 보존한다.
- [X] T011 [US1] `DEFERRED.md`의 모든 검색법·LangGraph/framework·agent 비교·UI/배포·전체 과목 관련 기본/선택과 복귀 조건을 승인 선택에 맞춘다. 기존 보류 이유·과제/자원/AI/Optional·미완료를 유지하고 복귀 조건 충족을 자동 재선택 권한으로 만들지 않는다.

**Checkpoint**: 전체 경로는 다른 시나리오의 새 요약이나 새 실습 없이 문서로 독립 검토할 수 있다. 실제 학습자 수행·채용 효과의 판정은 별도다.

## Phase 4: US2 — 공식 교육 운영과 적용 해석을 추적한다 (P1)

**목표**: 기존 공식 조사 원문/한계를 보존하며 채택 요소와 운영 문서의 연결을 검증한다. 승인된 조사를 다시 작성하거나 새 과정/채용 사실을 추측하지 않는다.

**독립 검증**: FSDL·Made With ML·DataTalksClub 3기관과 MIT 6.S191·CS224N·CS336 3강의의 판본별 7카드/9관점, 관찰/적용 해석/미확인을 보존된 카드에서 추적할 수 있어야 한다.

- [X] T012 [US2] `specs/002-learning-method-audit/evidence/plan-source-supplement.md`, `specs/002-learning-method-audit/evidence/official-education-sources.md`, `specs/002-learning-method-audit/evidence/proposal-traceability.md`의 출처 카드·URL/판본/구간/조회일·9관점 상태와 제안의 연결을 읽기만 대조하고 결과를 `specs/002-learning-method-audit/evidence/implementation-validation.md`에 남긴다. FSDL 2과정을 2기관으로 세지 않고 CS224N 비중 불일치·가변 main·접근 실패·자습 채점/멘토·정책 미확인을 보존한다.
- [X] T013 [US2] `CURRICULUM.md` 현재 3절에 승인된 교육 요소의 실제 사용처·판본/접근/권리 한계와 필요한 근거 링크만 보완한다. T010의 선수표와 맞추고 상세 카드·3×14·5×9 비교표를 복제하거나 모든 비교 과정을 필수 수강으로 바꾸지 않는다. 새로운 현재 사실이 필요하면 공식 원문 확인 전 주장하지 않는다.

## Phase 5: US3 — 불만과 진행을 연결해 튜터 운영을 교정한다 (P1)

**목표**: C-01~12의 운영 이행/문서 보완/근거 부족을 구별하고 충분한 답·질문 혼란·준비·명시 위임·실제 피드백 경계를 정리한다.

**독립 검증**: 기본 직접 학습, 자체 프로젝트의 현재 명시 위임, 과거 지원, 공식 과제/무보조 확인 각각의 기대 행동이 구별돼야 한다. 도움은 독립 숙달이 아니며 중복 승인·즉시 백지 재시험을 요구하지 않아야 한다.

- [X] T014 [US3] `.agents/references/learning-policies.md`의 소유권·허용 준비·디버깅 조항에 자체 프로젝트의 현재 명시적 수정/작성/필요 검증 위임을 요청 범위대로 수행하는 경계를 명확히 한다. 기존의 포괄 금지 문구와도 맞추되 기본 학습자 코드/데이터/실행/첫 해석, 세 시작 상태, 공식 과제/무보조 제한은 유지한다. 중복 승인·일괄 거절·과거 위임의 상시 권한화·도움 직후 즉시 백지 시험을 막고 실제 작성/실행 주체를 구분한다.
- [X] T015 [US3] `.agents/references/learning-policies.md`의 평가/운영 근거에 역할·처리 단계·허용 절차·사전 충분성 기준, 형식/내용/업무 유용성·독립 사례/반복·개발/최종·실패/미실행의 구분을 반영한다. 목적 미정의 복수 타당 해석과 중복 추가 질문 금지를 다루고 조건을 사후 변경하면 개발 검토임을 밝히도록 한다. V-A/B와 V-C를 구별한다.
- [X] T016 [US3] `.agents/skills/study-session/SKILL.md`에 온전한 작은 기능·사전 기준·실제 코드/저장 출력/첫 해석의 연결과 현재 명시 위임 처리의 짧은 요약/정책 링크를 반영한다. 기존의 대상 금지·수리 조항과 충돌을 정리하고 확인 한 번 제한·표현 변경·충분한 답 수용·실제 오류 때만 가설·연결 진행·중지/종료/과제 제한을 보존한다. 같은 답 재시험·매번 계속 여부 질문을 추가하지 않는다.
- [X] T017 [US3] `.agents/skills/study-session/references/tutor-cases.md`에 튜터 계약의 8상황을 기존 사례와 중복을 줄여 연결한다. 각 상황의 제공 사실·기대 행동·실패/미실행과 지원/기여·목표 미정·중지 경계를 명확히 하고 기존 준비/공식 과제/종료/회상 사례와 합성 검토·실제 효과 구분을 유지한다. 새 harness/agent 실행 의무는 넣지 않는다.
- [X] T018 [US3] `AGENTS.md`의 기본 소유권·대상 대행 금지·명시 위임 해석에 실제 충돌이 있는 부분만 최소 명확화하고 `.agents/references/learning-policies.md` 상세로 연결한다. 필독·단일 STATE·단계 승인·중지/권한·공개/과제·Git·추가 작성자 금지를 보존한다. `CLAUDE.md`는 편집하지 않고 symlink를 유지한다.

## Phase 6: US4 — 반복 실행과 관찰의 도구 경계를 정한다 (P1)

**목표**: 반복 실행 본체 하나와 선택적 관찰 노트북, 최소 준비와 재사용의 조건을 설명한다. 형식 변경을 성과로 세지 않는다.

**독립 검증**: research의 3안×14관점과 연결돼야 하며 Python 본체/선택적 얇은 notebook의 기준 구현·설정·출력/숨은 상태 책임이 분명해야 한다. 실제 두 파일의 bytes는 그대로여야 한다.

- [X] T019 [US4] `ROADMAP.md`에 반복 실행은 Python 본체 하나, 분석/시각화/텐서 관찰에 필요할 때만 얇은 notebook을 쓰는 기준을 간결히 반영하고 `specs/002-learning-method-audit/research.md`의 3×14 비교로 연결한다. notebook 금지·두 본체/지시문 복제·거대 패키지/선행 CI·확장자만으로 성능/재현 우위 주장을 막고 기존 notebook/CLI는 보존한다.
- [X] T020 [US4] `.agents/references/learning-policies.md`에 허용 준비/기존 실행 경로 재사용과 기준 구현·설정 한 곳, 관찰 출력 최신성·커널/외부 모델 수명·로딩 미측정의 책임을 보완한다. 준비 복붙·재승인·실습 이동을 의무화하지 않으며 이번 변경으로 `practice/ai-apps/inquiry-assistant.ipynb`나 `practice/ai-apps/inquiry_assistant.py`를 옮기거나 수리/실행하지 않는다.

## Phase 7: US6 — 문서·합성 응답·실제 학습 검증을 구별한다 (P1)

**목표**: 필요한 기존 검사만 바꾸고 V-B를 실제로 수동 검토한다. V-C는 재개 후의 검증으로 남긴다.

**독립 검증**: 유효한 후속/평가 북마크는 통과하고 무효 단위·빈/복수 행동·사적 정보는 거절돼야 한다. V-B는 8상황의 검토 응답·기대 행동·판정 이유가 분리돼야 하며 실제 학습 효과를 주장하지 않아야 한다.

- [X] T021 [US6] `tests/test_simplified_study_contract.py`의 `test_state_is_a_public_bookmark_with_one_next_action_and_preserved_original`을 AX-01·예전 행동 문자열·현재 `미실행` 필수 snapshot에서 유효 단위/필수 필드·의미 있는 다음 독립 행동 하나·사적 정보 배제의 계약 검사로 분리한다. 현재 경로/단위/범위·실제 근거/재확인과 다음 행동을 검증하고 양성 fixture에 후속 AX/RE 단위·평가/해석을, 음성 fixture에 없는 단위·빈 행동·서로 다른 독립 목표 두 개(한 줄 나열 포함)·사적 정보를 포함한다. 한 기능의 작성→실행→해석은 목적/관찰·완료 경계를 공유하는 한 행동으로 수용해 동사 개수로 거절하지 않는다. 과거 인용 hash·도움/미완료·현재 북마크 역할 검사는 보존하고 새 현재 snapshot/형식을 강제하거나 `STATE.md`를 고치지 않는다.
- [X] T022 [US6] `tests/test_simplified_study_contract.py`의 실제 바뀐 검색/framework 선택·현재 명시 위임·행동 검토 계약만 조정/보강한다. 요청 없는 상시 대행과 현재 위임, 제공 코드/학습자 구현·실행, V-A/B/V-C·과제/무보조 제한의 회귀를 검증하고 첫 baseline의 입력/정상·누락·범위 밖/미실행·기존 보존/권한 검사를 일괄 삭제하지 않는다. 변경한 assert와 유지한 보호 범위를 구현 검증 보고서에 남긴다.
- [X] T023 [US6] T002에서 고정한 `specs/002-learning-method-audit/contracts/tutoring-flow.md`의 8상황·제공 사실·사전 판정 기준으로 반영 지침의 이번 검토 응답을 한 작성자가 순차 작성하고 `specs/002-learning-method-audit/evidence/behavior-review.md`에 기존 검토 응답을 보존한 채 실제 검토 응답·기대 행동·판정 이유·실패/비교 한계를 구분해 저장한다. 충분한 답/혼란/준비 재사용/기본·무보조·과제/현재 위임/목표 미정/형식 pass·미실행/중지를 모두 포함한다. 합성 수동 검토이며 과거 응답 재현·독립 모델 평가·학습 효과가 아님을 명시한다.
- [X] T024 [US6] `.agents/references/learning-policies.md`와 `.agents/skills/study-session/references/tutor-cases.md`의 V-A/B/C 의미를 `specs/002-learning-method-audit/quickstart.md`에 대조하고 실제 활동 1단위 이상·6관점·별도 재개 요청 전제와 실패/미수행 판단을 유지한다. 현재 V-C/SC-007 미수행·효과 미검증을 `specs/002-learning-method-audit/evidence/implementation-validation.md`에 기록하며 실제 수업·코드/모델 실행·자동 기록은 하지 않는다.

## Phase 8: US5 — 지속 발전과 포트폴리오의 경계를 안내한다 (P2)

**목표**: 같은 서비스는 누적하고 독립 문제/연구는 필요에 따라 분리하는 기준과 기여/권리/재현 근거를 설명한다. 실제 repo 생성은 없다.

**독립 검증**: 초기 개발 저장소 시작 조건과 작동 기능/평가 baseline/AX-04·포트폴리오 성과 주장 조건을 구별해야 한다. 5전략×9관리와 출처·도움·공식 답안 비공개를 추적할 수 있어야 한다.

- [X] T025 [US5] `ROADMAP.md`에 목적·기준 구현·환경·권리/공개·원본 보존 경계를 정하면 초기 개발판부터 별도 서비스 repo 하나에서 발전할 수 있음을 반영한다. 최소 작동 기능/평가 baseline/AX-04를 repo 시작의 선행 시험으로 두지 않고 실제 작동/평가·실패·직접 기여/재현은 성과 주장의 근거로 구별한다. 같은 서비스 누적·독립 문제/연구 분리·개수 quota 없음과 5전략×9관리 근거 링크를 둔다. 생성/이전/게시/배포는 실행하지 않는다.
- [X] T026 [US5] `README.md`에 T004~T025의 실습 선택·서비스 지속 발전·제공 도구와 직접 기여·중지/재개의 필요한 요약/기준 링크만 동기화한다. 현재 위치 복제·긴 비교표·새 완료 주장 없이 기존 시작/종료·공개·권한·사이트 안내를 유지한다.
- [X] T027 [US5] `USAGE.md`에 초기 개발 공간과 포트폴리오 주장 구분·Python 본체/선택적 notebook·허용 준비/현재 위임·실제 근거의 짧은 안내와 기준 링크를 반영한다. 학습 중지·단일 STATE·기록/과제·Git 권한과 기존 재개/종료 흐름을 유지하고 새 repo/배포/학습 실행을 암시하지 않는다.
- [X] T028 [US5] `practice/README.md`의 기존 후보 공간·원본/도움·공식 과제·준비 책임 안내를 최종 기준 문서와 대조한다. 실제 불일치가 있을 때만 필요한 요약/링크를 최소 수정하고 없으면 그대로 둔 이유를 `specs/002-learning-method-audit/evidence/implementation-validation.md`에 남긴다. 경로 이동·초기화·새 실습 준비는 하지 않는다.

## Phase 9: Polish & Cross-Cutting Concerns — 저장 내용과 필수 검증

**목적**: 각 시나리오의 반영 내용·검사·보존을 최종 대조한다. 수정이 필요하면 원인/기존 변경/권한을 구별하고 해당 검사부터 재검증한다.

- [X] T029 실제 저장된 `ROADMAP.md`, `CURRICULUM.md` 현재 1~3절, `DEFERRED.md`, `.agents/references/learning-policies.md`, `.agents/skills/study-session/SKILL.md`, `.agents/skills/study-session/references/tutor-cases.md`, `AGENTS.md`, `tests/test_simplified_study_contract.py`, `README.md`, `USAGE.md`와 조건부 수정된 `practice/README.md`를 각 편집 직후 및 최종 연결 상태에서 재독한다. 기준/요약 역할·8단위/E-01~08·선수/조건부 선택·현재 위임/공식 제한·중지 의미가 맞는지 검토하고 결과를 `specs/002-learning-method-audit/evidence/implementation-validation.md`에 남긴다.
- [X] T030 `specs/002-learning-method-audit/evidence/proposal-traceability.md`와 `specs/002-learning-method-audit/tasks.md`를 최종 반영 파일에 대조해 38 FR·20제안·8단위·12불만·7카드×9상태·실습 3×14·저장소 5×9의 누락/오분류를 V-A로 검토하고 `specs/002-learning-method-audit/evidence/implementation-validation.md`에 실제 반영 위치/보존 근거·실패/미확인을 기록한다. 기존 추적표를 재작성하지 않고 표/문구 존재를 학습 효과로 세지 않는다.
- [X] T031 변경된 운영 Markdown과 `specs/002-learning-method-audit/plan.md`, `specs/002-learning-method-audit/tasks.md`, `specs/002-learning-method-audit/evidence/tasks-analysis.md`, `specs/002-learning-method-audit/evidence/behavior-review.md`, `specs/002-learning-method-audit/evidence/implementation-validation.md`의 로컬 파일/anchor·표 열·fence·공백·미완성 placeholder를 검사한다. 제외 영역의 기존 링크는 권한 범위를 구별하고 `web/`, `archive/`, private, 공식 clone, 사내비 원본에 진입/읽기하지 않는다. 새 자동 검사 시스템을 만들지 않는다.
- [X] T032 lab 루트에서 `uv run --frozen pytest -q tests .agents/skills`를 실행하고 exit code·통과/실패·실제 원인·기존 변경 관련 여부를 `specs/002-learning-method-audit/evidence/implementation-validation.md`에 기록한다. 허용된 운영/검사 변경에 원인이 있으면 수정·재검증하고 설치·학습자 실행·보호 파일 변경으로 green을 만들지 않는다.
- [X] T033 lab 루트에서 `uv lock --check`와 `git diff --check`를 실행해 결과를 `specs/002-learning-method-audit/evidence/implementation-validation.md`에 기록한다. 미추적 새 Markdown은 별도 공백 검사로 보완하고 lock/설정/STATE를 검사 통과용으로 바꾸지 않는다.
- [X] T034 `/tmp/learning-method-implementation-preservation.json`과 최종 상태를 재비교해 protected 35파일·기존 실습 bytes·001 전체·헌법·승인 spec/체크리스트/기존 evidence·STATE/pyproject/uv.lock·CURRICULUM 역사 구간·index·main·symlink 보존과 F 허용 경로 내 변경/생성만 있음을 `specs/002-learning-method-audit/evidence/implementation-validation.md`에 기록한다. baseline 갱신·reset/stash·stage/commit/push는 하지 않는다.
- [X] T035 `specs/002-learning-method-audit/evidence/implementation-validation.md`를 실제 반영 목록·V-A/필수 명령·V-B 8사례 판정/한계·V-C/SC-007 미수행·효과 미검증·Git 변경 작업 미실행으로 마무리하고 `tasks.md`는 실제 완료 근거가 있는 항목만 체크한다. 두 파일을 다시 읽고 같은 Run의 공식 dispatcher에 정상 반환하되 엔진 완료 상태를 직접 확인/수정했다고 주장하지 않는다.

## Dependencies & Execution Order

실행 순서: `T001~T003 → US1(T004~T011) → US2(T012~T013) → US3(T014~T018) → US4(T019~T020) → US6(T021~T024) → US5(T025~T028) → T029~T035`.

| 시나리오 | 의존성·독립 검증 |
| --- | --- |
| US1 | 기반 확인 이후 8단위 계약을 기준으로 문서만 검증. 다른 개선의 효과를 전제하지 않음. |
| US2 | 보존된 source card로 독립 검증 가능. 현재 자료표 동기화는 US1의 CURRICULUM 편집 뒤 수행. |
| US3 | 승인 튜터 계약으로 독립 검증. 평가/소유권 상세가 스킬·루트보다 먼저 확정돼야 함. |
| US4 | 승인 3×14 비교로 독립 검증. US1/US3과 같은 ROADMAP/정책을 쓰므로 후속 순차 편집. |
| US6 | 단위/필드/권한의 독립 fixture와 8사례 검토. 최종 규칙 적용 뒤 수행하며 전체 suite는 US5 안내 동기화 후 실행. |
| US5 | 승인 5×9·repo 조건으로 독립 검증. 기준 문서/도구/검증 경계를 확정한 뒤 요약을 반영. |

### Parallel execution examples — 이번에는 순차 대체

사용자의 단일 작성자·순차 진행이 템플릿의 병렬 예보다 우선한다. `[P]` 작업과 추가 agent/swarm은 0개다.

| 시나리오 | 가능한 분리 관점 | 실제 실행 예 |
| --- | --- | --- |
| US1 | 단위별 계약은 따로 대조 가능하지만 ROADMAP을 공유 | T004 → T005 → T006 → T007 → T008 → T009 → T010 → T011 |
| US2 | 출처 판본/한계 검토와 자료표 변경 | T012 → T013 |
| US3 | 정책·스킬·사례·루트는 파일이 달라도 상세/요약 의존 | T014 → T015 → T016 → T017 → T018 |
| US4 | 도구 기준과 준비 절차의 의존 | T019 → T020 |
| US6 | fixture·선택 계약·합성 응답의 검사 목적이 다름 | T021 → T022 → T023 → T024 |
| US5 | 기준과 안내는 독자가 달라도 같은 결정에 의존 | T025 → T026 → T027 → T028 |

## Requirements, proposals, and file coverage

기존 추적표는 설계·공식/사용자 근거의 기준으로 보존한다. 아래는 후속 실행의 연결이다. 선행 조사 요구는 기존 근거 확인·보존으로 충족 범위를 검증하며 조사를 새로 한 사실로 세지 않는다.

| 요구 | 실행/검증 작업 |
| --- | --- |
| FR-001 | T004, T009, T025~T027, T030 |
| FR-002 | T002, T010~T013, T029, T034 |
| FR-003 | T014~T016, T021~T024, T030 |
| FR-004 | T005, T012, T025, T034 |
| FR-005 | T004~T011, T029~T030 |
| FR-006 | T004~T011, T016, T029 |
| FR-007 | T004~T009, T016~T017, T023 |
| FR-008 | T004~T010, T015, T023~T024, T030 |
| FR-009 | T004, T009, T025~T027 |
| FR-010 | T012~T013, T030 |
| FR-011 | T012~T013, T030 |
| FR-012 | T003, T012~T013, T030 |
| FR-013 | T012~T014, T030, T034 |
| FR-014 | T012~T013, T024, T030 |
| FR-015 | T005, T014~T020, T023, T030 |
| FR-016 | T002~T003, T014~T018, T023, T030 |
| FR-017 | T014, T016~T018, T022~T024 |
| FR-018 | T005, T015~T017, T023 |
| FR-019 | T001~T002, T020, T034; 기존 nbpeek/CLI 읽기 근거 보존, 추가 실행 없음 |
| FR-020 | T015~T017, T022~T023 |
| FR-021 | T001~T003, T016~T018, T023~T024, T035 |
| FR-022 | T019~T020, T027, T030 |
| FR-023 | T019~T020, T030 |
| FR-024 | T019~T020, T023~T024 |
| FR-025 | T019~T020, T027, T034 |
| FR-026 | T025~T028, T030 |
| FR-027 | T025~T028, T030 |
| FR-028 | T025~T028, T030 |
| FR-029 | T014, T018, T025~T028, T034 |
| FR-030 | T001~T003, T014, T018, T021~T022, T034 |
| FR-031 | T022~T024, T030~T035 |
| FR-032 | T024, T035; 6관점의 계획/미수행만 확인, V-C 실행 제외 |
| FR-033 | T004~T009, T015, T023~T024, T030 |
| FR-034 | T003, T012, T030 |
| FR-035 | T010~T011, T014~T022, T025~T031, T034 |
| FR-036 | T002~T003, T035; 두 gate 승인 인계 적용, 역사적 명세 중지 지시 재적용 없음 |
| FR-037 | T001~T003, T020~T021, T028, T034~T035 |
| FR-038 | T001~T003, T035; setup 실제 결과와 엔진 상태 미확인을 구별 |

| 제안 | 실행/검증 작업 |
| --- | --- |
| R-01 | T004~T011, T029~T030 |
| R-02 | T005, T015, T023 |
| R-03 | T007, T010~T011, T022 |
| R-04 | T019~T020, T027, T030 |
| R-05 | T025~T028, T030 |
| R-06 | T014, T016~T018, T022~T024 |
| R-07 | T005, T015~T017, T023 |
| R-08 | T016~T017, T023 |
| R-09 | T004~T010, T015, T023~T024 |
| R-10 | T004, T025~T027 |
| R-11 | T021~T022, T032, T034 |
| R-12 | T001~T003, T023~T024, T029~T035 |
| U-AX-01 | T005, T010, T015, T029~T030 |
| U-AX-02 | T006, T010~T011, T022, T029~T030 |
| U-AX-03 | T007, T010~T011, T022, T029~T030 |
| U-AX-04 | T008, T010, T029~T030 |
| U-RE-01 | T009~T010, T029~T030 |
| U-RE-02 | T009~T011, T014, T029~T030 |
| U-RE-03 | T009~T011, T029~T030 |
| U-RE-04 | T009~T011, T029~T030 |

| 계획 경계 | 실행/검증 작업 |
| --- | --- |
| F-01 ROADMAP | T004~T009, T019, T025, T029~T031 |
| F-02 CURRICULUM 현재 1~3절 | T010, T013, T029~T031, T034 |
| F-03 DEFERRED | T011, T029~T031 |
| F-04 상세 정책 | T014~T015, T020, T024, T029~T031 |
| F-05 study-session | T016, T029~T031 |
| F-06 tutor-cases | T017, T023~T024, T029~T031 |
| F-07 AGENTS·CLAUDE link | T018, T029~T031, T034 |
| F-08 기존 검사 | T021~T022, T029, T032 |
| F-09 README·USAGE | T026~T027, T029~T031 |
| F-10 practice/README 조건부 | T028~T031, T034 |
| F-11 STATE 보존 | T001~T002, T021, T034 |
| F-12 실습/001/헌법/설정 보존 | T001~T003, T020, T034 |
| F-13 승인 원문·기존 evidence 보존 | T001~T003, T012, T030, T034 |
| F-14 같은 feature의 tasks/추가 근거 | T003, T012, T023~T024, T029~T035 |

## Implementation Strategy

**MVP**는 Phase 1~3의 보존 확인과 전체 8단위 계약 반영이다. 이것만으로도 경로의 직접 작업/선수/산출물을 검토할 수 있다. MVP는 이번 요청의 최종 종료 지점이 아니며 승인된 나머지 시나리오와 검증도 이어 수행한다.

기준 경로 → 출처/자료 한계 → 상세 정책 → 스킬/사례/루트 → 도구 경계 → 의미 검사와 V-B → 저장소/안내 → 전체 검증 순으로 진행한다. 같은 파일은 앞 변경을 보존해 후속 편집하고 저장 후 재독한다. 실제 실패·미수행·효과 미검증을 나누고 학습자 실행/STATE 변경으로 문서 검사를 통과시키지 않는다. 커밋/푸시/새 repo/배포는 이 전략의 작업이 아니다.
