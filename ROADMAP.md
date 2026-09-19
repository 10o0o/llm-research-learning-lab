# LLM Research Engineer Roadmap

이 문서는 상세한 진도표가 아니라 **장기 공부 방향을 잃지 않기 위한 참고 지도**입니다. 역량별 목표 깊이, 선수 관계, 현재 강의자료의 충족도와 보완 기준은 [`CURRICULUM.md`](./CURRICULUM.md)에서 관리합니다. 현재 학습 범위와 다음 행동은 [`STATE.md`](./STATE.md)만 정합니다.

```text
수학과 Tensor
-> 머신러닝 기본과 실험
-> PyTorch와 딥러닝
-> RNN·LSTM Sequence Modeling
-> Transformer와 Language Modeling
-> LLM Systems / Post-training / Evaluation
```

## 주강의 경로와 자료의 역할

목표는 **1년 내 ML Engineer 취업**이며, 고전 ML을 제대로 다진 뒤 그 위에 LLM과
추론 시스템을 얹습니다. 기초를 건너뛰지 않는 것이 이 경로의 설계 원칙입니다.
현재 위치는 `STATE.md`를 따르며, 이 경로가 다른 과정으로 자동 전환할 권한은
아닙니다.

```text
P0 기초 수학·통계 완성
-> P1 고전 ML 제대로
-> P2 딥러닝과 PyTorch 숙련
-> P3 NLP와 Transformer
-> P4 LLM 직접 구현과 시스템
-> P5 포트폴리오와 면접
```

이번 경로에서 뺀 자료는 [`DEFERRED.md`](./DEFERRED.md)에 복귀 조건과 함께
있습니다. 조건이 실제로 발생하면 필요한 범위만 꺼내고 사용자 승인 뒤에
`STATE.md`를 바꿉니다.

### 시간 예산의 근거

학습자가 하루 12시간을 계획하지만, 예산은 **주 60시간(실효)** 기준으로 잡습니다.
12시간 중 깊은 기술 학습으로 실제 전환되는 시간은 그보다 적고, 그 차이를 계획에
미리 넣어 두어야 미달이 곧 붕괴가 되지 않습니다. 초과 달성분은 버퍼입니다.
48주 × 60시간 = 약 2,900시간이 전체 예산입니다.

날짜는 마감이 아니라 **예산**입니다. 크게 밀리면 실력이 아니라 범위가 틀렸거나
공부 외 작업이 시간을 먹고 있다는 신호로 읽습니다. 어떤 Phase도 자동으로 다음
Phase를 선택하지 않습니다.

| Phase | 예산 | 시간 | 범위 |
|---|---|---:|---|
| `P0` 기초 수학·통계 | ~2026-11-01 | ~360h | 진행 중인 Karpathy makemore 마무리(Part 2 E01~E03, Part 3, Part 4), Stat110 연속분포·기댓값·MLE, 신뢰구간·bootstrap·가설검정 |
| `P1` 고전 ML | ~2027-01-10 | ~600h | KANT Advanced ML 완주, CS229로 이론 깊이 보강, Kaggle end-to-end 프로젝트 1개 |
| `P2` 딥러닝·PyTorch | ~2027-02-28 | ~420h | KANT 딥러닝 기초 잔여, CS231n, Karpathy "Let's build GPT"와 Tokenizer, 소규모 DL 프로젝트 |
| `P3` NLP·Transformer | ~2027-05-02 | ~540h | CS224N A1~A4 전부(written·수학·프로그래밍) |
| `P4` LLM 구현·시스템 | ~2027-07-25 | ~720h | 시스템 기초(메모리 계층·GPU 실행 모델), CS336 A1 Basics, CS336 A2 Systems |
| `P5` 포트폴리오·면접 | ~2027-09-19 | ~480h | 추론 최적화 프로젝트, 개념 구술·코딩 테스트 준비, 지원 |

`P1`이 이 경로에서 가장 긴 단일 구간입니다. ML Engineer 면접의 개념 질문은
대부분 여기서 나오고, 나중에 보충하기 가장 어려운 부분이기도 합니다.

### Phase별 자료

`SRC-KAM-*`, `SRC-KDL-*`, `SRC-KBM-*`, `SRC-HARV-STAT110-*`는 이미 보유한
자료이며 `CURRICULUM.md` registry에 등록돼 있습니다. 새로 확보할 것은 공개
강의뿐입니다.

| Phase | 주자료 | 역할 |
|---|---|---|
| `P0` | [Karpathy — Zero to Hero](https://karpathy.ai/zero-to-hero.html), `SRC-HARV-STAT110-2E-00-01`, `SRC-KBM-*` | 진행 중인 구현을 끊지 않으면서 확률·통계 공백을 메움 |
| `P1` | `SRC-KAM-*`(보유), [CS229](https://cs229.stanford.edu/) | KANT는 실무 절차, CS229는 유도와 이론. 두 축을 같이 감 |
| `P2` | `SRC-KDL-*`(보유), [CS231n](https://cs231n.stanford.edu/), [PyTorch Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html) | PyTorch 숙련도는 CS336 공식 선수 조건 |
| `P3` | [CS224N Spring 2024](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html) | CS336이 명시한 선수 배경 중 하나 |
| `P4` | [CS336 Spring 2026](https://cs336.stanford.edu/) A1, A2 | A2가 1순위 전문화 `TR-SYS-03`·`TR-SYS-04`의 본체 |
| `P5` | 자기 구현 모델 위의 직접 실험 | baseline·통제 비교·ablation·재현 조건·한계 보고 |

### Karpathy 수행 강의

| 순서 | 강의 | 공개 영상 | 공식 구현 자료 | Phase |
|---|---|---|---|---|
| 1 | micrograd | [영상](https://www.youtube.com/watch?v=VMj-3S1tku0) | [노트북](https://github.com/karpathy/nn-zero-to-hero/tree/master/lectures/micrograd) | 완료 |
| 2 | makemore: Bigram | [영상](https://www.youtube.com/watch?v=PaCmpygFfXo) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part1_bigrams.ipynb) | 완료 |
| 3 | makemore Part 2: MLP | [영상](https://www.youtube.com/watch?v=TCH_1BHY58I) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part2_mlp.ipynb) | `P0` 진행 중 |
| 4 | makemore Part 3: Activations, Gradients, BatchNorm | [영상](https://www.youtube.com/watch?v=P6sfmUTpUmc) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part3_bn.ipynb) | `P0` |
| 5 | makemore Part 4: Becoming a Backprop Ninja | [영상](https://www.youtube.com/watch?v=q8SA3rM6ckI) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part4_backprop.ipynb) | `P0` |
| 6 | Let's build GPT from scratch | [영상](https://www.youtube.com/watch?v=kCc8FmEb1nY) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/ng-video-lecture) | `P2` |
| 7 | Let's build the GPT Tokenizer | [영상](https://www.youtube.com/watch?v=zduSFxRajkE) | [minbpe](https://github.com/karpathy/minbpe) | `P2` |

Part 4는 MLP 전체 backward를 손으로 씁니다. `P4`에서 Triton kernel을 쓰려면
backward를 손으로 쓸 수 있어야 하므로 systems 트랙의 직접 선수입니다.
makemore Part 5(WaveNet)는 뺐고 복귀 조건은 `DEFERRED.md`에 있습니다.
[Let's reproduce GPT-2 (124M)](https://www.youtube.com/watch?v=l8pRSuU81PU)은
`P4` 진입 전 **Optional**입니다.

### 이 경로가 지키는 선수 조건

CS336 공식 선수 조건은 "strong familiarity with PyTorch", "basic systems
concepts like the memory hierarchy", "comfort with the basics of machine
learning and deep learning"(CS221·CS229·CS230·CS124·CS224N 중 하나)입니다.
`P1`이 CS229를, `P2`가 PyTorch 숙련을, `P3`가 CS224N을, `P4` 도입부가 시스템
기초를 각각 담당합니다. 이 순서를 앞당기지 않습니다.

### 산출물

각 Phase는 이력서에 쓸 수 있는 산출물을 하나씩 남깁니다. 강의 수강 자체는
산출물이 아닙니다.

| Phase | 산출물 |
|---|---|
| `P0` | makemore MLP 구현과 초기화·학습 실험 보고 |
| `P1` | Kaggle end-to-end 프로젝트: baseline, 누수 방지, error analysis, 한계 보고 |
| `P2` | 소규모 DL 프로젝트와 처음부터 구현한 GPT·BPE |
| `P3` | CS224N A1~A4 |
| `P4` | 자기 구현 Transformer LM과 FlashAttention2 Triton kernel |
| `P5` | 추론 최적화 프로젝트: latency·throughput·메모리 측정과 개선 보고 |

공식 저장소의 완성 노트북은 참고 자료입니다. 강의 속 전체 구현을 수행하고
별도 exercises도 직접 시도합니다. 영상·문서·공식 자료 기반 대화를 허용하며,
설명 매체를 바꾸어도 공식 내용과 실습을 축소하지 않습니다. 완성 노트북 실행이나
AI 보충 예제로 공식 실습을 대체하지 않습니다. 접근·실행 제약은 명시하고 해당 실습은 미완료로
남깁니다. Optional·Bonus는 선택 항목으로 표시합니다.

CS336 assignment는 공식 AI 정책을 엄격히 따르며 제약은 `AGENTS.md`에 있습니다.
CS224N 공식 AI 정책도 수행 시점에 그대로 적용됩니다. KANT 자료는 `P1`·`P2`의
정식 주자료이며 자체 실습을 포함하지만, 다른 과정의 공식 실습을 대체하거나
완료 기준이 되지 않습니다.


## 전문화 우선순위

현재의 1순위 전문화 방향은 **LLM Systems와 Inference Optimization**입니다. latency, throughput, memory, batching, KV cache와 quantization을 실제 측정·구현·디버깅하는 역량을 우선합니다.

2순위는 **Post-training과 LLM Evaluation**입니다. SFT·LoRA·preference optimization을 평가 설계, failure analysis, contamination 점검과 연결합니다.

Modeling과 Computer Vision은 별도 주력 트랙이 아니라 위 전문화를 이해하거나 검증하는 데 필요한 선수개념·연결 학습으로 다룹니다. 이 우선순위는 공통 핵심의 선수 관계를 건너뛴다는 뜻이 아닙니다. 필요한 prerequisite가 확인되면 현재 범위 안에서 보충을 제안하고 사용자 승인 뒤에만 `STATE.md`의 다음 행동을 바꿉니다.

## 정적 목표 endpoint

아래 표는 전문화 방향의 도착점을 고정할 뿐, 완료 여부나 현재 진도를 기록하거나 다음 목표를 자동으로 선택하지 않습니다. Pilot 중 실제 다음 목표는 `STATE.md`에 사용자가 승인한 내용만 사용합니다.

| 우선순위 | 단계 | 방향 | Endpoint |
|---:|---:|---|---|
| 1 | `1A` | Systems·Inference | `TR-SYS-03` |
| 1 | `1B` | Systems·Inference | `TR-SYS-04` |
| 2 | `2A` | Post-training·Evaluation | `TR-MOD-03` |
| 2 | `2B` | Post-training·Evaluation | `TR-EVAL-02` |
| 2 | `2C` | Post-training·Evaluation | `TR-EVAL-05` |

Modeling과 Computer Vision은 이 endpoint에 필요한 선수개념 또는 연결 학습으로만 선택합니다.

## 1. 수학과 Tensor

- 선형대수, 미분, 확률
- Tensor shape, broadcasting
- softmax, cross entropy, gradient

## 2. 머신러닝 기본과 실험

- train/validation/test와 data leakage
- loss, metric, generalization
- baseline과 error analysis
- 필요할 때 Kaggle 프로젝트 하나

## 3. PyTorch와 딥러닝

- forward, backward, optimizer
- 학습 루프와 디버깅
- normalization과 regularization
- RNN recurrence·unroll과 LSTM state·gate를 직접 구현하고 실제 sequence task에서 비교

## 4. Transformer와 Language Modeling

- `CC-SEQ-01`은 sequence 개념의 참고 역량이며, 전체 구현 완료를 일률적인 진입 조건으로 삼지 않음
- tokenization과 embedding
- attention과 Transformer block
- autoregressive training과 generation

## 5. 전문 분야

- LLM Systems: latency, throughput, memory, batching, KV cache
- Post-training: SFT, LoRA, preference optimization
- Evaluation: metric, failure analysis, contamination

누적 구현 골격과 module별 assignment·주요 phase capstone은 `CURRICULUM.md`의 정적 catalog가 관리합니다. 이 catalog와 ROADMAP endpoint는 진도나 mastery를 기록하지 않습니다.

TIL, `knowledge/`, 실제 실습 결과는 설명 수준과 보충 필요성을 판단하는 참고 근거입니다. 현재 source나 과제가 끝나면 Agent는 다음 선택지를 제안하고, 사용자가 승인한 뒤에만 `STATE.md`를 교체합니다. 어떤 기록도 새 강의나 추가 실습을 자동으로 선택하지 않습니다.
