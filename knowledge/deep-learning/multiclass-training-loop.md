---
title: "다중분류 학습 loop와 autograd"
updated: 2026-09-02
tags:
  - deep-learning
  - pytorch
  - multiclass-classification
  - autograd
---

# 다중분류 학습 loop와 autograd

## 핵심 요약

다중분류 모델은 입력을 class별 raw logits로 바꾸고, `CrossEntropyLoss`로 정답 class의 오차를 계산한다. 학습은 `zero_grad → forward → loss → backward → step` 순서로 진행하며, `backward()`가 계산한 gradient는 model parameter의 `.grad`에 저장된다. 검증은 `model.eval()`과 `torch.no_grad()` 아래에서 loss와 class-axis `argmax` 기반 accuracy를 계산한다.

## 개념 정리

### Tensor 역할과 Shape

입력 feature 수가 `F`, class 수가 `C`, batch 크기가 `B`라면:

```text
X:              (B, F)
layer.weight:   (C, F)
layer.bias:     (C,)
logits:         (B, C)
target:         (B,)
loss:           scalar
```

`nn.Linear(F, C)`의 저장된 weight는 `(C, F)`이고, 입력의 마지막 차원 `F`를 출력 차원 `C`로 바꾼다. 개념적으로는 다음과 같은 흐름이다.

```python
logits = X @ layer.weight.T + layer.bias
```

행렬곱은 `(B, F) @ (F, C)`를 `(B, C)`로 만든다. bias `(C,)`는 오른쪽 차원부터 맞춰져 `(1, C)`처럼 해석되고 batch의 각 행에 broadcasting된다.

### Cross-Entropy 계약

```text
input logits:  (B, C), floating-point dtype
target:        (B,), torch.long
target value:  0 <= target < C
```

target은 one-hot 벡터가 아니라 각 샘플의 정답 class index다. `CrossEntropyLoss`가 logits 내부에서 log-softmax와 negative log-likelihood 계산을 처리하므로, loss에 전달하기 전에 softmax를 직접 적용하지 않는다. 예측 class는 `logits.argmax(dim=1)`로 얻으며 shape은 `(B,)`이다.

### 학습과 검증의 분리

한 번의 parameter update는 다음 순서를 따른다.

```text
optimizer.zero_grad()
→ logits = model(train_X)
→ loss = criterion(logits, train_y)
→ loss.backward()
→ optimizer.step()
```

gradient는 기본적으로 누적되므로 다음 update 전에 `zero_grad()`가 필요하다. parameter는 forward에서 바뀌지 않고 `optimizer.step()`에서 바뀐다.

검증에서는 다음을 사용한다.

```text
model.eval()
torch.no_grad() 안에서 validation logits와 loss 계산
argmax(dim=1)로 예측
label과 비교해 accuracy 계산
```

baseline은 학습하지 않는 단순한 기준이다. 예를 들어 train label에서 가장 많이 등장한 class를 validation 전체에 예측해 model accuracy와 비교할 수 있다.

### Autograd 상태

`requires_grad`는 Tensor를 계산 그래프에 기록해 gradient를 계산할지 결정한다.

- model parameter: 보통 `requires_grad=True`
- 입력 feature: 보통 `requires_grad=False`
- class label: `requires_grad=False`

입력 feature가 gradient를 요구하지 않아도 parameter가 gradient를 요구하면 parameter까지의 연산이 graph에 기록된다. `loss.backward()` 후 gradient는 loss 자체가 아니라 leaf parameter에 저장된다.

```python
model.fc.weight.grad
model.fc.bias.grad
```

`no_grad()`는 블록 안의 계산 graph 생성을 막는다. `detach()`는 특정 Tensor를 현재 graph에서 분리한다. 둘 다 parameter gradient가 validation 경로로 만들어지는 것을 막는 데 도움을 주지만, `model.eval()`은 dropout이나 batch normalization 등의 평가 동작을 전환하는 별도의 기능이다.

## 예제 또는 적용

직접 실행한 작은 분류 문제에서 입력은 `(9, 2)`였고, train/validation 분리 후 `nn.Linear(2, 3)`으로 `(batch, 3)` logits를 만들었다. 세 번째 feature를 추가해 입력을 `(N, 3)`으로 바꾸고 `nn.Linear(3, 3)`을 사용했을 때 weight는 `(3, 3)`, logits는 여전히 `(batch, 3)`이었다.

실행 결과를 해석할 때 train loss가 감소하는지, validation accuracy가 단순 baseline보다 높은지 함께 확인했다.

## 주의점

- logits에 softmax를 직접 적용한 뒤 `CrossEntropyLoss`에 넣지 않는다.
- target은 실수 확률 벡터가 아니라 `torch.long` class index다.
- `requires_grad=True`는 gradient 계산 여부이고, optimizer에 전달하는 것은 실제 update 대상 여부다.
- `no_grad()`가 `optimizer.step()` 자체를 호출하지 못하게 하는 것은 아니다. 평가 경로에서 graph와 gradient를 만들지 않도록 하는 기능이다.
- 하나의 작은 synthetic dataset에서 loss나 accuracy가 좋아진 사실만으로 일반적인 모델 성능을 결론 내리지 않는다.

## 관련 기록

- TIL: [2026-09-02](../../til/2026/09/2026-09-02.md)
- Practice: [이번 진단 코드](../../main.py)
- Source: [Stanford CS336 Spring 2026](https://cs336.stanford.edu/)
