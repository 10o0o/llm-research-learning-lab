---
title: "RNN/LSTM sequence classification"
updated: 2026-09-01
tags:
  - deep-learning
  - sequence-modeling
  - pytorch
---

# RNN/LSTM sequence classification

## 핵심 요약

순서가 있는 입력을 문장 단위로 분류할 때 RNN은 이전 hidden state를 다음 위치로 전달하고, 같은 recurrent parameter를 모든 위치에서 재사용한다. LSTM은 hidden state와 별도의 cell state를 함께 이어 가며, gate로 보존·기록·노출을 조절한다. 최종 분류에는 마지막 hidden state를 linear readout에 넣어 sequence-level logits를 만든다.

## 개념 정리

### RNN의 state와 parameter sharing

- 현재 위치의 입력과 직전 hidden state가 다음 hidden state를 만든다.
- 직전 hidden state는 앞선 토큰에서 얻은 정보를 다음 위치로 전달하는 통로다.
- 입력-hidden, hidden-hidden parameter는 위치마다 새로 생기지 않고 모든 위치에서 공유된다.
- 오래전 정보는 같은 recurrent 경로를 여러 번 지나므로 영향이나 gradient가 작아지거나 커질 수 있다.

### LSTM의 hidden state와 cell state

- `h`는 다음 위치와 readout에 노출되는 hidden state다.
- `c`는 위치를 따라 이어지는 내부 cell memory다.
- forget gate는 기존 memory의 보존량, input gate는 새 정보의 기록량, output gate는 memory 중 hidden state로 노출할 양을 조절한다.
- 따라서 LSTM도 무조건 기억하는 장치는 아니다. gate가 보존하지 않도록 학습되면 이전 memory의 직접 기여는 줄어든다.

### sequence classifier의 data flow

`inputs`의 shape가 `(batch, steps, input)`이면 각 위치에서 `inputs[:, t, :]`는 `(batch, input)`이다.

- RNN cell은 현재 입력과 이전 `h`를 받아 다음 `h`를 만든다.
- LSTM cell은 현재 입력, 이전 `h`, 이전 `c`를 받아 다음 `h`, `c`를 만든다.
- 위치 loop가 끝난 뒤의 마지막 `h`를 readout에 넣으면 logits shape는 `(batch, classes)`다.
- native batch-first recurrent API의 `output`은 모든 위치의 hidden result를 보존하고, `h_n`은 마지막 hidden state, `c_n`은 마지막 cell state를 보존한다.

### train과 evaluation

- 학습 순서는 `zero_grad → forward → loss → backward → step`이다. 파라미터는 `forward`가 아니라 `optimizer.step()`에서 바뀐다.
- 평가는 `model.eval()`과 `torch.no_grad()` 아래에서 logits의 class 축 `argmax`를 label과 비교해 accuracy를 계산한다. 평가에는 `backward`나 `step`이 없다.
- sequence 모델과 baseline을 비교할 때는 generated data, train/eval split, readout, optimizer, learning rate, epoch budget 같은 조건을 고정한다.

## 주의점

- sequence-level label이 앞쪽 토큰의 정보에 달려 있다면 마지막 원본 토큰만 readout에 넣는 baseline은 필요한 단서를 보지 못할 수 있다. 마지막 hidden state는 앞선 위치의 정보를 전달받은 결과라는 점이 다르다.
- 한 seed와 하나의 synthetic delay에서의 결과는 RNN과 LSTM의 일반적 성능 우위를 증명하지 않는다.

## 관련 기록

- Practice: [RNN/LSTM sequence modeling](../../practice/deep-learning/rnn-lstm-sequence-modeling.ipynb)
