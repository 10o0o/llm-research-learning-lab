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

승인된 학습 경로는 **Karpathy Zero to Hero의 선별된 강의 → CS336 Assignment 1 →
CS336 Assignment 2(Systems) → 추론 최적화 직접 프로젝트**입니다. 1순위 전문화인
LLM Systems·Inference Optimization까지 가는 최단 경로로 구성했습니다. 현재 위치는
`STATE.md`를 따르며, 이 경로가 다른 과정으로 자동 전환할 권한은 아닙니다.

이번 경로에서 뺀 자료는 버린 것이 아니라 [`DEFERRED.md`](./DEFERRED.md)에 무엇을
열어 주는 자료인지와 다시 꺼낼 조건을 함께 적어 두었습니다. 조건이 실제로
발생하면 그때 필요한 범위만 꺼내 쓰고, 사용자 승인 뒤에 `STATE.md`를 바꿉니다.

### Phase와 시간 예산

아래 날짜는 마감이 아니라 **예산**입니다. 진도가 예산에서 크게 밀리면 실력이
모자란 것이 아니라 범위가 틀렸거나 공부 외의 작업이 시간을 먹고 있다는 신호로
읽고, 그때 경로를 다시 정합니다. 어떤 Phase도 자동으로 다음 Phase를 선택하지
않습니다.

| Phase | 예산 | 범위 | 도착점 |
|---|---|---|---|
| `P0` 기초 완성 | ~2026-10-18 (4주) | Karpathy makemore Part 2 잔여(E01~E03), Part 3, Part 4 | 초기화·정규화·gradient를 손으로 추적하고, MLP 전체 backward를 직접 쓴다 |
| `P1` Transformer 구현 | ~2026-11-15 (4주) | Karpathy "Let's build GPT", "Let's build the GPT Tokenizer" | decoder-only Transformer와 BPE를 처음부터 구현하고 모든 shape를 설명한다 |
| `P2` CS336 A1 | ~2027-01-17 (9주) | 기존 CS336 Assignment 1 복귀: BPE tokenizer, Transformer LM, 학습 루프 | 공식 테스트를 통과하는 자기 구현 LM을 학습·검증한다 |
| `P3` CS336 A2 Systems | ~2027-03-14 (8주) | 프로파일링, 벤치마킹, 메모리 회계, Triton kernel, FlashAttention, 분산 | **1순위 전문화의 본체.** 커널을 직접 쓰고 측정으로 개선을 입증한다 |
| `P4` 추론 최적화 | ~2027-04-25 (6주) | 자기 구현 모델의 KV cache, prefill/decode 분리, continuous batching, quantization | latency·throughput·메모리를 측정·개선하고 한계를 보고한다 |

`P3`가 `ROADMAP` endpoint `TR-SYS-03`·`TR-SYS-04`에 직접 닿는 구간입니다.
`P0`~`P2`는 그 구간을 실제로 수행하기 위한 선수 작업이며, 그 자체가 목적이
아닙니다.

### Phase별 자료

| 구간 | 주강의와 범위 | 연결 자료·실습 |
|---|---|---|
| `P0`·`P1` | [Karpathy — Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)의 선별 강의 | 각 강의 속 전체 구현과 공식 exercises. [PyTorch Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)는 구현 표현을 연결하는 보조 자료 |
| `P2`·`P3` | [Stanford CS336 Spring 2026](https://cs336.stanford.edu/) Assignment 1, Assignment 2 | 별도 과제 레포와 공식 환경·도움 정책. 공식 테스트가 완료 기준 |
| `P4` | 자기 구현 모델 위의 직접 실험 | baseline·통제 비교·ablation·재현 조건·한계 보고를 포함하는 `PHASE_CAPSTONE` |

Karpathy 구간에서 실제로 수행할 강의는 다음과 같습니다. 순서를 지킵니다.

| 순서 | 강의 | 공개 영상 | 공식 구현 자료 | 이 경로에서 남긴 이유 |
|---|---|---|---|---|
| 1 | micrograd | [영상](https://www.youtube.com/watch?v=VMj-3S1tku0) | [노트북](https://github.com/karpathy/nn-zero-to-hero/tree/master/lectures/micrograd) | 완료. autograd의 작동 방식 |
| 2 | makemore: Bigram | [영상](https://www.youtube.com/watch?v=PaCmpygFfXo) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part1_bigrams.ipynb) | 완료. 언어 모델링과 NLL |
| 3 | makemore Part 2: MLP | [영상](https://www.youtube.com/watch?v=TCH_1BHY58I) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part2_mlp.ipynb) | 진행 중. embedding, 미니배치, train/dev 분리 |
| 4 | makemore Part 3: Activations, Gradients, BatchNorm | [영상](https://www.youtube.com/watch?v=P6sfmUTpUmc) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part3_bn.ipynb) | 초기화 배율, activation·gradient 분포, 정규화. 저정밀도 학습이 왜 터지는지 이해하는 기초 |
| 5 | makemore Part 4: Becoming a Backprop Ninja | [영상](https://www.youtube.com/watch?v=q8SA3rM6ckI) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part4_backprop.ipynb) | MLP 전체 backward 수기 구현. **fused·Triton kernel을 쓰려면 backward를 손으로 쓸 수 있어야 하므로 systems 트랙의 직접 선수** |
| 6 | Let's build GPT from scratch | [영상](https://www.youtube.com/watch?v=kCc8FmEb1nY) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/ng-video-lecture) | decoder-only Transformer 전체 구현. `P2`의 직접 선수 |
| 7 | Let's build the GPT Tokenizer | [영상](https://www.youtube.com/watch?v=zduSFxRajkE) | [minbpe](https://github.com/karpathy/minbpe) | BPE. CS336 A1 전반부와 직접 대응 |

makemore Part 5(WaveNet)는 이번 경로에서 뺐습니다. 이유와 복귀 조건은
`DEFERRED.md`에 있습니다. [Let's reproduce GPT-2 (124M)](https://www.youtube.com/watch?v=l8pRSuU81PU)은
`P1`과 `P2` 사이의 **Optional**입니다. mixed precision, `torch.compile`, flash
attention, DDP를 실제 학습 속도 개선으로 보여 주므로 systems 트랙과 맞지만,
같은 내용을 `P3`가 더 엄밀하게 다루므로 완료 조건에는 넣지 않습니다.

공식 저장소의 완성 노트북은 참고 자료입니다. 강의 속 전체 구현을 수행하고
별도 exercises도 직접 시도합니다. 엔진 전체를 암기해 다시 쓰는 추가 시험은 없습니다.

CS336은 각 Assignment의 공식 handout과 공식 테스트를 완료 기준으로 씁니다.
Assignment 1은 이미 시작한 작업이 있으므로 보존한 상태에서 복귀하고, 새 clone이나
download는 사용자가 따로 요청할 때만 합니다. 공식 AI 정책을 엄격히 따르며 해당
제약은 `AGENTS.md`에 있습니다.

Karpathy에서 개념을 배우고, PyTorch 자료로 Tensor·parameter 직접 조작을
`nn.Module`·DataLoader·optimizer에 연결합니다. 공식 구현·exercises·assignments가
기본 실습입니다. KANT는 진도·주제 대조용이며 기본 실습이나 완료 기준으로
사용하지 않습니다. CS229와 MIT 6.S191은 필요한 수학적 설명을 보충하는 참고
자료로 두고 별도 완강 목표를 추가하지 않습니다.

영상·문서·공식 자료 기반 대화를 허용하며 설명 방식이 달라도 공식 내용과
실습을 축소하지 않습니다. 완성 노트북 실행이나 AI 보충 예제로 공식 실습을
대체하지 않습니다. 현재 설명에 필요한 선수개념만 보강하고 같은 주강의로
돌아갑니다. Optional·Bonus는 선택 항목으로 표시합니다. 접근·실행 제약은
명시하고 해당 실습은 미완료로 남깁니다. 기존 학습 기록과 코드는 보존합니다.

CS224N Spring 2024는 이번 경로에서 뺐습니다. A1~A4와 BERT 파이널 프로젝트의
개별 판단 근거와 복귀 조건은 `DEFERRED.md`에 있습니다. 남은 범위는 완료가 아니라
**미완료로 보류**입니다.


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
