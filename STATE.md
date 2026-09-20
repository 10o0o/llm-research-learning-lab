# Study State

이 파일은 현재 학습 범위와 다음 행동을 위한 재개 북마크입니다.
숙달 기록이나 진도 점수표가 아닙니다.

- Pilot 시작일: 2026-09-02
- 현재 ROADMAP Phase: P0
- 현재 주강의: Karpathy — Neural Networks: Zero to Hero
- 현재 강의: Building makemore Part 2: MLP
- 현재 범위: 강의 전체 구현과 공식 exercises E01~E03
- 현재 구간: E01 기준 모델 평가 후 추가 학습 비교
- 공개 영상과 exercises: https://www.youtube.com/watch?v=TCH_1BHY58I
- 공식 구현: https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part2_mlp.ipynb
- 작업 공간: main.ipynb
- 이전 보관본: practice/deep-learning/makemore-mlp-e02-initialization-training.ipynb
- 설명 방식: 공식 자료 기반 대화와 학습자의 직접 실행·해석
- CS336 Assignment 1: 기존 작업 보존, 새 구현 진도 보류

## 관찰된 근거

- 학습자의 명시적 예외 요청으로 AI가 기준 모델 코드를 재구성했다.
- 학습자가 실행한 초기 평가와 학습 후 train/dev 평가 출력을 확인했다.
- 기준 모델의 train/dev 손실이 함께 감소했다.
- E01 목표 달성과 E03 논문 아이디어 실험은 미완료다.

## 재확인할 항목

- 현재 모델은 새 초기화에서 학습했으며 다른 컴퓨터의 가중치 복구본이 아니다.
- AI가 재구성한 코드를 독립 구현의 근거로 삼지 않는다.
- 학습 결과의 학습자 해석은 아직 확인하지 않았다.
- 저장 출력과 실행 중 커널 상태를 구분한다.
- 초기화 셀 재실행은 모델과 학습 기록을 초기화한다.
- test는 튜닝에 사용하지 않는다.

## 다음 독립 행동

현재 모델에서 학습률과 구조를 유지하고 추가 학습을 실행한다.
추가 학습 전후의 train/dev 손실을 비교해 일반화 성능에도
개선이 있었는지 해석하고 노트북을 저장한다.
