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

- `CC-SEQ-01`을 필수 연결 역량으로 먼저 완료
- tokenization과 embedding
- attention과 Transformer block
- autoregressive training과 generation

## 5. 전문 분야

- LLM Systems: latency, throughput, memory, batching, KV cache
- Post-training: SFT, LoRA, preference optimization
- Evaluation: metric, failure analysis, contamination

누적 구현 골격과 module별 assignment·주요 phase capstone은 `CURRICULUM.md`의 정적 catalog가 관리합니다. 이 catalog와 ROADMAP endpoint는 진도나 mastery를 기록하지 않습니다.

TIL, `knowledge/`, 실제 실습 결과는 설명 수준과 보충 필요성을 판단하는 참고 근거입니다. 현재 source나 과제가 끝나면 Agent는 다음 선택지를 제안하고, 사용자가 승인한 뒤에만 `STATE.md`를 교체합니다. 어떤 기록도 새 강의나 추가 실습을 자동으로 선택하지 않습니다.
