# Study State

> 이 파일은 simplified study pilot의 재개 북마크입니다. 숙달 기록,
> 점수표, 세션 이력, evidence 저장소, progress database가 아닙니다.

- Pilot 시작일: 미시작 — 첫 simplified session에서 확정
- 마지막 사용자 확인일: 2026-09-02
- 주축: [Stanford CS336 Spring 2026](https://cs336.stanford.edu/)
- 기준 과제: [Assignment 1 at `a158843b20107949f1a8d7df1b05cd33b9166712`](https://github.com/stanford-cs336/assignment1-basics/tree/a158843b20107949f1a8d7df1b05cd33b9166712)
- 현재 범위: Assignment 1 진입 전 통합 준비도 진단

## 관찰된 근거

- [RNN/LSTM sequence modeling](practice/deep-learning/rnn-lstm-sequence-modeling.ipynb)에서
  직접 구현, train/eval, baseline 해석까지 완료한 artifact가 있다.
- 이 artifact는 다시 완료 처리하지 않으며 장기 기억을 증명하지 않는다.

## 재확인할 항목

- 빈 파일에서 모델, 학습, 검증을 연결하고 직접 실행·debug하기
- gradient 흐름과 `zero_grad`, `detach`, `no_grad`, `requires_grad` 설명하기
- 행렬곱, broadcasting, softmax, cross-entropy의 Tensor 계약과
  baseline, validation, metric 사용 설명하기

## 다음 독립 행동

빈 Python 파일에서 deterministic synthetic 다중분류 데이터를 만들고,
작은 `nn.Module`과 `forward`, train/validation 분리, raw logits,
cross-entropy, optimizer, 학습 순서, validation loss와 accuracy를 연결해
직접 실행한다. 이어서 feature 수 또는 class 수가 다른 조건으로 한 번
전이하고 주요 Tensor 역할과 autograd 상태를 설명한다. 오류가 발생했다면
수정 전에 세운 첫 원인 가설과 이를 확인한 방법도 설명한다.
