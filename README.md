# LLM Research Engineer Learning Lab

LLM Research Engineer를 목표로 공부하는 가벼운 개인 학습 저장소입니다.
공식 자료의 설명과 실습, 학습자의 독립 시도와 해석을 중심으로 진행합니다.

[현재 위치](./STATE.md) · [사용법](./USAGE.md) · [학습 로드맵](./ROADMAP.md) ·
[공통 지침](./AGENTS.md) · [역량 참고](./CURRICULUM.md) · [보류 자료](./DEFERRED.md)

## 가장 빠른 시작

저장소를 작업 공간으로 연 뒤 원하는 요청을 보냅니다.

| 요청 | 동작 |
|---|---|
| `오늘 학습 시작` | 현재 주강의의 연결된 모듈 하나 진행 |
| `오늘 전체 학습 흐름 시작` / `전체 학습 흐름 시작` | 승인된 같은 과정·과제 범위에서 모듈을 이어감 |
| `계속` | `STATE.md`의 다음 독립 행동 재개 |
| `$study-session` | 같은 학습 절차를 명시적으로 호출 |
| `이번 주 회상` | 사용자가 주간 마지막 세션에서 수동 회상 요청 |
| `오늘 학습 종료` | 종료하고, 재개 위치가 바뀌었을 때만 북마크 갱신 |
| `$finish-chapter` / `이번 챕터 정리해줘` | 챕터 보관·회고·검증 및 허용된 로컬 커밋 |

실제 챕터 전환에서는 다음 챕터 전에 마무리가 기본으로 실행됩니다.
일반 종료나 주간 회상은 챕터 마무리를 실행하지 않습니다.

## 학습 방식과 권한

[study-session 스킬](./.agents/skills/study-session/SKILL.md)에 수업·피드백·회상
절차를 모았습니다. Agent는 [공통 지침](./AGENTS.md)의 연결을 통해 스킬을
직접 읽으므로, 특정 도구의 자동 발견 기능에 의존하지 않습니다.

현재 공식 자료를 확인하고 연결된 설명을 들은 뒤 학습자가 직접 시도합니다.
공식 실습의 독립 설명과 변경 조건 적용을 근거로 확인하며, 도움받은 성공과
무보조 성공을 구분합니다. 단순 동의나 실행 성공만으로 이해를 인정하지 않습니다.
주간 회상은 요청할 때 지난주 개념 두 개와 더 이전 개념 하나를 다룹니다.

과정·판본·필수 범위는 [ROADMAP.md](./ROADMAP.md)에 있습니다. 공식 과제를
보충 예제나 완성 노트북 실행으로 대체하지 않습니다. 공식 과제 답안과
저작권 자료는 별도 비공개 공간에 두며, 과정별 도움 제한은 공통 지침을 따릅니다.

`STATE.md`는 재개 북마크입니다. 확인된 위치가 바뀌면 사전 승인 없이 수정하되
그 자체로 커밋·푸시를 허용하지 않습니다. TIL·knowledge의 단독 작성은 명시적으로
요청합니다. 챕터 마무리의 보관·knowledge·초기화·로컬 커밋 권한은
[finish-chapter](./.agents/skills/finish-chapter/SKILL.md)에 한정되며, 푸시는 포함하지 않습니다.

## 저장소 구조

| 위치 | 용도 |
|---|---|
| [`STATE.md`](./STATE.md) | 현재 범위와 다음 독립 행동 |
| [`materials/`](./materials/) | 원자료; 비공개 자료는 ignored `materials/private/` |
| [`practice/`](./practice/) | 학습자 실습·실험과 챕터 회고 |
| [`knowledge/`](./knowledge/) | 학습자 근거를 바탕으로 교정한 개념 노트 |
| [`til/`](./til/) | 요청한 날짜별 학습 기록 |
| [`challenges/`](./challenges/) | 외부 연습 플랫폼 작업 |
| [`ROADMAP.md`](./ROADMAP.md) | 장기 방향과 Phase 예산 |
| [`CURRICULUM.md`](./CURRICULUM.md) | 정적인 역량·자료 참고 |
| [`DEFERRED.md`](./DEFERRED.md) | 제외·보류 범위와 복귀 조건 |
| [`archive/`](./archive/) | 보존하는 과거 기록 |

## 지식 서재 웹

`knowledge/`를 홈·검색·분야별 목록·상세 화면으로 읽는
[GitHub Pages 사이트](https://10o0o.github.io/llm-research-learning-lab/)입니다.
일반 학습 중에는 사이트를 변경하지 않습니다.

Node와 npm을 준비한 뒤 `web/`에서 `npm ci`, `npm run build`, `npm run preview`를
실행합니다. [웹 실행·검증 안내](./web/README.md)를 참고하세요. `main`에 push하면
`public-validation` 검증 후 배포합니다. 수동 재배포는 Actions의 해당 workflow에서
`main`을 선택하고 **Run workflow**를 실행합니다. 다른 branch와 PR은 검증만 합니다.
실패하면 해당 job 로그를 확인합니다. 이 안내는 자동 push 권한이 아닙니다.
