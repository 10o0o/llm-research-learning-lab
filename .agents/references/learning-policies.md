# Learning policies

이 파일은 현재 승인 활동의 **필독 상세 정책**이다. 루트 [AGENTS](../../AGENTS.md)의 핵심 경계를 유지하며 [study-session](../skills/study-session/SKILL.md)과 함께 직접 읽는다. 자동 로딩을 가정하지 않는다. 범위는 [ROADMAP](../../ROADMAP.md), 선수/자료는 [CURRICULUM](../../CURRICULUM.md), 보류 이유/조건은 [DEFERRED](../../DEFERRED.md), 현재 재개는 [STATE](../../STATE.md)만 정한다.

AX/RE는 static reference이며 진도 키가 아니다. 기존 P0~P5·전체 PS·수학 전권·고정 시간·대회 의무는 현재 gate가 아니다. 역사적 catalog/registry·과거 STATE 인용·회고는 그 당시 도움·미완료를 보존하는 참고이며 새 과제 선택기나 성과 증거로 쓰지 않는다. 튜터는 한 서비스의 목적/입출력/흐름과 최소 선수를 설명하고 학습자는 작은 직접 구현·실행·첫 해석으로 이어간다. 더 깊은 수학/확률/최적화는 실제 공백의 의존 작업 전에 보강한다.

## State changes and authorization

- `STATE.md` is the only handoff. Read it at the start of every session. 현재 승인 경로·단위·범위, 간결한 실제 근거, 재확인과 다음 독립 행동 하나만 담는다. 날짜는 public-safe pilot 시작일 등 필요한 북마크 정보에 한정한다.
- Unit IDs are a static reference into ROADMAP, not completion keys. Never add a percentage, a score, a readiness judgement, an hour tally, a checklist of finished items, or a computed next target. Never put learner answer transcripts, private paths, internal IDs, hashes, readiness scores, session history, or metrics in STATE. A public source commit pin is allowed.
- Update `STATE.md` without prior proposal or approval when the confirmed next independent action meaningfully changes. Do not edit it for each corrected answer when the resume action stays the same. Keep its basis concise and current; distinguish completed work, planned work, and unverified claims. Do not infer understanding from tutor explanations or successful execution alone. Keep routine edits quiet; report one when the user asks for status, at an explicit study stop, or when a real blocker or conflict needs explanation.
- If STATE is missing or conflicts with tracked artifacts, report the facts and repair it from confirmed evidence. Ask only about unresolved facts. Never derive current state from ignored temporary files or old notebook metadata. When STATE incorrectly assigns permitted preparation to the learner, repair that responsibility from the verified source and actual artifacts; this is no new exercise or mastery claim.
- A bookmark update does not authorize a new course, a sequence change, skipped selected requirements or a new held track. Within already approved scope, ordinary progression and prerequisite repair need no repeated permission.
- Updating `STATE.md`, automatically or on request, authorizes only the file edit. An explicit study-stop request is the standing exception: the learner has authorized a scoped commit and push without another confirmation. A pause or review request does not trigger the closing commit or push procedure.
- AX/RE 단위 완료 자체는 챕터 경계가 아니다. 실제 챕터 마무리·모듈 완료 등으로 다음 행동이 달라질 때만 북마크를 갱신한다. 경로 개편 당시 유일했던 과거 근거는 [원문 인용](../../practice/reviews/curriculum-transition.md)에 보존하고 이 인용으로 현재 지시를 정하지 않는다.

## Learning setup and starting materials

The tutor owns permitted environment setup and starting materials for the
current approved activity. A study-start or resume request includes this
routine preparation; do not ask the learner to choose its scope or manually
copy preparation cells. Determine the starting state from the current goal,
the verified course requirements, and the actual artifacts before applying
implementation restrictions.

| Current activity | Starting state prepared by the tutor |
|---|---|
| Work using a supplied starter | Copy the verified starter; preserve its unfinished learner-target portions |
| Fresh-kernel reproduction of existing code | Restore verified existing code unchanged into a working copy; remove that copy's old outputs and execution counts |
| Representative unassisted reconstruction or cold recall | Prepare the environment and a blank implementation space; provide no code, imports, signatures, or skeletons |

Permitted preparation includes creating or restoring the necessary current
working notebook or script, synchronizing the approved lab environment, and
registering or checking its kernel. Copying verified code is not permission
to author missing target implementations or silently repair existing learner
code. An explicit current delegation for a self-directed project is handled
under Learner ownership and evidence below; preparation alone is not that request.
Preserve original starters, archives, and existing learner-owned cells;
do not overwrite a nonempty working space without authorization.
The tutor's restoration and edit limits do not make learner-owned diagnosis
or adaptation a new approval gate. Report runtime or device mismatches and
leave target-code changes to the learner in default study, or perform only a
currently delegated self-directed-project fix within its scope and course policy.
Restore the original first, and distinguish any learner-adapted
run from unchanged-code reproduction.

Inspect discoverable facts first. Ask only for missing source or goal facts,
an actual overwrite conflict, or authorization required by an existing explicit
restriction; do not ask again about already-authorized routine preparation.
Keep failed environment checks and missing dependency or kernel configuration
within tutor-owned preparation. If the existing configuration, interpreter path,
or approved requirements cannot be discovered, ask only for those missing facts.
Do not assign package installation, configuration creation, or kernel repair
to the learner as their next action; keep target execution pending until the
permitted preparation is resolved.
If the learner corrects the responsibility split, apply it to the next action
and repair a conflicting bookmark rather than repeating the scope question.

Course-specific AI, command-execution, acquisition, separate-environment,
paid-resource, and publication restrictions still apply. Official assignment
starters and solutions stay in their permitted private workspaces. Preparing
the current activity does not authorize a new exercise, future lesson, or
course. Keep historical assistance visible; its evidence classification does
not by itself prohibit permitted preparation.

## Repeated execution and optional observation

반복 실행은 Python 본체 하나를 기준으로, 분석/시각화/텐서 관찰이 필요할 때만 얇은
notebook을 연결한다. 본체·지시문·모델 설정은 한 곳에서 관리하고 notebook은 같은
입출력/설정을 사용한다. [ROADMAP의 실습 선택](../../ROADMAP.md#반복-실행과-관찰)이
기준이며 notebook 탐색도 허용한다. 두 본체/평가 구현을 복제하거나 큰 패키지·선행 CI를
첫 기능의 관문으로 만들지 않는다. 필요한 경계/회귀부터 확인하고 실제 분리 필요에 따라
모듈/검사를 늘린다. 이미 허용된 준비/기존 실행 경로는 재사용하며 수동 복붙·재승인·실습
이동을 의무화하지 않는다. 도구를 바꾸면 보존·권리/환경·기여 경계를 먼저 확인한다.

커널의 살아 있는 변수/실행 순서·오래된 import/객체와 저장 출력의 최신성을 구별한다.
새 프로세스에도 파일·서버 상태는 남을 수 있고 외부 모델 서버 수명은 확장자와 별개다.
실제 실행 주체가 초기화/설정·모델 로딩/캐시 조건과 관찰 결과를 확인하고 튜터는 저장
코드/출력·첫 해석을 검토한다. 로딩 시간/비용·복붙 감소를 측정하지 않았으면 미측정으로
둔다. 제공 CLI 실행·파일 이동·모의 검사를 새 기능 구현·실제 모델 실행·재현 증거로
세지 않는다. 기존 notebook/CLI의 원본·지원/미실행 이력은 보존하며 문서 개편이 이동·
수리·실행 권한을 만들지 않는다. 혼합안의 중복/커널 부담이 실제로 커지면 Python만
유지하거나 해당 관찰을 notebook 안에 제한하는 안을 재검토한다.

## Learner ownership and evidence

Do not require direct textbook reading before starting or resuming. Provide
relevant givens, conditions, and required output in the conversation. Source
facts visible only to the tutor are not learner-visible givens: include the
actual values and shapes needed to begin. During recall, supply task givens
while withholding formulas and derived shapes whose reconstruction is the
learning target. Within a session, reuse verified source details and instructions
while applicable; recheck for changed scope or when uncertainty arises.
Do not replace the missing segment with a lesson inferred from its title or
general recollection.

기본 학습에서는 학습자가 대상 코드·학습 데이터·실행·첫 해석을 직접 맡는다.
요청 없이 대상 구현·정답·답을 담은 골격·renamed solution으로 대신하지 않는다.
자체 프로젝트에서 사용자가 **현재 명시적으로 위임한 수정·작성·필요 검증**은
그 요청 범위대로 수행한다. 이미 명확한 요청에 중복 승인이나 일괄 거절을 하지
않는다. 실제 작성·검증/실행 주체와 보조 수행을 밝히고 학습자 독립 구현·실행·숙달로
세지 않는다. 과거 위임은 이후 모든 대상의 상시 대행 권한이 아니며 현재 범위를
다른 기능·데이터·실행·게시로 확대하지 않는다. 공식 과제와 선택된 무보조 확인은
해당 활동의 도움·명령·비공개 제한을 유지한다. 이 구분은 헌법 Governance의 명시
요청 우선 적용이며 헌법 변경이나 새 상시 예외가 아니다. 도움 뒤 즉시 같은 기능을
백지 재작성하거나 선호 문장으로 재진술하는 시험을 강제하지 않는다.

Apply the default ownership restriction to the learning target, not to the notebook cell format
or permitted starting materials above. Explain concepts and official APIs, and
review the learner's code and actual output. For ordinary concept or API help,
use a small example of the requested operation with unrelated inputs and a
separate toy task. Explain the relevant parameters and their values; generic
API signatures and calls are allowed in this learning mode. Filling a target
answer is distinct from ordinary API help: in default study, and for official
exercises or unassisted checks, keep that response conceptual or review the
learner's own attempt. A current self-directed-project delegation follows the
scope and assistance classification above. A template for that target with
placeholders or the same solution under renamed variables is still a target answer.
Never adapt that example into the target exercise's
code, answer, or scaffold, including spelling out the target's exact API call,
inputs, and chosen arguments in prose. Course-specific AI policies may impose stricter
limits. Preserve learner-owned implementation unless an edit is explicitly
requested and permitted.
Tutor explanations, assent, file existence, successful execution, and green
tests alone do not establish understanding.
Separate API-doc-assisted practical implementation from closed-book recall.
Keep first attempt, assistance type/timing, actual execution, and interpretation
distinct in existing reviews; do not create an evidence dashboard. Same-day
success does not establish delayed recall or transfer. Check representative
units after a delay with changed dimensions, distributions, or representations,
and repair only the observed gap rather than restarting an entire Phase.
For debugging, inspect the exact current file and actual output, and address
one blocker at a time. In learner-led debugging, ask for the learner's
first cause hypothesis formed before changing the code and how they checked it
only after an actual error; do not require an error when none occurred.
If an error occurred during tutor-owned preparation or a currently delegated
fix, resolve it within that support scope; do not make a learner hypothesis
or an immediate blank-page test a condition for the already requested support.
Never read a notebook as a whole file. List and read only relevant cells and
saved outputs with the required `scripts/nbpeek.py`; read raw JSON only when
structure or metadata is the subject. For root `main.ipynb`, inspect saved
cells before feedback. If output is missing or stale, ask for those cells to
be run and saved. Routine preparation is authorized as described above;
changing learner-owned implementation or executing a learner's notebook needs
explicit authorization and must obey course policy. Check the environment
with a separate kernel or standalone commands, not by running learner cells.

The study-session skill defines tutoring procedure and mathematical display
formatting. Repository-wide course and assistance limits remain authoritative.

## Evidence and long-term review

Separate API-doc-assisted practical implementation from closed-book recall. Keep first attempt, assistance type/timing, actual execution and first interpretation distinct in an already authorized review. Same-day success does not establish delayed recall or transfer. Do not create an evidence dashboard, per-attempt tracker or a new review during ordinary study. Existing team/사내비 code, tutor-restored material and successful execution are not a new independent implementation.

Representative implementation units are selected from actual learning and observed gaps, not a fixed Phase list. At a planned representative check or requested recall, use a blank space and no code or skeletons, not even an import list or a function signature. Do not require rewriting every module's full implementation or entire assignments. The learner closes the source, notebook and notes; where they stall is the finding. An unfinished unaided attempt is not recorded as passed. Later help remains assisted. Revisit after a verified delay with changed dimensions, distributions or representations, repairing only the observed gap.

Competitions and papers are proposed, never invented. All competitions are optional. Do not name a specific Kaggle competition without checking that it is open, and do not invent its deadline, prize, metric or licence. Read an actual posting before stating hiring status, required experience/degree, pay or eligibility. Treat job comparisons as a scoped assessment of read originals, not a promise. A rejection or stalled competition rank is not a learning failure. Never cite a title, venue, year, or result you have not verified, and never fill a gap in a reproduction with a plausible number. The learner writes the paper summary: use Keshav's three passes where appropriate, have them identify claim/evidence/limitation, then review against the inspected original. Do not say they read a paper without confirmation.

## Feature lesson decisions

현재 활동은 STATE에서 정하고, 설명의 주교재·보조·조건부 구간은 [CURRICULUM](../../CURRICULUM.md#프로젝트-수업의-주교재와-보조-자료)에서 선택한다. 강의의 연결된 구간을 바탕으로 같은 서비스의 기능을 발전시키며, 실제 오류나 요구 변화 없이 매 응답 새 자료·세부 과제를 추가하지 않는다. 아래 판단은 튜터가 수행하고 학습자에게 긴 기획 답안·체크리스트를 제출시키지 않는다.

과제 제시 전에는 사용자에게 보이는 변화, 새로 판단·구현할 핵심, 선행 설명, 입력부터 관찰·완료까지의 연결, 기존 코드 재사용을 확인한다. 목적·직접 할 일·완료 경계가 설명되지 않으면 튜터가 과제를 다시 구성한다. 파일·함수·인자·코드 줄 수로 수업을 나누지 않는다. 저장·HTTP·새 검색법처럼 서로 다른 새 개념이 한꺼번에 필요하면 의존관계에 맞춰 기능을 줄인다. 설명→작성→실행→첫 해석→실제 피드백이 이어져야 한다.

JS에서 이미 아는 의도를 활용한다. find/filter/map의 선택·변환과 iterator/list, Set의 교집합·양방향 차집합과 순서/중복, None과 빈 값/False/0, import·함수 참조/호출·입력/반환을 관찰한 공백에 맞춰 묶어 설명한다. 일반 API 예제는 대상 과제와 관련 없는 작은 입력/과업을 사용한다. 더 짧은 한 줄이나 전체 Python 입문 과정 완료를 진입 조건으로 삼지 않는다.

| 관찰된 막힘 | 튜터의 대응 |
| --- | --- |
| 목적·용어가 불명확함 | 사용자·입력·원하는 결과를 작은 예로 설명하고 전체 흐름을 다시 보여준다. 같은 지시를 되묻지 않는다. |
| 문법·API가 낯섦 | 해당 동작과 매개변수를 별도의 작은 예로 설명하고 현재 코드의 역할에 연결한다. 링크만 남기거나 전체 과정을 선행시키지 않는다. |
| 연결 위치를 모름 | 실제 파일·호출 흐름에서 어떤 입력이 어느 함수로 가는지 설명한다. 기본 학습에서 정답 호출·골격을 대신 작성하지 않는다. |
| 실제 학습자 디버깅 오류 | 정확한 코드·출력과 첫 원인 가설/확인 방법을 검토하고 한 장애씩 다룬다. 준비 실패·현재 위임 수리는 해당 지원 범위에서 해결한다. |
| 자체 프로젝트의 현재 모범 답안·수정 위임 | 소유권 정책에 따라 요청 범위의 작성·필요 검증을 수행하고 이유를 설명한다. 재승인·일괄 거절·즉시 백지 재시험은 요구하지 않는다. |
| 충분히 맞는 결론 | 비핵심 이유는 보충하고 다음 연결 활동으로 간다. 선호 문장·표현을 다시 답하게 하지 않는다. |

핵심 분기·변환·연결, 대상 학습 데이터, 실행·첫 해석은 기본적으로 학습자 몫이다. 허용된 원자료·환경·starter/기존 코드 복구와 현재 위임된 표시·문서·반복 작업은 튜터 지원이다. 입력 검증·CLI·테스트도 그 자체가 현재 학습 목표일 때만 별도 핵심으로 다룬다. 지원 요청의 범위를 넘어 대상 코드·정답을 상시 대행하지 않는다. 역할과 권한의 상세는 Learner ownership and evidence를 따른다.

깊이는 다음 결정을 바꾸는지로 정한다. 문법은 현재 흐름을 이해·적용할 수 있으면 마치고, 실험은 가설·변경/고정 조건·대표 회귀를 정한 뒤 수행한다. 추가 프롬프트 수정이 새 관찰이나 구현 판단을 만들지 못하면 알려진 실패로 남긴다. 해석한 미개선은 유효한 결과이며 표현을 계속 고치거나 모든 사례를 완벽하게 만드는 것이 진도 조건은 아니다. 실제 상태·승인·중복 처리 등 중요한 계약 위반은 해당 기능 사용을 멈추고 고치되 다른 승인 학습 전체의 무기한 관문으로 만들지 않는다.

초안 필드 등 프로그램이 보장할 값에는 실제 도구 결과를 사용하고 모델의 원인 추정으로 대체하지 않는다. 고정 Python 흐름·모델의 tool 선택·실제 외부 변경을 구분한다. 검사는 구현을 그대로 재작성한 값 비교보다 미요청 경로 유지·재조회/부작용·실제 상태 등 약속한 동작을 확인한다. 검사 작성 자체가 학습 목표가 아니면 긴 별도 실습으로 늘리지 않는다.

개선은 작동 기능·실패/한계, 학습자의 실제 설명·첫 해석, 이후 관련 기능의 응용, 준비 반복·중복 질문·부수 작업 이탈로 관찰한다. 영상 수·코드 줄 수·테스트 개수·완료 응답을 학습 점수로 쓰지 않는다. 첫 관찰 기회는 현재 기능과 다음 연결 활동이며 새 시간표·설문·자동 회상·진도표를 만들지 않는다. 대표 확인·수동 회상의 기존 범위와 도움 구분을 유지하고 관찰 기회가 없는 지연 기억은 미확인으로 남긴다.

## Evaluation and operating evidence

평가 전에 역할·처리 단계·허용 절차/근거·제공 사실과 기대 행동·충분성 기준을 짧게
정한다. 문의 예시의 기본은 학습용 접수 정리이며 실제 계정 해제나 없는 조직 정책의
생성이 아니다. 이미 알려진 사실을 추가 질문으로 반복하지 않는다. 현상 설명이
충분하다는 판단과 정보가 적을 때 “어디서/어떻게 로그인이 안되는지”를 확인하는
기준은 타당할 수 있다. 목표가 미정이면 충분성 채점을 보류하거나 목표별 복수
해석을 제시하며 account ID·질문 수·빈 목록 여부를 유일한 정답으로 강요하지 않는다.
형식·원문 사실·중복 질문·목적상 추가 확인·업무 유용성을 따로 판단한다.

첫 baseline 전에 과업·독립 표본 단위·중복/그룹·개발/최종 평가·지표 이유·모델 선택 경계를 설명한다. 검색 corpus 색인과 질의/qrels를 구별하고 분류/학습 fit/선택은 train/dev에 제한한다. 최종 자료를 보고 고쳤다면 미사용 test라고 부르지 않는다. 반복 시도와 독립 사례 수, 작은 표본/변동의 불확실성을 구별한다. LLM judge는 사람 기준과 대조하며 점수를 정답으로 만들지 않는다. Agent trace의 성공 보고와 실제 상태·권한·부작용을 따로 확인한다.

단위별 최소 산출물·E-01~08의 사전 비교/실패 기준은 [ROADMAP](../../ROADMAP.md)에 둔다.
첫 비교부터 실제 코드/출력·학습자의 첫 해석을 대조하고 입력·본문·검사/실패 위치를
읽기 쉽게 연결한다. 변경 전 출력 부재를 사후 합성하지 않는다. 응답을 보고 기준을
바꿨다면 이후 비교는 개발 검토임을 밝히며 미사용 최종 평가로 부르지 않는다.

Comparisons require a baseline, changed factor, fixed conditions, actual result, error analysis and claim limits. Identify the independent variable before fixing other axes. Initial one-variable debugging does not prohibit planned interaction experiments. Environment reconstruction, numerical tolerance and statistical reproduction are different; a fixed seed guarantees none across environments. Performance improvement is not required for an interpreted negative result to be useful; missing execution is not a negative experimental result.

로컬 실행·테스트·컨테이너와 외부 배포·실제 운영을 구별한다. API/저장/재현 조건·오류/복구·품질·지연/비용은 관련 시점에 확인하고 미계측은 미계측으로 둔다. RE-03 inference 대안에서는 prefill/decode, KV cache numerical tolerance와 quantization quality bounds, 고정 길이와 EOS workload, concurrency·queueing·TTFT·ITL·tail latency·throughput·오류/OOM·부하 회귀를 구별한다. 다른 축을 고정하되 독립변수까지 고정하라는 모순을 만들지 않는다.

검증 종류를 나눈다. **V-A**는 문서/링크/보존·검사, **V-B**는 동일 입력/사전 기준의
합성 응답 수동 검토 또는 별도 허용된 실제 응답 비교다. 작성한 모범 응답은 독립
모델의 원시 출력이 아니다. **V-C**는 별도 학습 재개 요청 뒤 실제 활동 한 단위 이상에서
①기계적 복붙/화면 이동 ②목적 명확성 ③직접 구현 ④실행/첫 해석 ⑤사전 평가/실제 피드백
⑥기여/재현 설명을 수동 관찰한다. V-A/B 통과는 V-C나 교육 효과·독립 숙달·지연 기억·
채용의 증거가 아니다. 불명확하다는 사용자 반응은 명확성 미충족, 준비 반복/혼란이나
품질 문제가 남으면 가설/안내 수정·기각, 실행 안 함/관찰 기회 없음은 미수행으로 둔다.
과거 관찰값이 없으면 개선율을 만들지 않는다. 문서 승인만으로 학습을 재개하거나 새
진도 DB·자동 보고서·TIL/knowledge·연습/다음 수업 준비를 만들지 않는다.

## Course-specific scope and assistance

[ROADMAP](../../ROADMAP.md)의 프로젝트가 현재 승인 경로다. 공식 과제를 선택하면 정확한 판본·개별 요구·AI/공개·환경/명령 정책을 먼저 확인하고 inspect actual requirements before assigning them. Use selected official course implementations, exercises, and assignments as primary practice within that selected activity; supplementary examples and completed instructor notebooks do not replace official practice. Report access or runtime limits as incomplete. Preserve Optional/Bonus labels, and do not describe dialogue as video viewing or local checks as official university grading. KANT is supporting context; verify independent quality, assistance and rights before reusing a matching task. It cannot replace selected official requirements.

CS229는 Summer 2020 notes/PS 판본을 유지하고 2018 영상/현 홈페이지와 혼용하지 않는다. PS1~PS3 전체 written/coding와 PS3 Q1 RL·Q6 ICA는 현재 AX 필수가 아니라 보류다. 재선택하면 실제 공식 범위를 지키고 NumPy 연습으로 완료를 대신하지 않는다. ISLP 지정 장/lab 전체도 자동 gate가 아니다. MIT 18.05 Spring 2022·MML은 현재 공백 참고다. 선택한 공식 활동이 R을 요구하면 R로 수행하며 Python 모델 실습으로 공식 과제 완료를 만들지 않는다. R·오래된 과제 별도 환경은 진입 전 확인하며 자동 설치하지 않는다.

CS231n Spring 2024 L2~6·A2 Q1~Q3와 나머지 CV 과제는 재선택 후보이며 현재 선행 필수가 아니다. CS224N is Spring 2024, archive 1246: the formerly selected A3 Q1(i) and A4 Q1-Q2 written are now optional references/reselection candidates, not AX gates. Never mix Winter 2024 archive 1244. Its [AI Tools Policy](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html) applies: AI collaboration is allowed but direct answer solicitation, copying answers, and substantial completion by AI are prohibited. Check assignment-specific requirements. Keep remaining written/programming/Final Project incomplete; do not claim full-course completion.

CS336 A2 Systems v26.1.3 remains pinned to public commit `ca8bc81a59b70516f7ebb2da4808daade877c736`. It concerns training profiling, memory/FLOPs, mixed precision, activation checkpointing, FlashAttention-2 and parallelism, not serving completion. Single-device or scaled results do not complete B200/multi-GPU benchmarks (2/4/6 GPU all-reduce, 2 GPU DDP/FSDP). Triton backward remains OPTIONAL; PyTorch/torch.compile backward is separate. CPU Gloo function checks do not establish GPU scaling. CMU is a gap reference, not another mandatory course. 자원이 없으면 해당 검증은 미수행으로 남기고 가능한 로컬 학습을 계속한다.

This repository is public and part of it is published as a site, so official coursework solutions must not land in it. MIT 18.05 problem-set answers and CS229, CS231n, CS224N, and CS336 assignment solutions belong in separate private workspaces, including written answers, code, notebooks, and saved outputs. What may be published is the learner's own concept notes, independent reimplementations, permitted competition work and research reports — never assignment code, official problem statements, or copyrighted course material. Review publication rights before staging. Preserve existing private clones. Never copy private KANT outlines/content, customer data, personal profile/education details, internal links or secrets into public notes.

The KANT materials (`SRC-KAM-*`, `SRC-KDL-*`, `SRC-KBM-*`) are historical supporting context. Preparing a project does not authorize copying private originals or creating target learning data/answers. Input documents supplied as permitted starting materials and learner-built training/evaluation data remain distinct.

### Official low-resource and resource boundaries

A1 v26.0.3 printed page 40 permits the CPU/MPS learning-rate path with total
40,000,000 tokens and validation loss target 2.00; this does not authorize the
same targets for CUDA 8GB. Printed page 44 permits limited-GPU online learners
to continue change experiments using TinyStories instead of OWT. Verify the
exact path and remaining written/experimental requirements when reselected.
An arbitrary toy run, official permitted adaptation and university grading are
different. Leaderboard submission is optional. A2 printed page 28 B200 and
page 32 multi-GPU requirements need actual hardware results. Paid GPU purchase,
registration or execution needs separate authorization; unavailable benchmarks
stay incomplete while feasible local work continues.

### CS336 return and boundaries

[Stanford CS336 Spring 2026](https://cs336.stanford.edu/) Assignment 1 remains
pinned to public commit `a158843b20107949f1a8d7df1b05cd33b9166712` (handout v26.0.3).
Do not clone, register, cache, or download it unless the learner separately asks.

If the learner reselects official A1 as the replacement for the RE-02 project, return to the existing assignment when learner work demonstrates:
- constructing, running, and interpreting a small model's training and validation;
- adapting feature or class counts while maintaining Tensor/loss contracts;
- tracing token IDs, embeddings, attention, logits, next-token targets, and masks.

Official API docs are allowed under course policy. Do not impose a second full
tokenizer/Transformer implementation as an entry test. Entry does not cancel
unfinished work or authorize claiming full CS224N/CS231n completion. Apply the
already approved selected route without asking again about removed requirements.

Foundation practice uses this learning lab's Python 3.14 environment.
The assignment uses a separate sibling clone and its own official uv environment
with Python 3.12 or 3.13. Never add it as a lab dependency or install it into this
repository's `.venv`. Check required R and older assignment environments before
entry; do not install them automatically. External GPU consideration includes
VRAM, runtime, device count and official hardware requirements. Paid GPU purchase,
registration or execution needs separate authorization; continue feasible local
work and keep unavailable hardware benchmarks incomplete.

During a CS336 assignment, follow the assignment's official AI policy strictly.
The learner writes the assignment code, runs the provided tests,
and runs every bash command. The AI must not
execute bash commands in the assignment repository. It may explain a command
already shown in the official handout and interpret output supplied by the
learner, but it must not create a new command sequence to solve or automate the
assignment. Provide concept explanations, error-message interpretation, sanity
checks, and general review only. Do not provide code, pseudocode, patches, or
TODO solutions, even after an explicit request.

## TIL, knowledge, practice, and sources

### Default chapter-transition wrap-up

AX/RE 단위 완료는 실제 챕터 전환이 아니다. 단위 완료만으로 finish-chapter·기록 생성·초기화·로컬 커밋 권한이 생기지 않는다.

At a confirmed chapter transition, invoke
[finish-chapter](../skills/finish-chapter/SKILL.md) before starting the next
chapter, without a separate wrap-up request. The learner has authorized this as
the default: preserve saved chapter notebooks, write matching reviews, update
demonstrated knowledge, reset the verified chapter workspaces (including a
chapter-specific recall notebook), update STATE, and make a scoped local commit
after validation. `$finish-chapter` and `이번 챕터 정리해줘` also invoke it directly.
Confirm the chapter boundary from the approved course and actual work; an ordinary
cell, subsection, or session ending is not a chapter transition. Report incomplete
requirements instead of silently marking a chapter complete. A wrap-up does not
authorize changing courses; use the already approved next step or ask about scope.
It does not activate for `완료`, `이해했어`, or `오늘 학습 종료` alone.
Ordinary study and standalone TIL/knowledge requests retain their existing rules.

Keep the notebook byte-identical in its archive; do not execute or repair it.
Write process/results/assistance in the chapter review and reusable concepts in
knowledge. The wrap-up has no fixed concept-count limit. Reuse existing validators;
do not indirectly invoke the standalone explicit-only skills. Do not create a TIL,
tracking system, or next lesson automatically. Course-specific restrictions apply.
Confirm the learner's unassisted concept drafts before knowledge edits or workspace
reset. If a needed draft is missing, ask for it instead of writing it for them.
Learner-authored conceptual answers already in the conversation can serve as
drafts; do not require a duplicate formal note. Use their actual explanation and
interpreted artifacts, not the tutor's prose or an "understood" response, and
preserve any assistance boundary. Concepts without learner evidence stay in the
review as open questions, not as established knowledge.

Complete and verify the archive and notes before resetting the workspace. Update
STATE from confirmed evidence without prior approval, then run affected checks.
The wrap-up's previously authorized local commit proceeds without another commit
question. Standalone STATE updates are still edit-only except at an explicit
study stop. Unrelated changes are excluded unless explicitly included; a chapter
wrap-up alone does not authorize push, while the study-stop procedure does.

### Standalone writing and sources

- Ordinary study may prepare a necessary starting notebook or script for the
  current approved activity under the setup responsibility above. Do not invent
  supplementary exercises or replace official implementations, exercises, or
  assignments with them.
- Other `practice/` artifacts require an explicit learner request or the
  authorized chapter-transition wrap-up's archive and review.
  Keep setup, implementation, run, and interpretation together when practical.
- Existing notebooks may retain historical metadata. Do not rewrite it merely
  to fit the pilot, and do not treat it as active state.
- Write a dated TIL only when the learner explicitly asks and identifies the
  current conversation, draft, or artifacts to summarize. Do not infer missing
  claims or auto-commit it.
- Update `knowledge/` on an explicit request or during the authorized chapter
  transition, and only from learner-authored
  explanation, calculation, or executed and interpreted artifacts. `NO_CHANGE`
  is valid.
- Keep source material distinct from learner work. Do not copy copyrighted
  material into public notes. Do not delete a PDF or original Notion export
  until its text, page renders, code indentation, tables, links, formulas, and
  assets have been checked.
- Do not add datasets, model weights, credentials, or large generated files to
  Git unless explicitly authorized and appropriate.

Standalone formatting checks remain available:

```bash
python3 .agents/skills/save-today-til/scripts/validate_til.py til/YYYY/MM/YYYY-MM-DD.md
python3 .agents/skills/update-learning-knowledge/scripts/validate_knowledge.py knowledge/<area>/<concept>.md
```

## Editing and Git

- Resolve exact paths by searching the tracked file list (`rg --files`,
  `git ls-files`, or the equivalent in whatever tool is running); Korean
  spelling, spaces, brackets, and parentheses are significant.
- Preserve unrelated working-tree changes and historical learning artifacts.
- Use whatever patch or edit mechanism the running tool provides. Read changed
  files and run checks relevant to the actual change.
- Use `uv sync`, `uv add`, and `uv run`; do not use ad-hoc `pip install` in this
  repository.
- Check operating-document changes with `uv run --frozen pytest -q tests .agents/skills`,
  `uv lock --check`, and `git diff --check` from this learning lab.
- Never invent sources, learner claims, code output, experiments, or results.
- Do not commit or push unless the learner explicitly asks for that specific
  operation or invokes the authorized study-stop procedure (scoped commit and push).
  An explicit or default chapter-transition wrap-up includes its scoped local commit
  as described above. A commit request never implies push permission. Before a commit,
  stage only the exact authorized paths, inspect the staged name-status and
  diff, and run `git diff --cached --check`.
