# Practice

완료된 lesson session 또는 명시적으로 지정한 finalized TIL에서 배운
내용을 직접 회상하고 구현하며, 실제 테스트 실패와 상태 변화를 해석한
증거를 둡니다.

## 산출물 형태

실습을 만들기 전에 정확한 target과 `captured-cycle | finalized-til`
learning input을 기준으로 action, mode, progression layer, implementation
depth를 판정합니다. 하루 전체 흐름은 TIL을 기다리지 않고 cursor v2에
불변 projection으로 captured된 schema-v10 session을 사용합니다.

- 수학·Tensor·메커니즘·작은 구현: `NOTEBOOK`
- latency·throughput·memory·batching·KV cache: `BENCHMARK`
- 데이터·validation·metric·error analysis: `DATASET_PROJECT`
- 검증된 짧은 외부 문제: `EXTERNAL_CHALLENGE`
- 실제 가치가 있고 현재 상태가 확인된 대회: `EXTERNAL_COMPETITION`

세 local mode는 재사용 모듈 경계 자체가 학습 대상이 아닌 한 단일
Notebook을 사용합니다.

누적 단계는 다음처럼 구분합니다.

- `PRE_LAB / I1_MECHANISM`: 한 개념 blocker를 푸는 용도이며 milestone
  credit이 없습니다.
- `MODULE_ASSIGNMENT / I3_WORKFLOW` 이상: 실제 component와
  data→model→loss→train/eval 흐름을 구현합니다.
- `PHASE_CAPSTONE / I5_RESEARCH`: 적어도 두 module artifact를 통합하고
  baseline, 통제 비교 또는 ablation, error analysis, 재현 조건, 한계를
  보고합니다.

준비된 capstone, module assignment, pre-lab 순으로 우선합니다. blocker가
없고 누적 과제를 아직 만들 시점이 아니면 `DEFER_TO_MILESTONE`으로 exact
`MA-*` 또는 `PC-*` ID에 연결하고 작은 Notebook을 추가하지 않습니다.

```text
practice/<area>/<topic>.ipynb
```

Notebook 안에서는 설명, 구현, 고정 fixture, 공개 검사, 결과 해석을
가까이 둡니다. 작은 학습·validation·checkpoint 흐름도 한 Notebook 안에서
완결합니다. 재사용 가능한 여러 모듈과 CI가 학습 대상인 별도 프로젝트를
사용자가 명시적으로 요청했을 때만 다중 파일 구조를 만듭니다.

기존 미완성 실습은 현재 target 또는 blocking prerequisite와 직접 연결되고,
필요한 실행 증거가 남아 있고, 비용 대비 가치가 있으며, 보류되지 않았고,
개념 blocker가 없을 때만 다시 선택합니다. 다음 chapter이거나 단순히
미완성이라는 이유만으로 자동 우선하지 않습니다.

Notebook은 자연스러운 목적과 요구사항, 작은 예, 단계별 힌트, 테스트
실행과 결과 해석을 안내합니다. 강의에서 배운 핵심 연산·판단만 TODO로
남기고 함수 시그니처, 반복 검증, 반환 조립, fixture와 bookkeeping은
기본으로 제공합니다. 따라서 제공된 helper와 scaffold는 완성 코드여도
되며 모든 함수를 통째로 `NotImplementedError`로 만들지 않습니다.

## 생성 원칙

`$suggest-learning-practice`에는 한 종류의 input을 정확히 전달합니다.

- 하루 전체 흐름: cursor v2 `captured_session`의 cycle·lesson ID,
  `projection_sha256`, primary/bridge target, concept/evidence ID
- 독립·과거 학습: 검증된 날짜별 TIL의 exact path/hash

`til/today.md`나 자동으로 고른 최신 TIL은 입력이 아닙니다. 실습은 captured
session 또는 TIL의 주요 학습 성과를 다음 action으로 바꿉니다. Capture가
깨졌으면 `SESSION_REPAIR_REQUIRED`, legacy TIL이 깨졌으면
`TIL_REPAIR_REQUIRED`로 구분합니다.

- `implement`: 핵심 메커니즘 직접 구현
- `test`: 정상·경계·실패 계약 확인
- `debug`: 의도적으로 깨진 경계나 흐름 진단
- `interpret`: Shape, gradient, metric, output의 의미 설명
- `design`: API, 데이터 계약, 모델 출력이나 실험 조건 설계

새 Notebook metadata schema v5는 artifact와 Outcome별 Curriculum target,
`practice_mode`, progression layer/depth, milestone definition hash, stable
source ID와 `learning_inputs`를 보존합니다. Captured-cycle Outcome은
`L001:C01`처럼 input-namespaced concept/evidence ID와 수행 action을
연결하고, finalized-TIL Outcome은 exact `til_location`을 유지합니다. Local source는
exact path와 hash를, temporary external source는
provider/course/offering 또는 edition, artifact, official URL, retrieval
hash와 scope를 기록합니다. Requirement의 source 위치는 변하기 쉬운 path
대신 stable source ID를 참조합니다. 기존 schema-v3/v4 Notebook은
`legacy-unclassified`로 계속 검증하지만 milestone credit을 받지 않으며 새
산출물은 v5만 사용합니다. 이 target 관계는 실습 relevance와 provenance이며
mastery나 Curriculum coverage 승격이 아닙니다.

Fresh v5 artifact는 learner surface를 먼저 보고 metadata/source fidelity를
나중에 보는 독립 review를 통과해야 합니다. `creation_reviews`는 한 번의
repair와 두 번째 fresh reviewer까지만 기록합니다. Module/capstone의
required interpretation target은 자신이 해석하는 `result_cell_ids`를
명시합니다.

직접 구현 근거가 부족해도 blocker가 없다면 작은 pre-lab을 반복하지
않습니다. 준비된 module assignment의 실제 component와 workflow를 가장
작게 유지하거나, 아직 그 시점이 아니면 exact milestone으로 defer합니다.
여러 module artifact가 준비된 뒤에만 capstone의 ablation·민감도·실패
분석을 수행합니다.

각 exercise는 하나의 주 개념과 최대 세 개의 학습자 작업만 다루며 다음
순서를 유지합니다.

```text
자연스러운 목적과 문제
→ 준비된 뼈대와 직접 완성할 부분
→ 모든 공개 검사 조건과 작은 예
→ 강의 핵심 연산·판단 구현
→ 바로 옆의 접힌 힌트
→ 공개 검사와 실패 진단
→ 결과의 의미와 한계 해석
```

힌트를 파일 아래쪽에 몰아두지 않습니다. 각 TODO 바로 앞에 `힌트 1`과
`힌트 2`를 접어 둡니다. 처음에는 `guided`, 익숙해지면 `partial`, 충분한
증거가 있는 뒤에는 `independent`로 비계를 줄이되 문제의 필수 조건은
끝까지 모두 공개합니다. 반드시 작성해야 하는 해석은 학습자 target으로
추적하고, 추적하지 않는 복습 메모는 선택 사항이며 완료 조건이 아니라고
밝힙니다.

## 강의 제공 실습

강의 제공 원본은 `materials/private/<course>/course-provided-practice/`에
남습니다. 각 과정 `INDEX.md`의 다음 열이 강의와 실습을 정확히 연결합니다.

```text
Practice path | Related lesson path | Variant | Format | Original
```

Session 또는 TIL의 exact source provenance와 일치하는 행만 자동으로
참고합니다. 원본은 learner evidence가 아닙니다. 기본·심화 자료의 starter,
TODO, fixture, check 경계를 먼저 감사하고 적절한 starter를 우선
보존합니다. 정답은 명세 확인과 임시 reference 실행에만 사용하며 답이나
가짜 출력을 Notebook에 복사하지 않습니다.

## 실행과 피드백

단일 Notebook은 setup을 한 번 실행한 뒤 현재 E번호의 구현 셀, fixture 셀,
`check_e01()` 형식의 검사 셀 순서로 실행합니다. 함수 수정 뒤에는 현재
구현 셀부터 다시 실행하면 됩니다.

미완성 핵심 지점에서만 `NotImplementedError`나 명시적 placeholder 실패가
정상입니다. 제공된 scaffold는 그대로 실행 가능해야 합니다. 막혔을 때
`$suggest-learning-practice`에 정확한 Notebook 경로를 주면 저장된 code와
실제 traceback을 기준으로 한 번에
가장 작은 blocker부터 안내합니다. 테스트 통과 뒤에도 결정적인 상태나
출력을 직접 설명해야 완료 증거가 됩니다.

검증 단계는 목적이 다릅니다.

```bash
python3 .agents/skills/suggest-learning-practice/scripts/validate_practice_artifact.py \
  practice/<area>/<topic>.ipynb --learner-state

python3 .agents/skills/suggest-learning-practice/scripts/validate_practice_artifact.py \
  practice/<area>/<topic>.ipynb --completion-ready
```

`--learner-state`는 진행 중 구조와 provenance를 검사하며, 사라진 temporary
external cache는 warning으로만 보고합니다. `--strict-external-sources`는
receipt와 cache identity/hash를 요구합니다. `--completion-ready`는 모든
learner target과 필수 reflection, setup·implementation·fixture·checker의
실제 실행, 최신 실행 순서, error output 부재, session-or-TIL/source 정합성,
declared result output을 모두 요구합니다. 이 gate와 학습자 해석이 확인된
뒤에만 exact Notebook path를 완료 커밋 대상으로 삼을 수 있습니다.

기존 v4 시도를 보존형 pre-lab으로 분류할 때만 다음 migration을 사용합니다.
실제 파일에 적용하기 전 exact path와 cursor projection을 확인합니다.

```bash
uv run python .agents/skills/suggest-learning-practice/scripts/migrate_practice_v4_to_v5.py \
  practice/<area>/<topic>.ipynb --repo-root .
```

이 작업은 `.cells`를 보존하고 `PRE_LAB / I1_MECHANISM /
preserved_attempt`와 null milestone만 기록합니다. 독립 review가 실제로 끝난
뒤에는 learner cell을 바꾸지 않는 다음 helper로 그 결과만 기록합니다.

```bash
uv run python .agents/skills/suggest-learning-practice/scripts/record_practice_creation_review.py \
  practice/<area>/<topic>.ipynb --repo-root . \
  --reviewer-id <independent-reviewer> \
  --reviewed-at <RFC3339> \
  --learner-surface-verdict pass \
  --metadata-verdict pass
```

[실습 Notebook 템플릿](./template.ipynb)은 위 구조의 Notebook 기준입니다.
실행하지 않은 결과를 기록하지 않고, 데이터셋·모델 가중치·API 키와 큰
출력 파일은 Git에 올리지 않습니다.
