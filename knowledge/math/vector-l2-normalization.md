---
title: "벡터 L2 정규화"
updated: 2026-09-14
tags:
  - vector
  - l2-norm
  - normalization
---

# 벡터 L2 정규화

## 핵심 요약

벡터 L2 정규화는 0이 아닌 벡터를 자신의 L2 노름으로 나누어 방향을 유지하면서 크기를 1로 만드는 연산이다.

## 개념 정리

### L2 노름

벡터를 다음과 같이 두자.

$$
\mathbf{v}=(v_1, v_2, \ldots, v_n)
$$

L2 노름은 각 성분을 제곱해 더한 뒤 제곱근을 취한 값이다.

$$
\lVert \mathbf{v} \rVert_2
= \sqrt{v_1^2 + v_2^2 + \cdots + v_n^2}
$$

### 정규화와 단위벡터

0이 아닌 벡터의 정규화 결과는 다음과 같다.

$$
\hat{\mathbf{v}}
= \frac{\mathbf{v}}{\lVert \mathbf{v} \rVert_2},
\qquad
\lVert \hat{\mathbf{v}} \rVert_2 = 1
$$

양수인 노름으로 모든 성분을 나누므로 벡터의 방향은 유지되고 크기만 1로 바뀐다.

### 특성 스케일링과의 차이

| 구분 | 계산 단위 | 목적 |
|---|---|---|
| 벡터별 L2 정규화 | 벡터 하나의 전체 성분 | 각 벡터의 크기를 1로 맞춘다. |
| feature별 Min-max scaling | 같은 feature의 여러 관측값 | feature별 값의 범위를 맞춘다. |

Min-max scaling은 feature별 최솟값과 최댓값을 사용한다.

$$
x' = \frac{x - x_{\min}}{x_{\max} - x_{\min}}
$$

## 주의점

- 영벡터의 노름은 0이므로 L2 정규화가 정의되지 않는다.
- 노름이 0인지 정확히 비교할지, 수치적으로 0에 가깝다고 판단할 임계값을 둘지는 데이터형과 적용 목적에 맞게 정해야 한다.

## 관련 기록

- Knowledge: [벡터](./vector.md) · [NumPy axis, keepdims와 브로드캐스팅](./numpy-axis-broadcasting.md)
- TIL: [2026-08-13](../../til/2026/08/2026-08-13.md)
- Source: KANT 기초수학, 1장 1강 「벡터의 수학적 정의와 기하학적 해석」
