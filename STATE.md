# Study State

이 파일은 현재 학습 범위와 다음 행동을 위한 재개 북마크입니다.
숙달 기록이나 진도 점수표가 아닙니다.

- Pilot 시작일: 2026-09-02
- 현재 주강의: [Karpathy — Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)
- 현재 강의: Building makemore Part 2: MLP
- 현재 범위: 강의 전체 구현과 공식 exercises E01~E03
- 현재 구간: E02 초기화·수동 갱신 구간 정리, E01 학습·검증 재개 준비
- 공개 영상과 exercises: https://www.youtube.com/watch?v=TCH_1BHY58I
- 공식 구현: https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part2_mlp.ipynb
- 작업 공간: main.ipynb
- 이번 보관본: practice/deep-learning/makemore-mlp-e02-initialization-training.ipynb
- 회고와 다음 학습 준비: practice/deep-learning/makemore-mlp-e02-initialization-training.md
- 이전 구현·출력: practice/deep-learning/makemore-mlp-before-e02-cleanup.ipynb
- 설명 방식: 공식 자료 기반 대화와 학습자의 직접 구현·실행
- CS336 Assignment 1: 기존 작업 보존, 새 구현 진도 보류

## 관찰된 근거

- 균등 예측 기준과 작은 출력 가중치의 초기 손실을 비교했다.
- AI 코드 도움을 받아 첫 갱신과 같은 배치의 반복 학습을 실행했다.
- 다섯 파라미터 갱신과 반복 종료 후 손실 재계산의 저장 결과를 확인했다.
- 학습자가 backward와 step의 혼동을 짚고 두 작업의 구분을 확인했다.
- E01 목표 달성과 E03 논문 아이디어 실험은 미완료다.

## 재확인할 항목

- E02 조정 전 초기화와의 비교는 이전 보관본을 함께 참고한다.
- 같은 배치의 손실 감소를 dev 성능 향상으로 해석하지 않는다.
- 보관본의 새 커널 재현과 영상 시청 위치는 확인하지 않았다.
- main.ipynb는 빈 셀로 정리되어 있으며 보관본은 수정하지 않는다.
- 프로젝트 .venv 커널을 사용하고 저장 출력과 실행 중 변수를 구분한다.
- 편집기의 이전 버퍼와 커널은 파일 초기화만으로 정리되지 않는다.

## 다음 독립 행동

학습자가 E01 재개를 위해 보관본의 데이터 분할과 학습·평가 코드를
참고하여 main.ipynb에 기준 모델의 학습·평가 흐름을 준비하고,
train/dev 손실을 실행·저장한다. 이 결과를 다음 설정 비교의 기준으로
사용하며 test 데이터는 튜닝에 사용하지 않는다.
