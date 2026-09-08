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
| `오늘 학습 시작` | 현재 주강의 범위에서 연결된 module 하나를 진행 |
| `전체 학습 흐름 시작` 또는 `오늘 전체 학습 흐름 시작` | 승인된 같은 과정·과제 범위에서 module을 이어 가되 다른 과정으로 자동 진입하지 않음 |
| `계속` | `STATE.md`의 다음 독립 행동을 재개 |
| `오늘 학습 종료` | 학습을 멈추고 필요한 `STATE.md` 전체 교체안만 제시 |

`STATE.md`가 없거나 실제 artifact와 충돌하면 Agent는 다른 운영 상태를
추측하지 않습니다. 확인한 사실과 `STATE.md` 전체 교체안을 제시하고 사용자
결정을 기다립니다.

## 학습 방식

기본 module은 다음 순서로 진행합니다.

```text
원강의의 연결된 구간 시청과 충분한 보조 설명
→ 작은 예제의 직접 실행과 해석
→ 하나의 자기완결적인 통합 checkpoint에서 핵심 재구성
→ 정답·수정점·빠진 생각을 묶은 한 번의 전체 피드백
→ 관련 PyTorch 표현과 기존 KANT 실습에 연결
```

주강의 예제와 기존 KANT 과제가 실습 역할을 합니다. 짧은 실행 확인은 대화 안의 작은 과제로
제시할 수 있지만, 별도 metadata Notebook이나 학습 관리 artifact를 자동으로
만들지 않습니다. 강의 완료, Tutor 설명, 파일 존재, green test만으로 이해를
판정하지 않습니다.

주강의의 순서와 자료별 역할은 [학습 로드맵](./ROADMAP.md)을 따릅니다.
학습 시작은 새 준비도 진단이나 로드맵 검토가 아니라 현재 주강의 단원으로
연결합니다. AI는 원강의를 보조하며, 확인하지 않은 영상 내용이나 시각을
만들지 않습니다. 현재 설명에 필요한 선수개념을 보강한 뒤 같은 주강의로
돌아갑니다. 핵심 재구성에는 공식 API 문서를 참고해도 됩니다.

오류가 발생했다면 수정 전에 세운 첫 원인 가설과 이를 확인한 방법을
설명합니다. 오류를 일부러 만들거나 이미 이해한 내용을 반복 시험하지 않습니다.

## CS336의 엄격한 AI 경계

[CS336 Assignment 1 공식 AI 지침](https://github.com/stanford-cs336/assignment1-basics/blob/a158843b20107949f1a8d7df1b05cd33b9166712/AGENTS.md)을
따릅니다.

- 학습자가 과제 코드를 직접 작성하고 제공된 테스트를 실행합니다.
- AI는 개념 설명, 오류 메시지 해석, sanity check와 일반적인 review만
  제공합니다.
- 학습자가 모든 bash command를 직접 실행하며, AI는 assignment repo에서
  command를 실행하지 않습니다.
- AI는 공식 handout에 이미 나온 command의 의미와 학습자가 제공한 실행
  결과는 설명할 수 있지만, 과제 해결·자동화를 위한 새로운 command
  sequence는 만들지 않습니다.
- 명시적으로 요청해도 AI는 과제 코드, pseudocode, patch, TODO 해답을
  제공하지 않습니다.

기초 실습은 learning-lab의 Python 3.14 환경에서 실행합니다. 실제 과제는
별도 sibling clone과 Python 3.12 또는 3.13의 독립 uv 환경을 사용하며,
과제 dependency를 learning-lab이나 현재 `.venv`에 합치지 않습니다.

CS336 복귀는 로드맵의 구현·실행·해석 근거로 제안합니다. 기존 작업을
보존하며, 사용자 승인 없이 현재 과정을 바꾸지 않습니다.

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
