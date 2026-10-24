# Official course policies

공식 과제를 선택·재개하거나 관련 자료·도움을 다룰 때 직접 읽는다. 일반 AX 프로젝트의 상시 필독이나 선수 gate가 아니다. 공통 소유권·준비·Git은 [AGENTS](../../AGENTS.md), 현재 재개는 [STATE](../../STATE.md)를 따른다.

## Course-specific scope and assistance

현재 선택은 [STATE](../../STATE.md)를 따르며 [ROADMAP](../../ROADMAP.md)은 선택지다. 공식 과제를 선택하면 정확한 판본·개별 요구·AI/공개·환경/명령 정책을 먼저 확인하고 inspect actual requirements before assigning them. Use selected official course implementations, exercises, and assignments as primary practice within that selected activity; supplementary examples and completed instructor notebooks do not replace official practice. Report access or runtime limits as incomplete. Preserve Optional/Bonus labels, and do not describe dialogue as video viewing or local checks as official university grading. KANT is supporting context; verify independent quality, assistance and rights before reusing a matching task. It cannot replace selected official requirements.

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

If the learner reselects official A1 as the replacement for the small LM project, return to the existing assignment when learner work demonstrates:
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
