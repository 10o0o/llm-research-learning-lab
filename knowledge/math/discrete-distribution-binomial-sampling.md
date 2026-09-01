---
title: "이산분포, Binomial, 표본 변동"
updated: 2026-09-01
tags:
  - probability
  - distribution
  - binomial
  - expectation
  - variance
---

# 이산분포, Binomial, 표본 변동

## 핵심 요약

이산 확률변수는 실험의 원시 결과를 숫자로 보내는 규칙이고, PMF는 각 숫자에 모인 확률질량을 나타낸다. PMF의 모든 값은 음수가 아니며 합은 1이다. Binomial은 시행 수가 고정되고, 매 시행의 성공 확률이 같으며, 시행들이 서로 독립일 때만 유지 개수처럼 성공 횟수를 모델링한다.

## 개념 정리

### PMF와 Binomial 조건

네 활성값이 각각 유지 또는 제거될 수 있으면 유지 개수는 0개부터 4개까지의 이산 확률변수다. 유지 확률이 같고 각 활성값의 유지 여부가 독립일 때, 유지 개수는 Binomial 모델로 나타낼 수 있다.

성공 횟수가 $k$, 시행 수가 $n$, 성공 확률이 $p$일 때 PMF는 다음과 같다.

$$
P(K=k) = \binom{n}{k}p^k(1-p)^{n-k}
$$

비복원추출처럼 한 시행 뒤 다음 시행의 확률이 달라지면 독립·공통 확률 조건이 깨진다. 구조화된 dropout도 여러 활성값이나 채널을 함께 유지·제거하므로, 개별 활성값들을 독립 시행으로 보는 단순 Binomial 모델과 맞지 않을 수 있다.

### 기댓값·분산과 반복 표본

기댓값은 확률을 가중치로 쓴 분포의 중심이고, 분산은 그 중심에서 떨어진 정도의 평균 제곱 거리다. Binomial 분포에서는 다음과 같다.

$$
E[K] = np
$$

$$
Var(K) = np(1-p)
$$

분포의 시행 수와 확률은 모델이 고정하지만, 실제로 뽑힌 유지 개수와 그 유한 표본의 평균·분산은 실행마다 달라진다. 따라서 적은 횟수로 관측한 평균과 분산이 이론값과 달라도 곧바로 구현 오류라고 결론 내리면 안 된다.

## 예제 또는 적용

[PMF와 dropout-like sampling 실습](../../practice/probability/stat110-pmf-dropout-sampling-prelab.ipynb)에서 활성값 4개와 유지 확률 0.75를 사용했다. 8개 마스크의 관측 유지 개수는 `[4, 3, 3, 4, 4, 2, 4, 4]`였고, 관측 평균과 분산은 각각 3.5와 0.5였다. 같은 모델의 이론 평균과 분산은 각각 3.0과 0.75이므로, 이 차이를 유한 표본의 변동으로 해석했다.

## 주의점

- 기댓값은 반복했을 때의 중심이지, 매번 실제로 나오는 값이나 반드시 가능한 값이라는 뜻은 아니다.
- 조합계수는 특정 유지 개수가 나오는 경우의 수일 뿐이며, PMF를 만들 때는 유지·제거 확률도 함께 반영해야 한다.
- 채널 단위의 구조화된 dropout을 개별 활성값 독립 모델로 해석하지 않는다.

## 관련 기록

- Practice: [PMF와 dropout-like sampling 실습](../../practice/probability/stat110-pmf-dropout-sampling-prelab.ipynb)
- Source: [Introduction to Probability, Second Edition, Chapter 3–4](../../materials/private/harvard-stat110-probability/00-01_introduction_to_probability_2e.pdf)
