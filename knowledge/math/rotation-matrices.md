---
title: "회전행렬과 Givens 회전"
updated: 2026-09-25
tags:
  - rotation
  - orthogonal-matrix
  - givens-rotation
---

# 회전행렬과 Givens 회전

## 핵심 요약

회전행렬은 기저벡터의 길이와 서로 이루는 각도를 유지하면서 방향을 바꾸는
선형변환이다. 표준기저를 회전한 결과가 행렬의 열이 되며, 직교행렬 조건 때문에
내적·거리·각도가 보존된다.

## 개념 정리

### 2차원 회전행렬

열벡터 관점에서 양의 각도는 반시계 방향 회전이다. 표준기저의 상은 다음과 같다.

$$
R(\theta)\mathbf e_1=
\begin{bmatrix}
\cos\theta\\
\sin\theta
\end{bmatrix},
\qquad
R(\theta)\mathbf e_2=
\begin{bmatrix}
-\sin\theta\\
\cos\theta
\end{bmatrix}
$$

두 결과를 열로 모으면 회전행렬을 얻는다.

$$
R(\theta)=
\begin{bmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{bmatrix}
$$

두 번째 기저벡터는 양의 회전에서 왼쪽으로 기울기 때문에 첫 좌표가 음수가
된다. 이것이 오른쪽 위 원소가 음의 사인인 기하학적 이유다.

### 능동 회전과 회전된 기저 좌표

고정된 좌표축에서 벡터 자체를 회전할 때는 다음을 사용한다.

$$
\mathbf y=R\mathbf x
$$

벡터는 고정하고 회전된 정규직교 기저에서 같은 벡터의 좌표를 구할 때는
역행렬을 사용한다. 회전행렬은 직교행렬이므로 역행렬은 전치행렬과 같다.

$$
[\mathbf x]_{\mathrm{rotated}}
=R^{-1}\mathbf x
=R^\mathsf{T}\mathbf x
$$

### 보존되는 양

회전행렬의 열은 정규직교이므로 다음 조건을 만족한다.

$$
R^\mathsf{T}R=I
$$

따라서 회전 전후의 내적이 같다.

$$
(R\mathbf x)^\mathsf{T}(R\mathbf y)
=\mathbf x^\mathsf{T}R^\mathsf{T}R\mathbf y
=\mathbf x^\mathsf{T}\mathbf y
$$

내적과 각 벡터의 길이가 유지되므로 두 벡터 사이의 거리와 각도도 유지된다.

### 3차원과 고차원

3차원에서는 한 축을 고정하고 나머지 두 좌표가 만드는 평면을 회전한다.
고차원의 Givens 회전은 두 좌표만 2차원처럼 회전하고 나머지 좌표를 고정한다.

선택한 좌표가 `i`, `j`라면 다음 두 성분만 바뀐다.

$$
y_i=\cos\theta\,x_i-\sin\theta\,x_j
$$

$$
y_j=\sin\theta\,x_i+\cos\theta\,x_j
$$

나머지 성분은 그대로다.

$$
y_k=x_k
\qquad
(k\ne i,\;k\ne j)
$$

## 예제 또는 적용

4차원에서 두 번째와 네 번째 좌표만 양의 90도로 회전하는 행렬은 다음과 같다.

$$
G_{24}(90^\circ)=
\begin{bmatrix}
1&0&0&0\\
0&0&0&-1\\
0&0&1&0\\
0&1&0&0
\end{bmatrix}
$$

이 행렬은 다음 벡터에서 둘째·넷째 좌표만 회전시키고 첫째·셋째 좌표는
그대로 둔다.

$$
G_{24}(90^\circ)
\begin{bmatrix}
1\\2\\3\\4
\end{bmatrix}
=
\begin{bmatrix}
1\\-4\\3\\2
\end{bmatrix}
$$

## 주의점

- 양의 각도의 방향과 열벡터·행벡터 관점을 먼저 확인한다. 관점이 바뀌면
  사인 항의 부호와 행렬을 곱하는 쪽이 달라질 수 있다.
- 3차원 이상에서는 서로 다른 평면의 회전이 일반적으로 가환하지 않는다.
  같은 회전을 사용하더라도 적용 순서에 따라 결과가 달라질 수 있다.
- `R @ x`와 `R.T @ x`는 각각 벡터의 능동 회전과 회전된 기저에서의 좌표라는
  서로 다른 질문에 답한다.

## 관련 기록

- Knowledge: [선형 변환과 기저벡터](./linear-transformation-basis.md) · [벡터 내적과 코사인 유사도](./dot-product-cosine-similarity.md)
- Practice: [MML 3장 해석기하 회고](../../practice/math/mml-ch03-analytic-geometry.md)
- Source: Deisenroth, Faisal, Ong, *Mathematics for Machine Learning*, Draft 2024-01-15, Chapter 3 §3.9, [공식 PDF](https://mml-book.github.io/book/mml-book.pdf)
