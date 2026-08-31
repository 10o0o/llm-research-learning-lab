# LLM Research Engineer Learning Lab

LLM Research Engineer를 목표로 **학습자료 구성 → 60~90분 대화형 수업 →
실습 → knowledge 갱신 → 다음 목표**를 반복하는 개인 학습 저장소입니다.

진도율이나 자동 mastery 판정보다, 학습자가 직접 설명하고 구현·실행한
뒤 결과를 해석한 근거를 우선합니다.

[자세한 사용법](./USAGE.md) · [학습 로드맵](./ROADMAP.md) ·
[역량·자료 기준](./CURRICULUM.md)

## 가장 빠른 시작

같은 저장소를 작업 공간으로 연 새 Codex 대화에서 target ID나 skill
이름을 직접 고를 필요가 없습니다. 하루 동안 여러 학습 사이클을
이어가려면 다음 한 문장으로 시작합니다.

```text
오늘 전체 학습 흐름 시작
```

`전체 학습 흐름 시작`도 같습니다. Agent가 현재 학습 근거에서 실제
다음 target을 정하고, 검토된 자료로 표준 60~90분 수업을 진행합니다.
수업 뒤에는 target에 맞는 실습을 제시하고, 학습자가 직접 구현·실행·
해석한 후 knowledge를 갱신하고 다음 target으로 넘어갑니다.

같은 날 새 대화를 열어도 다음처럼 이어갈 수 있습니다.

```text
계속
```

ignored `tmp/active-learning-flow.json`이 정확한 phase와 handoff/practice
경로를 보존합니다. 이는 운영 cursor일 뿐 진도 DB나 mastery 기록이
아닙니다.

오늘 흐름을 TIL 없이 멈추려면:

```text
오늘 학습 종료
```

완료된 오늘의 사이클을 나중에 한 번에 TIL로 정리하려면:

```text
오늘 TIL 저장해줘
```

TIL은 수업이나 실습의 선행 입력이 아닙니다. 이 명시적 요청에서만
완료 cycle, 실행·해석한 practice, knowledge 변경과 정확한 관련 commit을
검증해 개념 중심으로 종합하고, 날짜별 TIL 하나만 커밋합니다.

한 번의 수업만 하고 practice·knowledge·TIL까지 자동으로 이어가지
않으려면 다음처럼 말합니다.

```text
오늘 학습 시작
```

명시적으로 `짧게 하자`고 할 때만 short session을 사용합니다. Source의
focused source unit은 검토 비용 경계일 뿐 수업을 자동으로 짧게 만들지
않습니다. 범위는 페이지 목록이 아니라 연결된 단원·주제·예제군으로
선언하며, 내부적으로만 하나의 검증 가능한 source-anchor로 고정합니다.

## 기본 흐름

```text
ROADMAP endpoint와 learner evidence
        ↓
이번 cycle의 primary target과 선택적 inline bridge
        ↓
등록된 local source 또는 검토된 임시 official source
        ↓
선택 slice 독립 검토 + 3~5개 Module Plan
        ↓
60~90분 대화형 수업과 confirmed learner evidence
        ↓
Notebook / benchmark / dataset project / external challenge·competition
        ↓
직접 구현·실행·해석한 evidence
        ↓
knowledge 0~3개 갱신 또는 NO_CHANGE
        ↓
다음 target 계산과 다음 수업 준비
```

강의 수강, tutor 설명, 파일 존재, green checker, platform pass만으로는
이해나 완료를 인정하지 않습니다. 핵심 개념이 불확실하면 질문으로
종료하지 않고 설명 방식을 바꾸거나 `paused` 상태로 보존합니다.

## 저장소 구조

| 위치 | 용도 |
|---|---|
| [`materials/`](./materials/) | 강의자료와 원본; 비공개 자료는 ignored `materials/private/` |
| [`til/`](./til/) | 명시적 요청으로 작성하는 날짜별 학습 기록 |
| [`knowledge/`](./knowledge/) | 현재 이해를 주제별로 갱신하는 지식 베이스 |
| [`practice/`](./practice/) | Notebook, benchmark, dataset/Kaggle 실행 |
| [`challenges/`](./challenges/) | 짧은 외부 문제 제출 코드 |
| [`ROADMAP.md`](./ROADMAP.md) | 장기 전문화 방향과 정적 endpoint |
| [`CURRICULUM.md`](./CURRICULUM.md) | 목표 깊이·선수관계·필요 근거·자료 coverage |
| [`USAGE.md`](./USAGE.md) | 진입점, phase, 저장·승인 경계 |
| [`archive/`](./archive/) | 보존하는 과거 기록 |

`tmp/active-lesson-handoff.md`와
`tmp/active-lesson-sources/<lesson-id>/`도 ignored 운영 상태입니다.
Private 자료와 ignored cursor는 GitHub에 올라가지 않으므로 다른 clone이나
장치로 자동 동기화되지는 않습니다.
