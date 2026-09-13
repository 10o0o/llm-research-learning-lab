---
title: "표본 공분산과 PCA 투영"
updated: 2026-09-14
tags:
  - pca
  - covariance
  - dimensionality-reduction
---

# 표본 공분산과 PCA 투영

## 핵심 요약

PCA는 중심화한 데이터의 공분산행렬에서 분산이 큰 고유벡터 방향을 선택해, 각 샘플을 더 적은 수의 좌표로 표현하는 차원 축소 방법이다.

## 개념 정리

### 중심화와 표본 공분산

샘플 행렬 `X`의 shape이 `(N, d)`이면, feature별 평균 `mean`의 shape은 `(d,)`이고 중심화한 행렬 `X_c = X - mean`의 shape은 `(N, d)`이다. 표본 공분산은 다음과 같으며 shape은 `(d, d)`이다.

$$
C = \frac{X_c^T X_c}{N - 1}
$$

대각 원소는 각 feature의 표본분산이고, 비대각 원소는 두 feature가 함께 변하는 경향이다. `N - 1`로 나누므로 `N >= 2`가 필요하다.

### 주성분 선택과 투영

공분산행렬 `C`는 실수 대칭행렬이다. `np.linalg.eigh(C)`로 고유분해하면 고유값은 각 고유벡터 방향으로 투영한 데이터의 표본분산을 나타낸다. `eigh`는 고유값을 작은 순서로 반환하므로, 고유값과 대응 고유벡터 열을 같은 인덱스 순서로 큰 값부터 재정렬한다.

상위 `k`개 고유벡터 열을 `components`로 두면 shape은 `(d, k)`이고, 각 중심화 샘플의 주성분 좌표는 다음처럼 계산한다.

$$
scores = X_c \; components
$$

`scores`의 shape은 `(N, k)`이다. `k`는 `1 <= k <= d`를 만족해야 한다. 버리는 방향의 분산이 0이면 그 방향을 제거해도 재구성 정보가 줄지 않는다.

### 표준화의 선택

중심화는 공분산 기반 PCA의 기본 단계다. 반면 표준화는 feature의 단위나 스케일 차이가 큰 분산만으로 주성분을 지배하지 않게 하려는 선택이며, 항상 적용하는 규칙은 아니다.

## 예제 또는 적용

`[[1, 2], [2, 4], [3, 6]]`의 평균은 `[2, 4]`이고 표본 공분산은 `[[1, 2], [2, 4]]`이다. 고유값은 큰 순서로 `[5, 0]`이며, 버리는 방향의 분산이 0이므로 한 주성분만으로 데이터를 정확히 재구성할 수 있다.

## 주의점

고유벡터의 부호는 반대로 반환될 수 있다. component와 score의 부호가 함께 바뀌면 `scores @ components.T + mean`으로 얻는 재구성 결과는 같다.

## 관련 기록

- Knowledge: [고유기저와 행렬 대각화](./eigenbasis-diagonalization.md)
- TIL: [2026-08-20](../../til/2026/08/2026-08-20.md)
- Practice: [linear-algebra-recall](../../practice/math/linear-algebra-recall.ipynb)
- Source: KANT 기초수학, 3장 2강 「행렬 대각화와 PCA 구현」
