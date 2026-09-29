---
title: "SVD 저랭크 근사와 스펙트럴 오차"
updated: 2026-09-29
tags:
  - svd
  - rank
  - approximation
---

# SVD 저랭크 근사와 스펙트럴 오차

## 핵심 요약

영인 특잇값에 대응하는 기여는 생략해도 원래 행렬을 정확히 복원한다.
작은 양의 특잇값에 대응하는 기여를 버리면 근사가 된다. 스펙트럴 노름으로
잰 오차는 모든 단위 입력에서 생길 수 있는 최대 출력 차이다.

## 개념 정리

### 정확한 생략과 근사

SVD는 대응하는 특이벡터의 외적에 특잇값을 곱해 더한 것과 같다.
양의 특잇값 개수를 rank로 두면 다음과 같다.

$$
A=\sum_{i=1}^{r}\sigma_i\mathbf u_i\mathbf v_i^\mathsf T,
\qquad
\widehat A_k=\sum_{i=1}^{k}\sigma_i\mathbf u_i\mathbf v_i^\mathsf T
$$

양의 특잇값을 모두 포함하면 정확하다. 일부만 남기면 원래 행렬과 같은
크기의 낮은 rank 행렬이 된다. 원래 행·열을 삭제하는 연산은 아니다.

### 오차의 의미

$$
\|A-\widehat A_k\|_2
=\max_{\|\mathbf x\|_2=1}\|A\mathbf x-\widehat A_k\mathbf x\|_2
$$

특잇값을 큰 순서로 정렬하고 앞의 항들을 남겼을 때, 이 최대 오차는
버린 특잇값 중 가장 큰 값이다.

$$
\|A-\widehat A_k\|_2=\sigma_{k+1}\qquad(k<r)
$$

개별 입력의 오차가 항상 이 값인 것은 아니다. 허용할 최대 오차와 버린
특잇값을 비교하여 남길 항 수를 정할 수 있다.

## 예제 또는 적용

특잇값이 다음과 같다고 하자.

$$
\sigma_1=8,\qquad\sigma_2=3,\qquad\sigma_3=0.5
$$

첫 항만 남기면 최대 단위 입력 오차는 3이고, 두 항을 남기면 0.5다.
모든 단위 입력에서 출력 오차를 1 이하로 제한하려면 최소 두 항이 필요하다.

## 주의점

- 작은 양의 특잇값을 버리는 것은 정확한 분해의 표기만 줄이는 것과 다르다.
- rank는 독립 방향의 수이며 행렬의 행·열 개수 자체가 아니다.
- 최대 오차라는 조건 없이 단순히 출력 오차라고만 말하면 개별 입력 오차와 혼동한다.

## 관련 기록

- Knowledge: [SVD의 기저와 특잇값](./singular-value-decomposition.md) · [rank와 영공간](./rank-null-space-linear-systems.md)
- Practice: [MML 4장 회고와 도움 범위](../../practice/math/mml-ch04-matrix-decompositions.md)
- Source: Deisenroth, Faisal, Ong, *Mathematics for Machine Learning*, Draft 2024-01-15, §4.5~4.6, [공식 PDF](https://mml-book.github.io/book/mml-book.pdf)
