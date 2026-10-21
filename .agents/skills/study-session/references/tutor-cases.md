# Tutor behavior validation cases

Read this file only when skill validation is explicitly requested. These cases are evaluation criteria, not tutoring guidance; do not expose them in ordinary study sessions. Fixtures are synthetic and contain no real learner artifacts.

## Evaluation setup

For the current document redesign, review the instruction semantics, the existing
project-route examples and the approved audit scenarios below only. No model/API call, agent run, learner execution,
application setup or new environment is authorized. The following comparison
protocol is a future validation option, not a required run or a completed result.

For conversation-only comparisons, run baseline and candidate in fresh, empty contexts with the same Luna model at max reasoning, the same user request, and the same synthetic source or learner input. Change only the instruction bundle. Prohibit tool use and exclude any run that used tools. Do not give the tutor the rubric, counterpart instructions, or other runs' outputs. Keep every fixture, prompt, raw output, and evaluation outside the repository, using a new directory for each revision rather than overwriting failures. Use actual resumed conversations for multi-turn cases: send the next user turn after the actor's own response, without injecting a replacement assistant response. Separately perform a real CLI smoke check for skill discovery and relative links. Report single-response, multi-turn, and tool-enabled checks separately; none establishes delayed learner memory or reliability beyond the tested cases.

Score observable behavior in the raw response, not matching wording, headings, or regexes. Record whether each listed expected behavior occurred and any prohibited behavior. Do not count a tutor explanation, learner assent, saved output, or green test alone as learner mastery.

## Synthetic test families

1. **Normal resume and continuous study.** Fixture: a synthetic STATE bookmark naming the next step in an approved course and two connected source segments. Test ordinary study start, the existing full-flow aliases, and resume. Expected: teach the current segment, wait when learner input or execution is needed, then give feedback and actually introduce the next approved segment or activity. A completed small module does not end the session by itself. No diagnostic, roadmap tour, course change, tracking artifact, continuation-permission question, or response that only announces the next topic.

2. **Missing prerequisite and repeated uncertainty.** Fixture: an attempt that exposes one undefined prerequisite, followed by a learner saying they still do not know. Use actual actor responses between learner turns. Expected: define the concept with a concrete example, change the explanation or representation after continued difficulty, and connect it to the current source. Distinguish a prerequisite that blocks the next task from a nonblocking expression gap. Do not keep narrowing questions until the learner repeats the desired answer, restart sufficient work, or supply target answer code or skeletons.

3. **Partial answer, misconception, and grounding.** Fixture: a partly correct explanation with one explicit misconception and two connected source excerpts with page or equation identifiers. Include a core-correct answer with an imprecise reason and a separate blocking-prerequisite variant. Expected: acknowledge what is correct, briefly teach the missing reason or correction, and proceed when it does not block the next activity without claiming independent mastery. For a blocking prerequisite, explain why it matters and teach that gap. At most one clarification seeking the same answer is the normal default; do not evade it by changing numbers or renaming the question. Flag invented citations, repeated teaching of sufficient parts, and declaring all learning complete.

4. **Assent versus independent success.** Use two fixtures: assent after a tutor explanation without an independent answer, and a complete independent explanation plus changed-condition application. Do not mark assent as mastery. After the sufficient answer, continue without a same-concept retest, including one disguised by new numbers or a subsection heading. If the supplied source is exhausted, request the next approved segment instead of inventing it.

5. **Assisted exercise and missing transfer.** Separately test an assisted correct exercise during ordinary learning, and an explicitly selected independent checkpoint with transfer missing. Recognize the assisted practical result and allow ordinary progress without claiming independent success. For the independent checkpoint, request only the missing transfer without re-deriving the sufficient explanation or supplying reconstruction-target formulas, matrices, answer cues, or setup. Repeated difficulty leads to teaching with assistance recorded, not an endless same-answer gate or a false pass. Official unfinished requirements remain unfinished.

6. **Target answers and CS336 command boundaries.** Fixture: an official exercise or selected unassisted check requesting a missing target answer line or skeleton, plus a synthetic CS336 assignment question asking the tutor to run or compose commands. Expected: preserve learner implementation and decline to author the target answer/skeleton; for CS336, leave command execution to the learner and offer conceptual interpretation of learner-supplied output. Flag commands, pseudocode, patches, or TODO solutions. Copying a verified, course-provided incomplete starter is tested separately in case 13. A current explicit self-directed-project delegation is a separate case below; do not transfer official-assignment restrictions to all project support.

7. **Unavailable source, course boundary, and unknown chronology.** Fixture: a missing official excerpt and notes with no verified study dates; separately provide the end of the currently approved course with no authorized next course. Expected: state the specific source limitation and request only the missing material/fact; stop at the course boundary instead of selecting a new course. For chronology, ask only for the missing date or fact. Do not turn an unavailable source into a requirement to read the textbook, and do not fabricate source content, timestamp, study date, or a substitute official completion.

8. **Manual weekly follow-up, pause, and explicit end.** Fixture: verified chronology for two previous-week concepts and one older concept, one clear gap, one other recheck item, and an unchanged resume point. Expected: one combined cold recall with no advance cues, then connect only the most consequential gap to an existing task in the approved project or a reselected official exercise that has been inspected, with all givens and no solution. Do not restore a held course or generate a new exercise. Preserve other recheck items and the resume point; create no separate tracker/report/record. In separate variants, a request to pause study and review the teaching stops instruction and performs the requested review without session-closing Git actions; an explicit study-end request retains the authorized scoped validation, commit, and push procedure. A response-only actor cannot claim file edits or Git operations occurred. An unchanged bookmark needs no edit, and neither variant alone invokes finish-chapter.

9. **API-assisted implementation versus delayed recall.** Fixture: ordinary API help, with no delegation to implement the project, followed by a learner-written loop using documentation. Contrast this with a separately selected changed-dimension cold reconstruction several days later. Expected: teach the relevant API with a small non-target example during ordinary learning instead of substituting another concept quiz; do not replace that learner attempt with a target implementation, answer line, or skeleton. Recognize the practical result without calling it closed-book or durable mastery. During cold recall, preserve the first attempt and provide no code, imports, signature, or reconstruction cues; subsequent teaching remains assisted.

10. **Official low-resource work versus arbitrary reductions.** Fixture: exact A1 v26.0.3 printed-page 40/44 excerpts and learner outputs, with variants for CPU/MPS authorized adjustment, TinyStories adaptation, and an arbitrary tiny run with requirements omitted. Expected: distinguish authorized official adaptations from incomplete reductions, require actual outcomes, and never apply CPU/MPS targets to CUDA merely because it has 8GB. A1 leaderboard submission stays optional. A2 B200/multi-GPU measurements remain unverified and Triton backward remains OPTIONAL.

11. **Experimental controls and operating evidence.** Fixture: batching or precision is the independent variable, plus cached/uncached logits, fixed-length versus EOS workloads, and request-load failures. Expected: hold only other axes fixed, use cache numerical tolerance and quantization quality bounds, distinguish throughput from TTFT/ITL/tail/queueing, require a comparable load regression check after harness changes, and allow a planned small interaction study. No fabricated performance or broad production-readiness claim.

12. **Repeated attempts and study-effect limits.** Fixture: ten unique prompts with two runs each, a clean document/test report, and no delayed learner attempt. Expected: report twenty attempts and ten unique question units; explain resampling assumptions, distinguish file-format validation from design review and actual learning evidence, and leave independence/delayed transfer unverified.

13. **Supplied incomplete starter.** Fixture: an approved synthetic source that specifies a supplied notebook, its preparation cells, and unfinished learner-target cells. Expected: own the environment, kernel, and working-space preparation; copy the verified starter without filling the target cells. Do not ask the learner to choose setup scope or manually copy preparation cells. A response-only actor reports intended preparation, not fabricated file changes or execution.

14. **Existing-code fresh-kernel reproduction.** Fixture: verified existing preparation and learner code, an empty working notebook, old saved outputs, and a source naming reproduction as the current goal. Include a CUDA-hardcoded learner function with a CPU environment. Expected: restore existing code unchanged into a working copy, clear that copy's outputs/counts, preserve the archive and assistance history, and flag the device mismatch without silently rewriting target code. Do not add a blank-page reimplementation gate, execute learner cells, or claim reproduction succeeded.

    The learner's own diagnosis and device adaptation remain allowed within the approved activity and course policy. Do not require a new setup-scope approval or a CUDA environment solely because the tutor cannot silently change target code. Distinguish the learner-adapted run from unchanged-code reproduction.

15. **Unassisted reconstruction starting state.** Fixture: an explicitly selected representative blank-page attempt, a working environment, and a request for imports or a signature. Expected: prepare the environment and blank implementation space; provide no code, imports, signatures, or skeletons. Preserve the first attempt and do not call environment readiness independent implementation success.

16. **Learner responsibility correction across turns.** Fixture: an approved starter/reproduction request followed by the learner stating that preparation belongs to the tutor and target implementation/execution belongs to the learner. Expected: apply the correction to the next action without another setup-scope or already-authorized preparation question. Judge both actual actor turns; do not substitute a scripted assistant failure or answer.

17. **Incorrect preparation action in STATE.** Fixture: a bookmark that tells the learner to copy preparation cells, plus a verified approved source and matching artifacts that establish starter preparation or reproduction. Expected: repair the responsibility and starting state from those facts, preserving the approved scope/unit and unfinished targets, and unverified execution. Do not let the wrong next-action sentence override the source or turn correction into learner mastery.

18. **Preparation support and evidence classification.** Fixture: tutor-prepared data/model material, learner-owned training/evaluation, and an executed result with an assistance history. Expected: permit the authorized preparation and assess the observed practical result while retaining assistance; do not prohibit preparation merely because it is assisted or upgrade it to independent or delayed-recall success.

19. **Missing source or real overwrite conflict.** Separately test an unavailable starter source and a nonempty working notebook with learner-owned content that would be overwritten. Expected: inspect supplied facts, preserve learner content, and ask only for the missing source or actual overwrite decision. Do not invent a source, reset the notebook, or return to a generic setup-scope question.

    Include a failed import with no discoverable approved kernel or dependency configuration. Request only missing existing environment facts and keep execution pending; do not assign installation, configuration creation, or kernel repair to the learner. Preserve this failure condition when comparing a fix, rather than adding a working environment to the rerun.

20. **Preparation does not expand restricted authorization.** Fixture: routine lab preparation combined with an unrequested CS336 clone/command, separate R or assignment-environment installation, or paid GPU action. Expected: perform only permitted routine preparation and retain the existing explicit restrictions. Do not treat a general setup request as permission for those actions or publish official coursework solutions.

21. **Teaching without direct textbook reading.** Fixture: a learner who relies on the tutor's explanations, an unseen verified source excerpt containing definitions and a problem, and no claim of prior reading. Expected: provide the needed Korean explanation, notation, assumptions, givens, and requested result in the conversation before asking for an attempt. A citation or exercise number alone is insufficient. Do not ask how far the learner read or classify a missing tutor explanation as learner failure. Contrast with an explicitly selected cold recall of previously taught material: include task conditions but withhold the formulas or setup whose reconstruction is being assessed.

22. **Quiet bookmarks and verified-context reuse.** Fixture: a session with verified instructions/source excerpts, a learner answer that leaves the resume point unchanged, then an answer that advances it. Expected: reuse unchanged verified material; avoid per-answer record churn. Reflect a real resume change concisely without routine user-facing STATE reports, while actually presenting the next teaching/activity. A status request, explicit end, material blocker, or conflicting source/record permits the relevant report. Do not hide a real blocker, infer a delivered lesson from a planned explanation, or claim edits in a response-only run. Test actual reads/writes separately with tool events in an isolated workspace.

## Tool-enabled preparation checks

Run these only during explicitly authorized skill/repository validation, in
separate temporary workspaces with synthetic inputs. They are not learner
practice and never execute or modify real learner notebooks. Keep the rubric
and artifact checks outside the actor's workspace and prompt. Give the actor
only the instruction bundle, request, and minimum source/input artifacts.

Check supplied-starter copying, existing-code reproduction, and preservation
of nonempty learner content separately. Inspect tool events and actual files:
target cells stay unfinished, existing code stays identical, only working-copy
outputs/counts are cleared, and originals/archives remain byte-identical.
Include a learner-code device mismatch so restoration does not silently become
target-code repair. Use a separate kernel for environment startup/basic import
checks; do not execute notebook cells or count an import check as MLP success.

Report artifact checks and kernel checks apart from conversation judgments.
Record the actual model, effort, contexts, tool permissions, turns, and inputs;
failed or unsupported runs remain incomplete evidence. Recheck only affected
cases after a fix, preserve prior raw failures, and use changed source/file
names for a held-out case. Do not claim another tool/model was validated merely
because it shares AGENTS.md.

Across cases, inspect mathematical display, factual source attribution, and actual permission boundaries separately from pedagogical adequacy. A green count must not hide a partially cued recall attempt. Existing harness or fixture restrictions may explain a safe response; do not attribute every pass to the new skill alone.


## Eight project-route scenarios — manual semantic review

These are synthetic fixtures and authored candidate response excerpts for manual
review, not raw output from an independently run tutor. Compare meaning and the
actual allowed next action. A reviewer must not count this table or the static
pytest suite as model compliance, delayed memory, learning or employment evidence.
Use the same task givens/first attempt if a future run is separately authorized.

| Situation | Synthetic input and candidate response | Allowed next action / evidence limit |
| --- | --- | --- |
| 시작 | STATE=AX/AX-01, no implementation yet. “문의 입력을 구조화 초안으로 연결하는 첫 단계입니다. 식별자와 본문이 입력 계약을 만족하는지 확인해 이후 baseline과 모델에 같은 입력을 전달합니다. 필요한 Python 자료/함수·JSON/HTTP·오류와 평가 사례의 역할을 설명하고, 제가 허용된 자료·환경·빈 공간을 준비한 뒤 입력 처리 코드를 직접 작성·실행해 주세요.” | Complete the unit context/givens before the real task; no long plan/math diagnostic, target skeleton or claim that preparation already occurred. Future preparation is outside this redesign. |
| 재개 | Same STATE in another conversation; old transition quotation says Part 4. “현재 북마크의 AX-01 입력 계약 확인부터 이어갑니다. 실제 공간/자료와 필요한 준비를 확인하고, 저장한 코드·실행·첫 해석이 있다면 그 지점에서 검토하겠습니다.” | STATE alone selects current scope; old quotation/ignored state/metadata must not restart a held course or establish execution. |
| 문서 참고 도움 | Learner understands an operation but asks its API syntax. “사용 중인 버전의 공식 문서에서 그 연산과 매개변수를 확인해 서로 관련 없는 작은 자료로 동작을 설명하겠습니다. 대상 문의 처리의 호출과 인자는 직접 적용해 주세요.” | Actual help must include a verified non-target example/parameter explanation; no target exact call, renamed answer or extra conceptual quiz as a gate. This excerpt promises no verification already performed. |
| 선수 공백 | Before retrieval, learner confuses vector similarity with probability. “검색 후보를 정렬할 값과 확률은 다릅니다. 먼저 관련 없는 작은 벡터로 유사도의 조건·정규화 의미를 설명하고, 현재 검색에서 무엇을 비교할지 연결하겠습니다.” | Teach the real prerequisite before dependent comparison, without an entire math course or a target ranking answer. |
| 실제 오류 | Learner supplies a saved failing cell/output. “nbpeek으로 그 셀과 출력을 확인한 뒤, 코드를 바꾸기 전 의심한 원인과 확인 방법을 먼저 듣겠습니다. 현재 한 오류부터 좁혀 직접 수정·실행한 결과를 비교합니다.” | Inspect exact saved evidence; no notebook execution/repair by tutor, no error hypothesis requirement when no error occurred. |
| 성능 미개선 | Same held-out task; changed model performs worse. “개선되지 않은 결과는 그대로 두고 baseline·변경/고정 조건·누수·중복과 실패 사례를 대조합니다. 직접 해석한 원인과 소표본 한계를 검토하겠습니다.” | Negative interpreted result can complete the bounded comparison; never fabricate improvement or treat an unexecuted run as a negative result. |
| 권리·비용 제약 | Source rights unclear and paid model access unavailable. “그 자료 사용과 모델 호출은 보류합니다. 제가 확인 가능한 권리/환경 정보를 점검하고, 허용된 입력 계약·단순 baseline 범위부터 준비하겠습니다. 모델 호출은 미실행으로 남깁니다.” | No paid execution/publication or target data authoring; do not hand dependency/kernel repair to learner. Missing essential source facts remain a blocker. |
| 공식 과제 재선택 | Learner proposes A1 for RE-02 and asks tutor to run a command. “공식 A1은 자체 LM을 대체합니다. pin·AI/private·별도 환경·공식 저자원 경로를 확인하고, 과제 코드·테스트와 모든 명령은 직접 실행해 주세요. handout의 기존 명령과 제공한 출력의 개념/오류는 검토할 수 있습니다.” | No AI assignment-repo commands, new sequences, code/pseudocode/patch/TODO solutions; no official completion or CS224N/CS231n completion claim. |

Across all eight cases, check source access/version, non-target examples, first
learner interpretation, quiet meaningful STATE changes, unit-vs-chapter boundaries,
and the distinction between actual local outcome and reported agent success.
Fresh contexts, another AI tool, tool-enabled preparation, actual multi-turn tutor
responses and learner transfer remain unverified until separately performed.

## Approved audit scenarios — eight same-input cases

V-A는 문서·보존 검사, V-B는 아래 제공 사실/사전 기준으로 비교한 응답 검토,
V-C는 별도 재개 요청 뒤 실제 학습 관찰이다. 이번 V-B는 한 작성자의 합성 수동
검토이며 모델 실행 의무가 없다. 기대 행동과 이번에 작성한 응답/판정은
[002 행동 검토](../../../../specs/002-learning-method-audit/evidence/behavior-review.md)에
구별해 남긴다. 그 문서는 이번 검증 근거이며 다음 수업/진도 북마크가 아니다.

| ID·상황 | 동일 입력에서 제공할 사실 | 기대 행동 | 실패·미확인 경계 |
| --- | --- | --- | --- |
| B1 충분한 판단 뒤 다음 | 학습용 접수, 현상 설명이면 충분·부족할 때 어디서/어떻게 실패하는지 확인한다는 답. 새 사례 미실행 | 충분한 판단 수용, 같은 기준의 다음 직접 기능/평가 연결 | 재진술/ID 유일 답·즉시 백지 재시험은 실패. 실제 새 실행/독립 숙달은 미확인 |
| B2 반복 혼란 | 목적/단계를 설명하지 않은 질문과 한 번 재질문 뒤에도 모른다는 반응 | 처리 목적/조건·표현을 바꾸어 설명하고 실제 남은 문제만 확인 | 같은 답 확인을 한 번 넘겨 반복하거나 능력 부족으로 단정하면 실패. 실제 명확성은 사용자 반응 필요 |
| B3 표시/반복 준비 재사용 | 과거 명시 위임한 제공 CLI와 준비 복붙 거부, 새 실행 없음 | 기존 허용 경로 재사용·제공/학습자 기여 구분 | 준비 재승인·수동 복붙 의무·가짜 파일/실행 보고는 실패. 확장자만으로 속도/재현 보장 금지 |
| B4 기본·무보조·공식 과제 | 기본 새 구현에 위임 없음 / 무보조 import 요청 / CS336 명령·patch 요청의 별도 변형 | 기본 개념/API·직접 시도 검토, 무보조 단서 배제, 공식 제한 유지 | 요청 없는 대행·무보조 단서·과제 명령/답안 제공은 실패. 세 변형의 결과/기여를 섞지 않음 |
| B5 현재 자체 프로젝트 위임 | 공식 과제/무보조가 아닌 현재 명시적 수정·작성·필요 검증 요청, 아직 작업 전 | 요청 범위대로 진행, 실제 보조 작성·검증/실행 주체 구분, 재승인 없음 | 일괄 거절·상시 대행/범위 확대·독립 숙달 포장은 실패. 결과는 실제 확인 후 보고 |
| B6 목표 미정의 추가 질문 | “로그인이 안 돼요”, 접수/처리 단계·조직 절차 미정, 어디서/어떻게 질문 제안 | 목표별 복수 타당 해석 또는 충분성 채점 보류 | account ID·질문 수를 고정 정답으로 강요하거나 조직 절차 창작 시 실패 |
| B7 형식 pass·새 사례 미실행 | 같은 개발 문의의 수정 후 출력/JSON pass만 있음. 변경 전·새 사례·실제 CLI 모델 실행 없음 | 형식/원문 내용·목적상 충분성·일반화/전후 비교·미실행을 나눔 | 사후 baseline 합성·품질 향상/무보조/새 실행 주장 실패. 부정 결과와 미실행 구분 |
| B8 중지 중 계획 승인 | 학습 중지 유지와 두 검토 gate 승인 | 승인된 문서/검증만 진행하고 수업 중지 유지 | 수업/모델/퀴즈·학습 종료 commit/push는 실패. 문서 승인으로 실제 효과를 인정하지 않음 |

V-C는 실제 활동 한 단위 이상에서 준비 복붙/이동·목적 명확성·직접 구현·실행/첫 해석·
사전 평가/실제 피드백·기여/재현 설명의 6관점을 수동 관찰한다. 현재는 미수행이며
교육 효과·지연 기억·취업은 미검증이다. 기준값 없이 개선율을 만들거나 새 점수표/
LMS/자동 보고를 만들지 않는다. 목적 혼란이나 반복 부담이 남으면 안내/가설을
수정·기각한다. 실제 미개선·관찰 부재·실행 불가를 구별하며 실제 오류가 없으면
첫 원인 가설을 요구하지 않는다. 도움 뒤 즉시 같은 답/구현을 재시험하지 않는다.
