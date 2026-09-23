---
title: "아핀 공간과 아핀 사상"
updated: 2026-09-23
tags:
  - vector-space
  - linear-transformation
  - affine
---

# 아핀 공간과 아핀 사상

## 핵심 요약

아핀 부분공간은 벡터 부분공간을 고정된 벡터만큼 평행이동한 집합이다.
아핀 사상은 선형변환 뒤에 고정된 벡터를 더하는 규칙이다.
공간은 점들의 집합이고 사상은 입력을 출력으로 보내는 규칙이다.

## 개념 정리

### 부분공간의 평행이동

벡터 부분공간을 U, 이동 벡터를 p라고 하면 다음 집합이 아핀 부분공간이다.

$$
L=p+U=\{p+u:u\in U\}
$$

1차원 직선에 한정되지 않으며, 평면과 더 높은 차원의 공간에도 적용된다.
이동은 차원을 바꾸지 않는다. 이동한 집합이 원점을 포함하면 벡터 부분공간이기도 하다.

### 선형변환 뒤의 이동

입력 벡터에 행렬 A를 곱하고 고정된 출력 벡터 b를 더하면 아핀 사상이다.

$$
f(x)=Ax+b
$$

숫자 하나에서는 상수배 후 상수를 더하는 규칙이고, 여러 성분을 가진 벡터에서는
행렬이 성분들의 조합을 담당한다. 이동 벡터가 0이면 선형사상이며,
0이 아니면 영벡터의 출력이 0이 아니므로 선형사상이 아니다.

## 예제 또는 적용

평면의 점에서 첫째 성분을 유지하고 둘째 성분을 2로 고정하는 규칙은 다음과 같다.

$$
f\begin{pmatrix}x\\y\end{pmatrix}
=\begin{pmatrix}1&0\\0&0\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}
+\begin{pmatrix}0\\2\end{pmatrix}
=\begin{pmatrix}x\\2\end{pmatrix}
$$

이 규칙은 아핀 사상이다. 가능한 출력은 원점을 지나지 않는 수평 직선이므로
1차원 아핀 부분공간이며 벡터 부분공간은 아니다.
이동 벡터를 0으로 바꾸면 사상은 선형이고, 출력 전체는 가로축인 벡터 부분공간이다.

## 주의점

- 모든 선형사상은 아핀 사상이지만, 모든 아핀 사상이 선형인 것은 아니다.
- 입력 공간의 차원과 실제 출력들이 만드는 공간의 차원은 다를 수 있다.

## 관련 기록

- Knowledge: [벡터 부분공간](./vector-subspaces.md) · [선형 변환과 기저벡터](./linear-transformation-basis.md)
- Practice: [MML 2장 회고](../../practice/math/mml-ch02-linear-algebra.md)
- Source: Deisenroth, Faisal, Ong, *Mathematics for Machine Learning*, Draft 2024-01-15, §2.8, [공식 PDF](https://mml-book.github.io/book/mml-book.pdf)
