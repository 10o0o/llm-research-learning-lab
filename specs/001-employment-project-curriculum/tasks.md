# Tasks: 조사 근거로 다시 설계하는 취업 우선 커리큘럼

**Input**: `specs/001-employment-project-curriculum/`의 승인된 spec.md·plan.md·research.md·research/*·data-model.md·contracts/learning-contract.md·quickstart.md
**Run**: `17fc341e` — 2026-10-19 공식 6단계 completed, 문서 개편 31/31 확인
**범위**: 운영 Markdown·학습 스킬·기존 pytest 계약의 이행과 검증. 앱/모델/학습 데이터/실습 공간 생성·학습/추론/API 호출·공식 과제 저장소 명령·커밋/푸시/외부 게시/유료 실행은 제외한다.
**Tests**: FR-024·025 및 사용자 요청에 따른 기존 검사 이행. 테스트를 먼저 바꾸고 관련 실패를 확인한 뒤 문서를 구현한다. 문서 구현 완료와 실제 학습 성과는 구별한다.

## 최종 문서 개편 결과

공식 도우미의 `status 17fc341e`에서 specify·review-spec·plan·review-plan·tasks·implement와 Run 전체의 **completed**를 확인했다. CLI 반환 시 남은 T013의 family 8 한 문장은 부모 세션이 준비된 패치를 실제 적용하고 다시 읽어 의미를 확인했다. 이후 전체 pytest 73개·lock·diff 검사가 통과해 **31/31 작업 완료, 미완료 0개**다. 현재 재개는 AX/AX-01의 입력 계약 확인이며 과거 인용으로 돌아가지 않는다. 실제 학습·모델/API 실행·타 도구의 동작·배포/운영·채용 결과와 커밋·푸시는 이 완료의 범위가 아니다. 자세한 최종 근거는 `quickstart.md` 마지막 절에 둔다.

## 이전 tasks 재개 호출의 문서 구현 결과 — 과거 참고

부모 세션이 하위 CLI의 `.agents/` 쓰기 제한을 해결하기 위해 같은 Run을 중단하고, 검토된 패치를 실제 저장소에 적용했다. 새 feature/브랜치/Run을 만들지 않는다. 실제 전체 pytest 73개·lock·diff 검사, 보호 파일 207개/루트 노트북 3개, 옛 STATE/CURRICULUM 본문/기존 실습 목록 보존, 링크/표·단위/근거 대응을 확인했다. 승인 범위의 구현과 검증을 반복 승인 없이 마친다. 자세한 실제 결과는 `quickstart.md` 마지막 절에 있다.

T021은 이번 재개 호출에서 **실제 AGENTS→study-session→learning-policies→STATE를 차례로 열어 읽고**, AX/AX-01의 문의 식별자·본문 입력 계약 확인이라는 같은 다음 독립 행동을 찾았다. ROADMAP의 AX-01과 CURRICULUM의 관련 선수/자료도 대조했다. 과거 Part 4 인용은 현재 재개로 사용하지 않았으며 실제 수업·설치·학습자 코드 실행은 시작하지 않았다. 이는 현재 도구의 실제 읽기/판단이며 다른 AI 도구나 실제 학습자 수행의 검증은 아니다.

당시 T031에는 실제 검사·보존·필독 결과와 조회한 Run 상태를 기록했다. 그 호출 반환 전 Run은 `running / tasks`, 마지막 저장된 tasks 시도는 `Interrupted by user`였다. 당시의 문서 구현 체크를 공식 엔진의 tasks/implement 또는 Run 최종 완료로 보고하지 않았다. 상태 파일을 수동 변경하거나 도우미를 재귀 실행하지 않았고 STATE도 초기화하지 않았다. 이때의 31개 체크는 학습자 진도가 아니며 최신 작업 상태는 다음 절과 아래 체크를 따른다.

## 공식 implement 호출 반환 직전의 확인 — 과거 참고

이 절은 공식 implement 호출 반환 직전의 기록이다. 당시 같은 Run `17fc341e`의 specify·review-spec·plan·review-plan·tasks는 completed였고 저장된 단계는 `running / implement`였다. 기존 tasks를 재생성하거나 Run을 재귀 resume하지 않았다. 읽기 전용 analyze는 FR 34개·SC 10개와 작업 31개의 대응을 확인했고, 과거 Run 상태 표현과 현재 도구/타 도구 재개 검증의 구별을 MEDIUM 2건으로 보고했다. 실제 결과는 [quickstart 마지막 절](quickstart.md#최종-완료-확인--2026-10-19)에 둔다.

구현 의미 검토에서 주간 회상 후속을 공식 연습으로만 좁힌 옛 문구를 추가 발견했다. `USAGE.md`는 승인 프로젝트의 기존 작업 또는 이미 재선택한 공식 연습으로 수정했다. 같은 보완의 `.agents/skills/study-session/references/tutor-cases.md` 쓰기는 현재 환경의 읽기 전용 제한으로 거절됐다. 이번 호출에서는 해당 경로를 변경하지 않았고 검토용 패치는 `/tmp/llm-lab-tutor-cases-followup-17fc341e.patch`에 보존했다. 따라서 **당시 T013을 미완료로 되돌려 30/31 문서 작업만 확인했다.** 정적 검사 통과로 이 의미 불일치를 숨기거나 과거의 31/31을 이번 완료로 재사용하지 않는다. 당시 study-session의 실제 회상 절차는 이미 새 경로를 따랐고, 남은 항목은 tutor-cases의 기존 synthetic family 8 표현 한 곳이었다. 최종 반영은 위 최종 결과를 따른다.

## Format: `[ID] [P?] [Story] Description`

단일 작성자가 아래 순서로 수행한다. 병렬 작성 금지 요청에 따라 `[P]` 표시는 사용하지 않는다. 모든 task는 실제 증거 확인 후 `[X]`로 바꾸며 학습자 프로젝트 완료를 표시하는 표가 아니다.

## Phase 1: Setup — 승인·현재 경계 확인

- [x] T001 `scripts/speckit-workflow.sh status 17fc341e`, `.specify/extensions.yml`, `.specify/memory/constitution.md`, `specs/001-employment-project-curriculum/plan.md`로 동일 Run의 review-plan 통과·승인·hook·변경 범위를 확인한다 (FR-029~030).
- [x] T002 `.gitignore`, `pyproject.toml`, `uv.lock`의 기존 환경/ignore 경계와 예정 경로 충돌을 읽기 전용으로 확인한다. Docker/FastAPI/SQLite는 학습 후보일 뿐이며 `.dockerignore`·앱 설정·의존성을 추가하지 않는다 (FR-020·026·029).

## Phase 2: Foundational — 이행의 보존 전제

- [x] T003 `/tmp/llm-lab-curriculum-before-cr1mfa7m/snapshot.json`과 현재 트리·`STATE.md`·`CURRICULUM.md`를 비교해 보존 기준을 확인한다. data-model의 “기존 P0~P5, CC/SRC/MOD/MA/PC의 의미를 재사용하거나 새 단위를 옛 milestone 완료로 환산하지 않는다”와 기존 미완료/도움·헌법 변경을 유지한다 (FR-018·024).
- [x] T004 `practice/reviews/curriculum-transition.md`에 이행 직전 `STATE.md` 원문 전체를 ‘당시 북마크 인용·현재 재개 사용 금지’로 먼저 보존한다. 원문을 바꾸지 않고 상대 링크 원 목적지를 별도 표로 확인하며 “현재 지시/두 번째 STATE로 사용 금지; 기존 도움·미완료 그대로”를 지킨다. 북마크 변경은 T018까지 금지한다 (FR-018·022).

**Checkpoint**: 원문/링크/도움·미완료 보존 검증 후에만 활성 운영 문서를 이행한다.

## Phase 3: User Story 1 — 첫 작동 단위부터 근거를 쌓는다 (Priority: P1, MVP)

**Goal**: AX 한 서비스의 첫 기능·후속 연결·완료 경계를 찾는다. 대상 앱을 만들지 않는다.
**Independent Test**: AX-01 안내에서 최소 선수→직접 입력 처리→유용한 출력·사전 평가·실패 해석을 식별한다. AX 4단위 각각 열 개 요소와 근거/자료 연결이 있고 수학 완강/후속 심화 gate가 없다.

- [x] T005 [US1] `tests/test_simplified_study_contract.py`의 옛 foundations-first/Phase 고정 검사를 AX 4단위·10요소·첫 평가·예시 비고정 검사로 이행하고 변경 전 문서에서 실패를 확인한다 (FR-001~005·007·010, SC-001~002·009).
- [x] T006 [US1] `ROADMAP.md`에 기본 업무 문의 처리 보조 서비스와 AX-01~04의 “사용자 문제·구현 목적·이전/다음 연결·입출력·전체 흐름·학습자 직접 작업·관찰 결과·완료 기준·최소 선수·작업 중 보강 개념”을 계약 C2대로 반영한다. 사용자 예시를 필수 순서로 복원하지 않는다 (FR-001~005·007·019).
- [x] T007 [US1] `CURRICULUM.md` 1~3절을 AX 역량·최소 선수/사용처·관찰 공백·공식 자료 구간과 `research/decision-matrix.md` 근거 링크로 이행한다. 기존 4~8절 본문은 byte 단위로 유지하고 역사적 참고 경계를 그 앞에 표시한다 (FR-003~005·007·018·031~034).
- [x] T008 [US1] `ROADMAP.md`에 첫 평가의 독립 사례·중복/그룹·개발/최종 평가·지표·모델 선택, corpus 색인과 질의/qrels의 구별, 실제 도구 상태·품질/실패·재현·비용/지연 경계를 반영한다 (FR-010~012).

## Phase 4: User Story 2 — 맥락을 이해하고 직접 구현한다 (Priority: P1)

**Goal**: 튜터 준비·설명과 학습자 구현/실행/첫 해석의 책임을 유지한다.
**Independent Test**: 시작 안내·문서 도움·선수 공백·오류·준비 실패에서 허용 행동을 찾고 답안/골격·학습자 셀 실행·설치 책임 전가를 거부하는지 의미로 검토한다.

- [x] T009 [US2] `tests/test_simplified_study_contract.py`에서 준비/소유권·API 도움·nbpeek·실제 오류·무보조 회상·필독·12KiB/symlink 검사를 유지/이행하고 구형 경로의 충돌을 확인한다 (FR-013~017·023·025~027).
- [x] T010 [US2] `.agents/references/learning-policies.md`에 준비 상태 3종·정확한 원문·API 도움/대상 답안 경계·실제 근거·평가/기록/Git·공식 과제 판본/AI/private/환경·CS336 모든 명령/코드 제한을 보존해 배치한다. 자료 권리·유료/게시 권한을 확대하지 않는다 (FR-013~018·026~027).
- [x] T011 [US2] `AGENTS.md`를 12 KiB 이내로 이행하고 필독/핵심 소유권·공개·CS336·권한을 앞에 둔다. 상세는 `.agents/references/learning-policies.md`에 명시적 읽기 지시로 연결하고 `CLAUDE.md -> AGENTS.md`를 유지한다 (FR-021·023·027·029~030).
- [x] T012 [US2] `.agents/skills/study-session/SKILL.md`의 source 확인·10요소 맥락·허용 준비·작은 직접 작업·피드백/연속 진행·대표/지연 회상·조용한 STATE·종료 절차를 AX/RE로 이행한다. 전 과정/모든 API 암기·옛 필수 과제 gate는 제거하고 권한은 유지한다 (FR-013~017·021·023·025).
- [x] T013 [US2] `.agents/skills/study-session/agents/openai.yaml`과 `.agents/skills/study-session/references/tutor-cases.md`의 안내·대표 상황을 새 계약에 맞춘다. 모델/reasoning/전역 설정을 바꾸지 않고 정적/합성 검토와 실제 학습 결과를 구별한다 (FR-023·025).

## Phase 5: User Story 3 — 최소 지원 자료와 주장 한계 (Priority: P1)

**Goal**: AX-01의 조기 비교 자료와 AX-01~04 주 포트폴리오를 구별한다.
**Independent Test**: 후속 심화 없이 최소 여섯 항목을 찾고 성능 미개선/로컬 성공을 채용·공식 완료·실제 운영으로 확대하지 않는지 확인한다.

- [x] T014 [US3] `tests/test_simplified_study_contract.py`에 최소 산출물 6항목·미개선/미실행·지원 요건/운영 경계 검사를 반영한다 (FR-006·011~012, SC-003·006).
- [x] T015 [US3] `ROADMAP.md`에 “문제·직접 기능·평가/실패·재현 조건·기여/도움·주장 한계” 여섯 항목, AX-01 조기 비교와 AX-01~04 주 포트폴리오, 실제 JD 필수/우대·연차/학위 대조와 실패 해석 기준을 반영한다 (FR-006·011~012·031).
- [x] T016 [US3] `README.md`와 `USAGE.md`를 취업 우선·한 서비스·기준 문서 링크·시작/재개/종료·문서 도움·여섯 지원 설명의 요약으로 이행한다. 현재 진도/범위의 중복 권위를 만들지 않는다 (FR-001·006·021·023).

## Phase 6: User Story 4 — 보존과 단일 재개 (Priority: P1)

**Goal**: 과거 근거를 보존하고 새 대화에서도 현재 행동 하나로 재개한다.
**Independent Test**: transition 인용과 직전 STATE 전체가 같고 링크 원 목적지가 존재한다. 새 STATE는 AX/AX-01·다음 행동 하나이며 준비·실행을 완료했다고 기록하지 않는다.

- [x] T017 [US4] `tests/test_simplified_study_contract.py`에서 단일 STATE/다음 행동·과거 인용·권한·catalog/registry·기록 보존 검사를 이행한다. “점수·완료표·transcript·개인 경로·이력 없음”과 과거 ID/hash/판정 불변을 검사한다 (FR-018·021~024, SC-005·007).
- [x] T018 [US4] T004의 보존/링크 검증 후 `STATE.md`를 AX/AX-01로 이행한다. 다음 행동은 튜터 준비 문의 자료의 식별자·본문을 읽어 입력 계약을 확인하는 코드를 학습자가 직접 작성·실행하는 하나이며 미준비·모델 미실행·과거 미완료 보존 링크를 명시한다 (FR-015·020·022).
- [x] T019 [US4] `practice/README.md`와 `challenges/deep-ml/README.md`의 옛 순서·필수 재구현 트랙을 현재 경로의 자료/공백 참고로 바꾸고 예정 공개/private 공간의 비생성·권리·충돌 경계를 설명한다. 기존 개별 실습/풀이/회고는 수정하지 않는다 (FR-008~009·018~021·023).
- [x] T020 [US4] `.agents/skills/finish-chapter/SKILL.md`에 AX/RE 단위 완료만으로 챕터 마무리·기록·초기화·Git 권한이 생기지 않는 진입 조건만 보완한다. 실제 챕터 archive/노트북 byte 보존·학습자 초안·종료/커밋 권한은 유지한다 (FR-023).
- [x] T021 [US4] `AGENTS.md`→`.agents/skills/study-session/SKILL.md`→`.agents/references/learning-policies.md`를 현재 도구에서 실제로 열고 `STATE.md` 재개 행동 및 이동 링크/anchor를 대조한다. 새 컨텍스트/타 도구는 수행하지 않았다면 미검증으로 둔다 (FR-021~023·025).

## Phase 7: User Story 5 — 구체적인 장기 깊이와 옛 의무 재역할 (Priority: P2)

**Goal**: 장기 모델·LM·한 전문화·독립 실험의 선수/자료/직접 결과와 선택 근거를 남긴다.
**Independent Test**: RE 4범위 모두 목적/산출물/선수/자료/다음 진입 근거가 있다. research R6의 모든 옛 의무가 새 역할/이유/복귀 조건에 대응하고 AX/지원에 숨은 gate를 만들지 않는다.

- [x] T022 [US5] `tests/test_simplified_study_contract.py`의 고정 PS·시간표·대회·RE 이전 gate 검사를 RE 4범위·전문화/LM 대체 관계·R6 대응·판본/정책 보존 검사로 이행한다 (FR-008~009·027~028·031~034, SC-004·008~010).
- [x] T023 [US5] `ROADMAP.md`에 RE-01~04의 10요소·자료·진입 근거, post-training/evaluation 기본과 inference/systems 대안, 자체 LM/공식 A1 대체 관계를 반영한다. “전부 수행하는 병렬 과정이 아니다”를 유지하고 시간·합격·향상 보장을 만들지 않는다 (FR-001·008~009·027~028).
- [x] T024 [US5] `CURRICULUM.md`의 활성 1~3절에 RE의 모델/수학/통계·최적화·실험 선수와 실제 보강 사용처, 판본/접근 한계·근거 매핑을 연결한다. “새 앞부분이 현재 역량/자료 기준”이며 기존 4~8절의 역사적 필수/readiness는 현재 지시가 아니게 한다 (FR-007·018·028·031~034).
- [x] T025 [US5] `DEFERRED.md`를 research R6 및 decision-matrix의 전체 옛 의무·선택 해제·신규 보류의 범위/이유/관찰 가능한 복귀 조건으로 이행한다. “점수·날짜·완료표·자동 새 과정 시작 없음”을 지키고 공식 판본·Optional·비공개/환경/AI/명령 제한을 연결한다 (FR-008~009·026~028).

## Phase 8: Polish & Cross-Cutting Concerns

- [x] T026 `specs/001-employment-project-curriculum/tasks.md`의 checklist/ID/경로/US·의존성과 FR-001~034·SC-001~010 대응을 검증하고 같은 feature의 승인/설계 이력과 현재 구현 결과를 구별한다.
- [x] T027 `.agents/skills/study-session/references/tutor-cases.md`의 8개 대표 상황에서 실제로 검토한 허용 행동·학습자 직접 작업·주장 한계를 `specs/001-employment-project-curriculum/quickstart.md`에 기록한다. 합성 응답 의미 검토와 학습자 실행/새 컨텍스트/타 도구 필독을 구별한다 (FR-025, SC-006).
- [x] T028 `/tmp/llm-lab-curriculum-before-cr1mfa7m/snapshot.json`, `practice/reviews/curriculum-transition.md`, `CURRICULUM.md`와 Git diff로 보호 산출물 수정/삭제/이동 0건·옛 STATE 전체·역사적 4~8절·선행 헌법 변경·환경/ignore 경계를 확인한다 (FR-018·024·029, SC-005).
- [x] T029 lab 루트에서 `uv run --frozen pytest -q tests .agents/skills`를 실행해 관련 검사와 기존 archive/TIL/knowledge 도구 검사 통과를 확인한다. 공식 과제 저장소나 학습자 셀은 실행하지 않는다 (FR-024).
- [x] T030 lab 루트에서 `uv lock --check`, `git diff --check`, 운영 문서/feature의 로컬 링크·anchor·표·root 12KiB·`CLAUDE.md` symlink·필독/의미를 확인한다 (FR-021·023~024).
- [x] T031 `specs/001-employment-project-curriculum/quickstart.md`에 실제 task/검사/보존/대표 응답/필독 결과와 미검증 범위, Run 상태·Git/유료/외부 미실행을 남긴다. 근거가 확인된 문서 구현 task만 `specs/001-employment-project-curriculum/tasks.md`에서 완료로 표시한다 (FR-024~025·029~030).

## Dependencies & Execution Order

```text
Setup T001~002 → Foundational T003~004
  → US1 T005~008 → US2 T009~013 → US3 T014~016
  → US4 T017~021 → US5 T022~025 → Polish T026~031
```

US1의 첫 기능 계약이 이후 튜터/지원 안내의 기준이다. US2는 그 계약의 진행 방식, US3는 지원 설명의 경계이며 각각 독립 검토한다. US4의 원문 보존은 모든 변경 전 T004에서 끝내고 STATE 변경은 안내/권한 이행 후 T018에서만 한다. US5는 US1~4의 단기 진입 조건이 아니지만 이번 승인 범위에서 함께 구현한다. 각 story의 테스트를 문서보다 먼저 바꾸고 최종 전체 검사를 실행한다. 같은 ROADMAP/CURRICULUM/tests 파일의 작업은 반드시 직렬이다.

## Parallel Examples (이번 실행에서는 사용하지 않음)

사용자가 한 작성자를 지정했으므로 병렬 task·추가 에이전트는 **0개**다. 독립 검토 가능성만 구별한다.

| Story | 독립 검토 예 | 이번 실행 |
| --- | --- | --- |
| US1 | AX-01 입출력/완료와 AX-02 이후 개선 이유 | T005~008 순차 |
| US2 | API 도움과 준비 실패의 책임 | T009~013 순차 |
| US3 | 최소 6항목과 성능 미개선 해석 | T014~016 순차 |
| US4 | STATE 인용 동일성과 현재 행동 하나 | T017~021 순차 |
| US5 | RE 단계와 옛 의무/복귀 조건 | T022~025 순차 |

## Implementation Strategy

MVP는 Setup/Foundational+US1의 **문서 계약**이다. 첫 작동 단위의 목적/직접 작업/평가를 검토한 뒤 US2~5로 운영·지원·보존·장기 범위를 확장한다. 사용자가 전체 구현을 승인했으므로 MVP 확인 뒤 멈추거나 재승인을 요구하지 않는다. tasks 생성 뒤 공식 speckit-analyze의 읽기 전용 보고서를 먼저 출력하고, 승인된 범위의 누락/모순은 implement에서 보완한다. 앱 개발·실습 준비·실행·게시·커밋은 이 strategy의 배포 단계가 아니다.
