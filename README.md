# LLM Research Engineer Learning Lab

LLM Research Engineer를 목표로 공부하는 가벼운 개인 학습 저장소입니다.
복잡한 진도 관리보다 충분한 설명, 작은 실행, 학습자의 독립 시도와 해석을
우선합니다.

[현재 학습 위치](./STATE.md) · [자세한 사용법](./USAGE.md) ·
[학습 로드맵](./ROADMAP.md) · [역량 참고](./CURRICULUM.md)

## 가장 빠른 시작

이 저장소를 작업 공간으로 연 Codex는 [`STATE.md`](./STATE.md)의 현재 범위와
다음 독립 행동을 읽습니다. `STATE.md`는 재개용 북마크일 뿐, 숙달 기록이나
점수표가 아닙니다.

| 요청 | 동작 |
|---|---|
| `오늘 학습 시작` | 현재 범위에서 연결된 module 하나를 진행 |
| `전체 학습 흐름 시작` 또는 `오늘 전체 학습 흐름 시작` | 같은 source·과제 안에서 module을 이어 가되 새 강의로 자동 진입하지 않음 |
| `계속` | `STATE.md`의 다음 독립 행동을 재개 |
| `오늘 학습 종료` | 학습을 멈추고 필요한 `STATE.md` 전체 교체안만 제시 |

`STATE.md`가 없거나 실제 artifact와 충돌하면 Agent는 다른 운영 상태를
추측하지 않습니다. 확인한 사실과 `STATE.md` 전체 교체안을 제시하고 사용자
결정을 기다립니다.

## 학습 방식

기본 module은 다음 순서로 진행합니다.

```text
충분한 설명
→ 작은 수치 예시와 shape trace
→ 하나의 자기완결적인 통합 checkpoint
→ 학습자의 독립 시도
→ 정답·수정점·빠진 생각을 묶은 한 번의 전체 피드백
```

공식 과제가 실습 역할을 합니다. 짧은 실행 확인은 대화 안의 작은 과제로
제시할 수 있지만, 별도 metadata Notebook이나 학습 관리 artifact를 자동으로
만들지 않습니다. 강의 완료, Tutor 설명, 파일 존재, green test만으로 이해를
판정하지 않습니다.

## 첫 준비도 진단

현재 첫 행동은 Stanford CS336 Assignment 1 진입 전 통합 진단입니다.
학습자는 빈 Python 파일에서 다음을 직접 연결합니다.

- 고정 seed의 deterministic synthetic 다중분류 데이터
- 작은 `nn.Module`과 `forward`
- train/validation 분리
- raw logits, cross-entropy, optimizer
- `zero_grad → forward → loss → backward → step`
- validation loss와 accuracy
- feature 수 또는 class 수가 다른 조건으로의 한 번의 전이

실행 뒤에는 gradient 흐름, `zero_grad`, `detach`, `no_grad`,
`requires_grad`, 주요 Tensor의 역할과 첫 오류 가설을 자신의 말로
설명합니다. 부족한 항목만 최대 두 번의 집중 bridge에서 다루고,
Transformer·tokenizer·systems 세부사항은 CS336 진행 중 필요할 때
보충합니다.

## CS336의 엄격한 AI 경계

[CS336 Assignment 1 공식 AI 지침](https://github.com/stanford-cs336/assignment1-basics/blob/a158843b20107949f1a8d7df1b05cd33b9166712/AGENTS.md)을
따릅니다.

- 학습자가 과제 코드와 공식 test를 직접 작성하고 실행합니다.
- AI는 개념 설명, 오류 메시지 해석, sanity check와 일반적인 review만
  제공합니다.
- 명시적으로 요청해도 AI는 과제 코드, pseudocode, patch, TODO 해답을
  제공하거나 과제 명령을 대신 실행하지 않습니다.

필수 준비도를 통과하면 Agent가 Assignment 1 진입을 제안합니다. 사용자가
승인한 뒤에만 다음 `STATE.md` 교체안을 준비합니다.

## 파일 변경과 저장

학습 시작이나 `계속`은 파일 변경 권한이 아닙니다. Agent는 다음 작업을
자동으로 하지 않습니다.

- `STATE.md`, TIL 또는 knowledge 갱신
- 새 practice artifact 생성
- 다음 강의나 source 자동 선택·등록
- commit 또는 push

`STATE.md`를 바꿀 때는 항상 전체 교체안을 먼저 검토합니다. 사용자가 그
문구를 승인하고 `STATE 반영해`라고 명시한 경우에만 파일을 교체합니다.
Commit과 push는 각각 별도의 명시적 요청이 필요합니다.

날짜별 기록이 필요하면 `오늘 TIL 저장해줘` 또는 `$save-today-til`을,
재사용할 개념 노트가 필요하면 `$update-learning-knowledge`를 명시적으로
호출합니다. 두 도구 모두 현재 대화나 사용자가 정확히 지정한 artifact만
사용하며, 자동 commit이나 push를 수행하지 않습니다.

## 저장소 구조

| 위치 | 용도 |
|---|---|
| [`STATE.md`](./STATE.md) | 공개 가능한 현재 범위와 다음 독립 행동 |
| [`materials/`](./materials/) | 강의자료와 원본; 비공개 자료는 ignored `materials/private/` |
| [`til/`](./til/) | 명시적으로 저장하는 날짜별 학습 기록 |
| [`knowledge/`](./knowledge/) | 확인된 이해를 정리하는 주제별 개념 노트 |
| [`practice/`](./practice/) | 보존된 실행 Notebook과 실험 artifact |
| [`challenges/`](./challenges/) | 짧은 외부 문제 풀이 코드 |
| [`ROADMAP.md`](./ROADMAP.md) | 장기 학습 방향 참고 |
| [`CURRICULUM.md`](./CURRICULUM.md) | 역량과 기존 자료 범위 참고 |
| [`archive/`](./archive/) | 수정하지 않고 보존하는 과거 기록 |

공개 저장소에는 답변 원문, private 경로, 내부 ID·hash, 세션 이력이나
평가 점수를 기록하지 않습니다. 실행하지 않은 결과도 기록하지 않습니다.
