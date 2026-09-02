# 사용법

## 시작과 재개

이 저장소를 작업 공간으로 연 새 대화에서는 [`STATE.md`](./STATE.md)가
유일한 학습 재개 북마크입니다. 다음 문장으로 현재 범위의 연결된 모듈
하나를 시작합니다.

```text
오늘 학습 시작
```

같은 source나 과제 안에서 여러 모듈을 이어가고 싶다면 다음 중 하나를
사용합니다.

```text
오늘 전체 학습 흐름 시작
전체 학습 흐름 시작
```

이 요청은 새 강의나 새 과제로 자동 진입할 권한이 아닙니다. 현재 범위가
끝나면 다음 선택지를 제안하고 사용자 결정을 기다립니다.

새 대화에서 이어갈 때는 다음처럼 말합니다.

```text
계속
```

Agent는 `STATE.md`의 `다음 독립 행동`만 재개합니다. `tmp/`의 ignored
파일이나 Notebook metadata에서 과거 phase를 복원하지 않습니다.

멈출 때는 다음처럼 말합니다.

```text
오늘 학습 종료
```

파일은 자동으로 바뀌지 않습니다. 재개 지점이 달라졌다면 Agent가
`STATE.md` 전체 교체안을 먼저 보여 줍니다.

## 한 모듈의 진행 방식

기본 수업은 다음 흐름을 사용합니다.

```text
충분한 연결 설명
→ 작은 수치 예제, shape trace, 또는 code/data-flow trace
→ 조건이 모두 적힌 통합 checkpoint 하나
→ 학습자 시도
→ 맞은 점, 고칠 점, 이유, 빠진 핵심을 한 번에 피드백
```

질문에 필요한 Tensor 값, shape, dtype, device, 데이터 분리, 평가 목적은
같은 메시지 안에 모두 적습니다. 단순 계산이 학습 목표가 아니면 계산은
Agent가 채우고 개념과 해석에 집중합니다. 이미 정확히 설명한 내용을
다른 표현으로 반복 시험하지 않습니다. 내부 routing label, ID, review tag,
metadata는 사용자가 요청하지 않는 한 채팅에 표시하지 않습니다.

막혔을 때는 현재 파일 경로와 실제 오류 또는 출력을 함께 지정하면
좋습니다.

```text
practice/<area>/<file>을 보고 지금 난 오류 원인부터 설명해줘.
```

Agent는 저장된 코드와 실제 출력에서 첫 blocker를 확인합니다. 별도 요청
없이 학습자 구현을 덮어쓰지 않습니다.

## STATE.md 반영

`STATE.md`에는 공개 가능한 최소 정보만 둡니다.

- pilot 시작일과 마지막 사용자 확인일
- 현재 source와 범위
- 이미 존재하는 관련 artifact의 짧은 사실
- 다시 확인할 항목
- 다음 독립 행동 하나

답변 원문, private 경로, 내부 ID, hash, phase, 점수표, 세션 이력, metrics는
넣지 않습니다. 공개 source를 고정하는 commit은 예외입니다.

재개 지점이 바뀌면 Agent가 항상 파일 전체 교체안을 먼저 보여 줍니다.
내용을 확인한 뒤 다음처럼 승인합니다.

```text
STATE 반영해
```

이 문장은 `STATE.md` 수정만 허용합니다. commit과 push는 각각 별도의
명시적 요청이 필요합니다. 파일이 없거나 실제 artifact와 충돌하면 Agent는
임의로 합치지 않고 사실관계와 교체안을 제시합니다.

## 첫 통합 준비도 진단

현재 첫 행동은 CS336 Assignment 1 진입 전 진단입니다. 학습자가 빈 Python
파일에서 다음을 직접 연결합니다.

1. deterministic synthetic 다중분류 데이터
2. 작은 `nn.Module`과 `forward`
3. train/validation 분리
4. raw logits, cross-entropy, optimizer
5. `zero_grad → forward → loss → backward → step`
6. validation loss와 accuracy
7. feature 수 또는 class 수를 바꾼 조건으로 한 번 전이
8. gradient 흐름, `zero_grad`, `detach`, `no_grad`, `requires_grad`, 주요
   Tensor 역할 설명. 오류가 발생했다면 수정 전에 세운 첫 원인 가설과
   이를 확인한 방법도 설명

빈 파일 구현·실행·debug, autograd 상태, 행렬곱·broadcasting·softmax·
cross-entropy 계약, baseline·validation·metric 사용을 모두 확인합니다.
부족한 부분만 최대 두 번의 집중 bridge로 다룹니다. 통과하면 Agent가
Assignment 1 진입을 제안하며, 사용자가 승인한 뒤에만 `STATE.md` 교체안을
반영합니다.

Pilot의 주축은 [Stanford CS336 Spring 2026](https://cs336.stanford.edu/)이고,
Assignment 1 기준은
[`a158843b20107949f1a8d7df1b05cd33b9166712`](https://github.com/stanford-cs336/assignment1-basics/tree/a158843b20107949f1a8d7df1b05cd33b9166712)입니다.
이번 라우팅 변경만으로 과제를 clone하거나 다운로드하지 않습니다.

준비도 진단은 현재 learning-lab의 Python 3.14 환경에서 실행합니다. 실제
Assignment 1에 진입하면 별도 sibling clone을 만들고 공식 pyproject에 맞춘
Python 3.12 또는 3.13의 독립 uv 환경을 사용합니다. 과제를 learning-lab의
dependency로 추가하거나 현재 `.venv`에 설치하지 않습니다.

## CS336 과제에서 받을 수 있는 도움

과제에 진입한 뒤에는 공식 AI 지침을 그대로 적용합니다.

- 학습자가 코드와 test를 직접 작성합니다.
- 학습자가 모든 bash command를 직접 실행하며, Agent는 assignment repo에서
  command를 실행하지 않습니다.
- Agent는 개념 설명, 오류 메시지 해석, sanity check, 일반적 리뷰만
  제공합니다.
- 공식 handout에 이미 나온 command의 의미와 학습자가 제공한 실행 결과는
  설명할 수 있지만, 과제 해결·자동화를 위한 새로운 command sequence는
  만들지 않습니다.
- 코드, pseudocode, patch, TODO 해답은 명시적으로 요청해도 제공하지
  않습니다.

## Practice, TIL, knowledge

일반 학습에서는 공식 과제가 practice 역할을 합니다. 작은 실행 확인은
채팅 과제로 제공할 수 있지만 새 metadata Notebook을 자동 생성하지
않습니다. 별도 실험을 저장하고 싶을 때만 exact 경로와 형태를 정합니다.

```text
practice/deep-learning/<topic>.py에 이 실험 뼈대를 만들어줘.
```

CS336 과제에서는 위와 같은 코드 생성 요청도 공식 제한 때문에 수행하지
않습니다. 기존 Notebook의 historical metadata는 실행에 영향을 주지 않는
기록으로 보존하며 현재 학습 상태로 사용하지 않습니다.

날짜별 TIL은 명시적으로 요청할 때만 작성합니다.

```text
오늘 대화에서 내가 설명한 내용과 실행한 결과로 오늘 TIL 초안을 만들어줘.
```

대화, draft, 또는 artifact를 정확히 지정해야 합니다. Agent 설명만으로
이해를 꾸미거나 다른 기록을 자동 수집하지 않습니다. `$save-today-til`은
이 standalone 작업을 명시적으로 고정하고 싶을 때만 사용합니다.

Knowledge도 확인된 입력을 지정할 때만 갱신합니다.

```text
내 설명과 practice/<exact-path>의 실행·해석을 바탕으로 knowledge 갱신을 제안해줘.
```

`$update-learning-knowledge`는 이 작업을 명시적으로 고정하는 opt-in
유틸리티입니다. 새로 확인된 durable understanding이 없으면 `NO_CHANGE`가
정상입니다. TIL과 knowledge 파일 수정은 commit을 자동 허용하지 않습니다.

## 자료와 Python 환경

Private 자료는 `materials/private/<course>/`에 두고 공개 저장소에 올리지
않습니다. 강의 제공 실습은 해당 course 아래
`course-provided-practice/`에 보존하고 학습자 산출물인 top-level
`practice/`와 섞지 않습니다.

Notion이나 PDF 원본을 정리할 때는 본문, 토글, 코드 들여쓰기, 출력, 표,
링크, 수식, 그림과 PDF 페이지를 확인합니다. 변환 무결성이 불확실하면
원본을 삭제하지 않습니다.

```bash
cd /home/jake/llm-research-learning-lab
uv sync
uv run python path/to/script.py
```

새 dependency는 `uv add`로 관리합니다. VS Code Notebook kernel은 이
저장소의 `.venv/bin/python`을 사용합니다. 실행하지 않은 결과는 기록하지
않고, dataset·model weight·credential·큰 생성물은 명시적 승인 없이 Git에
추가하지 않습니다.

## 저장 권한

학습 시작, 재개, 종료, `STATE 반영해`, TIL 작성, knowledge 갱신은 commit이나
push를 암묵적으로 허용하지 않습니다. 다음처럼 작업을 각각 명시합니다.

```text
변경 파일만 검토해줘.
이 파일들을 commit해줘.
방금 commit을 push해줘.
```

Commit 요청은 push 권한이 아닙니다. Agent는 unrelated 변경을 보존하고,
승인된 exact path만 stage한 뒤 staged diff를 확인합니다.
