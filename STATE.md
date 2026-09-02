# Study State

> 이 파일은 simplified study pilot의 재개 북마크입니다. 숙달 기록,
> 점수표, 세션 이력, evidence 저장소, progress database가 아닙니다.

- Pilot 시작일: 2026-09-02
- 마지막 사용자 확인일: 2026-09-02
- 주축: [Stanford CS336 Spring 2026](https://cs336.stanford.edu/)
- 기준 과제: [Assignment 1 at `a158843b20107949f1a8d7df1b05cd33b9166712`](https://github.com/stanford-cs336/assignment1-basics/tree/a158843b20107949f1a8d7df1b05cd33b9166712)
- 현재 범위: Assignment 1 진입

## 관찰된 근거

- 빈 Python 파일에서 deterministic synthetic 다중분류 데이터, 작은 `nn.Module`,
  raw logits, cross-entropy, optimizer, train/validation 흐름을 직접 구현하고 실행했다.
- validation loss와 accuracy를 계산하고 baseline과 비교했다.
- 입력 feature 수를 변경해 모델의 입력 및 parameter shape 전이를 확인했다.
- `zero_grad`, `backward`, `requires_grad`, `no_grad`, `detach`와
  parameter gradient의 저장 위치를 설명했다.

## 재확인할 항목

- Assignment 1의 공식 handout에 정의된 첫 구현 요구사항과 Tensor/API 계약
- 과제별 테스트를 실행한 뒤 실패 원인과 출력 의미 해석하기
- 과제 구현에서 train/evaluation 경계와 shape 계약 유지하기

## 다음 독립 행동

Assignment 1 공식 handout의 entry section을 읽고,
별도 sibling clone과 공식 uv 환경을 준비한 뒤 handout에 적힌 첫 검증 단계를
직접 실행한다.
