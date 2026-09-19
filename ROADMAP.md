# LLM Research Engineer Roadmap

이 문서는 장기 학습 경로와 시간 예산을 정하는 참고 지도입니다.
현재 학습 범위와 다음 행동은 [`STATE.md`](./STATE.md)만 정합니다. 역량·자료 감사는
[`CURRICULUM.md`](./CURRICULUM.md), 제외 범위와 복귀 조건은
[`DEFERRED.md`](./DEFERRED.md)에 있습니다.

목표는 기초 개념을 자기 말로 설명하고 수식·구현·실험으로 뒷받침하며 낯선 조건에
적용하는 능력입니다. 이를 바탕으로 ML Engineer 지원 근거를 만들고, LLM systems와
inference를 깊게 구현·측정하여 장기적으로 LLM Research Engineer를 준비합니다.

```text
P0 수학·확률·통계와 학습 루프
-> P1 고전 ML·실험·프로덕션
-> P2 딥러닝·PyTorch
-> P3 NLP·Transformer
-> P4 LLM 구현·학습 시스템·추론 기초
-> P5 독립 inference 연구·포트폴리오·지원
```

## 시간 구조

1년은 **52주 달력 안의 48개 실효 학습주**를 참고선으로 둡니다. 주 60시간(실효),
합계 2,880시간이며 나머지 4주는 실행 장애와 밀린 공식 과제를 위한 달력
여유입니다. 아래 값은 실제 소요시간이 입증된 예측이 아니라 **초기 배분 가설**입니다.
기간은 마감이 아니라 **예산**입니다. 깊이에 시간이 더 들면 이후 일정을 옮기며,
공식 핵심 과제나 무보조 설명·해석 단계를 잘라 날짜를 맞추지 않습니다.

각 활동은 수행하는 Phase에 한 번만 계산하며 다른 Phase 예산으로 넘기지 않습니다.
공식 과제와 지정 독서는 첫 열에, P5의 지정 독서만 통합 프로젝트 시간에 포함합니다.
P0·P2 프로젝트 열은 기존 구현의 비교·해석과 선택 실험을 위한 시간이며 추가
Kaggle 의무가 아닙니다. P1·P2의 짧은 공고 대조는 구술·재구현 열의 Phase 전환
점검에 포함합니다. 지원 활동이 0인 Phase에 실제 지원하기로 하면 다른 Phase에서
시간을 빌려 계산하지 않고 그 Phase의 배분이나 이후 일정을 명시적으로 조정합니다.

| Phase | 실효 주 | 주과정·공식 과제·지정 독서 | 프로젝트 | 구술·재구현 | 지원 활동 | 작업 버퍼 | 합계 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `P0` | 1~8 | 330h | 30h | 72h | 0h | 48h | 480h |
| `P1` | 9~18 | 330h | 120h | 90h | 0h | 60h | 600h |
| `P2` | 19~24 | 225h | 45h | 54h | 0h | 36h | 360h |
| `P3` | 25~32 | 330h | 0h | 72h | 30h | 48h | 480h |
| `P4` | 33~42 | 390h | 0h | 90h | 60h | 60h | 600h |
| `P5` | 43~48 | 0h | 120h | 36h | 168h | 36h | 360h |
| **합계** | **48주** | **1,605h** | **315h** | **414h** | **258h** | **288h** | **2,880h** |

### Phase별 필수 결과

| Phase | 공식 학습·프로젝트에서 확인할 결과 |
|---|---|
| `P0` | 행렬·미분·확률·통계의 설명과 계산, MIT 18.05 PS1~PS11 직접 수행, MLP 학습·검증·초기화 비교 해석 |
| `P1` | CS229 PS1~PS3 written·coding, 지정 ISLP lab, 누수 없는 모델 비교와 사용 시나리오가 있는 배포 프로젝트 |
| `P2` | CS231n A2 Q1~Q5, PyTorch 학습 진단과 CNN, 작은 GPT·BPE 구현·설명 |
| `P3` | CS224N A1~A4 written·수학·프로그래밍 전체와 RNN·LSTM·attention·Transformer 연결 설명 |
| `P4` | CS336 A1·A2 모델·커널·분산 학습의 구현·측정, Lecture 10에 근거한 추론 병목 설명 |
| `P5` | 한 추론 연구 질문의 baseline·통제 비교·논문 재현 보고서, 성능·품질·메모리 해석과 기초·시스템 면접 연습 |

이 결과와 아래 무보조 설명·대표 재구현으로 Phase 전환을 검토합니다. 날짜가
되었다는 이유로 다음 Phase에 진입하거나 기존 과제를 완료 처리하지 않습니다.

## 자료 역할

- **주과정**은 지정 범위와 공식 과제를 모두 수행합니다.
- **보조 자료**는 막힌 설명이나 다른 관점에 필요한 절만 봅니다.
- **비교 자료**인 `SRC-KAM-*`, `SRC-KDL-*`, `SRC-KBM-*`는 기본 실습이나 완료
  기준이 아닙니다.
- **선택 범위**는 Phase별 추천 근거와 예산에 맞춰 제안합니다. P0 첫 제출은
  예측 능력을 근거로 하며, P2·P3 Kaggle은 핵심 학습을 마친 뒤에만 제안합니다.

`CURRICULUM.md`의 정적 catalog는 장기 선수관계 참고이며 Phase gate가 아닙니다.
현재 설명에 필요한 선수만 보충하고 같은 주과정으로 돌아갑니다.

KANT는 진도·주제 대조용이며 기본 실습이나 완료 기준으로 사용하지 않습니다.
영상·문서·공식 자료 기반 대화를 허용하되 공식 구현과 필수 과제의 범위는 유지합니다.
완성 노트북 실행이나 AI 보충 예제로 공식 실습을 대체하지 않습니다. 문제 본문을
읽고 Optional·Bonus 표시를 유지하며 접근·실행 제약이 있으면 미완료로 남깁니다.
강의 수강 자체는 구현·실행·해석의 근거가 아니며 로컬 검사는 공식 대학 채점이 아닙니다.
새 자료를 여기 연결하는 것은 다운로드·전체 감사·환경 설치 완료를 뜻하지 않습니다.

### 참고한 공개 커리큘럼과 반영 내용

| 출처 | 반영한 설계 | 수행 범위 |
|---|---|---|
| [fast.ai](https://course.fast.ai/) | 동작하는 모델로 전체 흐름을 먼저 보는 top-down 입문 | P0 Lesson 1~2만 |
| [Made With ML](https://madewithml.com/) | 사용자·데이터 계약에서 테스트·배포·모니터링으로 연결 | P1의 같은 Kaggle 프로젝트에 적용 |
| [Full Stack Deep Learning 2022](https://fullstackdeeplearning.com/course/2022/) | ML 시스템 설계, 학습 진단과 배포 관점 비교 | 필요한 절만 보조, 전체 과정은 보류 |
| [roadmap.sh AI Engineer](https://roadmap.sh/ai-engineer) | 응용 구현과 모델·시스템 역량의 범위 비교 | 직무 구분 참고, 추가 수강 의무 없음 |

fast.ai를 앞에 짧게 붙이는 구성은 기초 → ML → DL → NLP → systems의 선수 순서를
바꾸지 않습니다. 판본 주의: fast.ai Part 1과 FSDL 2022의 도구 사용법은 실행 시점의
공식 문서와 대조합니다. 참고 커리큘럼의 전체 과정을 별도 졸업 조건으로 추가하지 않습니다.

### Karpathy 공식 구현 연결

기존 실습과 지식은 보존합니다. 아래는 자료 위치이며 완료 기록이 아닙니다.

| 범위 | 공개 영상 | 공식 구현 |
|---|---|---|
| P0 makemore Part 2 | [MLP](https://www.youtube.com/watch?v=TCH_1BHY58I) | [notebook](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part2_mlp.ipynb) |
| P0 makemore Part 3 | [Activations, Gradients, BatchNorm](https://www.youtube.com/watch?v=P6sfmUTpUmc) | [notebook](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part3_bn.ipynb) |
| P0 makemore Part 4 | [Backprop Ninja](https://www.youtube.com/watch?v=q8SA3rM6ckI) | [notebook](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part4_backprop.ipynb) |
| P2 GPT | [영상](https://www.youtube.com/watch?v=kCc8FmEb1nY) | [공식 구현](https://github.com/karpathy/nn-zero-to-hero/tree/master/lectures/ng-video-lecture) |
| P2 Tokenizer | [영상](https://www.youtube.com/watch?v=zduSFxRajkE) | [minbpe](https://github.com/karpathy/minbpe) |

micrograd와 bigram의 기존 작업은 다시 완료 판정을 내리지 않습니다. makemore
Part 5 WaveNet의 복귀 조건은 `DEFERRED.md`를 따릅니다.

## P0 — 수학·확률·통계와 학습 루프

현재 `STATE.md`의 makemore Part 2를 그대로 이어 다음 순서로 진행합니다.

1. Karpathy makemore Part 2 전체 구현과 공식 exercises E01~E03
2. [fast.ai Practical Deep Learning for Coders](https://course.fast.ai/) Lesson 1~2
3. [Mathematics for Machine Learning](https://mml-book.github.io/) Chapter 2~5, 7을
   기준 범위로 삼아 개념별 무보조 설명·계산을 확인하고 부족한 부분만 본문·공식
   연습문제로 보강
4. [MIT 18.05 Spring 2022](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/)의
   [class reading·in-class materials](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/pages/classes-reading-and-in-class-materials/)와
   [problem sets](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/pages/problem-sets/) 순서로 probability,
   Bayes, NHST, confidence interval, bootstrap, regression을 학습하고
   **PS1~PS11을 R 요구까지 모두 수행**
5. Karpathy makemore Part 3, Part 4 전체 구현과 공식 exercises

fast.ai Lesson 1~2는 전체 workflow를 먼저 보는 top-down 입문입니다. 나머지 Part
1은 기본 경로가 아닙니다. MML은 두 번째 완독 과정이 아니라 확인된 선형대수·
해석기하·행렬분해·벡터미분·최적화 약점을 고치는 reference입니다.
Chapter 2 선형대수, 3 해석기하, 4 행렬분해, 5 다변수 미분, 7 최적화의 핵심을
빠짐없이 다루되 이미 설명·계산한 내용을 반복 수강하지 않습니다. 현재 연결된
학습 단위에서 확인하며 매 세션 새 진단으로 시작하지 않습니다. 단변수 미분이나
정적분이 막히면 [MIT 18.01SC Fall 2010](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/)의
해당 기초 단원만 보강합니다. 별도 수학 과정 전체를 추가하지 않습니다.

MIT 18.05가 확률·통계의 주과정입니다. 보유 Stat110과 OpenIntro는 다른 설명이
필요할 때만 쓰며 전체 과정 요구가 아닙니다. P0 산출은 makemore MLP 초기화·학습
비교와 학습자가 직접 실행·해석한 통계 problem set입니다.
R이 필요한 과제는 R로 수행하며 Python 대체로 완료 처리하지 않습니다.
기존 Stat110 자료와 학습 기록은 그대로 보존합니다. 분포·기댓값·분산·LLN·CLT,
likelihood·MLE·MAP, Bayesian inference와 빈도주의 추론, 검정력·bootstrap의
설명 기준은 `CURRICULUM.md`에 연결하며 다중비교는 P1 ISLP 13장에서 보완합니다.

## P1 — 고전 ML·실험·프로덕션

주과정은 [CS229 Summer 2020](https://cs229.stanford.edu/summer2020/)입니다.
공개 [syllabus](https://cs229.stanford.edu/summer2020/syllabus-summer2020.html)와 공식 notes를 따라가며 **PS1, PS2, PS3의 필수 written과 coding을 모두
수행**합니다. 공식 PDF와 Python starter ZIP을 사용하며, 공식 문제를 임의 NumPy
연습으로 대체하지 않습니다. 2018 공개 영상은 설명 보조일 뿐 Summer 2020 과정
완료 근거가 아닙니다.
최종 프로젝트와 공식 시험은 수행 범위에 포함하지 않으며 이 범위를 마쳤다고
“CS229 완주”라고 표현하지 않습니다.

실제 tabular model selection은 [ISLP](https://www.statlearning.com/) Chapter 5,
6, 8, 13 텍스트와 [공식 lab](https://islp.readthedocs.io/en/latest/labs.html)으로
보강합니다. Python판 5장 교차검증·bootstrap, 6장 규제, 8장 트리·앙상블,
13장 다중검정의 본문과 공식 Python lab을 수행합니다. 비교 실험을 같은 P1
프로젝트에 연결하며 전체 책 완독은 추가하지 않습니다.

P1의 유일한 필수 competition은 도달 시점에 열린 tabular 대회 하나입니다.
데이터·평가지표·마감·라이선스·연산량을 읽고 선택합니다. 같은 프로젝트에
[Made With ML](https://madewithml.com/)의 design, testing, reproducibility,
CI/CD, monitoring 절을 적용해 사용 시나리오가 있는 배포 프로젝트를 만듭니다.
시작 전에 사용자, 입력 schema와 허용 범위, split과
leakage 경계, 감시할 오류·입력 분포·응답 지연, 실패 동작을 고정합니다.
순위가 아니라 누수 없는 비교·오류 분석·재현성과 use case의 일관성이 근거입니다.

## P2 — 딥러닝·PyTorch

주과정은 [CS231n Spring 2024 schedule](https://cs231n.stanford.edu/2024/schedule.html) Lecture 2~6과
[Assignment 2](https://cs231n.github.io/assignments2024/assignment2/) Q1~Q5
전체입니다. Assignment 1, Assignment 3, final project는 기본 경로에서 제외합니다.
설명 매체는 공개 notes·slides를 기본으로 하며 접근 불가능한 영상을 본 것으로
취급하지 않습니다. A2의 fully-connected network, batch normalization, dropout,
CNN, PyTorch Q1~Q5를 빠짐없이 수행합니다.
[PyTorch Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)와
공식 API 문서로 tensor·autograd·module·optimizer·data pipeline·train/eval loop를
보수합니다. 이미지 Kaggle은 공식 A2와 PyTorch 흐름을 끝낸 뒤 전이학습·과적합
진단을 실제로 보여 준 경우에만 선택합니다.

P2 마지막에는 Karpathy의
[GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY)와
[Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE)를 따라 GPT와 BPE를 직접
구현합니다. CS231n 지정 범위와 PyTorch 보강 뒤에 tokenization, causal mask,
autoregressive loss, generation의 전체 흐름을 연결하고 나서 P3에 진입합니다.

## P3 — NLP·Transformer

P2 끝에서 GPT와 BPE 구현을 마친 것을 전제로
[CS224N Spring 2024](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html)
Assignment 1~4를 **written·수학·programming 요구사항까지 전부 수행**합니다.
RNN·LSTM·attention·Transformer는 이 과정 안에서 연결합니다.
2024 notes와 assignment가 주자료이고, 공개 2023 영상은 설명 보조입니다. 판본을
섞어 과제 요구를 바꾸지 않습니다. Final Project는 완료가 아니라 미완료 보류입니다.
지정 reading은 논문 읽기에 포함하며 별도 월별 논문 quota나 두 번째 Transformer
전체 구현을 겹쳐 요구하지 않습니다. NLP Kaggle은 선택입니다.


## P4 — LLM 구현·학습 시스템·추론 기초

주과정은 [CS336 Spring 2026](https://cs336.stanford.edu/) Assignment 1 Basics와
Assignment 2 Systems 전체와 관련 강의이며 P4 끝에 2026 Lecture 10 inference를
연결합니다. A2는 training
systems 과제이지 serving 과제가 아닙니다. prefill/decode, KV cache, batching과
serving 측정은 강의 10에서 P5 독립 연구로 연결합니다.

공식 AI 정책과 private repository 경계를 따릅니다. 기존 assignment 작업은
보존하며 A1의 tokenizer·LM과 A2의 kernel·분산 학습을 별도 두 번째 산출물로 다시
요구하지 않습니다. 공식 과제와 학습자의 실행·해석이 P4 구현 근거입니다.
기존 A1은 공개 commit
[`a158843b20107949f1a8d7df1b05cd33b9166712`](https://github.com/stanford-cs336/assignment1-basics/tree/a158843b20107949f1a8d7df1b05cd33b9166712)에
고정합니다. 별도 요청 없이 clone·등록·cache·다운로드하지 않습니다.

## P5 — 하나의 독립 inference 연구

프로젝트와 논문 재현을 따로 만들지 않습니다. **하나의 독립 inference research
question**과 관련 논문의 주장 하나를 같은 실험 안에서 재현합니다. 고정 workload와
모델에서 다음을 보고합니다.

- prefill과 decode를 분리한 baseline
- KV cache와 batching의 통제 비교
- 출력 품질 또는 정확성 보존 조건
- memory, latency, throughput 측정
- workload·환경·재현 조건과 측정 오차
- 실패한 시도, 남은 한계, 원 주장과의 차이

논문 선택 때 이 연구 질문에 직접 연결되는 주장을 확인하고 원 논문과 현재
환경·모델·workload의 차이를 먼저 명시합니다. 논문 전체 성능을 재현했다고
일반화하지 않고 실제 비교한 범위의 결과만 보고합니다.

quantization은 baseline과 측정 계약이 안정된 뒤의 선택 항목입니다. 지원·코딩테스트·
시스템 면접 준비도 P5 예산에 포함합니다. 실패해도 원인을 진단하고 측정 한계를
보고했다면 유효한 결과이며 성공으로 바꾸어 기록하지 않습니다.

## 실전 competition 트랙과 논문 읽기

Kaggle은 P1만 필수입니다. P0·P2·P3은 선택이며, P0는 예측을 만들 수 있으면
첫 제출 경험을 제안합니다. **이전 제출 경험을 요구하지 않습니다.** P2·P3는
핵심 학습 이후 선택하며 제출 결과가 다음 Phase의 선수조건은 아닙니다.
이 문서에 특정 대회를 고정하지 않습니다. 실제 후보는 도달 시점에
[실제 목록](https://www.kaggle.com/competitions)을 확인합니다.
데이터 규모·필요 연산량·남은 기간·라이선스와 학습 목적을 읽고 후보를 고르며,
참여 시 해당 Phase 예산 안의 시간 상한을 정합니다. 순위 정체는 학습 실패가
아니며 상한에 도달하면 결과를 해석하고 중단합니다.

공식 과정의 지정 reading을 논문 시간에 포함하고 별도 월별 quota를 더하지 않습니다.
P5만 논문 주장 하나를 독립 연구 질문 안에서 집중 재현합니다.
읽기는 [Keshav의 3-pass](https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf)를
틀로 삼습니다. 학습자가 주장·근거·한계를 먼저 요약하고 Agent는 오독을 짚습니다.
재현 실패도 원인을 규명했다면 유효한 산출물이며 가상의 수치나 성공으로 채우지 않습니다.

## 무보조 설명과 빈 파일 구현 트랙

연결된 학습 단위를 마치면 먼저 1~2분 안에 목적·원리·가정·한계를 말하고 조건 하나를
바꾼 후속 질문 하나에 답합니다. Agent는 정답·수정점·빠진 생각을 한 번에
피드백합니다. 설명과 조건 변경 사례는 하나의 통합 checkpoint이며 이미 이해한
부분은 반복 시험하지 않습니다. Tensor·모델 문제에서는 학습자가 shape와 흐름을
직접 제시합니다. knowledge는 학습자가 대화를 닫고 기억으로 쓴 초안 이후에만
교정하며 AI가 면접 답변집을 먼저 작성하지 않습니다.
주간 점검은 지난주 개념 2개와 더 이전 개념 1개를 예고 없이 묶어 확인합니다.
일반 수업을 매번 진단으로 시작하거나 별도 회상 추적 시스템을 만들지 않습니다.

| Phase | 대표 무보조 재구현 |
|---|---|
| `P0` | scalar autodiff와 MLP training 흐름 |
| `P1` | linear/logistic regression, PCA, k-means, CV loop |
| `P2` | PyTorch train/eval loop와 scaled dot-product attention |
| `P3` | Transformer block과 causal mask |
| `P4` | KV cache와 inference measurement |

공식 과제 수행과 무보조 재구현은 서로 다른 근거입니다. 전체 모듈의 구현이나
전체 과제를 다시 쓰는 의무를 추가하지 않고 위 대표 단위를 확인합니다. 강의·
노트·완성 코드를 닫고 코드·뼈대·import 목록·함수 signature 도움 없이 시도하며,
도움받은 구현을 무보조 성공으로 기록하지 않습니다. deep-ml 챌린지, 시간 제한
구현, 알고리즘 코딩 테스트는 부족한 부분을 보강하는 선택 수단입니다. 해당 Phase의
구술·재구현 또는 지원 활동 예산 안에서 사용하며 별도 문제 수를 졸업 조건으로
추가하지 않습니다. 통과하지 못한 항목은 완료로 기록하지 않습니다.

## GPU, 취업, Phase 전환 점검

P2 시작 전에 단일 GPU 환경에서 CS231n A2와 PyTorch workload가 실행되는지
확인합니다. P4 시작 전에는 CS336 A2 공식 요구를 수행할 유료 GPU 수단을 포함해
환경을 확보합니다. 서비스·비용·사용 한도·공식 요구 충족 여부는 해당 과제 진입 전에
확인하며 현재 설치나 구매를 자동 진행하지 않습니다. 확보하지 못하면
과제를 미완료로 두며 대체 과제로 완료 처리하지 않습니다.

특정 Phase가 취업이나 지원 자격을 보장하지 않습니다. 학위 선호, 직무명, systems
수요를 고정 사실로 두지 않습니다. P1부터 Phase 종료 때 실제 공고 3~5건을 학습자가
열어 요구 역량과 learner-owned 산출물, 빠진 필수 요건, 지원 여부를 대조합니다.
공고가 경로와 다르면 공고를 기준으로 경로를 재검토합니다.

### 직무 사다리와 최종 목표

다음 연결은 저자의 판단이지 채용 공고의 인용이나 취업 시점의 보장이 아닙니다.
지원할 때 실제 공고의 요구사항으로 다시 확인합니다.

| 검토할 직무 | 비교할 학습자 산출물 |
|---|---|
| ML Engineer / AI Engineer (주니어) | 고전 ML 설명, 검증·배포·테스트·모니터링 프로젝트 |
| LLM Application Engineer | Transformer·입력 계약·평가 이해와 실제 응용 요구 사이의 차이 |
| LLM Systems / Inference Engineer | 모델·커널·분산 구현과 품질·메모리·성능 측정 |
| LLM Research Engineer | 독립 연구 질문·통제 실험·논문 재현·한계 보고 |

더 이른 단계 지원을 포기나 실패로 기록하지 않습니다. 불합격도 학습 실패로
기록하지 않고 요구 범위를 재검토하는 정보로 사용합니다.

Phase 종료 전 아래를 확인하고 필수 항목이 비면 Phase를 닫지 않습니다.

| 항목 | 확인 내용 |
|---|---|
| 공식 과제·산출물 | 지정 범위의 직접 수행, 실행·해석과 재현 가능성 |
| 무보조 설명 | Phase의 핵심을 노트 없이 연결하고 바뀐 조건에도 답하는가 |
| 대표 재구현 | 위 대표 단위를 도움 없이 수행했는가, 도움과 미완료를 구분했는가 |
| 지정 독서 | 해당 과정 reading 또는 P5 통합 재현의 주장·근거·한계를 설명하는가 |
| 시간 | 현재 Phase 예산 초과가 이후 일정에 주는 영향 |
| 직무 | P1부터 실제 공고와 산출물·빠진 요건·지원 여부를 대조했는가 |
| 범위 | 다음 Phase의 필수 범위와 보류 항목을 혼동하지 않는가 |

재개 지점이 바뀌면 닫히는 Phase·관찰된 근거·다음 범위를 담은 `STATE.md` 전체
교체안을 먼저 보여 줍니다. **자동으로 쓰이지 않으며 승인해야 반영됩니다.**
Phase ID는 `P0`~`P5`의 정적 위치 참조이며 점수·시간 합계·완료 목록을 넣지 않습니다.
어떤 기록도 새 강의나 추가 실습을 자동으로 선택하지 않습니다.

## 공식 과제의 보존과 공개 경계

MIT 18.05 문제 세트 답안과 CS229·CS231n·CS224N·CS336 공식 과제 답안은
written·코드·노트북·저장 출력 모두 별도 비공개 작업 공간에 보존합니다.
공개 저장소에는 공식 문제 원문·과제 답안·저작권 자료를 넣지 않습니다. 자신의
개념 노트, 공식 답안과 분리된 빈 파일 재구현, 공개 가능한 대회 작업과 재현
보고서만 남깁니다. 자습에도 적용하며 과목별 AI 정책은 `AGENTS.md`를 따릅니다.

## 전문화 방향

1순위는 LLM Systems와 Inference Optimization입니다. latency, throughput, memory,
prefill/decode, batching, KV cache를 직접 구현·측정·디버깅합니다. Post-training,
evaluation, data engineering, multimodal은 현재 경로의 병렬 의무가 아니며 복귀
조건은 `DEFERRED.md`에 둡니다. 이 우선순위는 수학·통계·ML·딥러닝·NLP 선수를
생략한다는 뜻이 아닙니다.
