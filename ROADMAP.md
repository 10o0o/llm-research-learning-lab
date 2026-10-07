# LLM Research Engineer Roadmap

이 문서는 개인 LLM Research Engineer 성장과 취업을 위한 승인된 학습 설계다.
현재 학습 범위와 다음 행동은 [`STATE.md`](./STATE.md)만 정합니다. 역량 참고는
[`CURRICULUM.md`](./CURRICULUM.md), 제외 범위와 복귀 조건은
[`DEFERRED.md`](./DEFERRED.md)에 있습니다. KANT는 필요한 설명과 과제를 연결하는
보조 과정이며 개인 학습의 순서·속도·완료 판정을 정하지 않는다.

기존 소프트웨어 개발 경험을 실험 코드·재현성·운영 측정에 연결한다. Python,
PyTorch, 수학은 이미 한 작업과 남은 공백을 구분해 보강한다. 처음부터 다시
시작하거나 현재 결과를 연구 역량으로 확대하지 않는다. 특정 Phase가 취업이나
지원 자격을 보장하지 않습니다. 9개월 또는 고정 달력 안의 완료도 보장하지 않는다.

```text
P0 실행 가능한 수학·확률·통계 + PyTorch 학습 루프
→ P1 ML 목적함수·일반화 + 실험 근거
→ P2 신경망 진단·attention 구성요소
→ P3 자기 작은 Transformer LM + 독립 공식 구현
→ P4 하나의 잠정 전문화: Systems / Inference (평가는 전 과정 공통)
→ P5 한 질문의 독립 연구·재현 + 근거에 맞는 지원
```

## 시간 구조

확인된 의도는 **개인 학습 주 60시간 이상**이다. **KANT 수업 주 40시간,
알고리즘 약 2시간/일, 취업 준비는 제외**한 예산이다. 이를 전체 활동을 합친
60시간으로 바꾸지 않는다. 이 구분은 합계 100시간 이상의 주간 달력이 이미
실행 가능하다는 판단이 아니다.

다음은 개인 학습 60시간의 **초기 배분 가설**이며 최적 비율이나 의무 시간표가 아니다.

| 개인 학습 활동 | 예시 |
|---|---:|
| 공식 읽기·수학·통계 | 18h |
| 학습자 구현·디버깅 | 27h |
| 실험·평가·해석 | 9h |
| 지연 회상·전이·정리 | 6h |
| 합계 | 60h |

첫 1~2주 동안 실제 확보 시간, 새 환경 재현, 도움 없이 설명·구현한 결과를
수동 확인한다. 필요하면 이후 달력 길이와 배분을 조정하며 목표 깊이를 낮추거나
핵심 학습을 잘라 날짜를 맞추지 않는다. 기존 52주·2,880시간 표는 이번 재설계의
확정 기본값으로 계승하지 않는다. 자동 일정이나 새 시간 추적기는 만들지 않는다.

## 기존 범위에서 무엇이 바뀌었나

이 표는 범위 결정이며 완료 기록이 아니다. 빠진 요구는 미완료 보류로 남는다.
기존 코드·노트북·회고·실험 출력은 보존한다.

| 기존 규칙 | 이번 승인 범위 | 이유·남은 범위 |
|---|---|---|
| MIT Class별 남은 요구를 순서대로 수행 | 기존 MLP 새 커널 재현을 현재 실무 관문으로 연결; 확률·통계는 모델 학습·평가에서 보강 | 현재 위치는 STATE만 정함; fast.ai Lesson 1~2와 MML의 미검증 항목은 회고에 보존 |
| MIT 18.05 전체 reading·in-class·온라인 문제·PS1~PS11·R | 전체 이수 의무 해제; 필요한 확률·통계 역량은 유지 | 미선택 활동은 미완료 보류; 선택한 공식 활동의 요구는 지키며 Python 모델 실습을 MIT 과제 완료로 세지 않음 |
| CS229 Summer 2020 PS1~PS3 written·coding | 유지 | PS3의 RL·ICA까지 보존; GP·ICA 추가 심화·넓은 RL 과정은 보류 |
| CS231n 2024 L2~6·A2 Q1~Q5 전체 | 필요한 설명 + A2 Q1~Q3의 FC/backprop·optimizer·normalization·dropout | Q4 CNN·Q5 CIFAR-10, A1·A3·Final Project는 미완료 보류 |
| Karpathy GPT·Tokenizer 전체 후 CS224N 전체 | 흐름이 막힐 때 GPT 설명만 선택 | A1 이전 보조; A1 중에는 공식 정책에 따라 다른 구현을 참고하지 않음 |
| CS224N Spring 2024 A1~A4 전체 | 1246 판본 A3 Q1(i), A4 Q1~Q2 written | 나머지 written·programming·Final Project는 미완료 보류 |
| CS336 A1·A2 모두 P4 전체 의무 | A1은 P3의 공식 독립 구현 기준; A2는 P4 학습 systems 기초 선택 | A1 공식 저자원 경로 인정; A2 B200·다중 GPU 측정은 별도 자원 조건·미검증 범위 |
| LLM evaluation·post-training 전문화는 P5 이후 보류 | P0부터 공통 평가; Transformer 기초 후 작은 SFT/eval 비교 | 기존 P1 ML 평가도 유지; 전문화 두 트랙을 병렬 의무화하지 않음 |
| Phase마다 새 포트폴리오 | 최대 세 산출물을 점진적으로 발전 | 작은 LM, serving/eval harness, 독립 연구 보고서 |

## 자료 역할과 판본

튜터가 정확한 공식 구간과 문제에 필요한 조건·수치를 빠짐없이 확인해 한국어로
가르친다. 학습자의 교재 사전 읽기는 기본 요구가 아니다. 일반 학습은 승인된 현재
과정 안의 연결된 모듈로 이어간다. 수업·일시정지·종료 절차는 [study-session 스킬](./.agents/skills/study-session/SKILL.md)을
따른다. 공식 문서를 볼 수 있는 실무 구현과 자료를 닫은 대표 회상은 다른 근거다.
강의 수강 자체는 구현·실행·해석의 근거가 아니며 로컬 검사는 공식 대학 채점이
아니다.

| 자료 | 고정 범위와 역할 |
|---|---|
| [MIT 18.05 Spring 2022 syllabus](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/pages/syllabus/) | P0~P1 핵심 확률·통계의 필요한 구간 설명·공식 연습 참고; 전체 이수는 필수 조건이 아님 |
| [MML](https://mml-book.github.io/) | Chapter 2~5, 7의 확인된 공백만 보강 |
| [Karpathy Zero to Hero](https://karpathy.ai/zero-to-hero.html) | P0 makemore 3·4와 공식 exercises; 기존 micrograd·bigram·MLP 보존; GPT는 필요할 때만 |
| [CS229 Summer 2020 syllabus](https://cs229.stanford.edu/summer2020/syllabus-summer2020.html) | P1 notes·PS1~PS3; 현재 홈페이지의 다른 연도로 교체하지 않음 |
| [ISLP 공식 labs](https://islp.readthedocs.io/en/latest/labs.html) | P1 Chapter 5·6·8·13 본문·Python lab 유지 |
| [CS231n Spring 2024 A2](https://cs231n.github.io/assignments2024/assignment2/) | P2 Q1~Q3; Q4·Q5와 구분 |
| [CS224N Spring 2024, 1246](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html) | P2/P3 attention written 선택; Winter 2024, 1244와 혼용하지 않음 |
| [CS336 Spring 2026](https://cs336.stanford.edu/) | P3 A1 Basics, P4 A2 Systems 선택 및 Lecture 10 inference |
| [CMU Deep Learning Systems](https://dlsyscourse.org/) | 메모리·autodiff·kernel·parallelism 공백만; 추가 전체 과정 아님 |
| [Hugging Face smol-course](https://huggingface.co/learn/smol-course/en/unit0/1) | Transformer·PyTorch 기초 후 chat template·SFT·평가 비교에 필요한 절 |
| [Berkeley Deep RL](https://rail.eecs.berkeley.edu/deeprlcourse/) | DPO/RLVR 질문에 실제 필요한 RL 개념만; P0/P1 전체 RL 병렬 과정 아님 |
| [Raschka LLMs from Scratch](https://www.sebastianraschka.com/llms-from-scratch/) | LM 흐름 설명의 선택 reference; CS336과 같은 모델을 다시 전부 구현하는 의무 없음 |

판본 주의: 현재 API는 사용하는 버전의 공식 문서로 확인한다.
[Karpathy training recipe](https://karpathy.github.io/2019/04/25/recipe/)는 작은 배치
과적합·단순 baseline 진단의 보조다. [fast.ai](https://course.fast.ai/) Lesson 1~2는
이미 시도한 top-down 작업이며 미검증 재현·배포는 완료가 아니다.
[Made With ML](https://madewithml.com/)은 같은 P1 실험에 ML 시스템 설계·테스트·
배포를 연결한다. [Full Stack Deep Learning 2022](https://fullstackdeeplearning.com/course/2022/)와
[roadmap.sh](https://roadmap.sh/ai-engineer)는 비교 참고이며 전체 과정을 별도 졸업 조건으로 추가하지 않습니다.

KANT는 진도·주제 대조용 보조다. 기본 실습이나 완료 기준으로 사용하지 않습니다.
독립 품질이 확인된 같은 주제의 과제는 출처·도움·공개 권한을 밝히고 중복 연습을
줄이는 데 재사용할 수 있으나 공식 필수 과제 완료를 대신하지 않는다.
영상·문서·공식 자료 기반 대화를 허용한다. 완성 노트북 실행이나 AI 보충 예제로
공식 실습을 대체하지 않습니다. Optional·Bonus를 유지하고 제약은 미완료 또는
공식 허용 조정 수행으로 구분한다. 새 자료를 여기 연결하는 것은 다운로드·전체 감사·환경 설치 완료를 뜻하지 않습니다.
비공개 KANT 상세 일정·문제·슬라이드·내부 링크는 공개 문서에 옮기지 않는다.

## P0 — 현재 기초를 실행 가능한 근거로 연결

기존 MLP의 data → train → eval 새 환경 재현을 **현재 실무 관문**으로 연결하고
필요한 확률·통계를 손실·샘플링·평가에서 보강한다. 현재 작업 구간과 다음 행동은
STATE만 정한다. 새로운 입문 과정이나 전체 재진단으로 시작하지 않는다.
MIT 전체 이수는 필수 조건이 아니다. Agent가 노트북을 수정하거나 실행해 통과시키지 않는다.

기존 [MLP 학습·평가 회고](practice/deep-learning/makemore-mlp-training-recall.md)는
학습자 train/eval 함수와 AI의 데이터·모델·API 도움을 구분했다.
[E01·E03 회고](practice/deep-learning/makemore-mlp-e01-e03.md)의 초기화·배치 통제
설명은 당시 해석이며 셀 이력은 새 커널 재현을 입증하지 않는다. 기존 결과를
독립 모델·데이터 구현 또는 새 커널 성공으로 승격하지 않는다.

- 조건부확률·독립성, 확률변수·분포, 기댓값·분산, LLN·CLT의 의미와 성립 조건을
  유지한다. 기존 MLP의 손실·샘플링·평가에서 연결하고
  [MIT class 자료](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/pages/classes-reading-and-in-class-materials/)의
  필요한 정확한 구간으로 실제 공백을 보강한다. 전체 reading·in-class·온라인
  문제·PS1~PS11·R 튜토리얼은 일괄 의무에서 제외하고 미선택 범위를 DEFERRED에 둔다.
- P0~P1에서 likelihood·MLE와 손실함수의 관계를 모델 학습에 연결한다.
  [CS229 Summer 2020](https://cs229.stanford.edu/summer2020/syllabus-summer2020.html)의
  확률 복습·MLE notes를 사용하고 likelihood·prior·posterior·MAP의 기본 구분은
  해당 공식 작업에 필요한 범위로 보강한다. 표본 단위·누수·신뢰구간·검정·검정력·
  bootstrap·다중비교는 실제 평가에 연결해 배우며 P1의 ISLP 5·13장 본문·lab을 활용한다.
  연속 사전분포·켤레 사전분포의 상세 계산은 과제나 논문에서 필요해질 때 복귀한다.
- 선택한 공식 활동이 R을 요구할 때만 R로 수행하며 Python 대체로 완료 처리하지 않습니다.
  모델 연결 실습은 Python/PyTorch로 진행하고 MIT 공식 과제 완료와 구분한다.
  핵심 선수 공백은 의존하는 활동 전에 맥락 안에서 보강하며 별도 전체 확률 과정이나
  명령마다의 문법 회상 관문을 추가하지 않는다.
- MML Chapter 2~5, 7의 행렬·투영·분해·chain rule·gradient·Jacobian·최적화 공백을
  본문·공식 연습문제의 무보조 설명·계산으로 보강한다. 이미 설명·계산한 내용을 반복 수강하지 않습니다.
  미분·정적분이 막히면 [MIT 18.01SC Fall 2010](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/)의
  해당 절만 사용한다. 별도 수학 과정 전체를 추가하지 않습니다.
- 학습자가 MLP의 데이터 출처·split·seed·초기화·배치 순서·dtype·device·의존성을
  설명하고 새 커널에서 실행한다. 작은 배치 과적합, train/eval 모드, label/loss
  계약, zero_grad·backward·갱신을 확인한다. 저장 출력만으로 독립 수행을 판단하지 않는다.
- 기존 MLP 재현 이후 makemore Parts 3~4와 공식 exercises를 유지한다. Python 함수·객체·
  indexing·환경 사용은 실제 막힌 동작만 보강한다.

fast.ai Lesson 1~2 미완료와 MML 미확인 연습은 기존 회고·DEFERRED에 남는다.
Stat110과 OpenIntro는 다른 설명이 필요할 때만 쓰며 새 전체 과정이 아니다.

## P1 — ML 목적함수와 믿을 수 있는 실험

회귀·분류·likelihood·최적화·규제 → split·CV·baseline → 오류 분석·불확실성을 연결한다.
CS229 Summer 2020 **PS1, PS2, PS3의 필수 written과 coding을 모두 수행**한다.
[PS1](https://cs229.stanford.edu/summer2020/ps1.pdf), [PS2](https://cs229.stanford.edu/summer2020/ps2.pdf),
[PS3](https://cs229.stanford.edu/summer2020/ps3.pdf)의 공식 PDF·starter ZIP·환경을 사용한다.
공식 문제를 임의 NumPy 연습으로 대체하지 않습니다. 2018 영상은 보조다.

선수관계 예외: **PS3 Q1 RL와 Q6 ICA는 기존 필수 범위로 유지**한다. 해당 문제 전에
MDP·Bellman, likelihood·분포·행렬 미분에 필요한 notes를 읽는다. GP·ICA 추가 심화·
전체 RL 과정 보류가 PS3 삭제를 뜻하지 않는다. 이 작은 RL 문제만으로 독립 RLVR
연구 준비를 인정하지 않는다.

ISLP Chapter 5·6·8·13 본문·Python lab을 유지한다. 전처리 fit은 train 안에서 하고
독립 표본·시간·그룹 단위로 split한다. CV로 모델 선택을 하고 test를 반복 보며
튜닝하지 않는다. baseline·규제·트리/앙상블 비교에서 error slice와 bootstrap의
재표집 단위·가정·불확실성을 해석한다. 신뢰구간·검정·검정력·다중비교의 의미와
가정도 같은 평가에 연결하고 필요한 MIT 설명으로 보강한다.

Kaggle은 P1만 필수입니다. 실제 열린 tabular 대회 하나의 데이터·지표·기한·라이선스·
연산량을 읽고 선택한다. 같은 실험에 입력 계약·작은 배포·CI·모니터링을 연결하며
향후 harness의 출발점으로 재사용한다. 별도 거대 포트폴리오를 추가하지 않는다.

## P2 — PyTorch 진단과 LM 구성요소

P0/P1의 loss·gradient·split을 tensor·module·optimizer·data pipeline으로 연결한다.
[PyTorch 기초](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)와 공식 API는
공백만 보수한다. feature·class·batch 차원을 바꿔도 loss 계약을 지키고 작은 배치
과적합·validation·gradient·수치 안정성을 진단한다.

CS231n Spring 2024 Lecture 2~6의 필요한 설명과 **A2 Q1~Q3**를 선택한다.
FC/backprop·optimizer·batch/layer normalization·dropout을 다루고 Q4 CNN·Q5
CIFAR-10 전체는 보류한다. 전체 A2·과정 완주라고 하지 않는다.

token ID·embedding → attention score·softmax → causal mask → 출력 shape를 연결한다.
[CS224N Spring 2024 A3 written](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/assignments/a3_spr24_student_handout.pdf)의
Q1(i)의 attention 비교와 [A4 written](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/assignments/a4_spr24_student_handout.pdf)의
Q1 Attention Exploration·Q2 Position Embeddings Exploration을 사용한다. 나머지 written·programming은 보류다. RNN/LSTM·
seq2seq는 비교 설명이 필요한 부분만 쓴다. Karpathy GPT bridge는 연결이 막힐 때만
쓰며 완성 GPT·BPE·CS224N·CS336 전체를 연속으로 반복하지 않는다. A1 진입 전에
전체 Transformer를 추가 구현하는 시험은 만들지 않는다.

## P3 — 자기 작은 Transformer LM과 공식 독립 구현

P2의 train/validation 실행·해석, 바뀐 tensor/loss 계약 적용, token·attention·mask
흐름이 확인되면 기존 CS336 Assignment 1 Basics 작업으로 돌아간다. **A1 자체가
독립 구현의 공식 기준**이다. 모든 보조 과정을 완강해야 진입하는 구조가 아니다.

tokenization·embedding·attention·causal mask·block·next-token target·cross-entropy·
sampling·checkpoint 저장/재개를 같은 작은 LM에서 연결한다. 데이터 출처·사용 권한·
중복·tokenizer 학습 범위·train/dev/test 경계를 명시한다. 미래 token 누수·target
shift를 확인하고 평가 데이터로 tokenizer나 모델을 튜닝하지 않는다.

공식 A1 [handout v26.0.3](https://github.com/stanford-cs336/assignment1-basics/blob/a158843b20107949f1a8d7df1b05cd33b9166712/cs336_assignment1_basics.pdf)은
Spring 2026, 공개 commit `a158843b20107949f1a8d7df1b05cd33b9166712`다. README의
이전 연도 표기보다 PDF 판본을 기준으로 한다. 기존 private clone을 보존하고
별도 요청 없이 clone·설치하지 않는다. 다음 범위를 구분한다.

| 범위 | 확인할 증거·표현 |
|---|---|
| 교육용 핵심 구현 | 학습자 LM 구성요소·train/eval·sampling·resume의 실행·설명; P3 핵심 확인이며 공식 전체 완료 아님 |
| 임의 축소 실험 | 작은 model/data/step로 correctness·학습 곡선 확인; 바꾼 요구·미수행을 밝히고 공식 완료로 세지 않음 |
| 공식 A1 수행 | BPE·Transformer·AdamW·훈련 인프라·실험의 해당 필수 요구; 기본 또는 공식 허용 저자원 경로와 결과를 명시 |

**공식 저자원 경로를 자원 부족만으로 불완료라고 판정하지 않는다.** v26.0.3 인쇄
40쪽 `learning_rate` Low-Resource Tip은 CPU/MPS에서 총 처리량을 40,000,000 tokens,
validation loss 목표를 2.00으로 조정할 수 있게 한다. 이는 CUDA 8GB에 같은 목표를
임의 적용하는 허가가 아니다. 인쇄 44쪽은 GPU가 제한된 온라인 학습자가 OWT 대신
TinyStories에서 변경 실험을 이어가는 경로를 제시한다. 적용한 조정·해당 written/
실험 요구·남은 항목을 명시해 공식 허용 저자원 수행으로 기록한다. 임의 toy Run All,
대학 채점, OWT 성능 재현과 구분한다. Leaderboard 제출은 선택이며 공식 A1
경로 완료의 필수 조건이 아니다.

P3의 지정 과제 범위는 선택한 공식 A1 경로의 필수 요구다. 교육용 핵심 확인이나
임의 축소 실험만으로 전체 A1 또는 P3 종료를 선언하지 않는다. 공식적으로 허용된
조정은 그 경로의 수행으로 인정하고, 허용되지 않은 생략은 미완료로 남긴다.

Transformer·PyTorch 기초 후 작은 base/instruct와 SFT/eval 비교를 한 번 제한된
범위로 한다. chat template·label masking·SFT/LoRA 설정과 held-out 품질·퇴행을
설명하며 loss 감소만으로 성공이라 하지 않는다. 학교의 같은 주제와 연결할 수
있으나 전문화 선택의 참고이며 독립 DPO/RL 완료나 필수 병렬 트랙으로 세지 않는다.

## P4 — 잠정 Systems / Inference 전문화

현재 1순위는 잠정 **Systems / Inference**다. 자기 LM과 기존 backend 경험을
serving·측정에 연결하고 P3 SFT/eval 비교와 실제 공고로 방향을 검토한다.

### 학습 systems 기초와 자원 범위

[A2 Systems v26.1.3](https://github.com/stanford-cs336/assignment2-systems/blob/ca8bc81a59b70516f7ebb2da4808daade877c736/cs336_assignment2_systems.pdf),
공개 commit `ca8bc81a59b70516f7ebb2da4808daade877c736`의 profiling·메모리/FLOPs·
mixed precision·activation checkpointing·attention kernel·parallelism을 필요 범위로 사용한다. **A2는 주로
학습 성능·분산 학습 과제**다. inference serving 전체를 대신하지 않는다.
8GB 단일 장치의 로컬·축소 작업을 A2 전체 완료로 세지 않는다. 공식 전체 A2는
현재 필수 관문이 아니다. CMU는 공백 reference이며 추가 full course가 아니다.

| 작업 | 로컬 필수 검증 | 축소·추가 자원 검증의 경계 |
|---|---|---|
| P0 MLP·확률 핵심·P1 CS229/ISLP | 학습자가 CPU/단일 GPU에서 재현·해석; 선택한 공식 활동이 요구할 때만 R 사용 | 미선택 MIT 활동은 보류; 작은 data 실험으로 선택된 공식 PS 요구를 삭제하지 않음; 과제 환경 호환성 확인 후 실행 |
| P2 CS231n Q1~Q3·attention written | gradient·optimizer·norm/dropout 요구와 작은 구성요소 | Q4·Q5·미선택 programming은 미완료 보류 |
| P3 LM/A1 | 구성요소 correctness·fresh kernel·sampling/resume; 선택한 공식 경로 요구 | 공식 저자원 조정과 임의 축소 구분; 큰 실행은 자원 확인 후 학습자가 수행 |
| P4 profiling·mixed precision | 들어갈 크기의 forward/backward/step·메모리/FLOPs·수치 오차 비교 | A2 큰 model/context sweep은 미검증; 로컬 성능을 다른 장치로 일반화하지 않음 |
| P4 kernel | 단일 GPU 호환성·작은 shape의 FlashAttention-2 forward 및 PyTorch/torch.compile backward 출력·gradient 비교 | A2 인쇄 28쪽 B200 benchmark·큰 sweep은 외부 자원 검증; Triton backward는 **OPTIONAL** |
| P4 parallelism | collective·DDP·optimizer sharding·FSDP 구조/비용 설명; CPU Gloo 기능 연습 | 인쇄 32쪽 2/4/6 GPU all-reduce와 2 GPU DDP/FSDP 측정은 다중 장치 필요; CPU는 GPU scaling 증거 아님 |
| P4 harness·P5 연구 | 한 장치의 작은 workload·정확성·품질·부하 시험 | cluster·다른 accelerator·대규모 serving은 실행 전까지 미검증 |

kernel·mixed precision의 장치/driver 지원을 먼저 확인한다. 외부 GPU 검토는
VRAM뿐 아니라 연산시간·장치 수·공식 지정 hardware 요구를 근거로 한다. 필요한
검증·장치·비용·한도를 확인해 별도 승인받기 전 구매·등록·실행하지 않는다.
그동안 해당 검증은 미수행으로 두고 가능한 로컬 학습을 계속한다.

### 별도 inference·운영 측정

[CS336 2026 Lecture 10](https://cs336.stanford.edu/)을 연결해 같은 LM/harness에서
prefill·decode·KV cache·batching을 구현·측정한다. workload·warmup·반복·동기화·
측정 경계를 명시한다. **독립변수로 정한 축을 제외한 model revision·데이터·장치·
workload·sampling 조건을 고정**한다. batching 비교에서 batch, quantization
비교에서 precision을 고정하라는 모순된 규칙을 만들지 않는다.

cache는 eval mode, 같은 위치·mask 조건에서 uncached 기준 logits와 사전 수치
허용 오차를 비교한다. quantization은 baseline 이후 선택이며 bitwise 일치가 아닌
사전 품질 허용 범위를 평가한다. 고정 생성 길이 성능 시험과 EOS를 따르는 실제
요청 시험을 구분한다. 초기 debugging은 한 번에 한 변수로 원인을 좁히되 연구에서는
사전 설계한 작은 batch×length 상호작용 실험도 허용한다.

같은 harness에 요청 도착 패턴·concurrency·queueing, TTFT·ITL·tail latency·
throughput, 취소·오류·OOM과 복구 동작, metrics/logs/traces, 재현 가능한 부하 시험을
붙인다. 코드 변경 뒤에는 같은 요청 부하와 품질 허용 범위에서 TTFT·ITL·tail·
오류·OOM의 부하 회귀를 검사한다. 단일 요청·평균 latency를 운영 역량 전체로 확대하지 않는다. Linux·배포·
API 계약은 기존 경험과 연결해 검증하고 다른 언어 경력으로 Python/FastAPI 실무를
이미 갖췄다고 주장하지 않는다.

### 대안 Eval / Post-training

선택하면 held-out eval·dedup·contamination·metric variance → base/instruct·chat
template·label masking·SFT/LoRA → 독립 평가 → **하나의 DPO 또는 RLVR 질문**으로
간다. SFT loss·held-out 품질·다른 능력 퇴행을 분리한다. DPO는 preference data·
reference policy·목적함수, RLVR는 reward/verifier·policy gradient·variance·평가의
선수를 확인한 뒤 연구한다. 두 방법·넓은 RL을 동시에 졸업 요건으로 추가하지 않는다.
학교 노출은 독립 연구 증거가 아니며 공통 평가 핵심은 어느 분기에서도 유지한다.

## P5 — 한 질문의 독립 연구와 재현

프로젝트와 논문 재현을 따로 만들지 않습니다. 선택한 전문화의 **한 연구 질문**에서
논문 주장 하나를 baseline·통제 조건·ablation·재현·작은 variation으로 확인한다.
학습자가 주장·근거·한계를 먼저 읽고 쓰며 paper와 local model·data·hardware·
workload 차이를 실험 전에 명시한다.

환경·실행 방법·측정 오차·품질·memory·latency·throughput 또는 선택한 eval 지표,
실패 사례·부정적 결과·claim limits를 보고한다. 코드·도움·자기 기여를 밝히고
논문 전체 결과를 재현했다고 일반화하지 않는다. 실패는 원인·한계를 보고한 유효한
결과이며 성공이나 가상 수치로 채우지 않는다. 한 cycle을 끝낼 작은 범위로 잡는다.

최대 세 산출물: **재현 가능한 작은 LM, serving/eval harness, 독립 연구 보고서**.
과제·대회·대화를 모두 별도 포트폴리오로 늘리지 않는다. 공식 과제 답안은 비공개다.

## 평가와 대표 관문

P0 split·train/eval·실험 단위 → P1 leakage·CV·baseline·error analysis·bootstrap →
P2/P3 LM dev/test·target shift·dedup·contamination·metric variance → P4/P5 품질을
보존한 시스템 비교·주장 한계를 확인한다. 평가를 P5까지 미루지 않는다.

질문 **10개를 두 번 실행한 것은 20회 시도이며 독립 질문 20개가 아니다**.
질문·문서·사용자 같은 독립 표본 단위를 정하고 seed/응답 반복은 그 안의 변동으로
다룬다. 불확실성 해석에서 재표집 단위와 가정을 설명한다.

| Phase | 대표 확인 행동 |
|---|---|
| `P0` | 모델의 조건부확률·분포와 기댓값·분산, LLN·CLT의 의미·조건 설명; 차원이 바뀐 작은 계산에서 scalar loss까지 shape·VJP와 SGD 한 step 부호 예상; MLP fresh kernel·작은 배치 과적합·label/zero_grad 대표 오류 진단 |
| `P1` | 회귀/분류·규제 유도/실행; 누수 없는 CV·baseline·error slice·bootstrap 단위 설명; PS1~PS3·지정 lab 증거 |
| `P2` | feature/class/batch 변경의 train/eval 계약·gradient·norm/dropout 진단; scaled dot-product attention shape·mask 설명/구현 |
| `P3` | token→target→logits→CE→sampling/resume 설명/실행; target shift·미래 정보 누수 진단; 핵심·축소·공식 A1 경로별 결과 표기 |
| `P4` | cache correctness·prefill/decode·batching 품질·메모리·성능·운영 부하 측정; 또는 선택한 SFT/eval held-out 품질·퇴행·variance 독립 해석 |
| `P5` | baseline·통제 비교·ablation·재현 variation·실패 사례로 한 주장과 일반화 한계를 설명 |

대표 무보조 재구현은 P0 scalar autodiff·MLP loop, P1 linear/logistic regression·
PCA, k-means·CV loop, P2 train/eval·attention, P3 block·causal mask, P4 cache·측정
경계다. 공식 과제 수행과 무보조 재구현은 서로 다른 근거다. 전체 과제를 다시 쓰는
의무를 추가하지 않고 대표 단위만 확인한다. 강의·노트·코드를 닫고 import 목록·
signature·뼈대 도움 없이 시도하며 도움받은 구현을 무보조 성공으로 기록하지 않습니다.
이 **빈 파일 구현 트랙**의 Deep-ML·짧은 시간제한 시도는 관찰된 공백만 보강하고
개인 구현·회상 예시 배분 안에 포함한다. 별도 취업 알고리즘 연습의 제외 시간과
중복 계산하거나 새 주간 문제 수·필수 트랙으로 만들지 않는다.

같은 날 성공과 **며칠 뒤 자료 없이 복원하고 차원·분포·표현을 바꾼 전이**를 구분한다.
요청한 주간 회상은 지난주 개념 2개와 더 이전 개념 1개를 묶고 실제 학습 시기로
선택한다. 기존 회고에 첫 시도·도움 시점·오류 가설·실제 결과만 짧게 남긴다.
knowledge는 학습자 무보조 초안 이후 교정한다. 공백만 보강하고 Phase 전체를 다시
시작하지 않는다. 별도 작은 퀴즈·dashboard·회상 추적기를 계속 만들지 않는다.

[PyTorch reproducibility](https://docs.pytorch.org/docs/2.14/notes/randomness.html)에 따라
seed 고정과 완전 수치 재현을 동일시하지 않는다. 환경 재구성, 같은 환경의 사전
수치 허용 오차 내 재현, 여러 seed/표본에서 통계적 결과 재현을 구분한다. 실제
실행·해석한 범위만 주장한다. Run All은 확률·미분·독립 구현 관문을 대신하지 않는다.

## 취업 근거와 Phase 전환

P1부터 전환 때 실제 공고 3~5건을 읽어 필수 경력·학위 또는 동등 경험·지역·언어·
실험/운영 요건과 자기 산출물을 대조한다. 공고가 경로와 다르면 공고를 기준으로
경로를 재검토합니다. 채용 여부·요건·급여는 원문을 읽고 확인한다. 지원 자격을
이미 갖췄다고 추정하지 않으며 더 이른 적합한 역할 지원이나 불합격은 학습 실패가 아니다.

| 비교할 역할 | 실제로 확인할 근거 |
|---|---|
| ML Engineer / Research Engineer | PyTorch 학습 pipeline·실험 주도·재현·오류 분석·자기 기여 |
| LLM Systems / Inference | Linux·profiling·memory/kernel·KV·TTFT/tail/throughput·부하·오류 대응 |
| Model enablement | 모델 구조·kernel·수치 정확성·backend 검증 |
| Eval / Post-training | 독립 eval 설계·통계·운영 신뢰성·Python·held-out 품질 |
| Python ML Backend / LLM Application | 해당 framework의 실제 API·운영 경험, 평가·입력 계약; 다른 언어 경력을 자동 환산하지 않음 |

Phase 종료 전 지정 범위의 직접 수행, 실행·해석과 재현 가능성, 노트 없는 핵심
연결 설명·대표 전이, 남은 자원/보류 요구, 실제 시간과 다음 달력, P1부터 공고
대조를 확인한다. 필수 항목이 비면 Phase를 닫지 않는다. 문서·링크·테스트 검사는
교육적 타당성 검토와 다르며 실제 학습 효과·독립 수행은 학습자 실행·지연 회상 후
확인할 수 있다.

재개 위치가 실제로 바뀔 때만 사전 승인 없이 확인된 내용을 `STATE.md`에 간결하게
기록하며, 일상적인 갱신은 별도 보고하지 않는다. 상태 요청, 명시적 학습 종료, 실제 차단이나 충돌이
발생하면 필요한 결과와 미완료 항목을 보고한다. 답변별 전사나 세션 이력을 쌓지 않는다.
이는 새 과정·보류 트랙 진입·선수 생략
권한이 아니다. Phase ID는 정적 위치이며 점수·누적 시간·완료 목록을 붙이지 않는다.
승인된 현재 경로의 수업은 반복 승인 질문 없이 진행한다.

## 실전 competition·논문·공개 경계

P0·P2·P3은 선택 competition이다. P0는 예측을 만들 수 있으면 첫 제출 경험을
제안합니다. 이전 제출 경험을 요구하지 않습니다. P2·P3는 핵심 학습 뒤 선택하고
제출 결과가 다음 Phase의 선수조건은 아닙니다. [실제 목록](https://www.kaggle.com/competitions)의
지표·라이선스·연산량을 확인해 시간 상한을 정한다. 지정 reading을 논문 학습에
포함하고 월별 quota는 더하지 않는다. [Keshav 3-pass](https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf)로
학습자가 주장·근거·한계를 먼저 요약한다.

MIT 18.05 문제 세트 답안과 CS229·CS231n·CS224N·CS336 공식 과제 답안은
written·코드·노트북·저장 출력 모두 별도 비공개 작업 공간에 보존한다. 공개 저장소에는
공식 문제 원문·과제 답안·저작권 자료를 넣지 않는다. 자신의 개념 노트, 공식 답안과
분리된 빈 파일 재구현, 공개 가능한 대회 작업과 재현 보고서만 남긴다. 비공개 KANT
자료·고객 데이터·개인 정보·비밀정보는 넣지 않는다.
