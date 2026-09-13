# Study State

이 파일은 현재 학습 범위와 다음 행동을 위한 재개 북마크입니다.
숙달 기록이나 진도 점수표가 아닙니다.

- Pilot 시작일: 2026-09-02
- 현재 주강의: [Karpathy — Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)
- 현재 강의: Building makemore Part 2: MLP
- 현재 범위: 강의 전체 구현과 공식 exercises E01~E03
- 현재 구간: E02 새 초기화 모델의 backward 완료, 첫 가중치 갱신 전
- 공개 영상: [Building makemore Part 2: MLP](https://www.youtube.com/watch?v=TCH_1BHY58I)
- 공식 구현 자료: [강의 노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part2_mlp.ipynb)
- 공식 exercises: 공개 영상 설명란의 E01~E03
- 작업 공간: `main.ipynb`
- 이전 코드·출력 보관: `practice/deep-learning/makemore-mlp-before-e02-cleanup.ipynb`
- 환경 이동 안내: `USAGE.md`의 다른 컴퓨터에서 이어가기
- 설명 방식: 공식 자료 기반 대화와 학습자의 직접 구현·실행
- KANT: 진도·주제 대조용
- CS336 Assignment 1: 기존 작업을 보존하고 새 구현 진도는 잠시 보류

## 관찰된 근거

- 문자 문맥 데이터 구성, embedding과 MLP forward, 미니배치 학습과
  train/dev 평가의 코드와 저장된 출력을 확인했다.
- 학습률 탐색, embedding 시각화와 문자 생성 실험을 진행했다.
- E02에서 균등 logits의 손실을 계산하고, 출력 가중치 배율을 줄이고
  출력 편향을 영으로 초기화하여 초기 손실이 균등 예측 기준에 가까워짐을 확인했다.
- 학습자가 다섯 파라미터를 parameters_init으로 묶고 gradient를 활성화한 뒤,
  forward 재계산, gradient 초기화, backward를 구현·실행했다.
  다섯 gradient의 shape가 각 파라미터와 일치하는 저장 출력을 확인했다.
- 새 초기화 모델의 가중치 갱신과 갱신 전후 손실 비교는 아직 확인하지 않았다.
- E01의 목표 달성과 E03의 논문 아이디어 실험은 미완료다.
- 영상 시청 여부와 재생 위치는 확인하지 않았다.

## 재확인할 항목

- Notebook kernel은 패키지가 설치된 프로젝트 `.venv` Python을 선택하기
- 새 커널에서는 저장된 출력이 실제 변수와 가중치를 복원하지 않음을 구분하기
- 이전 실험 셀은 주석 처리되어 있으며, 현재 데이터·배치·초기화·backward
  셀을 순서대로 실행하면 재개에 필요한 변수를 준비할 수 있음
- 초기화 셀을 다시 실행하면 `_init` 모델이 새로 초기화됨
- 기존 학습 모델과 parameters_init을 구분하고, 과거 배치와 반복 실행
  상태를 정확히 재현했다고 가정하지 않기
- 초기화로 손실을 낮추는 것과 데이터로 문자 패턴을 학습하는 것의 차이는
  학습자의 설명으로 재확인하기

## 다음 독립 행동

새 커널이면 main.ipynb의 활성 셀을 학습자가 순서대로 실행하여
parameters_init의 gradient 계산까지 준비한다.
이어서 학습자가 새 셀에서 현재 손실을 저장하고, 학습률 0.1과
torch.no_grad()로 다섯 파라미터를 한 번 갱신한다.
같은 Xbatch와 Ybatch로 forward와 손실을 다시 계산하여 갱신 전후를
출력·저장하고, 초기화에 의한 손실 감소와 이번 갱신의 차이를 설명한다.
