# LLM Research Engineer Learning Lab

LLM Research Engineer를 목표로 **학습 목표 → 검토된 자료 → 대화형 수업 → TIL → 실행 실습 → 지식 정리**를 연결하는 개인 학습 저장소입니다.

완벽한 학습 관리 시스템이나 진도율보다, 나중에 다시 확인할 수 있는 학습자 설명과 실제 실행 근거를 우선합니다.

[자세한 사용법](./USAGE.md) · [학습 로드맵](./ROADMAP.md) · [역량·자료 기준](./CURRICULUM.md)

## 가장 빠른 시작

이 저장소를 작업 공간으로 연 Codex의 새 대화에서 target ID나 skill 이름을 직접 고를 필요는 없습니다. 기본 수업과 TIL 저장까지 시작하려면 다음처럼 말하면 됩니다.

```text
오늘 학습 시작
```

Agent가 현재 TIL·knowledge·실행된 practice에서 다음 target과 자료를 정하고, source 검토 범위와 별개인 **표준 심화 세션**을 진행합니다. 표준 세션은 동기 → 개념 모형 → worked example → 한계·반례 → 통합 전이까지 이어지며, 빠르게 맞혀도 이 arc 자체를 생략하지 않습니다. 마지막에는 확인된 학습자 답변으로 자연스러운 TIL을 구성하고 그 날짜별 TIL 하나만 자동 커밋합니다. 별도의 `오늘 학습 내용 검토`나 `저장해줘` 요청은 필요 없습니다.

수업 뒤 실습·knowledge·다음 target까지 한 사이클 전체를 이어가려면 다음처럼 말합니다.

```text
전체 학습 흐름 시작
```

`전체 학습 흐름으로 진행해줘`도 같은 뜻입니다. 일반 `오늘 학습 시작`과 동일하게 수업·TIL 자동 커밋까지 진행한 뒤, 실습 판정·학습자 실행·evidence-backed knowledge·다음 target 미리보기까지 기존 전문 skill을 이어서 연결합니다. 완료된 practice와 knowledge의 제한된 자동 커밋을 포함하지만 push는 포함하지 않습니다.

자동 커밋 없이 수업부터 시작하고 싶다면 다음과 같이 요청합니다.

```text
현재 학습 근거로 다음 목표를 정해서 수업을 시작해줘.
저장과 커밋은 내가 요청할 때만 해줘.
```

명시적으로 `짧게 하자`고 말한 경우에만 short 세션을 사용합니다. Source의
focused slice가 작다는 이유만으로 수업 자체를 짧게 줄이지 않습니다.

진행 중인 수업이나 TIL 저장은 로컬 `tmp/active-lesson-handoff.md`가 있을 때 다음처럼 재개합니다.

```text
현재 진행 중인 수업을 이어서 해줘.
```

단순히 `계속`이라고 해도 같은 active 단계에서 재개합니다. 수업이 끝났다면 TIL 구성·검증·날짜별 TIL 단독 커밋을 이어갑니다. 기존 handoff가 `저장과 커밋은 요청할 때만` 정책을 기록했다면 그 선택은 그대로 유지됩니다. 검토 중 수정 가능한 문제가 발견되면 Agent가 같은 흐름에서 계약을 고치고 targeted recheck를 거치므로, 사용자가 reset 문구나 target ID를 다시 입력할 필요가 없습니다. 실제로 멈추는 경우는 source 손상·접근 실패, 해결 불가능한 사실 모호성, 또는 사용자의 범위 선택이 필요한 때뿐입니다.

새 대화에서 Notebook 실습을 재개할 때는 추측을 막기 위해 정확한 경로를 함께 줍니다.

```text
practice/<area>/<topic>.ipynb를 이어서 하자.
```

상황별 시작 문장과 각 요청이 허용하는 저장·커밋 범위는 [새 대화에서 시작하기](./USAGE.md#새-codex-대화에서-시작하기)에 정리되어 있습니다.

## 어떻게 이어지는가

```text
ROADMAP endpoint와 실제 학습자 근거
        ↓
이번 사이클의 primary target과 선택적 bridge 결정
        ↓
등록된 로컬 자료 또는 검토된 임시 공식 자료 해결
        ↓
선택 범위만 검토한 handoff → 기본 표준 심화 수업
        ↓
확인된 학습자 답변으로 TIL 자동 구성·단독 커밋
        ↓
전체 학습 흐름 요청일 때만 target에 맞는 실습
        ↓
직접 구현·실행·해석한 근거로 knowledge와 다음 target 갱신
```

별도 진도 DB는 없습니다. 새 학습 사이클마다 다음 파일에서 현재 상태를 다시 계산합니다.

| 근거 | 역할 |
|---|---|
| `til/YYYY/MM/YYYY-MM-DD.md` | 당시 직접 배우고 설명한 내용 |
| `knowledge/` | 현재 다시 설명할 수 있는 개념 |
| `practice/` | 직접 구현·실행·해석한 결과 |
| `challenges/` | target이나 TIL에 명시적으로 연결된 외부 문제 근거 |
| `tmp/active-lesson-handoff.md` | 같은 로컬 작업 공간에서 진행 중인 수업을 재개하기 위한 임시 상태 |

강의 수강, tutor 설명, 파일 존재, green checker만으로는 이해나 숙련을 인정하지 않습니다.

## 구조

| 위치 | 용도 |
|---|---|
| [`materials/`](./materials/) | 강의자료와 원본 자료; 비공개 자료는 ignored `materials/private/`에 보관 |
| [`til/`](./til/) | 그날 배운 것과 생각을 남기는 날짜별 학습 일기 |
| [`knowledge/`](./knowledge/) | 지금 이해하고 있는 내용을 주제별로 갱신하는 지식 베이스 |
| [`practice/`](./practice/) | 직접 실행한 Notebook, benchmark, dataset 실험 |
| [`challenges/`](./challenges/) | 외부 문제 플랫폼의 제출 코드와 학습 기록 |
| [`ROADMAP.md`](./ROADMAP.md) | 장기 전문화 방향과 정적 endpoint |
| [`CURRICULUM.md`](./CURRICULUM.md) | 역량별 깊이·선수 관계·필요 근거와 자료 충족도 |
| [`USAGE.md`](./USAGE.md) | 새 대화 진입점과 단계별 학습 운영 방법 |
| [`archive/`](./archive/) | 구버전 TIL 보관 |

실제로 자주 사용하는 곳은 `til/`, `knowledge/`, `practice/`, `challenges/`입니다. 자료 등록, 단계별 skill 호출, TIL·실습 검증, 전체 흐름의 권한 경계는 [USAGE.md](./USAGE.md)를 참고합니다.
