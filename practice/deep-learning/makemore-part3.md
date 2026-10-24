# makemore Part 3 — 초기화·활성값·BatchNorm 회고

정리일: 2026-10-08. 기준은 Karpathy의 공식 Part 3 영상·설명란과 저자
노트북이다. 공식 E01·E02와 강의 진단 사본을 검토했다. 이는 P0 종료나
영상 전체 시청, 챕터 전체의 무보조 숙달 판정이 아니다.

## 보존과 수행 범위

공식 연습 구현·제공 코드·저장 출력이 포함된 네 노트북과 각각의 상세 회고는
공개 Git에서 제외되는 비공개 챕터 보관 영역에 두었다. 노트북은 원본과 바이트가
같으며 실행하거나 정리된 해답으로 고치지 않았다. 공개 문서에는 학습 과정,
도움의 범위와 재현 한계만 남긴다.

- E01 초기화 비교: 제공 MLP에서 학습자가 초기화를 바꾸고 학습·평가했다.
- E01 첫 backward 관찰: 학습자 요청으로 튜터가 관찰 셀을 준비했고 학습자가 실행했다.
- 저자 진단 사본: 기존 구현을 복구한 사본을 실행하고 층별 통계를 살펴봤다.
- E02 평가용 변환: 제공 모델을 학습한 뒤 학습자가 변환과 같은 입력의 전체 비교를 작성했다.

루트 `main.ipynb`는 앞선 MLP 재현 산출물이며 이 챕터의 초기화 대상이 아니다.
빈 `recall.ipynb`와 공식 원본도 보존했다. 개념 초안과 보관본·문서를 검증한 뒤
Part 3 작업 사본 네 개를 빈 코드 셀로 초기화했다. 모든 보관본의 원본 바이트와
작업 노트북의 메타데이터 보존을 확인했다. 초기화는 저장 파일에 대한 작업이며
편집기의 미저장 내용이나 실행 중인 커널을 바꾼 것은 아니다.

## 확인한 구현·해석과 도움

E01의 저장 출력은 초기화별 학습 결과와 첫 backward의 관찰을 담고 있다.
대화에서 학습자가 갱신 범위와 문맥 학습의 제한을 답했으며, 구체적인 기울기
전달 경로와 표현의 정확성은 튜터가 보충했다. 기본 코드와 관찰 코드의 제공을
전체 독립 구현으로 바꾸지 않는다.

E02의 현재 저장 셀에는 학습자가 작성한 전체 평가용 층과 같은 입력의 logits
비교가 있다. 비교 결과는 로컬 허용오차 안이다. 클래스 호출·반환값 연결,
수식과 속성 대응, 제자리 변경 오류, 비교 API에 대한 도움을 구현 전에 받았다.
첫 오류 가설은 학습자가 답했지만 수정 전의 구체적 검증 방법은 확인되지 않았다.
평가 전용이라는 해석도 고정 통계 설명 뒤의 응답이므로 독립 회상과 구분한다.

진단 사본은 강의의 구현을 읽고 실행한 범위다. 분포·포화·gradient·업데이트
비율의 목적은 튜터 설명 도움을 받았다. 그림과 성공한 실행만으로 학습자의
독립적인 진단 능력이 확인됐다고 기록하지 않는다.

## 재현 한계와 마무리 위치

E01 비교는 CUDA 코드이고, 저자 진단 및 E02 사본은 CPU 코드다. 진단과 E02의
학습 루프는 디버깅 중단 조건이 있어 표시 상한 전체를 수행한 것이 아니다.
E01의 단계 기록은 초기화 사이에 이어지므로 표시 숫자를 해당 모델의 학습
횟수로 바로 읽지 않는다. 최초 minibatch loss와 전체 split 평가도 구분한다.
자세한 셀 번호와 수치는 비공개 상세 회고에 있다.

저장 출력과 seed 고정은 새 커널 전체 재현이나 통계적 재현을 뜻하지 않는다.
E02의 수치 확인을 학습 모드의 동등성·속도 개선·모든 입력의 실측으로 확대하지
않는다. 새로운 챕터 전체 재시험이나 추가 전체 구현은 부과하지 않는다.

자료를 닫고 기억으로 작성하도록 요청한 뒤 학습자가 초기화 크기와 Tanh 포화,
작은 값에서의 신호 약화, 적절한 분산·기울기 흐름의 목적을 설명했다. 이를 개념
초안으로 사용했다. 작은 값과 포화의 원인 구분, 출력층을 작게 초기화하는 목적,
도함수와 수치 예시는 튜터가 보충했다. 이 첫 초안을 지연된 회상이나 챕터 전체의
독립 설명 통과로 바꾸지 않는다. BatchNorm 통계와 전체 진단 흐름의 독립 설명은
미확인으로 남기며 해당 개념의 완성 노트를 대신 쓰지 않았다.

다음 승인된 범위는 makemore Part 4이며 P0 안에서 이어간다.

## 관련 자료

- [MLP와 경사하강](https://github.com/10o0o/llm-research-learning-lab/blob/5f0fccb96894e75805430ad194282319d6e44c4c/knowledge/deep-learning/mlp-and-gradient-descent.md)
- [초기화 크기와 Tanh 포화](https://github.com/10o0o/llm-research-learning-lab/blob/5f0fccb96894e75805430ad194282319d6e44c4c/knowledge/deep-learning/initialization-and-tanh-saturation.md)
- [계산 그래프와 역전파](https://github.com/10o0o/llm-research-learning-lab/blob/5f0fccb96894e75805430ad194282319d6e44c4c/knowledge/deep-learning/computational-graph-autograd.md)
- [다중분류 학습 반복](https://github.com/10o0o/llm-research-learning-lab/blob/5f0fccb96894e75805430ad194282319d6e44c4c/knowledge/deep-learning/multiclass-training-loop.md)
- [행렬곱과 완전연결층](https://github.com/10o0o/llm-research-learning-lab/blob/5f0fccb96894e75805430ad194282319d6e44c4c/knowledge/math/matrix-multiplication-linear-layer.md)
- [Part 3 공식 영상·연습 안내](https://www.youtube.com/watch?v=P6sfmUTpUmc)
- [Part 3 공식 저자 노트북](https://github.com/karpathy/nn-zero-to-hero/blob/master/lectures/makemore/makemore_part3_bn.ipynb)
