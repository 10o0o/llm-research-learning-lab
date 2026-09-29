---
title: "전치행렬 곱과 양의 준정부호"
updated: 2026-09-29
tags:
  - gram-matrix
  - positive-semidefinite
---

# 전치행렬 곱과 양의 준정부호

## 핵심 요약

실수 행렬의 전치와 원래 행렬을 곱하면 대칭 양의 준정부호 행렬이 된다.
이에 대한 이차형식은 변환된 벡터의 길이 제곱이므로 음수가 될 수 없다.

## 개념 정리

### 크기와 대칭성

$$
\underbrace{S}_{n\times n}
=\underbrace{A^\mathsf T}_{n\times m}\underbrace{A}_{m\times n}
$$

정사각형이라는 사실만으로 대칭성이 보장되지는 않는다. 전치 결과가 원래
행렬과 같은지 확인해야 한다.

$$
S^\mathsf T=(A^\mathsf T A)^\mathsf T
=A^\mathsf T(A^\mathsf T)^\mathsf T=A^\mathsf T A=S
$$

### 길이 제곱으로 보는 양의 준정부호

$$
\mathbf x^\mathsf T S\mathbf x
=\mathbf x^\mathsf T A^\mathsf T A\mathbf x
=(A\mathbf x)^\mathsf T(A\mathbf x)
=\|A\mathbf x\|_2^2\ge0
$$

양의 준정부호는 이 값이 모든 입력에서 음수가 아니라는 뜻이다.
모든 행렬 원소가 음수가 아니라는 조건과는 다르다.

## 주의점

양의 정부호는 영벡터 아닌 모든 입력에서 엄격한 양수를 요구한다.
영벡터 입력의 결과가 0이라는 사실만으로 양의 정부호를 반박할 수 없다.

$$
\mathbf x^\mathsf T S\mathbf x>0\qquad(\mathbf x\ne\mathbf0)
$$

## 관련 기록

- Knowledge: [벡터 내적](./dot-product-cosine-similarity.md) · [SVD](./singular-value-decomposition.md)
- Practice: [MML 4장 회고와 도움 범위](../../practice/math/mml-ch04-matrix-decompositions.md)
- Source: Deisenroth, Faisal, Ong, *Mathematics for Machine Learning*, Draft 2024-01-15, §4.2 Theorem 4.14, [공식 PDF](https://mml-book.github.io/book/mml-book.pdf)
