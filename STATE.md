# Study State

이 파일은 현재 학습 범위와 다음 행동을 위한 재개 북마크입니다.
숙달 기록이나 진도 점수표가 아닙니다.

- Pilot 시작일: 2026-09-02
- 현재 주강의: [Karpathy — Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)
- 현재 강의: Building makemore Part 2: MLP
- 현재 범위: 강의 전체 구현과 공식 exercises E01~E03
- 현재 구간: E02 출력층 초기화 실험 후 학습 준비
- 공개 영상: [Building makemore Part 2: MLP](https://www.youtube.com/watch?v=TCH_1BHY58I)
- 공식 구현 자료: [강의 노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part2_mlp.ipynb)
- 공식 exercises: 공개 영상 설명란의 E01~E03
- 작업 공간: `main.ipynb`의 저장된 코드와 출력 유지
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
- 초기 손실 감소와 문자 패턴 학습은 다르다는 설명을 제공했으며,
  학습자의 구분에 대한 이해는 재확인이 필요하다.
- 새 초기화 모델의 gradient 활성화와 이후 학습은 아직 확인하지 않았다.
- E01의 목표 달성과 E03의 논문 아이디어 실험은 미완료다.
- 영상 시청 여부와 재생 위치는 확인하지 않았다.

## 재확인할 항목

- 새 컴퓨터에서는 저장된 출력과 실제 커널 변수를 구분하기
- 현재 실습에 필요한 데이터 구성과 배치 생성 셀을 확인하고 실행하기
- 기존 학습 모델과 새 초기화 모델의 파라미터를 구분하기
- 과거 반복 실행과 배치 상태를 정확히 재현했다고 가정하지 않기

## 다음 독립 행동

main.ipynb의 현재 초기화 실험과 필요한 셀의 의존관계를 확인하고,
새 커널이라면 필요한 데이터·배치·초기화 셀을 학습자가 실행한다.
이어서 parameters_init의 gradient 계산을 활성화하고 forward를
다시 구성하여 새 초기화 모델의 학습을 준비한다.
