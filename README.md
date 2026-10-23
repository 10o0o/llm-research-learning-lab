# LLM Research Engineer Learning Lab

단기 최우선은 **AX/AI 애플리케이션 취업 준비**, 장기 목표는 **LLM Research Engineer**입니다. 문의 처리 보조 서비스 하나를 작은 AI 기능→데이터/검색→도구 workflow→서비스 품질로 발전시키고, 이후 모델 학습 실험→작은 LM 하나→전문화 하나→독립 실험으로 깊이를 늘립니다. 목적·흐름·최소 선수를 먼저 배우고 대상 코드·실행·첫 해석은 직접 합니다. 고정 기간의 취업·완료를 보장하지 않습니다.

[현재 위치](./STATE.md) · [사용법](./USAGE.md) · [학습 로드맵](./ROADMAP.md) ·
[공통 지침](./AGENTS.md) · [역량 참고](./CURRICULUM.md) · [보류 자료](./DEFERRED.md)

## 가장 빠른 시작

저장소를 작업 공간으로 연 뒤 원하는 요청을 보냅니다.

| 요청 | 동작 |
|---|---|
| `오늘 학습 시작` | 승인된 현재 프로젝트/재선택 과정 안에서 연결된 활동을 이어서 진행 |
| `오늘 전체 학습 흐름 시작` / `전체 학습 흐름 시작` | 위 요청의 별칭; 같은 승인 범위에서 연결된 활동을 이어서 진행 |
| `계속` | `STATE.md`의 다음 독립 행동 재개 |
| `$study-session` | 같은 학습 절차를 명시적으로 호출 |
| `검토를 위해 잠시 멈춰` | 검토 대기; 학습 종료 절차는 아님 |
| `이번 주 회상` | 원할 때 수동 회상 요청; 자동 일정 없음 |
| `오늘 학습 종료` | 종료·확인된 북마크 갱신; 해당 세션의 승인된 변경 검증·커밋·푸시 |
| `$finish-chapter` / `이번 챕터 정리해줘` | 챕터 보관·회고·검증 및 허용된 로컬 커밋 |

실제 챕터 전환에서는 다음 챕터 전에 마무리가 기본으로 실행됩니다.
일반 종료나 주간 회상·AX/RE 단위 완료는 챕터 마무리·기록 생성·노트북 초기화를 실행하지 않습니다.

## 현재 실습과 학습 방식

현재 서비스 코드는 [문의 보조 Python 실습](./practice/ai-apps/README.md)에 있습니다.
실행 옵션·파일 역할·비공개 입력 조건은 그 안내를, 현재 재개 행동은 [STATE](./STATE.md)를 봅니다.
노트북은 분석·시각화·텐서 관찰에 필요할 때 사용하고, 반복 실행은 Python 본체 하나를 사용합니다.

[주교재·보조 자료](./CURRICULUM.md#프로젝트-수업의-주교재와-보조-자료)의 연결된 구간에서
목적·입출력·전체 흐름과 최소 선수를 배운 뒤 작은 기능을 작성→실행→첫 해석합니다.
실제 코드·출력으로 피드백하고 충분한 답을 반복 시험하지 않습니다. JS 경험을 바탕으로
현재 필요한 Python 표현을 함께 설명합니다. 막힘별 지원과 반복 수정 종료는
[기능 수업 판단](./.agents/references/learning-policies.md#feature-lesson-decisions)을 따릅니다.

튜터는 [허용된 준비](./.agents/references/learning-policies.md#learning-setup-and-starting-materials)를
맡고, 학습자는 대상 구현·실행·첫 해석을 맡습니다. 자체 프로젝트의 현재 명시적 수정 위임은
범위대로 수행하되 독립 숙달의 증거로 바꾸지 않습니다. 수업·피드백·회상·종료 절차는
[study-session](./.agents/skills/study-session/SKILL.md), 사용자가 요청할 수 있는 도움은
[USAGE](./USAGE.md), 공통 권한은 [AGENTS](./AGENTS.md)에 있습니다.

현재 범위는 STATE, 승인 범위·완료 기준은 ROADMAP입니다. 옛 P0~P5·전체 수학/과제·고정
시간/대회 의무를 시작 조건으로 복원하지 않습니다. [과거 북마크 인용](./practice/reviews/curriculum-transition.md)은
도움·미완료 보존용입니다. 문서 검토나 검증 통과는 학습 재개·교육 효과가 아닙니다.
별도 서비스 repo와 포트폴리오의 근거·한계는
[지속 발전 기준](./ROADMAP.md#초기-개발-공간과-서비스의-지속-발전)을 따릅니다.

공식 과제의 도움·비공개 제한과 개별 기록·챕터 정리 권한은 각각
[공식 과제 정책](./.agents/references/official-course-policies.md)과
[기록 정책](./.agents/references/recordkeeping-policies.md)에 있습니다.
일반 학습에서 이 정책 전체나 새 기록 양식을 추가 관문으로 요구하지 않습니다.

## 저장소 구조

| 위치 | 용도 |
|---|---|
| [`STATE.md`](./STATE.md) | 현재 범위와 다음 독립 행동 |
| [`materials/`](./materials/) | 원자료; 비공개 자료는 ignored `materials/private/` |
| [`practice/ai-apps/`](./practice/ai-apps/README.md) | 현재 문의 보조 서비스의 Python 코드·실행 안내 |
| [`practice/`](./practice/) | 학습자 실습·실험과 보관된 챕터 회고 |
| [`knowledge/`](./knowledge/) | 학습자 근거를 바탕으로 교정한 개념 노트 |
| [`til/`](./til/) | 요청한 날짜별 학습 기록 |
| [`challenges/`](./challenges/) | 외부 연습 플랫폼 작업 |
| [`ROADMAP.md`](./ROADMAP.md) | 승인된 AX/RE 범위·단위 계약·최소 산출물 |
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
