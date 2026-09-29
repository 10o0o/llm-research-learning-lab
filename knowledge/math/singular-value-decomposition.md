---
title: "SVD의 입력·출력 기저와 특잇값"
updated: 2026-09-29
tags:
  - svd
  - linear-transformation
---

# SVD의 입력·출력 기저와 특잇값

## 핵심 요약

SVD는 입력을 나눠 볼 정규직교 기저, 성분별 길이 배율, 변환된 성분을
합칠 출력 정규직교 기저로 행렬을 표현한다. 직사각형을 포함한 모든 실수
행렬에 존재하며 특잇값은 음수가 아니다.

## 개념 정리

### 세 인자의 역할과 크기

$$
\underbrace{A}_{m\times n}
=\underbrace{U}_{m\times m}
\underbrace{\Sigma}_{m\times n}
\underbrace{V^\mathsf T}_{n\times n}
$$

오른쪽부터 입력 기저의 계수를 구하고, 특잇값으로 배율을 적용하고,
출력 기저로 성분을 합친다. 입력과 출력 기저는 서로 다른 공간의 기준이다.
영화별 행·관객별 열인 평점표에서는 오른쪽 특이벡터가 관객들에 걸친
패턴이고 왼쪽 특이벡터가 영화들에 걸친 패턴이다.

### 특잇값은 길이 배율

단위 오른쪽 특이벡터를 변환한 결과의 길이가 특잇값이다. 양의 특잇값에
대응하는 출력 벡터를 길이로 나누면 단위 왼쪽 특이벡터가 된다.

$$
A\mathbf v_i=\sigma_i\mathbf u_i,
\qquad
\sigma_i=\|A\mathbf v_i\|_2,
\qquad
\mathbf u_i=\frac{A\mathbf v_i}{\sigma_i}\quad(\sigma_i>0)
$$

출력 성분의 음수 부호는 방향을 나타내며 특잇값에 음의 길이를 부여하지
않는다. 특잇값 0은 해당 입력 방향이 없다는 뜻이 아니라 그 방향의 출력이
영벡터라는 뜻이다.

## 예제 또는 적용

입력과 출력 기저를 표준기저로 고른 다음 변환을 생각한다.

$$
A=\begin{bmatrix}3&0\\0&1\\0&0\end{bmatrix},
\qquad
A\begin{bmatrix}c_1\\c_2\end{bmatrix}
=\begin{bmatrix}3c_1\\c_2\\0\end{bmatrix}
$$

두 번째 특잇값을 0으로 바꾸면 첫 번째 출력 기저 방향의 성분만 남는다.
출력 좌표가 3개여도 가능한 출력은 직선에 놓인다.

$$
\begin{bmatrix}3&0\\0&0\\0&0\end{bmatrix}
\begin{bmatrix}c_1\\c_2\end{bmatrix}
=\begin{bmatrix}3c_1\\0\\0\end{bmatrix}
$$

## 주의점

- 사라지는 성분은 입력 특이벡터 기저의 성분이며, 원래 좌표축과 반드시 같지는 않다.
- 행이나 열이 추가되면 인자 크기뿐 아니라 기존 기저의 값도 달라질 수 있다.
- 특잇값을 큰 순서로 정렬할 때 대응하는 입력·출력 벡터의 순서도 맞춘다.
- 일반적인 SVD에서 입력·출력 기저 행렬은 서로 같거나 서로의 역행렬일 필요가 없다.

## 관련 기록

- Knowledge: [저랭크 근사](./svd-low-rank-approximation.md) · [벡터 정규화](./vector-l2-normalization.md)
- Practice: [MML 4장 회고와 도움 범위](../../practice/math/mml-ch04-matrix-decompositions.md)
- Source: Deisenroth, Faisal, Ong, *Mathematics for Machine Learning*, Draft 2024-01-15, §4.5, [공식 PDF](https://mml-book.github.io/book/mml-book.pdf)
