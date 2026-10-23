# 수업 운영 문서와 레포 스킬 정리 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task in the current session. Steps use checkbox (`- [ ]`) syntax for tracking. 사용자 요청으로 실행 방식을 바꾸지 않는 한 추가 에이전트나 다른 모델을 선택하지 않는다.

**Goal:** 개선한 기능 단위 수업에 맞춰 문서와 레포 스킬의 중복·과거 지시·잘못된 권한 안내를 정리하고, 실제로 필요한 정책을 해당 작업에서 읽을 수 있게 한다.

**Architecture:** STATE·ROADMAP·CURRICULUM·DEFERRED의 역할은 유지한다. AGENTS는 공통 경계와 진입점을, study-session은 수업 절차를, learning-policies는 공통 수업 판단을 맡고 공식 과제·기록 정책은 조건부 참고로 분리한다. 사용자 안내는 이 기준을 요약하고 현재 Python 실습의 진입점을 연결한다.

**Tech Stack:** Markdown, 기존 스킬 frontmatter와 `agents/openai.yaml`, Python 3.14, uv, pytest. 새 런타임 의존성이나 학습 관리 도구는 추가하지 않는다.

**Spec:** [채택한 수업 개선 설계](../../../specs/002-learning-method-audit/tutoring-redesign-2026-10-23.md), [현재 저장소 지침](../../../AGENTS.md), 이번 사용자의 문서 전수 검사·레포 전용 스킬 포함 요청.

**상태:** 계획 검토 대기. 아래 구현 체크박스는 아직 수행 완료가 아니다. 기본 실행 방식은 현재 세션의 `executing-plans`이며, 이 계획 작성은 커밋·푸시·학습 재개를 포함하지 않는다.

## Global Constraints

설계의 다음 문장을 그대로 유지할 계약으로 삼는다.

- “기존 코드·가상 원자료·실행 로그·노트북·과거 도움 이력은 보존한다.”
- “모든 파일에 같은 긴 규칙을 복제하지 않는다.”
- “강의 구간은 제목만 골라 산발적으로 인용하지 않는다.”
- “영상 시청 수, 테스트 개수, 생성된 코드 줄 수, 동의·완료 응답을 학습 점수로 쓰지 않는다.”

추가로 현재 프로젝트 경계를 보존한다.

- STATE의 AX-03·학습 중지·다음 초안 미리보기 연결 행동은 변경하지 않는다.
- `CLAUDE.md -> AGENTS.md` symlink를 유지한다. 범용 스킬의 symlink 제거 권고를 적용하지 않는다.
- 학습자 구현·실행·첫 해석, 현재 자체 프로젝트 위임, 공식 과제·무보조 확인을 구별한다. 문서 정리로 도움·독립 숙달을 승격하지 않는다.
- CS336의 AI 명령 실행·code/pseudocode/patch/TODO 답안 제한과 별도 환경을 유지한다. 과제 저장소에서 명령을 실행하지 않는다.
- A1 pin `a158843b20107949f1a8d7df1b05cd33b9166712`, A2 pin `ca8bc81a59b70516f7ebb2da4808daade877c736`, 공식 판본·저자원·Optional/Bonus 경계를 옮기되 바꾸지 않는다.
- Zoomcamp 기준 revision `1c42efbeb8141c183e7ae51698ad912c70c06a06`, 주교재·보조·조건부 선택과 AX/RE 범위를 유지한다. 새 강의·새 필수 과제는 선택하지 않는다.
- 기존 학습 기록·archive·퇴역 자산은 보존한다. `web/`·사내비·private 자료·학습 코드를 수정하거나 학습자 노트북을 실행하지 않는다.
- 실제 챕터 마무리의 보관·초안·초기화 선행 조건과 로컬 커밋 권한, 명시적 학습 종료의 제한된 commit+push, 단독 기록의 편집 권한을 섞지 않는다.

## Review Focus

자동 검사로 튜터의 의미 판단을 입증하지 않는다. 아래 다섯 조건을 해당 Task의 검사 또는 작성자 시나리오 검토에 연결한다.

1. **평범한 AX 재개:** 현재 기능의 설명·구현으로 연결하며 보류 과정·기록 정책 전체를 새 필독으로 만들지 않는다. Task 1·2의 필독 경로 검토.
2. **현재 코드 위임 / 공식 과제 / 무보조 확인:** 세 요청의 허용 행동이 다르며 단순 위임을 재승인하거나 무보조 성공으로 포장하지 않는다. Task 1·2의 세 갈래 의미 검토.
3. **`완료` / 학습 종료 / 실제 챕터 전환 / 단독 기록:** 초기화·기록·Git 권한을 서로 넘겨받지 않는다. Task 2의 호출 설정·기존 보관 안전성 검사.
4. **과거 명세·예시 링크·옮긴 정책 anchor:** 과거 지시가 현재 규칙이 되지 않고 기존 공개 링크는 계속 찾을 수 있어야 한다. Task 4·5의 역사 경계·링크 검사.
5. **로컬에만 있는 자료와 녹색 검사:** 공개 사본에서도 문서 연결이 유효해야 하며 정적 통과를 모델 준수·학습 효과로 보고하지 않는다. Task 3·5의 자료 없는 사본·증거 구분.

---

## 조사 기준과 확인한 문제

기준 커밋은 `fb71cfd`다. 계획 작성 전 작업 트리는 깨끗했고 `uv run --frozen pytest -q tests .agents/skills`는 **104 passed**, `uv lock --check`와 `git diff --check`는 정상 종료했다.

추적 문서 165개를 목록·역할로 검사했다. 운영·안내 후보 25개에는 CLAUDE symlink가 포함된다. 나머지는 명세·근거 35개, 학습 기록 71개, archive 18개, 퇴역 참고 15개, 사이트 안내 1개다. 사이트는 범위에서 제외했고 보존 자료는 경로·역할·링크를 검사했다. 학습 노트 전체의 과학적 정확성이나 외부 강의 전체를 재검증했다는 뜻은 아니다.

운영·안내 후보의 로컬 파일 링크 231개에는 누락이 없었다. archive의 `../relative/path.md` 한 건은 예시 placeholder로 확인했으며 과거 원본을 고쳐 현재 문서의 결함처럼 처리하지 않는다. Anchor 검사는 Task 5에서 보강한다.

| 문제 | 현재 근거 | 결정 |
| --- | --- | --- |
| 필독의 실제 범위가 과도함 | AGENTS 11,117B + study-session 20,637B + learning-policies 36,989B = 68,743B. 공통 정책 안에 공식 과제·기록 상세가 함께 있음 | 공통 필독과 활동별 정책 분리. 줄 수·byte 감소는 문서 지표로만 보고 |
| 현재 정책이 퇴역 헌법을 승인 근거로 인용함 | learning-policies의 소유권 절에 “헌법 Governance”·“헌법 변경” 설명이 남아 있음 | 현재 사용자 요청·AGENTS를 기준으로 설명하고 역사 자료는 참고로만 연결 |
| 자동 기록처럼 읽히는 안내 | materials/README 마지막 문장은 공부한 날의 기록을 TIL에 남기도록 안내 | 명시적으로 요청한 기록만 작성한다는 현재 정책으로 수정 |
| 현재 Python 실습 진입 안내가 없음 | README·USAGE·practice/README에 `ai-apps`·`inquiry` 연결이 없고 피드백 예시는 notebook 중심 | 현재 실습 안내 추가, notebook 안내는 선택 사용 맥락으로 배치 |
| 모델 변경 권한이 불명확함 | USAGE의 모델·reasoning을 난도/품질로 “조정”한다는 설명 | 사용자 설정·기존 허용 범위 안에서 선택한다는 의미로 명확화 |
| 검증 지침에 당시 작업의 권한·미실행 상태가 고정됨 | tutor-cases의 “No model/API call … is authorized”, “현재는 미수행”; 이를 고정하는 계약 검사 | 현재 검증 프로토콜과 날짜가 있는 과거 결과를 구분. 허가·금지를 fixture가 새로 정하지 않도록 수정 |
| 옛 registry 관리 규칙의 적용 범위가 넓음 | CURRICULUM §9가 자료 변경 때 옛 ID/module/milestone 배정을 다시 요구할 수 있음 | 기존 역사 registry를 실제로 유지보수할 때만 적용. 현재 새 자료 등록의 일반 의무로 쓰지 않음 |

## 파일별 처리와 책임

| 파일·묶음 | 처리 | 책임 / 보존 범위 |
| --- | --- | --- |
| `AGENTS.md` | 정리 | 공통 안전·소유권·북마크·검증 명령·작업별 진입점 |
| `CLAUDE.md`, `STATE.md` | 유지 | symlink와 현재 재개 내용을 보존 |
| `.agents/references/learning-policies.md` | 정리 | 공통 수업 판단과 짧은 호환 링크 |
| `.agents/references/official-course-policies.md` | 생성 | 선택된 공식 과제의 판본·도움·공개·환경·자원 제한 |
| `.agents/references/recordkeeping-policies.md` | 생성 | 단독 기록·챕터 마무리·종료의 권한 구분; 절차는 해당 스킬로 연결 |
| `.agents/skills/study-session/SKILL.md` | 정리 | 설명→작성→실행→첫 해석→피드백, 충분한 답 수용·필요한 지원·종료 |
| `.agents/skills/study-session/agents/openai.yaml` | 점검·의미 유지 | 학습/회상 진입 안내와 implicit 호출 설정 |
| `.agents/skills/study-session/references/tutor-cases.md` | 정리 | 재사용 가능한 평가 상황·기대 행동·증거 한계 |
| `.agents/skills/finish-chapter/SKILL.md`, `agents/openai.yaml` | 정리 | 새 정책 링크·검증된 보관/초기화 조건. 단위 완료·일반 완료로 호출 범위를 확대하지 않음 |
| `.agents/skills/finish-chapter/references/chapter-review.md` | 점검·유지 | 실제 초안·보관본·도움·미확인에 근거한 회고 |
| `.agents/skills/save-today-til/SKILL.md`, `agents/openai.yaml` | 점검·정합화 | 별도 명시 호출, 지정 근거, 편집만 허용; implicit=false 유지 |
| `.agents/skills/update-learning-knowledge/SKILL.md`, `agents/openai.yaml` | 점검·정합화 | 별도 명시 호출, 해당 스킬의 0~3/NO_CHANGE, 편집만 허용; implicit=false 유지 |
| 위 스킬의 `scripts/`·`tests/` | 검토·기존 검사 실행 | 문서의 명령/인자/효과를 실제 helper와 대조. 기존 학습 대상이나 보관 코드를 정리 편의로 고치지 않음 |
| `README.md`, `USAGE.md` | 정리 | 사용자 시작·재개·도움 요청·기존 환경 사용 안내; 상세 정책 반복 축소 |
| `practice/README.md` | 정리 | 현재 프로젝트와 보관 산출물의 안내. 기존 보관 목록 보존 |
| `practice/ai-apps/README.md` | 생성 | 이미 구현된 파일·CLI·비공개 입력 필요·실행 한계 |
| `materials/README.md` | 수정 | 원자료 보관·준비 안내; 자동 TIL 문구 교정 |
| `challenges/README.md`, `challenges/deep-ml/README.md` | 정리 | 선택적 연습·실제 결과와 이해 구분. 옛 readiness 용어·무조건 공개 가능 문구 정리 |
| `ROADMAP.md`, `DEFERRED.md` | 필요한 연결만 수정 | 기존 단위 계약·제외/복귀 조건 유지, 옮긴 정책 링크 정합화 |
| `CURRICULUM.md` | 필요한 연결·§9 경계 수정 | 주교재 선택·1~3절 역할 유지, 역사적 4~8절 본문 byte 보존 |
| `knowledge/README.md`, `knowledge/template.md`, `til/README.md`, `til/template.md` | 점검·유지 | 기존 작성 규칙·개념 목록·명시 요청 원칙은 유효. 학습 내용을 새로 쓰지 않음 |
| `.specify/README.md` | 점검·유지 | 이미 존재하는 퇴역 안내를 재사용 |
| `.specify/memory/constitution.md` | 역사 안내만 추가 | 원래 비준·판본·본문은 보존, 현재 작업을 통제하는 헌법으로 사용하지 않음 |
| `specs/`의 과거 명세·계획·quickstart·근거 | 역할·연결 검사, 원문 유지 | 과거 승인·측정·실행을 현재 결과로 다시 쓰지 않음. 2026-10-23 설계는 이번 변경의 근거 |
| `.specify/retired/`, `archive/`, 개별 knowledge/TIL/회고 | 보존 | 퇴역 스킬 10개와 템플릿 5개도 활성 호출과 분리됐는지 검사 |

## Task 1: 공통 필독과 활동별 정책의 기준 위치 정리

**Files:** Modify `AGENTS.md`, `.agents/references/learning-policies.md`, `tests/test_simplified_study_contract.py`; Create `.agents/references/official-course-policies.md`, `.agents/references/recordkeeping-policies.md`.

**Interfaces:**
- Consumes: 현재 AGENTS 경계와 learning-policies의 `Course-specific scope and assistance`, `TIL, knowledge, practice, and sources` 구간.
- Produces: 공식 과제 정책의 세 heading `Course-specific scope and assistance`, `Official low-resource and resource boundaries`, `CS336 return and boundaries`; 기록 정책의 `Default chapter-transition wrap-up`, `Standalone writing and sources`.
- Produces: `_contract() -> str`는 AGENTS·공통·공식 과제·기록 정책의 계약을 검토하는 테스트 helper다. 이 합본을 수업의 필독 목록이나 실행 로더로 사용하지 않는다.

- [x] **Step 1:** 원본·작업 트리와 문서별 기준 위치를 임시 작업 공간에 저장한다. `STATE.md`와 보존 대상의 원본 비교 기준도 잡는다. AGENTS의 12항목 triage에서 실제 결함과 최소 diff를 제시하고, 동일 기준으로 수정 후 대조한다. 이 자료를 새 학습 기록으로 공개하지 않는다.
- [x] **Step 2:** 공식 과제 절을 새 정책으로 옮긴다. 판본·두 pin·공개 제한·CS336 명령 정책·공식 저자원/임의 축소/미완료 구분을 유지한다. 기록 절은 권한 구분으로 정리하고 상세 작업 순서를 finish-chapter와 개별 기록 스킬에 중복하지 않는다.
- [x] **Step 3:** 기존 공통 정책의 `course-specific-scope-and-assistance`, `cs336-return-and-boundaries` anchor를 짧은 이동 안내로 유지한다. 옛 링크가 새 정책을 찾게 하며 긴 본문을 두 곳에 복제하지 않는다. 다른 실제 사용 anchor도 이전 전 검색한다.
- [x] **Step 4:** AGENTS의 일반 학습 필독은 현재 북마크·학습 스킬·공통 정책·현재 단위/필요 자료로, 공식 과제와 기록 정책은 해당 활동 때 직접 읽도록 명시한다. 모든 작업의 핵심 소유권·private·CS336·노트북·Git 경계는 루트에 남긴다. 퇴역 헌법을 현재 위임 권한의 근거로 쓰는 문장을 제거한다.
- [x] **Step 5:** `_contract()`의 원본 경로를 분리된 정책까지 명시적으로 포함하도록 바꾸고, `_contract`가 모든 파일의 상시 필독을 뜻한다는 주석은 고친다. 기존 안전 계약을 삭제하지 않는다.
- [x] **Step 6:** `uv run --frozen pytest -q tests/test_simplified_study_contract.py` 실행. 통과 후 Review Focus 1·2를 문서 의미로 대조한다. 일반 AX가 공식 과제 전체를 읽도록 요구하지 않고, 세 도움 모드의 제한을 유지해야 한다.

## Task 2: 레포 스킬 네 개의 진입·절차·효과 대조

**Files:** Modify Task 1 표에 명시한 네 `SKILL.md`와 필요한 `agents/openai.yaml`; Inspect 각 `references/`, `scripts/`, `tests/`; Modify 관련 계약 검사만 `tests/test_simplified_study_contract.py`에서 정합화.

**Interfaces:**
- Consumes: Task 1의 공통·공식 과제·기록 정책과 STATE.
- Produces: 같은 호출 이름과 권한을 유지하는 네 스킬. `study-session`·`finish-chapter` implicit=true, 두 standalone utility implicit=false를 유지한다.
- Produces: archive helper의 `--source`, `--archive`, `--expected-sha256`, `--reset` 계약과 기존 validator 명령은 변경하지 않는다.

- [x] **Step 1:** 각 frontmatter의 이름·호출 조건, YAML의 안내·implicit 설정, 본문의 실제 효과, 링크/명령을 한 묶음으로 대조한다. 자동 발견과 파일 존재를 실제 스킬 로딩의 증거로 세지 않는다.
- [x] **Step 2:** study-session은 현재 요청 분기와 기능 단위 절차를 중심으로 정리한다. 공통 정책과 같은 긴 도움/평가 설명은 링크로 통합한다. 충분한 답·한 번의 동일 취지 후속 질문·JS→Python 보강·실제 결과 피드백·pause 경계를 유지한다.
- [x] **Step 3:** finish-chapter의 새 정책 링크와 당시 개편만을 가리키는 문구를 정리한다. YAML 안내도 확인된 범위·초안·보관 검증 후의 초기화를 표현하게 한다. 학습자 대화 초안을 재사용하며 새 형식의 초안 재제출을 의무화하지 않는다. 보관·초안이 없으면 knowledge 작성/초기화를 대신하지 않는다.
- [x] **Step 4:** 두 standalone 스킬의 명시 호출·입력·편집 한계를 유지하고 필요한 정책 연결만 수정한다. 0~3 제한을 일반 수업이나 챕터 전체에 퍼뜨리지 않는다. 정상인 메타데이터는 그대로 둔다.
- [x] **Step 5:** 작성자 시나리오로 `일반 시작`, `충분한 답`, `현재 수정 위임`, `검토 중지`, `완료`, `명시 종료`, `실제 챕터 전환`, `standalone 호출`을 대조한다. 각각의 학습/기록/초기화/Git 효과가 승인 범위를 넘지 않아야 한다. 이는 작성자 검토이며 독립 모델 응답 검증이 아니다.
- [x] **Step 6:** `uv run --frozen pytest -q tests .agents/skills` 실행. 보관 digest 불일치·기존 목적지 충돌·원본 보존, TIL/knowledge 링크·provenance 검사가 통과해야 한다. 학습자 노트북이나 private 과제에 helper를 실행하지 않는다.

## Task 3: 현재 실습 안내와 하위 문서의 불필요한 의무 교정

**Files:** Modify `README.md`, `USAGE.md`, `practice/README.md`, `materials/README.md`, `challenges/README.md`, `challenges/deep-ml/README.md`, 필요한 정책 연결의 `ROADMAP.md`·`DEFERRED.md`; Create `practice/ai-apps/README.md`.

**Interfaces:**
- Consumes: Task 1·2의 기준 문서와 이미 저장된 `practice/ai-apps/` 코드.
- Produces: 현재 CLI의 `--all`, `--id`, `--history`, `--latest`, `--search`, `--account-status`, 선택 인자 설명. 존재하지 않는 초안 연결 옵션·실제 접수 기능은 완료로 안내하지 않는다.
- Produces: 사용자 시작/도움 안내는 USAGE, 현재 실습 실행/파일 안내는 ai-apps README. 보관 실습과 개념 목록은 기존 인덱스에 보존한다.

- [x] **Step 1:** 새 실습 안내에 실제 파일 책임·입력→조회/검색→모델/검사→기록 흐름을 설명한다. 비공개 입력이 clone에 없고 모델 준비가 별도라는 실행 조건을 명확히 한다. 새 학습 데이터·정답·target skeleton을 작성하지 않는다.
- [x] **Step 2:** README는 목적·짧은 시작·안내 링크, USAGE는 사용자 행동을 중심으로 정리한다. 현재 Python 실습을 먼저 연결하고 notebook 전용 예시는 해당 사용 상황으로 구분한다. 같은 소유권·과정 제한·평가 설명을 여러 번 복제하지 않는다.
- [x] **Step 3:** materials의 자동 TIL 문구를 명시 요청 원칙으로 고친다. challenge 안내의 `target/prerequisite satisfied` 같은 옛 상태 용어는 실제 수행·도움·미확인 설명으로 바꾼다. 풀이 파일의 공개 가능성을 무조건 보장하지 않고 실제 권리·정책 확인 경계를 남긴다. 참여·제출은 실행하지 않는다.
- [x] **Step 4:** 모델·reasoning 조정 안내를 사용자 설정·허용 범위에 맞게 고친다. 수업 진행을 위한 고정 주간 시점·추가 기록 양식으로 오인될 표현은 요청 시 동작으로 명확히 한다. 이미 승인된 회상 범위나 스킬 권한 자체는 바꾸지 않는다.
- [x] **Step 5:** 아래 두 명령을 lab 루트에서 실행해 정상 종료·문서와 실제 옵션 일치를 확인한다. 모델 생성 요청과 기존 실행 로그 추가는 하지 않는다.

```bash
uv run --frozen python practice/ai-apps/inquiry_assistant.py --help
uv run --frozen python practice/ai-apps/evaluate_retrieval.py --help
```

- [x] **Step 6:** 현재 AX-03가 기존 조회값으로 초안 미리보기를 연결할 단계라는 점, helper와 agent·초안과 실제 접수의 차이를 대조한다. 정상·미요청·조회값 부재를 한 기능에서 관찰한다는 설계는 유지한다. 학습자에게 새 과제나 중복 질문을 제시하지 않는다.

## Task 4: 역사 자료와 검증 프로토콜의 현재 권한 분리

**Files:** Modify `CURRICULUM.md:341`, `.specify/memory/constitution.md`, `.agents/skills/study-session/references/tutor-cases.md`, `tests/test_simplified_study_contract.py`; Inspect `.specify/README.md`, `specs/`, `.specify/retired/`.

**Interfaces:**
- Consumes: 현재 권한은 사용자 요청·AGENTS·활동별 스킬이 정하며 과거 자료는 그 당시 근거라는 계약.
- Produces: 과거 판본·비준·승인·미실행 결과를 보존하면서 현재 동작과 구분하는 안내. 새 모델/API/에이전트 권한은 생성하지 않는다.

- [x] **Step 1:** 헌법에 역사 자료임을 알리는 짧은 앞말과 현재 지침 링크만 추가한다. 원래 본문·비준일·버전을 바꾸거나 새 헌법 승인 절차를 만들지 않는다. 이미 과거 참고를 명시한 quickstart·퇴역 README에는 같은 긴 안내를 반복 추가하지 않는다.
- [x] **Step 2:** CURRICULUM §9의 적용을 기존 registry의 명시적 유지보수로 한정한다. 새 현재 자료 등록에 옛 module/milestone 체계를 강제하지 않는다. §4~8과 보관된 ID/hash·감사 판정은 그대로 보존한다.
- [x] **Step 3:** tutor-cases의 당시 문서 작업 한정 허가/금지를 현재 일반 검증 규칙에서 분리한다. 허용된 방식·비용·도구 범위는 실제 요청에서 판단하고 fixture가 새로 허가하거나 금지하지 않게 한다. 과거 작성 응답·미실행 상태는 날짜가 있는 근거 문서를 참조한다.
- [x] **Step 4:** `test_validation_boundaries_cover_the_eight_cases_without_claiming_learning_effects`에서 “현재는 미수행”, “모델 실행 의무가 없다” 같은 과거 상태 문구를 영구 요구하는 부분을 정리한다. B1~B8의 평가 상황·기준과 정적/작성자/실제 모델/학습자 증거 구분은 유지한다. 다른 동의어를 새 정답 문구로 고정하지 않는다.
- [x] **Step 5:** 활성 스킬 목록에 퇴역 speckit 스킬이나 사라진 runner를 복원하는 연결이 없는지 검사한다. 퇴역 파일을 호출·설치·이동하거나 과거 검증 결과를 새 성공으로 변경하지 않는다.

## Task 5: 링크·보존·공개 사본 검사와 최종 의미 검토

**Files:** Modify `tests/test_simplified_study_contract.py`; Verify 위 처리 표의 문서·메타데이터·기존 스킬 검사. 별도 문서 파서 패키지·명령 선택기·진도 DB는 만들지 않는다.

**Interfaces:**
- Consumes: Task 1~4의 문서·상대 링크·이전 anchor와 기존 `validate_knowledge.py`의 `extract_link_targets(line: str) -> list[str]`.
- Produces: 테스트 내부 `_doc_link_errors(path: Path) -> list[str]`. 실제 로컬 파일/heading 누락을 보고하며 외부 URL·fenced 예시·template placeholder를 실행 지시로 처리하지 않는다.
- Produces: `OPERATING_DOCS: tuple[str, ...]`는 위 처리 표의 운영·안내 Markdown 경로와 새 정책 두 개·실습 README를 열거한다. CLAUDE 별칭·개별 학습 기록·archive·과거 specs·퇴역 원본·web은 제외한다. `test_operating_doc_links_resolve`가 각 경로에서 `_doc_link_errors`의 빈 결과를 요구한다.

- [x] **Step 1:** 다음 상수와 링크 검사 테스트를 먼저 추가한다. 오류 문자열은 실패한 실제 target을 포함한다.

```python
OPERATING_DOCS = (
    "AGENTS.md", "STATE.md", "README.md", "USAGE.md",
    "ROADMAP.md", "CURRICULUM.md", "DEFERRED.md",
    ".agents/references/learning-policies.md",
    ".agents/references/official-course-policies.md",
    ".agents/references/recordkeeping-policies.md",
    ".agents/skills/study-session/SKILL.md",
    ".agents/skills/study-session/references/tutor-cases.md",
    ".agents/skills/finish-chapter/SKILL.md",
    ".agents/skills/finish-chapter/references/chapter-review.md",
    ".agents/skills/save-today-til/SKILL.md",
    ".agents/skills/update-learning-knowledge/SKILL.md",
    ".specify/README.md", ".specify/memory/constitution.md",
    "practice/README.md", "practice/ai-apps/README.md",
    "materials/README.md", "challenges/README.md",
    "challenges/deep-ml/README.md", "knowledge/README.md",
    "knowledge/template.md", "til/README.md", "til/template.md",
)


def test_doc_link_errors_handle_real_and_example_targets(tmp_path: Path) -> None:
    target = tmp_path / "참고 문서(1).md"
    target.write_text("## 절 하나\n", encoding="utf-8")
    page = tmp_path / "guide.md"
    page.write_text(
        "[정상](<참고 문서(1).md#절-하나>)\n\n"
        "```md\n[예시](missing-example.md)\n```\n",
        encoding="utf-8",
    )
    assert _doc_link_errors(page) == []
    page.write_text("[누락](missing.md)\n", encoding="utf-8")
    assert any("missing.md" in error for error in _doc_link_errors(page))
    page.write_text("[없는 절](<참고 문서(1).md#없는-절>)\n", encoding="utf-8")
    assert any("없는-절" in error for error in _doc_link_errors(page))


@pytest.mark.parametrize("relative", OPERATING_DOCS)
def test_operating_doc_links_resolve(relative: str) -> None:
    assert _doc_link_errors(REPO / relative) == []
```

Run: `uv run --frozen pytest -q tests/test_simplified_study_contract.py::test_doc_link_errors_handle_real_and_example_targets`. 처음에는 helper 미구현으로 FAIL, Step 2 뒤에는 PASS를 확인한다.
- [x] **Step 2:** 기존 링크 추출 함수를 재사용해 검사 helper를 작성하고 위 테스트를 통과시킨다. 운영 문서·스킬·메타데이터 참조를 검사하되 archive의 과거 예시나 learner 기록 전체를 새 형식으로 강제하지 않는다. 옮긴 정책의 호환 anchor도 검사한다.
- [x] **Step 3:** 기존 안전/구조 검사를 유지하며 의도적으로 바꾼 필독 위치·중복 표현 요구만 정합화한다. 문구 일치를 튜터 행동 증명으로 부르는 테스트는 만들지 않는다. 변경한 각 기존 검사는 유지한 계약과 바뀐 위치를 설명할 수 있어야 한다.
- [x] **Step 4:** 아래 필수 검사를 실행한다. 모두 정상 종료해야 하며 테스트 개수는 실행 결과대로 보고한다.

```bash
uv run --frozen pytest -q tests .agents/skills
uv lock --check
git diff --check
```

- [x] **Step 5:** HEAD와 이번 허용 변경만으로 저장소 밖 사본을 만들고 같은 검사를 실행한다. private 자료·로컬 로그가 없어도 링크/테스트가 성립해야 한다. learner 코드·새 데이터·원본 스크립트를 대행 실행하지 않는다.
- [x] **Step 6:** 원본 비교로 STATE·개별 학습 기록·보관 파일·학습 코드·역사적 CURRICULUM 본문·퇴역 자산의 보존을 확인한다. 네 스킬의 본문·호출 설정·참조·helper 효과를 다시 맞춰 읽는다. Claude 등 다른 실행기의 실제 자동 로딩까지 확인하지 않았다면 미검증으로 보고한다.
- [x] **Step 7:** 문서 전수 목록의 처리 결과, 수정 이유, 필독 경로의 실제 분량 변화, 수행 검사와 남은 모델/학습 효과 검증을 구분해 보고한다. 이 계획의 체크박스는 문서 작업 확인용이며 학습자의 진도표로 쓰지 않는다. 커밋·푸시는 별도 현재 요청이 있을 때 정확한 허용 경로로 수행한다.

## Self-review and execution handoff

- 설계의 자료 선택·기능 경계·수업 흐름·도움·충분성·평가·기록/보존을 Task 1~5에 대응시켰다. 새 커리큘럼·강의 선택·학습 코드 구현은 포함하지 않는다.
- 두 조건부 정책의 경로·heading과 테스트 helper 인터페이스를 고정했고, 기존 링크 호환과 실제 공개 사본 누락을 확인 항목에 넣었다.
- 문서 변경은 확인한 문제→수정→기존 검사/링크→의미 검토로 진행한다. TDD는 새 기계적 링크 검사에 적용하며 수업 효과를 확인하기 위한 문구 테스트나 가짜 실패를 만들지 않는다.
- 네 레포 스킬은 본문·호출 조건·메타데이터·참고·스크립트/기존 테스트를 함께 검수한다. 정상인 호출 권한을 일괄 재설정하지 않는다.
- 계획 검토 후 기본 방식인 현재 세션의 `executing-plans`로 진행한다. 실행 방식 선택을 다시 요구하지 않으며 추가 모델·하위 에이전트·Git 작업은 이 계획으로 자동 승인되지 않는다.
