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

승인된 학습 경로는 **Karpathy 초반 세 강과 공식 exercises → CS224N 2024
공식 과제·프로젝트 → 기존 CS336 Assignment 1 복귀**입니다. 현재 위치는 `STATE.md`를
따르며, 이 경로가 다른 과정으로 자동 전환할 권한은 아닙니다.

| 구간 | 주강의와 범위 | 연결 자료·실습 |
|---|---|---|
| 기초 | [Karpathy — Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)의 아래 세 강 | 각 강의 속 전체 구현과 공식 exercises. [PyTorch Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)는 구현 표현을 연결하는 보조 자료 |
| NLP·Transformer | [CS224N Spring 2024](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html)의 Word Vectors → Language Models → Backpropagation·Dependency Parsing → RNN → Seq2Seq·Attention·번역 → Transformers → Pretraining과 과제·프로젝트에 필요한 강의 | A1~A4의 written·수학·프로그래밍 요구사항과 Final Project 하나. 기본값은 공식 BERT 프로젝트 |
| 직접 구현 | [CS336 Spring 2026](https://cs336.stanford.edu/)의 기존 Assignment 1 작업으로 복귀 | 별도 과제 레포와 공식 환경·도움 정책 |

초기 주강의의 정확한 순서는 다음과 같습니다.

1. **The spelled-out intro to neural networks and backpropagation: building micrograd**
2. **The spelled-out intro to language modeling: building makemore**
3. **Building makemore Part 2: MLP**

| 강의 | 공개 영상 | 공식 구현 자료 | 공식 exercises |
|---|---|---|---|
| micrograd | [영상](https://www.youtube.com/watch?v=VMj-3S1tku0) | [노트북](https://github.com/karpathy/nn-zero-to-hero/tree/master/lectures/micrograd) | [설명란의 Colab](https://colab.research.google.com/drive/1FPTx1RXtBfc4MaTkf7viZZD4U2F9gtKN?usp=sharing) |
| makemore: Bigram | [영상](https://www.youtube.com/watch?v=PaCmpygFfXo) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part1_bigrams.ipynb) | 영상 설명란 E01~E06 |
| makemore Part 2: MLP | [영상](https://www.youtube.com/watch?v=TCH_1BHY58I) | [노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part2_mlp.ipynb) | 영상 설명란 E01~E03 |

공식 저장소의 완성 노트북은 참고 자료입니다. 강의 속 전체 구현을 수행하고
별도 exercises도 직접 시도합니다. micrograd 도입부의 이해만으로 전체
강의를 완료 처리하지 않습니다. 엔진 전체를 암기해 다시 쓰는 추가 시험은 없습니다.

CS224N은 [2024 공개 영상](https://www.youtube.com/playlist?list=PLoROMvodv4rOaMFbaqxPDoLWjDaRAdP9D)과
[같은 판본의 일정·과제](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html#schedule),
[프로젝트 안내](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html#coursework)를
함께 사용합니다. A1 word vectors, A2 신경망·Tensor 미분·dependency parsing,
A3 Seq2Seq·attention·subword 번역, A4 Transformer 자기지도학습·fine-tuning의
written·수학·프로그래밍 부분을 모두 포함합니다. Final Project 하나를
수행하며 기본값은 공식 BERT 프로젝트입니다. 변경·생략은 사용자 결정으로만 합니다.

Karpathy에서 개념을 배우고, PyTorch 자료로 Tensor·parameter 직접 조작을
`nn.Module`·DataLoader·optimizer에 연결합니다. 공식 구현·exercises·assignments가
기본 실습입니다. KANT는 진도·주제 대조용이며 기본 실습이나 완료 기준으로
사용하지 않습니다. 필요한 [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1)
단원도 공식 요구사항을 이해하는 보조 자료로 사용합니다.
CS229와 MIT 6.S191은 필요한 수학적 설명이나 전체 구조를 보완하는 참고
자료로 두고 별도 완강 목표를 추가하지 않습니다.

영상·문서·공식 자료 기반 대화를 허용하며 설명 방식이 달라도 공식 내용과
실습을 축소하지 않습니다. 완성 노트북 실행이나 AI 보충 예제로 공식 실습을
대체하지 않습니다. 현재 설명에 필요한 선수개념만 보강하고 같은 주강의로
돌아갑니다. Optional·Bonus는 선택 항목으로 표시합니다. 접근·실행 제약은
명시하고 해당 실습은 미완료로 남깁니다. 기존 학습 기록과 코드는 보존합니다.

CS336 복귀는 다음을 실제 구현·실행·해석한 근거로 제안합니다.

- 공식 API 문서를 참고하며 작은 모델의 학습·검증 프로그램을 구성한다.
- 입력 feature 수나 class 수를 바꾸고 모델 출력·target·loss의 관계를 맞춘다.
- token ID, embedding, attention, logits, 다음 token target과 causal mask의
  관계를 작은 예제로 추적한다.

준비도 충족이 남은 CS224N 공식 과제나 프로젝트를 자동 취소하지 않습니다.
순서 변경을 제안할 때 남은 범위를 미완료로 명시하고 사용자 결정을 따릅니다.
tokenizer·Transformer 사전 완성을 추가 진입 시험으로 요구하지 않습니다.
기존 과제 작업을 보존하고 사용자 승인 뒤에만 현재 과정을 전환합니다.

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
