---
title: "NumPy axis, keepdims와 브로드캐스팅"
updated: 2026-09-14
tags:
  - numpy
  - tensor
  - broadcasting
---

# NumPy axis, keepdims와 브로드캐스팅

## 핵심 요약

`axis`는 연산으로 줄일 축을 지정하고, `keepdims=True`는 줄인 축을 크기 1로 남겨 broadcasting에 맞는 Shape을 유지하는 데 사용한다.

## 개념 정리

### `axis`

`axis=k`는 입력 Tensor에서 k번째 축을 따라 값을 모아 계산하고 그 축을 줄인다는 뜻이다. 지정하지 않은 축은 결과에서 각 값을 구분하는 축으로 남는다.

다음 예시 Tensor에서는 각 위치의 마지막 성분 4개를 벡터 하나로 본다.

```text
H.shape = (2, 3, 4)
           batch, vector, feature
```

| 연산 | 결과 Shape | 의미 |
|---|---|---|
| `np.linalg.norm(H, axis=2)` | `(2, 3)` | 벡터 6개의 노름 |
| `np.linalg.norm(H, axis=2, keepdims=True)` | `(2, 3, 1)` | 마지막 축을 1로 보존한 벡터별 노름 |
| `np.linalg.norm(H, axis=(0, 1))` | `(4,)` | feature 4개에 대한 노름 |
| `np.linalg.norm(H, axis=(0, 1), keepdims=True)` | `(1, 1, 4)` | 앞의 두 축을 1로 보존한 feature별 노름 |

`axis`는 줄일 위치만 결정한다. L2 노름, 평균, 최솟값처럼 어떤 연산을 적용하는지에 따라 결과의 의미가 달라진다.

### `keepdims`와 broadcasting

`keepdims=True`는 연산한 축을 삭제하지 않고 크기 1로 남긴다. Shape이 `(2, 3, 1)`이면 마지막 `1`이 broadcasting을 통해 4개 성분에 맞게 확장되므로, 한 벡터의 모든 성분을 같은 노름으로 나눌 수 있다.

Broadcasting은 두 Shape을 오른쪽부터 비교한다. 각 위치의 크기가 같거나 둘 중 하나가 1이면 연산할 수 있다.

## 예제 또는 적용

```python
import numpy as np

H = np.arange(1, 25, dtype=float).reshape(2, 3, 4)
norms = np.linalg.norm(H, axis=2, keepdims=True)
H_unit = H / norms
```

```text
H:      (2, 3, 4)
norms:  (2, 3, 1)
H_unit: (2, 3, 4)
```

영벡터가 없는 예제에서 `np.linalg.norm(H_unit, axis=2)`의 여섯 값이 모두 1이면 Tensor 안의 벡터 6개가 각각 정규화된 것이다.

## 주의점

`keepdims=False`로 얻은 `(2, 3)`을 `(2, 3, 4)`로 나누면 오른쪽부터 비교한 첫 크기가 `3`과 `4`이므로 broadcasting 오류가 발생한다.

## 관련 기록

- Knowledge: [벡터 L2 정규화](./vector-l2-normalization.md)
- TIL: [2026-08-13](../../til/2026/08/2026-08-13.md)
