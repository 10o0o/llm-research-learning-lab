---
title: "벡터 내적과 코사인 유사도"
updated: 2026-09-14
tags:
  - vector
  - dot-product
  - cosine-similarity
---

# 벡터 내적과 코사인 유사도

## 핵심 요약

벡터 내적은 두 벡터의 크기와 방향 관계를 하나의 스칼라로 나타낸다. 코사인 유사도는 내적을 두 벡터의 L2 노름으로 나누어 크기 영향을 제거하고 방향의 유사성을 비교한다.

## 개념 정리

### 내적

성분 수가 같은 두 벡터의 내적은 같은 위치의 성분끼리 곱한 뒤 모두 더한 값이다.

$$
\mathbf{a} \cdot \mathbf{b}
= \sum_{i=1}^{n} a_i b_i
$$

내적은 두 벡터 사이의 각도와 다음 관계를 가진다.

$$
\mathbf{a} \cdot \mathbf{b}
= \lVert \mathbf{a} \rVert_2
\lVert \mathbf{b} \rVert_2
\cos\theta
$$

따라서 내적값에는 두 벡터의 크기와 방향이 함께 반영된다.

### 코사인 유사도

두 벡터가 모두 영벡터가 아닐 때 코사인 유사도는 다음과 같다.

$$
\cos_{\mathrm{sim}}(\mathbf{a}, \mathbf{b})
= \frac{\mathbf{a} \cdot \mathbf{b}}
{\lVert \mathbf{a} \rVert_2 \lVert \mathbf{b} \rVert_2}
$$

두 벡터를 각각 L2 정규화한 뒤 내적한 값과도 같다.

$$
\cos_{\mathrm{sim}}(\mathbf{a}, \mathbf{b})
= \hat{\mathbf{a}} \cdot \hat{\mathbf{b}}
$$

| 값 | 방향 관계 |
|---:|---|
| `1` | 같은 방향 |
| `0` | 직교 |
| `-1` | 반대 방향 |

### 크기 변화와 순위

양수 `c`를 한 벡터에 곱하면 내적은 `c`배가 되지만 코사인 유사도는 유지된다.

$$
\mathbf{a} \cdot (c\mathbf{b})
= c(\mathbf{a} \cdot \mathbf{b}),
\qquad c>0
$$

$$
\cos_{\mathrm{sim}}(\mathbf{a}, c\mathbf{b})
= \cos_{\mathrm{sim}}(\mathbf{a}, \mathbf{b}),
\qquad c>0
$$

내적 기반 순위에는 벡터의 크기가 영향을 주지만, 코사인 유사도 기반 순위는 양수 배율에 영향을 받지 않는다. 따라서 같은 후보들을 비교하더라도 두 점수의 순위가 서로 다를 수 있다.

### NumPy Shape

후보 벡터 네 개를 행으로 쌓고 기준 벡터 하나와 내적하면 후보마다 스칼라 점수 하나가 나온다.

```text
candidates: (4, 2)
query:      (2,)
scores:     (4,)
```

```python
dot_scores = candidates @ query
```

### 유클리드 거리와의 차이

코사인 유사도는 방향을 비교하고, 유클리드 거리는 두 벡터의 실제 위치 차이를 측정한다. `(1, 0)`과 `(100, 0)`은 코사인 유사도가 `1`이지만 유클리드 거리는 `99`이다.

## 주의점

- 영벡터는 L2 노름이 `0`이므로 코사인 유사도가 정의되지 않는다.
- 크기 자체가 중요한 정보라면, 크기를 제거하는 코사인 유사도만으로는 그 차이를 구분할 수 없다.

## 관련 기록

- Knowledge: [벡터](./vector.md) · [벡터 L2 정규화](./vector-l2-normalization.md)
- TIL: [2026-08-14](../../til/2026/08/2026-08-14.md)
- Source: KANT 기초수학, 1장 2강 「내적과 코사인 유사도」
