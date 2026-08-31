# 사용법

## 새 Codex 대화에서 시작하기

이 저장소를 작업 공간으로 연 Codex는 루트 [`AGENTS.md`](./AGENTS.md)와
`.agents/skills/`의 repository skill을 읽습니다. 보통은 target ID나
`$skill-name`을 직접 입력하지 않아도 됩니다. 다른 저장소나 작업
디렉터리에서 연 대화에는 이 프로젝트의 흐름이 적용되지 않습니다.

### 하루 전체 흐름 시작

```text
오늘 전체 학습 흐름 시작
```

`전체 학습 흐름 시작`도 같습니다. 이 요청은 Asia/Seoul 기준 오늘
동안 여러 cycle과 새 Codex 대화에 걸쳐 다음 순서를 계속할 권한을
부여합니다.

1. 실제 다음 target과 자료를 정합니다.
2. 선택한 source slice를 검토하고 60~90분 표준 수업을 구성합니다.
3. 대화형으로 배우고 학습자의 확인된 답변을 cursor에 보존합니다.
4. target에 맞는 실습 또는 exact milestone deferral을 정합니다.
5. 실습이면 학습자가 직접 구현·실행·해석하고, 확인된 근거로 knowledge를
   0~3개 갱신합니다.
6. deferral이면 cycle을 `milestone-pending`으로 보존하고 실습·knowledge를
   완료로 꾸미지 않은 채 다음 target으로 이동합니다.
7. 다음 target을 계산하고 다음 reviewed lesson의 첫 teaching move를
   준비합니다.

이 권한에는 완료 준비를 통과한 exact practice와 evidence-backed
knowledge의 path-limited commit이 포함됩니다. 다음은 포함되지 않습니다.

- TIL 자동 저장
- push
- permanent source 등록
- 유료·로그인 자료 다운로드
- 외부 계정 접근, 대회 참여 또는 제출
- 학습자 대신 답하거나 learner-owned practice를 구현하는 일

날짜가 바뀌면 commit 권한은 만료됩니다. 미완료 cycle과 아직 TIL에
기록되지 않은 완료 cycle은 삭제되지 않습니다. 새 날짜에 같은 전체
흐름 문장을 말하면 미완료 cycle을 다시 활성화합니다.

### 정확한 phase 재개

```text
계속
```

`tmp/active-learning-flow.json`의 정확한 phase를 재개합니다.

| phase | 이어지는 작업 |
|---|---|
| `SELECT_TARGET` | 다음 primary target 결정 |
| `PREPARE_LESSON` | source 해결, handoff 작성·독립 검토·repair |
| `TEACH` | 현재 teaching step에서 수업 재개 |
| `DECIDE_PRACTICE` | practice action·modality·progression layer 결정 |
| `AWAIT_PRACTICE` | exact Notebook 또는 challenge 시도 재개 |
| `UPDATE_KNOWLEDGE` | terminal practice 근거로 knowledge 갱신 |
| `PLAN_NEXT` | 다음 target 계산 |
| `PAUSED` | 저장된 resume phase로 복귀 |

같은 target/source의 locator, 문구, objective mapping, module, teaching
order 문제는 Agent가 같은 흐름에서 고치고 targeted recheck합니다.
Source 손상·접근 실패, 해결 불가능한 사실 모호성, 사용자 범위 선택만
실제 blocker입니다. 특수 reset 문구를 다시 입력할 필요가 없습니다.

### 안전하게 멈추기

```text
오늘 학습 종료
```

현재 cycle과 정확한 resume phase를 보존하고 오늘 권한을 종료합니다.
TIL을 만들거나 불확실한 개념을 완료 처리하지 않습니다.

### 한 수업만 진행

```text
오늘 학습 시작
```

Target·자료 결정과 reviewed lesson까지만 진행합니다. Practice,
knowledge, TIL은 자동 실행하지 않습니다. 한 수업이 끝나면 session을
capture하고 멈춥니다.

### 오늘 TIL 명시적으로 저장

```text
오늘 TIL 저장해줘
```

완료됐지만 아직 기록되지 않은 cycle만 날짜별 TIL에 반영합니다.
미완료·paused cycle은 제외합니다. 같은 날 여러 번 요청하면 이전 기록을
보존하면서 새로 완료된 cycle만 소비합니다. 이전 날짜에 완료된 pending
cycle은 그 cycle의 완료 날짜 TIL로 저장합니다.

### 계획만 읽기

```text
현재 학습 근거를 확인해서 다음에 무엇을 공부할지 정해줘.
```

Read-only planner만 사용합니다. 파일을 수정하거나 수업·캐시·실습을
시작하지 않습니다.

## 운영 cursor와 영구 근거

`tmp/active-learning-flow.json`은 원자적으로 갱신되는 단일 ignored
cursor입니다. 날짜, 승인 모드, phase, exact handoff/practice, cycle별
confirmed learner evidence와 hash, exact learning commit만 보존합니다.
명시적으로 다시 시작한 cycle은 `superseded`로 보존되고, 여러 수업의
근거를 누적하는 cycle은 `milestone-pending`으로 남을 수 있습니다. 둘 다
완료나 mastery로 계산되지 않습니다.
별도 snapshot, 진행률, mastery DB가 아닙니다.

| 파일 | 역할 |
|---|---|
| `tmp/active-learning-flow.json` | 같은 장치·저장소에서 day flow 재개 |
| `tmp/active-lesson-handoff.md` | 한 reviewed lesson의 계약·전달·답변 |
| `tmp/active-lesson-sources/<lesson-id>/` | 한 lesson의 임시 official source cache |
| `til/today.md` | 사용자가 직접 적는 수동 scratchpad |
| `til/YYYY/MM/YYYY-MM-DD.md` | 명시적으로 저장한 날짜별 역사 기록 |
| `knowledge/` | 학습자가 증명한 현재 reusable understanding |
| `practice/`, `challenges/` | 직접 구현·실행·해석한 수행 근거 |

Ignored cursor와 private 자료는 Git으로 동기화되지 않습니다. 다른
장치나 clone에서 자동 복원된다고 가정하지 않습니다.

## 하루 cycle의 상세 순서

### 1. Target-first planning

[`plan-roadmap-learning`](./.agents/skills/plan-roadmap-learning/SKILL.md)은
ROADMAP endpoint와 이번 cycle의 실제 primary target을 분리합니다.

선택 순서는 사용자 지정 target, 가장 이른 endpoint route의 blocking
frontier, 같은 target의 부족한 evidence, 가장 많은 downstream을 여는
frontier 순입니다. 거의 충족된 직접 선수 하나만 inline bridge가 될 수
있습니다. 독립적인 학습이 필요한 blocker는 primary target입니다.

Source 유무, 다음 chapter, 무관하거나 보류된 미완료 practice는 target
우선순위를 바꾸지 않습니다. Platform pass만으로 prerequisite를
satisfied 처리하지 않습니다.

### 2. 자료 해결과 reviewed lesson

자료는 직접 관련 existing practice, 감사된 local source, repair가 필요한
local source, official external source 순으로 해결합니다. 외부 자료는
provider, course, offering/edition, artifact, official URL, exact scope로
식별합니다.

[`coach-llm-research-study`](./.agents/skills/coach-llm-research-study/SKILL.md)
는 schema-v10 handoff를 준비하고 독립 검토합니다. Focused review는
선택한 topic/section/example-family unit, 그 boundary unit, 직접 asset과
관련 registry 행에만 비례합니다. 각 unit의 source-anchor는 경계 확인용이며
책 전체를 매번 다시 감사하지 않습니다.

Review slice는 수업 길이가 아닙니다. 기본 `standard` session은 다음을
요구합니다.

- 실질적으로 다른 연결 module 3~5개
- 이 module들이 묶는 연결 concept path 3~5개
- 60~90분 예상 시간
- 서로 다른 worked example 최소 2개
- module마다 하나의 closing application, 평가 checkpoint는 최대 한 번
- 성립 조건과 반례·한계
- 모든 비보류 핵심 개념을 새 task/code 문맥에서 결합하는 마지막 전이
- 구현·디버깅 D2 target의 실제 class/API/`forward`/data-flow walkthrough

`짧게 하자`라는 명시적 시간·형식 요청이 있을 때만 `short`를
사용합니다. `압축`, `빠르게`, `따라잡기`만으로는 standard arc를 줄이지
않습니다. 설명하지 않은 개념을 먼저 평가하지 않으며, 한 module을
목적·설명·worked trace/code walk·적용까지 이어서 진행합니다.

### 3. 대화형 수업과 evidence

[`teach-course-material`](./.agents/skills/teach-course-material/SKILL.md)은
검토된 Module Plan을 따라 학습자의 현재 이해에 맞게 진행합니다.
질문은 답에 따라 다음 설명이 달라질 때 사용합니다. 핵심 개념을
확인하지 못하면 표현·예시·trace를 바꿔 계속 가르칩니다.

Confirmed learner answer만 daily cursor에 저장됩니다. Tutor 설명, 단순
동의, partial answer, misconception, source 요약, green test는 learner
evidence가 아닙니다. 불확실한 non-deferred concept가 남으면 handoff와
cursor를 `paused`로 보존합니다.

Completed는 계획한 session arc와 exit evidence가 끝났다는 뜻이지
Curriculum mastery가 아닙니다.

### 4. Practice modality

[`suggest-learning-practice`](./.agents/skills/suggest-learning-practice/SKILL.md)
는 completed schema-v10 captured session 또는 exact finalized TIL을 새
실습 입력으로 받습니다. Cursor의 schema-v9 legacy capture는 기존 v4
Notebook을 `PRE_LAB / I1_MECHANISM / preserved_attempt`로 보존 분류하는
migration에서만 쓸 수 있고, fresh milestone artifact로 승격할 수 없습니다.

| 학습 성과 | 기본 modality |
|---|---|
| 수학·Tensor·mechanism·작은 구현 | `NOTEBOOK` |
| latency·throughput·memory·batching·KV cache | `BENCHMARK` |
| data·validation·metric·error analysis | `DATASET_PROJECT` |
| 짧은 algorithm/API | `EXTERNAL_CHALLENGE` |
| 실제 가치가 검증된 data competition | `EXTERNAL_COMPETITION` |

실습은 다음 세 층으로 구분됩니다. 이 중 `PRE_LAB`은 누적 milestone
credit이 아니라 다음 구현을 막는 blocker를 푸는 보조 층입니다.

| 층 | 쓰는 때 | 최소 수행 경계 |
|---|---|---|
| `PRE_LAB` | 다음 구현을 막는 작은 mechanism 공백 | 계산·shape·단일 연산 |
| `MODULE_ASSIGNMENT` | 한 module을 실제로 사용할 준비가 됐을 때 | component와 data→model→loss→train/eval |
| `PHASE_CAPSTONE` | 여러 module assignment를 연결할 때 | baseline·통제 비교/ablation·error analysis·재현·한계 |

아직 assignment 경계가 준비되지 않았으면 `DEFER_TO_MILESTONE`으로
누적하며 `NO_EXTRA_PRACTICE`로 위장하지 않습니다.

모든 새 local artifact는 metadata-v5
`practice/<area>/<topic>.ipynb` 하나입니다. Session input은 live handoff를
재해석하지 않고 cursor의 immutable captured-cycle projection과 hash를
보존합니다. Historical/manual 학습은 exact finalized TIL 경로·hash를
계속 사용할 수 있습니다. 기존 metadata-v3/v4 Notebook은
`legacy-unclassified`로 검증되지만 milestone credit은 자동으로 받지
않습니다.

Notebook에는 자연어 명세, learner-owned TODO, deterministic fixture,
`check_e##()`, required reflection이 인접합니다. 생성본은 실행·커밋하지
않습니다. 학습자가 직접 구현하고 실행한 뒤 결과를 해석해야 합니다.
Completion gate는 placeholder, reflection, 실행 순서, 최신 checker, error
output, source/session provenance를 검사합니다.

Kaggle처럼 data handling·validation·metric·error analysis가 핵심일 때만
competition을 제안합니다. 실제 추천은 당시 official page에서 확인하고,
계정 접근·참여·제출 전에 별도 승인을 받습니다. Kaggle 실행 Notebook은
`practice/`, 짧은 제출 코드는 `challenges/`에 둡니다. Platform pass만
으로 practice 완료나 knowledge 갱신을 하지 않습니다.

### 5. Knowledge 갱신

[`update-learning-knowledge`](./.agents/skills/update-learning-knowledge/SKILL.md)
는 TIL 없이 completed session과 terminal practice를 읽을 수 있습니다.
학습자가 직접 확인한 범위만 date-free concept note 0~3개에 반영합니다.

실습을 만들었다면 exact artifact, 실행 순서, 해석과 path-limited commit이
검증되기 전에는 knowledge 단계로 가지 않습니다. 동등한 수행 evidence가
이미 있어 `NO_EXTRA_PRACTICE`인 경우 session evidence만으로 판단할 수
있습니다. 새 durable understanding이 없으면 `NO_CHANGE`가 정상입니다.

### 6. 다음 target

Knowledge terminal state 뒤 planner가 새 evidence로 target graph를 다시
계산합니다. Full-day 권한이 유효하면 다음 reviewed lesson의 첫 teaching
move까지 준비합니다. 새로운 cycle을 시작했다는 사실 자체는 mastery를
의미하지 않습니다.

## 명시적 일일 TIL

TIL은 cycle 중간 gate가 아닙니다. `오늘 TIL 저장해줘` 요청 때만
[`save-today-til`](./.agents/skills/save-today-til/SKILL.md)이 다음을
종합합니다.

- 완료된 unconsumed cycle의 concept와 confirmed learner evidence
- 실행·해석이 끝난 practice 또는 challenge
- knowledge 변경 또는 `NO_CHANGE`
- cursor가 기록한 exact path-limited commit
- source, primary target, 실제 전달된 bridge provenance

`git log` 전체를 추측해서 요약하지 않습니다. Cursor의 각 SHA에 대해
commit 존재, committer date, subject, exact changed-path set과 현재
artifact를 교차 확인합니다.

Flow-generated TIL은 concept-first로 씁니다.

1. 개념과 핵심 정의
2. 성립 조건·작동 원리·한계
3. 어떤 예시와 실습으로 확인했는지
4. 실제 관찰하고 해석한 결과
5. source·practice·knowledge 링크와 target provenance

자동 생성본에는 `남은 질문`, “내 말로 설명해야 한다”, 학습 지시,
평가 문구, 내부 marker를 넣지 않습니다. 미완료 학습은 cursor에 남겨
다음 수업에서 해결합니다. 사용자가 직접 작성한 standalone 또는 mixed
메모의 실제 불확실성만 coach의 한 번 검토 뒤 보존할 수 있습니다.

같은 날짜 TIL이 있으면 이미 저장된 개념 기록과 provenance를 보존하고 새
unconsumed cycle만 자연스럽게 병합·소비합니다. v9 이전 자동 생성본의 첫
저장에서는 확인된 본문을 유지하되 잘못 종료된 `남은 질문`, 다음 학습 지시,
내부 marker를 제거합니다. 날짜별 TIL 하나만
`til: YYYY-MM-DD 학습 기록`으로 커밋하고 push하지 않습니다. 실패하면
file과 cursor를 보존해 `계속`으로 재시도합니다.

## 수동 scratchpad와 standalone TIL

`til/today.md`는 사용자가 자유롭게 쓰는 ignored inbox입니다. Reviewed
lesson이 자동으로 여기에 쓰지 않습니다. Standalone self-study를 이
scratchpad에서 저장하려면 exact draft를 명시합니다.

```text
$save-today-til을 사용해 til/today.md의 수동 학습 기록을 저장해줘.
```

수동 내용은 coach가 같은 저장 흐름에서 한 번 사실·불확실성을
검토합니다. 이 경우에는 학습자가 실제로 남긴 질문을 보존할 수
있습니다.

## 실습을 새 대화에서 재개

Cursor에 exact practice path가 있는 full-day flow는 `계속`으로
재개합니다. Cursor 밖의 manual/historical practice는 경로를 직접
지정합니다.

```text
practice/<area>/<topic>.ipynb를 이어서 하자.
현재 저장된 코드와 실제 check 실패부터 확인해줘.
```

Agent는 현재 cell과 실제 traceback에서 첫 blocker만 다룹니다. 별도
허가 없이는 learner-owned 핵심 구현을 대신 완성하지 않습니다.

## 자료 등록과 임시 official source

Private 자료는 Git에 올라가지 않는 위치에 둡니다.

```text
materials/private/<course>/NN-NN_title.pdf
materials/private/<course>/NN-NN_title.md
```

과정 `INDEX.md`는 정확히 하나의 uppercase `source_namespace`를
선언하고 source path/hash/audit를 기록합니다. 반복할 bounded lesson
범위는 선택적 `학습 범위` 표에 Source ID, 연결된 단원·주제·예제군의
`Included units`, 그리고 `Boundary units`로 등록할 수 있습니다. 각 unit은
사람이 읽는 제목과 하나의 검증 가능한 source-anchor를 함께 적습니다.
예를 들어 `Chapter 2 §2.1–§2.2: 조건부확률과 two-card 예시
[materials/private/course/00-01.pdf#page-56--63]`처럼 선언합니다. 페이지를
한 줄씩 열거하지 않으며, anchor는 검토 경계 확인용일 뿐 durable coverage나
mastery가 아닙니다.

공개 HTTPS official source는 한 reviewed lesson 동안
`tmp/active-lesson-sources/<lesson-id>/`에 content-addressed cache할 수
있습니다. Agent가 exact URL을 발견·검증하고 helper는 그 URL만
retrieval합니다. Login, payment, archive, dataset, weight 또는 기본
100 MiB 초과는 승인을 기다립니다. 임시 사용은 Curriculum coverage를
바꾸지 않습니다.

## Python·Notebook 환경

```bash
cd /home/jake/llm-research-learning-lab
uv sync
uv run python path/to/script.py
```

새 dependency는 `pip install` 대신 `uv add`로 추가합니다. VS Code
Notebook kernel은 repository의 `.venv/bin/python`을 사용합니다.

실행하지 않은 결과는 기록하지 않습니다. Dataset, model weight,
credential, 큰 생성물은 명시적 허가와 적절한 ignore 없이는 Git에
넣지 않습니다.

## Skill을 직접 고정할 때

자연어 진입점으로도 충분하지만 특정 단계만 실행하려면 다음처럼
명시할 수 있습니다.

```text
$plan-roadmap-learning으로 다음 target만 읽기 전용으로 정해줘.

$coach-llm-research-study와 $teach-course-material로
materials/private/<course>/<lesson>을 표준 수업으로 진행해줘.

$suggest-learning-practice로 현재 completed session의 practice modality를 정해줘.

$update-learning-knowledge로 terminal session·practice evidence만 knowledge에 반영해줘.

$save-today-til로 완료된 unconsumed cycle을 오늘 TIL에 저장해줘.
```

하나의 거대 orchestration skill이나 별도 progress DB는 두지 않습니다.
Daily cursor가 phase만 연결하고 각 전문 skill의 증거·권한 경계를
유지합니다.
