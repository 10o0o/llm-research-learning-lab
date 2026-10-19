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
code. Preserve original starters, archives, and existing learner-owned cells;
do not overwrite a nonempty working space without authorization.
The tutor's restoration and edit limits do not make learner-owned diagnosis
or adaptation a new approval gate. Report runtime or device mismatches and
leave target-code changes to the learner within the approved activity and
course policy. Restore the original first, and distinguish any learner-adapted
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

Do not supply learner-owned target exercise implementations, answer lines,
answer-bearing cells or skeletons, or rewritten solutions, even when asked.
Apply this restriction to the learning target, not to the notebook cell format
or permitted starting materials above. Explain concepts and official APIs, and
review the learner's code and actual output. For ordinary concept or API help,
use a small example of the requested operation with unrelated inputs and a
separate toy task. Explain the relevant parameters and their values; generic
API signatures and calls are allowed in this learning mode. An explicit request
to fill an exercise answer is not ordinary API help: keep that response
conceptual or review the learner's own attempt. A template for that target with
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
one blocker at a time. If an error occurred, ask for the learner's first cause
hypothesis formed before changing the code and how they checked it; do not
require an error when none occurred.
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

## Evaluation and operating evidence

첫 baseline 전에 과업·독립 표본 단위·중복/그룹·개발/최종 평가·지표 이유·모델 선택 경계를 설명한다. 검색 corpus 색인과 질의/qrels를 구별하고 분류/학습 fit/선택은 train/dev에 제한한다. 최종 자료를 보고 고쳤다면 미사용 test라고 부르지 않는다. 반복 시도와 독립 사례 수, 작은 표본/변동의 불확실성을 구별한다. LLM judge는 사람 기준과 대조하며 점수를 정답으로 만들지 않는다. Agent trace의 성공 보고와 실제 상태·권한·부작용을 따로 확인한다.

Comparisons require a baseline, changed factor, fixed conditions, actual result, error analysis and claim limits. Identify the independent variable before fixing other axes. Initial one-variable debugging does not prohibit planned interaction experiments. Environment reconstruction, numerical tolerance and statistical reproduction are different; a fixed seed guarantees none across environments. Performance improvement is not required for an interpreted negative result to be useful; missing execution is not a negative experimental result.

로컬 실행·테스트·컨테이너와 외부 배포·실제 운영을 구별한다. API/저장/재현 조건·오류/복구·품질·지연/비용은 관련 시점에 확인하고 미계측은 미계측으로 둔다. RE-03 inference 대안에서는 prefill/decode, KV cache numerical tolerance와 quantization quality bounds, 고정 길이와 EOS workload, concurrency·queueing·TTFT·ITL·tail latency·throughput·오류/OOM·부하 회귀를 구별한다. 다른 축을 고정하되 독립변수까지 고정하라는 모순을 만들지 않는다.

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
