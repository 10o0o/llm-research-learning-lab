# 사용법

## Python 실습 환경 준비

이 저장소의 Python 패키지와 `.venv`는 uv로 관리합니다. 저장소를 처음 받았거나 의존성이 바뀌었을 때 다음 명령으로 잠금 파일과 동일한 환경을 준비합니다.

```bash
cd /home/jake/llm-research-learning-lab
uv sync
```

새 패키지는 `pip install` 대신 `uv add <패키지명>`으로 추가하고, 명령은 `uv run`으로 실행합니다.

```bash
uv add <패키지명>
uv run python <파일명>.py
```

VS Code에서 Notebook을 실행할 때는 `/home/jake/llm-research-learning-lab/.venv/bin/python`을 커널로 선택합니다. 직접 의존성은 `pyproject.toml`, 정확한 설치 버전은 `uv.lock`에 기록되므로 두 파일을 함께 유지합니다.

## 세 공간만 구분하기

| 위치 | 남기는 것 | 성격 |
|---|---|---|
| `til/` | 오늘 무엇을 배우고 어떻게 생각했는지 | 날짜별 기록, 과거의 흔적 |
| `knowledge/` | 지금 내가 그 개념을 어떻게 이해하는지 | 주제별 문서, 계속 갱신 |
| `practice/` | 직접 실행한 코드, 테스트, 출력과 해석 | Notebook이 안내하는 실행 증거 |

[`ROADMAP.md`](./ROADMAP.md)는 큰 학습 방향을, [`CURRICULUM.md`](./CURRICULUM.md)는 역량별 목표 깊이·선수 관계·현재 강의자료의 충족도와 보완 기준을 담습니다. 둘 다 개인 진도율이나 점수를 기록하는 문서는 아닙니다.

## 공부한 날

1. KANT 라이브 수업을 듣습니다.
2. 사용한 강의자료를 `materials/private/<course>/`에 등록합니다.
3. `$coach-llm-research-study`와 `$teach-course-material`로 자료를 감사하고 `CURRICULUM.md`의 관련 역량·공백을 확인합니다.
4. 수업 계약이 fresh reviewer의 검토를 통과하면 기술 개념 단위로 학습합니다. 답에 따라 다음 설명이 달라지는 지점에서만 질문·계산·자기 설명으로 이해를 확인하고, 그렇지 않은 단계는 질문 없이 이어갑니다.
5. 형식 없는 메모는 `til/today.md`에 직접 쓰고, 대화형 수업에서 확인된 자신의 답변은 같은 파일에 자동으로 누적합니다.
6. `$coach-llm-research-study`로 오늘 실제로 다룬 핵심이 이해 또는 불확실성의 형태로 `til/today.md`에 모두 있는지 검토합니다.
7. 오개념이나 확인이 필요한 표현이 있으면 `$teach-course-material`로 다시 학습하고, 직접 다시 설명한 답변 중 확인된 것만 초안에 반영합니다.
8. `저장 가능` 판정을 받으면 `$save-today-til`로 날짜별 TIL을 저장하고 그 날짜별 TIL만 자동 커밋합니다.
9. 저장된 날짜별 TIL의 정확한 경로를 `$suggest-learning-practice`에 전달합니다. 스킬은 TIL의 주요 학습 성과 전체를 실습 action으로 매핑하고, 강의 INDEX에 정확히 연결된 제공 실습만 자동으로 참고해 하나의 단일 Notebook을 만듭니다.
10. 핵심 로직을 직접 구현하고 normal·edge·failure test를 실행합니다. 실패 원인을 한 단계씩 진단하고, 통과 뒤에도 출력과 상태 변화를 해석합니다.
11. `$update-learning-knowledge`로 실제로 이해했다고 확인된 내용만 `knowledge/`에 반영합니다.
12. 새 지식 문서를 더 깊게 공부하고 싶다면 그 문서를 대상으로 다시 질문하고, 새 이해가 확인된 경우 같은 문서만 갱신합니다.

동등한 구현·실행·해석 증거가 이미 있으면 추가 실습 없음도 가능하고, 새로 반영할 지식이 없다는 결론도 정상입니다. 영구 중복 강의록이나 학습자 진도표는 만들지 않으며, `tmp/active-lesson-handoff.md`는 확인된 학습자 답변과 오늘 학습한 범위가 초안에 모두 반영되고 날짜별 TIL 커밋이 성공한 후에만 제거하는 임시 운영 캐시입니다.

## 강의자료 등록

비공개 강의자료는 Git에 올라가지 않는 다음 위치에 둡니다.

```text
materials/private/<course>/NN-NN_주제.md
materials/private/<course>/NN-NN_주제.pdf
```

파일을 옮긴 뒤 전체 페이지와 수식·표·코드·그림이 읽히는지 확인합니다. Notion에서 내보낸 자료라면 접힌 내용도 포함되어야 합니다. 과정 폴더에 `INDEX.md`가 있다면 새 파일명과 원본 위치를 함께 갱신합니다.

## TIL 작성

하루에 파일 하나를 만들고 날짜가 쌓이는 구조로 저장합니다.

```text
til/2026/08/2026-08-13.md
til/2026/08/2026-08-20.md
til/2026/09/2026-09-01.md
```

처음부터 정해진 목차에 맞추지 않습니다. `til/today.md`에는 다음 내용이 자연스럽게 섞여도 됩니다.

- 오늘 본 자료와 이해한 내용
- 처음 생각과 달라진 부분
- 여전히 헷갈리는 점
- 직접 계산하거나 실행해본 결과
- 다음에 이어서 보고 싶은 것

다 쓴 뒤 바로 저장하지 않고, 평가 코치가 handoff의 완료·현재 Teaching Step과 Objective Delivery, 확인된 학습자 답변, 실제 학습 대화, 명시한 자율학습 범위를 기준으로 초안을 먼저 검토합니다. 원자료 전체를 요약할 필요는 없지만 **오늘 실제로 다룬 기술적 핵심은 모두** 남겨야 합니다. 이해가 확인됐으면 `오늘의 학습`이나 `배운 점`에, 아직 불확실하면 `남은 질문`에 적습니다. 필요할 때만 알려 주는 로드맵·학습법·자기진단 같은 Guidance는 학습 증거나 TIL 핵심으로 세지 않습니다. 오늘 다루지 않은 원자료 내용은 `deferred`이며 누락이 아닙니다.

검토를 마치면 [`til/template.md`](./til/template.md)의 순서에 맞게 저장됩니다. `오늘의 학습`은 항상 남기고, 나머지 항목은 실제 내용이 있을 때만 남깁니다. 라이브 수업과 GPT 보충 학습을 구분해서 썼다면 `오늘의 학습` 안에서 그 구분을 유지합니다.

강의자료를 보고 공부했다면 `관련 기록`에 그 자료의 정확한 링크가 들어갑니다. 이후 실습 스킬은 날짜별 TIL을 필수 입력으로 받고 이 링크를 따라 자료를 확인하므로, 자료명을 추측해서 링크하지 않습니다.

TIL은 그날의 생각을 보존하는 기록입니다. 나중에 이해가 바뀌어도 과거 글 전체를 교과서처럼 다시 쓰지 않습니다. 짧게 정정하거나 새로운 날의 TIL에 남기고, 현재의 정확한 이해는 `knowledge/`에 반영합니다.

## 지식 베이스 갱신

다시 사용할 만한 개념은 날짜 없이 주제별 파일로 저장합니다.

```text
knowledge/math/vector.md
knowledge/ml/data-split.md
knowledge/llm/attention.md
```

[`knowledge/template.md`](./knowledge/template.md)를 사용합니다. 이곳은 강의를 그대로 옮기는 곳이 아니라 **지금의 내가 설명할 수 있는 가장 정확한 이해**를 적는 곳입니다. 새로 이해한 내용이 생기면 기존 문서를 고치고, 같은 개념의 문서를 중복해서 만들지 않습니다.

모든 TIL을 지식 문서로 만들 필요는 없습니다. 여러 번 다시 볼 개념, 다른 개념의 기반이 되는 내용, 직접 설명하거나 적용해본 내용만 하루 최대 0~3개 반영합니다. GPT가 설명했을 뿐 아직 내가 설명하지 못한 내용은 반영하지 않습니다.

## 실습 저장

생성되는 모든 실습은 단일 `.ipynb`에 구현·fixture·검사·해석 셀을 나란히 둡니다. 수학, Tensor·Shape, 작은 학습·검증 흐름, 디버깅, 출력 계약을 파일로 나누지 않고 exercise로 구성합니다.

```text
practice/math/vector-normalization.ipynb
practice/deep-learning/tiny-image-classifier-contracts.ipynb
```

[`practice/template.ipynb`](./practice/template.ipynb)는 이 단일 워크북의 기본 구조입니다. 관련 날짜별 TIL과 강의자료는 Notebook 상단에 정확히 링크합니다.

단일 Notebook에서는 setup을 한 번 실행한 뒤 현재 E번호의 구현 셀, fixture 셀, `check_e01()` 형식의 검사 셀을 순서대로 실행합니다. 함수 수정 뒤에는 현재 구현 셀부터 다시 실행합니다.

워크북은 TIL의 주요 성과를 `implement`, `test`, `debug`, `interpret`, `design`에 연결한 Practice Coverage Map을 가집니다. 각 exercise는 실제 사용 맥락, 실행 전 회상·예측, 작은 계약, 직접 구현, 바로 옆의 접힌 힌트, 테스트와 실패 진단, 결과 해석 순서입니다. 원문 링크는 출처와 추가 복습용이며, 문제를 풀기 위해 열어야 하는 숨은 명세가 아닙니다. 테스트가 요구하는 임계값·분기 순서·반환 token과 key·dtype/device 표현·축·경계 포함 여부·집계·오류 조건은 TODO 전에 `source-given` 또는 `practice-given` 계약으로 공개하고, 학습자가 계산할 결과는 `derive`로 분리합니다. 전역 힌트 절은 만들지 않습니다. 난이도는 `Core`, `Applied`, `Advanced` 중 하나이며, 설명을 잘했더라도 구현 증거가 없으면 작은 Core부터 시작합니다.

처음에는 learner function이 `NotImplementedError`라서 해당 exercise의 check가 실패하는 것이 정상입니다. JSON·import·셀 순서 자체가 실패하면 워크북 결함입니다.

실행하지 않은 결과는 기록하지 않고, 데이터셋·모델 가중치·API 키·큰 출력 파일은 Git에 올리지 않습니다. Notebook 출력도 결과를 이해하는 데 필요한 것만 남깁니다.

## GPT 스킬

### 1. 강의자료와 지식 개념 맞춤 학습

[`teach-course-material`](./.agents/skills/teach-course-material/SKILL.md)은 관련 `knowledge/`, 최근 TIL과 현재 대화에서 확인되는 이해 수준을 바탕으로 강의를 재구성합니다. 이미 이해한 내용은 짧게 연결하고, 부족한 선수개념은 보충합니다. 이 압축은 설명의 깊이와 반복을 줄이는 것이며, “모두”, “전부”, “1~4강 전체”처럼 요청한 범위의 핵심 학습목표를 삭제하는 뜻이 아닙니다. 생각할 가치가 있는 문제는 작은 힌트부터 시작하지만, 정의나 막힌 선수개념은 바로 설명합니다.

강의자료의 오류와 누락도 함께 확인하려면 평가 스킬을 같이 사용합니다.

```text
$coach-llm-research-study와 $teach-course-material을 함께 사용해
materials/private/kant-basic-math/01-01_벡터의_정의와_기하학적_해석.md를 학습하고 싶어.

관련 knowledge와 최근 TIL에서 내 현재 이해를 먼저 확인하고,
강의의 오류·누락·선수개념을 실제 설명에 반영해줘.
한 번에 전부 설명하지 말고 개념 단위로 진행하면서 내 설명과 계산을 통해 이해를 확인해줘.
```

수업 전에 ignored 임시 파일인 `tmp/active-lesson-handoff.md`에 자료 hash, 수업 계약, 검토 결과와 현재 Teaching Step을 남깁니다. 전체 범위는 `full-source`, 명시한 일부 범위는 `focused`로 기록합니다. 먼저 모든 명시적 목표를 본문 근거와 대조해 `learning`, `guidance`, `source-gap`으로 나눕니다. 학습법·로드맵·최종 산출물·자기진단·환경 안내는 Guidance Map에 보존하되, Trigger가 생길 때만 안내하고 이해 질문이나 학습 증거로 만들지 않습니다. 목표 문구만 있고 설명 본문이 없으면 source-core 내용을 만들어내지 않습니다.

3~7개의 Concept Path는 큰 탐색 묶음일 뿐입니다. 기술적 완전성은 개수 제한 없는 Observable Objective Map으로, 실제 전달 순서는 Prepared Teaching Steps로 관리합니다. `check_policy: adaptive`는 답에 따라 다음 설명이 달라질 때만 사용하고, 그 차이가 없으면 `none`으로 두어 질문 없이 진행합니다. 각 기술 목표가 실제로 설명됐는지는 Objective Delivery에 별도로 기록하며, 필수 목표가 하나라도 남으면 전체 수업을 완료로 표시할 수 없습니다. 이 전달 기록은 학습자의 이해 증거가 아니므로 TIL에는 여전히 학습자가 직접 확인한 답변만 들어갑니다.

fresh reviewer가 계약을 통과시켜야 수업을 시작하며, 각 강의 파일의 선언 목표와 실제 본문 근거, 공식·코드·그림·본문 예제가 목표표와 Teaching Step에 정확히 연결됐는지 확인합니다. 원문에 없는 메커니즘의 과잉 승격, Guidance의 평가 목표화, 다음 설명을 바꾸지 않는 질문도 실패 사유입니다. 첫 검토와 수정 후 재검토까지 총 2회 안에 통과하지 못하거나 reviewer를 사용할 수 없으면 수업을 중단합니다. 이 파일은 컨텍스트 복구용 운영 캐시이며 영구 강의록이나 학습 증거가 아닙니다.

평가 결과는 필요한 곳에 `[선수개념]`, `[정정]`, `[보충]`으로 반영됩니다. 학습자의 답변 중 정확한 이해가 확인된 것만 `til/today.md`에 자동으로 추가되며, 튜터 설명·단순 동의·부분 이해·오개념은 추가되지 않습니다. 별도 평가 보고서까지 필요할 때만 요청합니다.

기존 지식 문서에서 궁금한 부분을 더 배우는 데도 같은 학습 스킬을 사용합니다. 이때 지식 문서는 정답지가 아니라 현재 이해를 보여주는 출발점입니다.

```text
$coach-llm-research-study와 $teach-course-material을 사용해
knowledge/math/vector.md에서 내가 이해한 범위를 먼저 확인하고,
관련 강의자료와 연결해 부족한 부분을 대화형으로 가르쳐줘.
```

### 2. til/today.md 저장 전 검토

[`coach-llm-research-study`](./.agents/skills/coach-llm-research-study/SKILL.md)는 `til/today.md`를 오늘 본 강의자료와 학습 대화에 대조해 다음을 구분합니다.

- 정확하게 설명한 내용
- 저장 전에 반드시 고쳐야 할 잘못된 개념
- 아직 확실한 사실처럼 쓰면 안 되는 혼동과 불확실성
- 오늘 실제로 다뤘지만 이해나 불확실성 어느 쪽에도 적히지 않은 핵심
- 오늘 배우지 않아 TIL에 없어도 되는 deferred 내용
- TIL에 넣지 않아도 되는 선택 보강 내용
- GPT가 설명했지만 아직 내가 다시 설명하지 않은 내용

```text
$coach-llm-research-study를 사용해
til/today.md를 오늘 본 강의자료 기준으로 저장 전에 검토해줘.
```

검토 결과는 다음 중 하나입니다.

- `저장 가능`: 그대로 저장해도 되는 상태
- `수정 후 저장`: 고칠 내용이 명확하며 이해를 확인한 뒤 반영해야 하는 상태
- `추가 확인 후 저장`: 질문이나 재학습을 통해 판단해야 하는 상태

`수정 후 저장`이나 `추가 확인 후 저장`이면 중요한 문제부터 하나씩 해결합니다.

```text
$teach-course-material을 사용해
저장 전에 확인해야 할 첫 번째 개념부터 다시 가르쳐줘.
내가 다시 설명해서 이해가 확인되면 내 답변만 til/today.md에 반영해줘.
```

평가 코치는 오개념이나 빠진 내용을 정답 문장으로 몰래 바꾸지 않습니다. 작은 확인 질문에 내가 다시 설명한 내용만 학습으로 반영하고, 해결되지 않은 부분은 `남은 질문`에 둡니다. 모든 강의 내용을 추가하는 것이 아니라 오늘 실제로 학습한 핵심의 경계를 빠짐없이 기록하는 것이 목표입니다. Handoff 기반 수업은 최종 draft hash와 coverage를 `--til-ready`로 확인합니다.

### 3. 오늘의 TIL 저장

[`save-today-til`](./.agents/skills/save-today-til/SKILL.md)은 검토를 마친 `til/today.md`를 적당히 분류하고 다듬어 `til/YYYY/MM/YYYY-MM-DD.md`에 저장합니다.

```text
$save-today-til을 사용해 til/today.md를 정리하고 날짜별 TIL로 저장해줘.
```

다른 초안이나 지난 날짜도 지정할 수 있습니다.

```text
$save-today-til을 사용해 rough.md를 2026-08-13 TIL로 저장해줘.
```

사용자의 말투, 질문, 계산, 코드와 실제 결과는 보존하고 맞춤법·문단·중복만 가볍게 정리합니다. 저장 스킬은 사실 검증을 반복하지 않습니다. 같은 날짜의 TIL이 있으면 기존 내용에 합치며, 내부 중복 방지 marker는 최종 TIL에서 제거합니다. 검증과 날짜별 TIL 하나의 path-limited 커밋이 성공한 뒤에만 `til/today.md`와 완료된 handoff를 정리하며 push하지 않습니다. 검증이나 커밋이 실패하면 둘 다 그대로 보존합니다.

나중에 새로운 오류를 발견했거나 자료가 바뀌었다면 완성된 TIL을 평가 코치로 다시 검토할 수 있지만, 매일 저장 후 같은 평가를 반복할 필요는 없습니다.

### 4. 현업형 실습 생성과 시도 피드백

[`suggest-learning-practice`](./.agents/skills/suggest-learning-practice/SKILL.md)의 생성 모드는 검토와 저장을 마친 날짜별 TIL 하나를 필수 입력으로 받습니다. 정확한 경로를 지정해야 하며, 최신 TIL이나 `til/today.md`를 추측하지 않습니다.

```text
$suggest-learning-practice를 사용해
til/2026/08/2026-08-13.md의 주요 학습 성과 전체를 직접 구현하고
테스트하는 실습으로 만들어줘.
```

스킬은 TIL의 정확한 강의 링크를 따라가고, 해당 과정 `INDEX.md`에서 `Related lesson path`가 그 강의와 일치하는 강의 제공 실습만 자동으로 읽습니다. 기본·심화가 모두 매핑돼 있으면 비교하되, 원본을 수정하거나 모범답안·대표 출력을 복사하지 않습니다. 차시 번호나 비슷한 파일명으로 매핑을 추측하지 않습니다.

TIL이 올바르더라도 구현 경험이 없다면 **실습 생성**이 기본입니다. TIL의 주요 성과를 Practice Coverage Map에 넣고 `implement`, `test`, `debug`, `interpret`, `design` 중 하나 이상으로 연결합니다. 증거가 적으면 실습을 막는 대신 작은 `Core`부터 시작합니다. 이미 같은 성과를 구현·실행·해석한 동등한 증거가 있으면 기존 미완성 실습을 계속하거나 예외적으로 추가 실습 없이 끝낼 수 있습니다.

실습은 언제나 `practice/<area>/<topic>.ipynb` 하나로 만듭니다. 이 파일만 읽어도 모든 TODO와 check의 고정 조건을 알 수 있어야 하며, 강의 링크를 열어야만 알 수 있는 임계값이나 반환 규칙은 허용하지 않습니다. 함수 signature, deterministic fixture와 local normal·edge·failure check는 제공하지만 핵심 로직은 `NotImplementedError`에서 내가 직접 시작합니다. 각 check는 공개된 Contract ID를 참조하고, 힌트는 각 TODO 바로 앞의 접힌 블록에 있습니다. `힌트 1`은 관찰 상태, `힌트 2`는 작은 trace나 Shape 흐름을 제공합니다. 생성물은 Notebook-only 명세 검토와 원문 대조를 포함한 validator·fresh reviewer를 통과해야 준비 완료로 전달됩니다.

시도 중 막혔을 때는 날짜별 TIL 대신 정확한 실습 경로를 줍니다.

```text
$suggest-learning-practice를 사용해
practice/<area>/<topic>.ipynb의 현재 코드와 check 실패를 보고
첫 blocker만 힌트로 설명해줘.
```

이 모드에서는 저장된 코드와 실제 traceback을 기준으로 개념 힌트, 부분 trace, 최소 API 뼈대 순서로 돕습니다. 별도 요청 없이는 핵심 구현을 대신 완성하지 않으며, 테스트가 통과해도 parameter·gradient·Shape·metric 같은 결정적 상태 변화를 내가 설명해야 완료로 판단합니다.

### 5. 확인된 이해를 knowledge에 반영

[`update-learning-knowledge`](./.agents/skills/update-learning-knowledge/SKILL.md)는 TIL, 현재 대화의 답변, 계산과 실행 결과 중 학습자가 직접 보여준 이해만 골라 기존 지식 문서를 갱신하거나 새로 만듭니다.

```text
$update-learning-knowledge를 사용해
오늘의 TIL, 평가 결과와 학습 대화에서 내가 이해했다고 확인된 개념만 knowledge에 반영해줘.
증거가 부족하거나 기존 문서와 달라진 것이 없다면 파일을 만들지 말고 그렇게 알려줘.
```

한 학습 흐름에서 최대 0~3개만 다루고, 같은 개념은 기존 문서를 갱신합니다. GPT의 설명이나 정정만으로는 지식에 넣지 않습니다. 실습이 제안되었다면 수행하고 결과를 해석한 뒤 이 스킬을 실행하는 편이 좋습니다. 지식 문서를 대상으로 추가 학습한 뒤 새 이해를 직접 설명했다면 같은 스킬을 다시 실행해 기존 문서를 보완할 수 있습니다.

## 가장 간단한 흐름

수업 직후에는 다음 요청으로 시작합니다.

```text
$coach-llm-research-study와 $teach-course-material을 사용해
이 강의자료를 내 현재 knowledge에 맞춰 오늘 학습하자.
개념별로 진행하고 내 답변에서 확인된 이해와 불확실성을 구분해줘.
```

`til/today.md`를 쓴 뒤에는 먼저 검토합니다.

```text
$coach-llm-research-study를 사용해
til/today.md를 오늘 본 강의자료 기준으로 저장 전에 검토해줘.
수정이나 추가 확인이 필요하면 저장하지 말고 중요한 것부터 하나씩 해결해줘.
```

`저장 가능` 판정을 받은 뒤 날짜별 TIL로 저장합니다.

```text
$save-today-til로 til/today.md를 저장해줘.
```

저장 스킬이 알려준 정확한 날짜별 경로를 다음 요청에 넣습니다.

```text
$suggest-learning-practice를 사용해
til/YYYY/MM/YYYY-MM-DD.md를 기준으로 실습을 진행해줘.
```

워크북이 만들어졌다면 직접 실행하고 결과 해석까지 적습니다. 실습 없음 판정을 받았거나 워크북을 마쳤다면 마지막으로 다음처럼 요청합니다.

```text
$update-learning-knowledge를 사용해 오늘의 TIL, 학습 대화와
실행한 실습이 있다면 그 결과까지 포함해서,
내가 설명하고 해석한 범위만 knowledge에 반영해줘.
```
