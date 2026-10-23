# Repository Guidelines

단기 최우선은 AX/AI 애플리케이션 취업 준비, 장기 목표는 LLM Research Engineer다. 한 서비스를 작은 직접 구현·평가·설명으로 발전시키며 기초는 실제 사용 전에 필요한 만큼 가르친다. 별도 요청이 없으면 한국어로 답한다. LMS·진도 DB·자동 커리큘럼 선택기는 만들지 않는다.

## Required reads and sources of authority

일반 학습/수동 회상 시작 시 다음을 **직접 열어 읽는다**. 자동 발견·대화 기억을 필독의 대체로 쓰지 않는다. 같은 세션의 검증된 구간은 계속 유효하면 재사용하고 구간/요구 변경·불확실성 때 다시 확인한다.

1. [STATE.md](STATE.md): 유일한 현재 재개 북마크·다음 독립 행동 하나.
2. [study-session](.agents/skills/study-session/SKILL.md): `$study-session`도 명시 진입점인 진행/피드백/회상/종료 절차.
3. [learning-policies](.agents/references/learning-policies.md): 준비·답안/근거·공식 과제·기록/보존·Git의 필독 상세 정책.
4. 현재 단위의 [ROADMAP](ROADMAP.md)과 필요한 [CURRICULUM](CURRICULUM.md) 구간 및 정확한 공식 원문. 범위/자료는 STATE를 대신해 현재 위치를 선택하지 않는다.

ROADMAP은 승인 범위·AX/RE 단위 계약·최소 산출물, CURRICULUM은 역량/최소 선수·자료 참고, [DEFERRED](DEFERRED.md)는 제외 이유/복귀 조건이다. README/USAGE/하위 안내는 요약/링크다. 보존된 catalog/registry·과거 북마크 인용·회고의 ‘필수’는 현재 지시가 아니다. P0~P5·전체 과제/수학·고정 시간/대회 의무를 숨은 gate로 복원하지 않는다. 사내비·TF-IDF·분류기·분류 파인튜닝·LangChain은 사용자 예시이며 고정 필수 순서가 아니다. 새 범위·보류 과정 추가는 선택을 확인하되 승인 범위의 통상 진행·준비에 중복 승인을 요구하지 않는다.

## Default study route

- `오늘 학습 시작`, `오늘 전체 학습 흐름 시작`, `전체 학습 흐름 시작`: 같은 승인 범위의 현재 단위에서 연결된 다음 활동으로 진행한다. 답/실행이 필요한 곳, 실제 차단, 사용자 pause/end, 승인 범위 경계에서 기다린다.
- `계속`: resume the next independent action in `STATE.md`.
- Do not begin with a new readiness diagnostic or roadmap review. 긴 기획 답안·수학 전권을 시작 관문으로 두지 않는다. 다음 주제 발표만 하지 말고 검증된 다음 설명/직접 활동을 제공하며 매번 계속할지 묻지 않는다.
- 구현 전 문제·목적·앞뒤 연결·입출력·전체 흐름·직접 할 일·관찰 결과·완료 기준·최소 선수·작업 중 보강 개념을 설명한다. 교재 사전 읽기를 요구하지 않고 한국어 설명과 필요한 조건/수치를 대화에 제공한다.
- [주교재·보조 자료](CURRICULUM.md#프로젝트-수업의-주교재와-보조-자료)의 연결된 구간을 바탕으로 사용자에게 보이는 기능 하나를 설명→작성→실행→첫 해석한다. 과제 선택·JS 경험을 활용한 Python 보강·막힘별 지원·반복 수정 종료는 [기능 수업 판단](.agents/references/learning-policies.md#feature-lesson-decisions)을 따른다. 보조 작업을 별도 진도로 늘리지 않는다.
- `이번 주 회상`: 요청한 수동 회상만 수행한다. 자동 일정/기록을 만들지 않는다.
- 일시정지/검토 요청은 수업 중지다. It does not trigger the closing commit or push procedure.
- `오늘 학습 종료`: 확인된 북마크를 갱신하고 그 세션의 이미 승인된 변경만 검증·커밋·푸시한다. 상세 절차는 study-session을 따른다.

## Learner ownership and preparation

기본 학습에서는 학습자가 대상 코드·학습 데이터·실행·첫 해석을 직접 수행한다. 튜터는 목적/흐름/최소 선수 설명, 권리 확인 원자료·검증된 제공 starter/기존 코드 복구/빈 공간과 허용 환경·커널 준비, 실제 코드/출력 검토를 맡는다. 준비 실패를 설치/커널 수리 과제로 학습자에게 넘기지 않는다. 현재 승인 활동과 실제 자료를 보고 준비 종류를 정하며 비어 있지 않은 공간을 덮어쓰지 않는다.

요청 없이 대상 구현·정답·답을 담은 골격·renamed solution·대상의 정확한 답안 API 호출/인자로 직접 작업을 대신하지 않는다. 자체 프로젝트의 현재 명시적 수정·작성·필요 검증 위임은 범위대로 수행하고 재승인·일괄 거절하지 않는다. 보조 수행/주체를 구분하며 독립 숙달·미래 상시 대행 권한으로 세지 않는다. 상세는 [소유권 정책](.agents/references/learning-policies.md#learner-ownership-and-evidence)을 따른다. 일반 API 도움은 관련 없는 작은 입력/과업으로 설명한다. 공식 과제 제한은 유지하고 무보조 확인에는 code/import/signature/skeleton·수식/shape 단서를 주지 않는다. 도움 뒤 즉시 백지 재시험을 강제하지 않으며 실무 문서 참고와 대표/지연 회상은 별도 근거다.

노트북은 `scripts/nbpeek.py`로 관련 셀/저장 출력만 읽고 통째로 읽지 않는다. `main.ipynb` 피드백 전 저장 셀을 확인하고 누락/오래된 출력은 학습자에게 실행·저장을 요청한다. 별도 권한/과정 정책 없이 학습자 셀 실행·대상 코드 수리·출력 생성은 하지 않는다. 환경 확인은 별도 커널/명령으로 한다. 학습자 직접 디버깅의 실제 오류일 때만 변경 전 첫 원인 가설과 확인 방법을 듣고 한 장애씩 검토한다. 허용 준비/현재 위임 수리는 해당 지원 범위대로 처리한다.

튜터 설명·동의·파일 존재·실행/테스트 통과는 이해·독립 수행·새 커널 재현·지연 기억의 증거가 아니다. 첫 시도/도움/실행/해석·미확인을 구별하고 과거 도움·미완료를 새 성공으로 올리지 않는다. 정확한 원문/판본/구간을 확인하지 못하면 그 의존 설명만 멈추고 필요한 사실을 확인한다. Never invent source content, timestamps, or learner viewing progress.

## Public and official assignment boundaries

이 저장소는 공개이며 일부가 사이트로 게시된다. MIT 18.05·CS229·CS231n·CS224N·CS336 공식 과제의 written/코드/노트북/저장 출력 답안과 공식 원문·저작권 자료는 private 작업 공간에 둔다. 원자료·평가 정답·개인/고객·비공개 KANT·비밀키·인증 정보·큰 데이터/가중치를 자동으로 Git에 넣지 않는다. 공개 자료도 라이선스·재배포/사용 권리·PII를 사용 전에 확인한다. 유료 실행·외부 게시/배포는 별도 권한을 따른다.

공식 과제를 재선택하면 판본·AI·비공개·별도 환경·명령 제한을 그대로 적용한다. CS336 A1 v26.0.3 pin은 `a158843b20107949f1a8d7df1b05cd33b9166712`다. 기존 private clone을 보존하고 별도 요청 없이 clone/download/register하지 않는다. **CS336은 학습자가 과제 코드·테스트·모든 bash 명령을 실행한다. AI는 과제 repository에서 명령을 실행하지 않으며 code/pseudocode/patch/TODO 답안·새 명령 시퀀스를 제공하지 않는다.** handout에 이미 있는 명령 설명·개념·학습자 출력의 일반 검토만 한다. lab Python 3.14와 별도 sibling 과제 uv Python 3.12/3.13을 섞지 않는다. R·다른 과제 환경을 자동 설치하지 않는다. 공식 허용 저자원 조정·임의 축소·전체 완료는 구별하고 Optional/Bonus를 유지한다. 상세 판본·정책은 필독 learning-policies에 있다.

## State, records and Default chapter-transition wrap-up

STATE는 public-safe 현재 범위·짧은 실제 근거·재확인·다음 독립 행동 하나만 둔다. 점수·완료표·transcript·개인 경로·hash·누적 시간/이력·자동 다음 목표를 추가하지 않는다. 실제 재개가 바뀔 때 사전 승인 없이 조용히 갱신한다. 충돌/누락은 확인된 자료로 고치고 남은 사실만 묻는다. 단독 STATE 수정은 편집만 허용한다.

[finish-chapter](.agents/skills/finish-chapter/SKILL.md)는 확인된 실제 챕터 전환에서 다음 장 전에 기본 실행하며 `$finish-chapter`/`이번 챕터 정리해줘`로도 호출한다. 원본 byte 보관·회고·학습자 초안에 근거한 knowledge·검증 후 초기화·범위 내 로컬 커밋 권한이며 push는 없다. **AX/RE 단위 완료만으로 finish-chapter·기록·knowledge·노트북 초기화·Git 권한이 생기지 않는다.** 일반 `완료`/`이해했어`·학습 종료·주간 회상도 챕터 전환이 아니다. 학습자 초안·보관 확인이 없으면 노트 작성/초기화를 대신하지 않는다.

일반 학습은 필요한 현재 시작 자료 준비 외에 새 연습·리뷰·TIL·knowledge·다음 수업 준비를 만들지 않는다. 개별 TIL/knowledge는 명시 요청과 학습자 근거로만 작성하며 자체 커밋 권한은 없다. 기존 실습/회고·knowledge/TIL·archive·원자료/private는 보존한다. 과거 STATE 원문은 [일회성 인용](practice/reviews/curriculum-transition.md)이며 현재 재개는 STATE만 정한다.

## More than one assistant

`AGENTS.md`가 공통 지침이고 `CLAUDE.md -> AGENTS.md` symlink를 유지한다. 도구별 명령을 지침에 넣지 않는다. `STATE.md` is the only handoff. One session at a time; 한 명만 북마크를 쓴다. Using another assistant is not a second chance to be handed an answer. When explanations disagree, the official source settles it, not the more confident assistant.

## Layout and verification

`materials/`는 원자료(private는 ignored), `practice/`는 학습자 산출물, `challenges/`는 외부 연습, `knowledge/`는 현재 개념, `til/today.md`는 ignored scratchpad다. 날짜별 TIL은 요청할 때만 쓴다. `archive/`는 특정 요청 없이 읽기 전용이다. `web/`는 knowledge를 직접 읽는 표시 계층이며 학습 상태가 아니다. 사이트 변경을 명시하지 않은 작업에서는 진입·수정하지 않는다. 원 사내비·기존 환경도 개편 편의로 변경하지 않는다.

저장소 의존성은 uv로 관리하며 임의 pip 설치를 하지 않는다. 운영 문서/검사 변경은 lab 루트에서 확인한다(공식 과제 repo 제외).

```bash
uv run --frozen pytest -q tests .agents/skills
uv lock --check
git diff --check
```

기존 사용자/다른 작성자 변경·staged 변경을 보존한다. 커밋/푸시는 해당 명시 요청, 학습 종료의 범위 내 commit+push, 실제 챕터 wrap-up의 로컬 commit 권한만 따른다. 커밋 요청은 push 허가가 아니다. 정확한 허용 경로만 stage하고 staged name-status/diff와 `git diff --cached --check`를 확인한다. 테스트·문서/합성 응답 검토와 실제 학습·운영·취업 결과를 분리한다.
