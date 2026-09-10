# Study State

이 파일은 현재 학습 범위와 다음 행동을 위한 재개 북마크입니다.
숙달 기록이나 진도 점수표가 아닙니다.

- Pilot 시작일: 2026-09-02
- 현재 주강의: [Karpathy — Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)
- 현재 강의: building makemore
- 현재 범위: 강의 구현과 공식 exercises E01~E06
- 현재 구간: 실습·결과 해석을 진행하고 챕터 회고와 지식 정리를 마친 지점
- 실습 보관본: `practice/deep-learning/makemore-bigrams.ipynb`
- 챕터 회고: `practice/deep-learning/makemore-bigrams.md`
- 지식 안내: `knowledge/README.md`
- 작업 공간: `main.ipynb`는 보관본 검증 후 초기화함
- 설명 방식: 공식 자료 기반 대화와 직접 구현·실행
- KANT: 진도·주제 대조용
- CS336 Assignment 1: 기존 작업을 보존하고 새 구현 진도는 잠시 보류

## 관찰된 근거

- Bigram·trigram 구현, 데이터 분할, smoothing 비교의 코드와 출력을 확인했다.
- 행 인덱싱, cross-entropy, sampling·greedy 실험과 학습자 설명을 확인했다.
- E03의 test 조회 조건과 E06의 AI 주제 제안·구현 도움은 회고에 구분했다.
- 보관본의 문법 오류와 저장 출력의 한계를 보존했으며 전체 재실행은 검증하지 않았다.
- 영상 시청 여부와 재생 위치는 확인하지 않았다.
- Building makemore Part 2: MLP 학습은 아직 시작하지 않았다.

## 재확인할 항목

- 입력 문자 ID, 다음 문자 정답, 후보 logits의 역할을 후속 구현에 적용하기
- 보관된 출력과 새 커널에서 재현한 결과를 구분하기
- 다음 강의의 공식 구현과 exercises 범위를 실제 자료에서 확인하기

## 다음 독립 행동

Building makemore Part 2: MLP의 공식 영상·구현 자료와 exercises 범위를
확인하고, 학습 시작 요청에서 첫 연결 구간을 진행한다.
