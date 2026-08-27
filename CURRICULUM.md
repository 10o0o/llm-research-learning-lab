# LLM Research Engineer 세부 커리큘럼

<!-- curriculum-schema: 1 -->

## 1. 목적과 비목적

이 문서는 `ROADMAP.md`의 큰 방향을 실행 가능한 학습 성과로 풀고, 현재 강의 자료가 각 성과를 어느 깊이까지 직접 뒷받침하는지 판단하는 기준이다. 수업 계약은 한 번에 관련 ID 1~3개를 선택하고, 연결 자료의 관계·무결성·공백 처리를 근거로 보충 범위를 결정한다.

이 문서는 학습자의 완료 여부, 점수, 진도율, 학습 날짜 또는 mastery를 기록하지 않는다. 별도 LMS, 일일 진도표, 강의 순서 강제 장치도 아니다. 아래 자료 평가는 **자료의 충족도**이며 학습자의 이해도를 뜻하지 않는다.

## 2. ID, 깊이, 자료 충족도 범례

- 역량 ID: 공통 핵심은 `CC-<AREA>-NN`, 선택 전문 트랙은 `TR-<TRACK>-NN`이다. ID의 의미는 한 번 부여한 뒤 바꾸거나 재사용하지 않는다.
- 자료 ID: `SRC-<대문자 namespace>-<NN-NN>` 형식이다. namespace는 숫자를 포함한 여러 대문자 토큰을 `-`로 연결할 수 있으며, 과정과 판본을 함께 식별한다. 예: `SRC-KDL-08-01`, `SRC-HARV-STAT110-2E-00-01`.
- 자료 관계: `primary`는 학습 성과를 직접 가르치고, `supporting`은 일부 개념이나 선수를 보완하며, `context`는 언급 또는 응용 맥락만 제공한다. `context`만 연결된 역량은 `충분`이 될 수 없다.

깊이는 다음 세 단계로 고정한다.

- `D1`: 목적, 작동 방식, 한계를 작은 예제로 설명한다.
- `D2`: D1에 더해 계산, shape 추적, 구현, 디버깅, 출력 해석을 수행한다.
- `D3`: D2에 더해 가설, baseline, 통제 실험, ablation, 통계적 한계, 논문 주장을 평가한다.

요구 근거에는 `explain`, `calculate`, `shape`, `implement`, `debug`, `interpret`, `design`, `transfer`만 쓴다. 한 행에 적힌 토큰은 그 역량을 입증할 때 필요한 관찰 가능한 산출물이다.

자료 충족도는 다음으로 고정한다.

- `미감사`: 연결 자료를 아직 전체 감사하지 않았다.
- `충분`: 현재 연결 자료만으로 목표 깊이의 요구 근거를 직접 만들 수 있다.
- `부분`: 직접 다루는 내용은 있으나 목표 깊이 또는 필수 하위 주제가 비어 있다.
- `없음`: 직접 가르치는 자료가 없다. `context` 연결은 있을 수 있다.
- `판정보류`: 원본 또는 근거가 불완전해 현재 판단할 수 없다.

공백 처리는 `그대로 사용`, `수업 내 보충`, `별도 자료 확보`, `원본 복구 후 재감사`, `트랙 선택 시 확보` 중 하나만 쓴다.

자료 registry의 무결성은 `complete`, `limited`, `blocked`, `unverified`, 감사 상태는 `complete`, `blocked`, `pending`을 쓴다. `limited`는 현재 파일을 감사할 수 있지만 변환 훼손이나 원본 누락 같은 제약이 있음을 뜻한다. 파일 hash가 registry와 달라지면 validator가 별도 상태값을 저장하지 않고 stale 오류로 계산한다.

## 3. 공통 핵심 역량

| ID | 학습 성과 | 목표 깊이 | 선수 ID | 요구 근거 | 자료 연결 | 자료 충족도 | 공백 처리 | 비고 |
|---|---|---|---|---|---|---|---|---|
| CC-MATH-01 | 벡터·행렬·선형변환을 기하와 좌표, 행렬곱 shape, 작은 NumPy 구현으로 연결한다. | D2 | — | explain, calculate, shape, implement | primary:SRC-KBM-01-01,SRC-KBM-01-03,SRC-KBM-02-01; supporting:SRC-KBM-01-02,SRC-KBM-01-04 | 충분 | 그대로 사용 | 벡터별 L2 정규화와 특성별 scaling은 구분해 가르친다. |
| CC-MATH-02 | rank·최소제곱·고윳값·SVD를 계산하고 해의 존재·유일성, 저랭크 근사, 수치적 선택을 해석한다. | D2 | CC-MATH-01 | explain, calculate, shape, implement, interpret | primary:SRC-KBM-02-02,SRC-KBM-02-03,SRC-KBM-03-01,SRC-KBM-03-03,SRC-KBM-04-01; supporting:SRC-KBM-03-02,SRC-KBM-04-02,SRC-KBM-04-03 | 부분 | 수업 내 보충 | rank-deficient 최소제곱, full SVD의 기저 범위, solver별 수치 차이를 보충한다. |
| CC-MATH-03 | 미분·chain rule·gradient·autodiff를 손계산, 계산 그래프, 코드의 gradient 흐름으로 연결한다. | D2 | CC-MATH-01 | explain, calculate, shape, implement, debug | primary:SRC-KBM-07-01,SRC-KBM-07-02,SRC-KDL-06-01,SRC-KDL-06-02,SRC-KDL-06-03; supporting:SRC-KDL-01-04,SRC-KDL-06-04,SRC-KDL-06-05 | 충분 | 그대로 사용 | scalar chain rule 손계산부터 gradient shape·누적·graph 단절 디버깅까지 직접 다룬다. Jacobian·VJP·gradcheck는 후속 심화다. |
| CC-MATH-04 | 부동소수점, overflow·underflow, conditioning과 안정적인 연산 선택을 계산·디버깅에 적용한다. | D2 | CC-MATH-02, CC-MATH-03 | explain, calculate, implement, debug, interpret | supporting:SRC-KBM-01-04,SRC-KBM-02-03,SRC-KBM-04-01,SRC-KBM-04-02,SRC-KBM-06-02,SRC-KBM-07-01,SRC-KDL-02-03,SRC-KDL-06-05 | 부분 | 수업 내 보충 | 안정적 softmax·finite gradient 점검은 있으나 conditioning·precision·오차 전파의 통합 설명이 없다. |
| CC-PROB-01 | 확률분포·조건부확률·기댓값·분산·sampling을 계산하고 실험 출력과 연결한다. | D2 | CC-MATH-01 | explain, calculate, implement, interpret | context:SRC-KAM-02-01 | 없음 | 별도 자료 확보 | bootstrap sampling은 등장하지만 확률 기초를 가르치지 않는다. |
| CC-PROB-02 | likelihood·MLE·Bayes와 불확실성의 의미를 계산하고 모델 추정에 적용한다. | D2 | CC-PROB-01, CC-MATH-03 | explain, calculate, implement, interpret | context:SRC-KBM-06-02 | 없음 | 별도 자료 확보 | negative log-likelihood 언급만으로 추정 원리를 충족하지 못한다. |
| CC-PROB-03 | entropy·cross entropy·KL divergence·mutual information을 계산하고 분포 차이와 학습 목적을 해석한다. | D2 | CC-PROB-01 | explain, calculate, implement, interpret | supporting:SRC-KBM-06-02 | 부분 | 수업 내 보충 | cross entropy는 직접 다루지만 entropy·KL·mutual information은 없다. |
| CC-STAT-01 | 추정량·신뢰구간·bootstrap의 가정과 불확실성을 계산하고 보고한다. | D2 | CC-PROB-01, CC-PROB-02 | explain, calculate, implement, interpret | context:SRC-KAM-02-01,SRC-KAM-05-01 | 없음 | 별도 자료 확보 | resampling과 fold 평균·표준편차는 쓰지만 통계적 추론을 가르치지 않는다. |
| CC-STAT-02 | 가설검정·효과크기·다중검정의 한계를 적용해 비교 결론을 평가한다. | D2 | CC-STAT-01 | explain, calculate, interpret, design | context:SRC-KAM-05-01 | 없음 | 별도 자료 확보 | 후보 비교는 있으나 유의성·효과크기·다중 비교 통제가 없다. |
| CC-ML-01 | 문제 유형을 정의하고 train·validation·test 분리와 단순 baseline을 설계한다. | D2 | CC-PROB-01 | explain, implement, interpret, design | primary:SRC-KAM-01-01,SRC-KDL-01-02,SRC-KDL-01-03,SRC-KDL-07-04; supporting:SRC-KAM-04-02,SRC-KDL-08-05,SRC-KDL-08-08 | 충분 | 그대로 사용 | 무작위·시간·그룹 데이터의 분리 선택과 train·validation·test 역할을 포함하며, 08-08은 고정 seed 분리와 최종 test 1회 평가를 구현한다. |
| CC-ML-02 | metric·threshold·calibration·불균형을 비용과 오류 유형에 맞춰 선택하고 해석한다. | D2 | CC-ML-01, CC-PROB-01 | explain, calculate, implement, interpret, design | primary:SRC-KAM-01-01,SRC-KAM-04-01; supporting:SRC-KDL-01-02,SRC-KDL-04-03,SRC-KDL-04-04,SRC-KDL-08-06,SRC-KDL-08-08 | 부분 | 수업 내 보충 | sample-weighted accuracy와 불균형 주의는 있으나 threshold 선택과 calibration의 계산·검증이 얕다. |
| CC-ML-03 | 일반화·bias-variance·regularization을 진단하고 적절한 개입을 실험한다. | D2 | CC-ML-01, CC-MATH-03 | explain, calculate, implement, interpret, design | primary:SRC-KAM-03-01,SRC-KAM-03-02; supporting:SRC-KAM-02-01,SRC-KAM-02-02; context:SRC-KDL-07-04 | 부분 | 원본 복구 후 재감사 | 핵심 자료 두 개에 수식 변환 훼손 또는 신버전 원본 누락이 있다. |
| CC-ML-04 | 선형·거리·트리·ensemble 모델 계열과 해석 도구를 데이터 조건에 맞춰 비교한다. | D2 | CC-ML-01, CC-ML-03 | explain, implement, interpret, design, transfer | primary:SRC-KAM-01-02,SRC-KAM-02-01,SRC-KAM-02-02,SRC-KAM-02-03; supporting:SRC-KDL-01-01 | 충분 | 그대로 사용 | SHAP은 예측 설명이지 인과 설명이 아님을 유지한다. |
| CC-ML-05 | CV·search·leakage·pipeline·재현성을 하나의 공정한 선택 및 재사용 절차로 구현한다. | D2 | CC-ML-01, CC-ML-03 | explain, implement, debug, interpret, design, transfer | primary:SRC-KAM-04-02,SRC-KAM-05-01,SRC-KAM-05-02; supporting:SRC-KAM-04-01,SRC-KDL-07-03,SRC-KDL-07-04 | 충분 | 그대로 사용 | 전처리·sampler의 fit 경계, split별 transform, 재현 가능한 분리와 최종 test 1회 원칙을 포함한다. |
| CC-DL-01 | tensor의 shape·dtype·device·broadcasting 계약을 추적하고 관련 오류를 고친다. | D2 | CC-MATH-01 | explain, calculate, shape, implement, debug | primary:SRC-KDL-02-01,SRC-KDL-02-02,SRC-KDL-02-03,SRC-KDL-02-04,SRC-KBM-05-01,SRC-KBM-05-02,SRC-KDL-07-05; supporting:SRC-KDL-03-03,SRC-KDL-03-04,SRC-KDL-03-05,SRC-KDL-05-01,SRC-KDL-05-02,SRC-KDL-06-02,SRC-KDL-06-03,SRC-KDL-07-01,SRC-KDL-07-02,SRC-KDL-07-03 | 충분 | 그대로 사용 | batch 축, gradient·label shape, dtype와 device 계약을 코드 실행 전후로 확인한다. |
| CC-DL-02 | 데이터·모델·손실·optimizer·평가로 이어지는 학습 루프를 구현하고 출력 흐름을 해석한다. | D2 | CC-ML-01, CC-MATH-03, CC-DL-01 | explain, shape, implement, debug, interpret | primary:SRC-KDL-01-02,SRC-KDL-01-04,SRC-KDL-06-04,SRC-KDL-06-05,SRC-KDL-07-01,SRC-KDL-07-02,SRC-KDL-07-04,SRC-KDL-07-05,SRC-KDL-08-03,SRC-KDL-08-04,SRC-KDL-08-05,SRC-KDL-08-08; supporting:SRC-KBM-07-02,SRC-KDL-03-05,SRC-KDL-04-01,SRC-KDL-04-03,SRC-KDL-04-04,SRC-KDL-05-01,SRC-KDL-05-02,SRC-KDL-05-03,SRC-KDL-05-04,SRC-KDL-06-01,SRC-KDL-06-02,SRC-KDL-06-03,SRC-KDL-07-03,SRC-KDL-08-01,SRC-KDL-08-02,SRC-KDL-08-06,SRC-KDL-08-07 | 충분 | 그대로 사용 | Dataset·DataLoader, model·loss·optimizer 연결, gradient update 순서, train·validation 함수, metric 누적과 통합 실행 루프를 다룬다. |
| CC-DL-03 | autograd 그래프와 gradient를 추적하고 vanishing·exploding·detach·in-place 문제를 진단한다. | D2 | CC-MATH-03, CC-DL-01, CC-DL-02 | explain, calculate, shape, implement, debug | primary:SRC-KBM-07-02,SRC-KDL-06-01,SRC-KDL-06-02,SRC-KDL-06-03,SRC-KDL-06-05; supporting:SRC-KDL-02-04,SRC-KDL-04-01,SRC-KDL-04-02,SRC-KDL-05-01,SRC-KDL-05-04,SRC-KDL-06-04 | 부분 | 수업 내 보충 | 계산 그래프·gradient 누적·detach·graph 단절·finite gradient 점검은 직접 다루지만 vanishing/exploding 원인 진단, in-place 오류 재현·수정, 수동 gradient check가 부족하다. |
| CC-DL-04 | activation·initialization·normalization·regularization의 상호작용을 구현하고 비교한다. | D2 | CC-DL-02, CC-ML-03 | explain, implement, debug, interpret, design | primary:SRC-KDL-04-01,SRC-KDL-04-02; supporting:SRC-KDL-04-03,SRC-KDL-04-04,SRC-KAM-03-02 | 부분 | 수업 내 보충 | 비선형성·ReLU·출력 activation은 직접 다루지만 initialization·normalization·통합 regularization 실험이 없다. |
| CC-DL-05 | MLP·CNN·RNN·Transformer 등 주요 architecture의 inductive bias와 shape 흐름을 비교한다. | D2 | CC-DL-04 | explain, shape, implement, interpret, transfer | primary:SRC-KDL-03-01,SRC-KDL-03-02,SRC-KDL-03-03,SRC-KDL-03-04,SRC-KDL-03-05,SRC-KDL-08-01,SRC-KDL-08-02; supporting:SRC-KDL-04-01,SRC-KDL-08-08 | 부분 | 수업 내 보충 | MLP의 경계·층·shape·forward와 통합 적용은 직접 다루지만 CNN·RNN·Transformer inductive bias 비교가 없다. |
| CC-DL-06 | loss curve·gradient·validation을 진단하고 checkpoint·mixed precision을 안전하게 운용한다. | D2 | CC-DL-02, CC-DL-03, CC-SYS-01 | explain, implement, debug, interpret, design | supporting:SRC-KDL-01-02,SRC-KDL-01-04,SRC-KAM-02-02,SRC-KDL-02-03,SRC-KDL-05-01,SRC-KDL-05-03,SRC-KDL-05-04,SRC-KDL-06-03,SRC-KDL-06-05,SRC-KDL-07-05,SRC-KDL-08-05,SRC-KDL-08-07,SRC-KDL-08-08 | 부분 | 수업 내 보충 | validation·gradient 점검·기본 curve 진단과 validation 기준 best weight 선택은 다루지만, optimizer·epoch·history·RNG까지 보존하는 checkpoint/resume와 AMP는 없다. |
| CC-DL-07 | SGD·momentum·AdamW, learning-rate schedule, weight decay·gradient clipping의 update 동역학과 trade-off를 계산·구현·비교한다. | D2 | CC-MATH-03, CC-DL-02, CC-DL-03 | explain, calculate, implement, debug, interpret, design | primary:SRC-KBM-07-01,SRC-KDL-05-03; supporting:SRC-KDL-01-02,SRC-KDL-01-04,SRC-KDL-06-04,SRC-KDL-08-03,SRC-KDL-08-04,SRC-KDL-08-08 | 부분 | 수업 내 보충 | SGD·momentum·Adam, 기본 learning-rate 변경과 gradient update 순서는 직접 다루지만 AdamW·scheduler·decoupled weight decay·clipping의 계산과 통제 비교가 없다. |
| CC-NLP-01 | 텍스트 normalization·tokenization·subword vocabulary의 trade-off를 구현하고 해석한다. | D2 | CC-PROB-01 | explain, implement, debug, interpret, design | context:SRC-KBM-06-02,SRC-KDL-07-02,SRC-KDL-07-03 | 없음 | 별도 자료 확보 | token ID와 dataset·transform 맥락만 있고 tokenizer를 가르치지 않는다. |
| CC-NLP-02 | embedding·padding·mask·sequence batching의 shape와 의미를 구현·디버깅한다. | D2 | CC-NLP-01, CC-DL-01 | explain, shape, implement, debug, interpret | supporting:SRC-KBM-06-01,SRC-KBM-06-02; context:SRC-KDL-01-03,SRC-KDL-07-03 | 부분 | 수업 내 보충 | causal mask와 transform shape는 있으나 embedding·padding mask·가변 길이 batching이 부족하다. |
| CC-LM-01 | autoregressive objective·log-likelihood·perplexity를 계산하고 token loss와 연결한다. | D2 | CC-PROB-02, CC-PROB-03, CC-NLP-02 | explain, calculate, shape, implement, interpret | supporting:SRC-KBM-06-02 | 부분 | 수업 내 보충 | NLL·cross entropy는 있으나 sequence factorization과 perplexity가 없다. |
| CC-LM-02 | greedy·beam·sampling 계열 decoding과 generation 설정의 품질·다양성 trade-off를 실험한다. | D2 | CC-LM-01 | explain, implement, interpret, design, transfer | supporting:SRC-KBM-06-02 | 부분 | 수업 내 보충 | greedy와 temperature만 다루며 top-k·top-p·beam과 종료 조건이 없다. |
| CC-TRF-01 | QKV·scaled attention·mask·multi-head attention의 전체 shape 계약을 계산·구현한다. | D2 | CC-MATH-01, CC-DL-01, CC-NLP-02 | explain, calculate, shape, implement, debug | primary:SRC-KBM-06-01,SRC-KBM-06-02 | 부분 | 수업 내 보충 | single-head까지는 상세하지만 multi-head 분할·병합을 의도적으로 보류했다. |
| CC-TRF-02 | residual·normalization·FFN·position 구성요소의 역할과 정보 흐름을 구현·비교한다. | D2 | CC-TRF-01, CC-DL-04 | explain, shape, implement, debug, interpret | context:SRC-KBM-06-01 | 없음 | 별도 자료 확보 | 자료가 다음 단계로 명시만 하고 직접 가르치지 않는다. |
| CC-TRF-03 | 작은 causal LM을 구현해 teacher forcing으로 학습하고 loss와 generation을 검증한다. | D2 | CC-LM-01, CC-TRF-02, CC-DL-02 | explain, shape, implement, debug, interpret, transfer | context:SRC-KBM-06-02 | 없음 | 별도 자료 확보 | attention loss의 일부만 있어 end-to-end model·학습 자료가 필요하다. |
| CC-LLM-01 | pretraining data의 provenance·deduplication·contamination과 품질 통제를 설계한다. | D2 | CC-LM-01, CC-TRF-03 | explain, implement, interpret, design | context:SRC-KAM-04-02 | 없음 | 별도 자료 확보 | 일반 데이터 누수는 있지만 대규모 말뭉치 구축은 다루지 않는다. |
| CC-LLM-02 | compute·data·model scaling law를 해석하고 제한된 예산의 실험을 설계한다. | D2 | CC-LM-01, CC-STAT-01, CC-SYS-01 | explain, calculate, interpret, design, transfer | — | 없음 | 별도 자료 확보 | 전용 자료가 없다. |
| CC-LLM-03 | SFT·LoRA·PEFT의 목적, parameter·memory trade-off, 구현 경계를 비교한다. | D2 | CC-TRF-03, CC-MATH-02 | explain, calculate, shape, implement, interpret | context:SRC-KBM-04-02 | 없음 | 별도 자료 확보 | LoRA를 저랭크 맥락에서 언급할 뿐 학습 절차를 가르치지 않는다. |
| CC-LLM-04 | preference learning·reward model·DPO·RLHF의 데이터와 목적함수, 실패 모드를 설명한다. | D2 | CC-LLM-03, CC-PROB-02 | explain, calculate, implement, interpret, design | — | 없음 | 별도 자료 확보 | 전용 자료가 없다. |
| CC-EVAL-01 | 평가 질문·dataset·metric·오류 분류를 연결하고 비교 가능한 평가를 설계한다. | D3 | CC-ML-01, CC-ML-02, CC-STAT-01 | explain, implement, interpret, design, transfer | supporting:SRC-KAM-01-01,SRC-KAM-04-01,SRC-KAM-04-02 | 부분 | 수업 내 보충 | 일반 supervised 평가 기반은 있으나 LLM task·slice·통계 보고가 부족하다. |
| CC-EVAL-02 | human judge와 model judge의 rubric·일치도·편향·신뢰도를 측정하고 한계를 보고한다. | D3 | CC-EVAL-01, CC-STAT-02 | explain, calculate, implement, interpret, design | — | 없음 | 별도 자료 확보 | 전용 자료가 없다. |
| CC-EVAL-03 | contamination·robustness·safety 평가의 위협 모델과 실패 사례를 설계한다. | D3 | CC-EVAL-01, CC-LLM-01 | explain, implement, debug, interpret, design, transfer | context:SRC-KAM-04-02,SRC-KDL-01-03 | 없음 | 별도 자료 확보 | 일반 leakage와 민감 응용 예시는 LLM 안전성 평가를 직접 충족하지 않는다. |
| CC-SYS-01 | GPU 연산·메모리·대역폭·precision·profiling의 병목을 측정하고 해석한다. | D2 | CC-DL-01 | explain, calculate, implement, debug, interpret | supporting:SRC-KDL-02-03,SRC-KDL-02-04; context:SRC-KDL-07-01,SRC-KDL-07-05 | 부분 | 수업 내 보충 | device 이동과 DataLoader 옵션 맥락은 있으나 memory hierarchy·kernel·AMP·profiler가 없다. |
| CC-SYS-02 | distributed training의 data·tensor·pipeline parallelism과 sharded checkpoint를 구현·진단한다. | D2 | CC-SYS-01, CC-DL-06 | explain, calculate, shape, implement, debug, interpret | — | 없음 | 별도 자료 확보 | 전용 자료가 없다. |
| CC-SYS-03 | inference latency·throughput·batching·KV cache·quantization의 trade-off를 측정한다. | D2 | CC-SYS-01, CC-TRF-03 | explain, calculate, implement, debug, interpret, design | — | 없음 | 별도 자료 확보 | 전용 자료가 없다. |
| CC-RES-01 | 논문의 주장·실험·근거·한계를 분리해 읽고 주장의 강도를 평가한다. | D3 | CC-STAT-01, CC-ML-05 | explain, interpret, design, transfer | — | 없음 | 별도 자료 확보 | 논문 읽기와 주장 검증을 직접 가르치는 자료가 없다. |
| CC-RES-02 | 가설·baseline·ablation·confounder를 통제한 실험을 설계하고 반증 가능성을 높인다. | D3 | CC-STAT-02, CC-RES-01 | explain, calculate, interpret, design, transfer | context:SRC-KAM-03-01,SRC-KAM-05-01 | 없음 | 별도 자료 확보 | 모델 진단·후보 비교는 있으나 연구 ablation과 confounder 통제를 가르치지 않는다. |
| CC-RES-03 | 재현 절차·artifact·환경·부정적 결과·한계를 검증 가능하게 보고한다. | D3 | CC-RES-01, CC-ML-05 | explain, implement, debug, interpret, design, transfer | context:SRC-KAM-05-02,SRC-KDL-07-04 | 없음 | 별도 자료 확보 | seed 고정과 모델 저장·재로드는 있으나 연구 재현 패키지와 한계 보고가 없다. |

## 4. 선택 전문 트랙

모든 선택 트랙의 목표 깊이는 `D3`다. 트랙을 선택하기 전에는 자료가 없어도 즉시 확보하지 않고 `트랙 선택 시 확보`로 둔다.

| ID | 학습 성과 | 목표 깊이 | 선수 ID | 요구 근거 | 자료 연결 | 자료 충족도 | 공백 처리 | 비고 |
|---|---|---|---|---|---|---|---|---|
| TR-MOD-01 | 현대 LLM architecture 변형의 가설, 계산 비용, 품질 trade-off를 구현·평가한다. | D3 | CC-TRF-03, CC-RES-01 | explain, shape, implement, interpret, design, transfer | — | 없음 | 트랙 선택 시 확보 | MoE·long-context·state-space 등 선택 시점의 핵심 계열을 다룬다. |
| TR-MOD-02 | scaling·data·model 요인을 분리한 ablation으로 개선 원인을 검증한다. | D3 | CC-LLM-02, CC-RES-02 | calculate, implement, interpret, design, transfer | — | 없음 | 트랙 선택 시 확보 | 전용 자료가 없다. |
| TR-MOD-03 | 고급 post-training 목적함수와 online·offline preference 최적화를 비교한다. | D3 | CC-LLM-04, CC-EVAL-02 | explain, calculate, implement, interpret, design | — | 없음 | 트랙 선택 시 확보 | 전용 자료가 없다. |
| TR-MOD-04 | 모델링 논문의 핵심 결과를 재현하고 차이를 ablation으로 설명한다. | D3 | TR-MOD-01, CC-RES-03 | implement, debug, interpret, design, transfer | — | 없음 | 트랙 선택 시 확보 | 전용 자료가 없다. |
| TR-SYS-01 | CUDA·Triton kernel의 메모리 접근과 연산 병목을 profile하고 최적화한다. | D3 | CC-SYS-01 | calculate, shape, implement, debug, interpret, design | — | 없음 | 트랙 선택 시 확보 | 전용 자료가 없다. |
| TR-SYS-02 | sharding·distributed optimizer·collective 통신을 구현하고 scaling 효율을 분석한다. | D3 | CC-SYS-02, TR-SYS-01 | calculate, shape, implement, debug, interpret, design | — | 없음 | 트랙 선택 시 확보 | 전용 자료가 없다. |
| TR-SYS-03 | serving·scheduling·speculative decoding을 구현하고 latency·throughput을 최적화한다. | D3 | CC-SYS-03 | calculate, implement, debug, interpret, design, transfer | — | 없음 | 트랙 선택 시 확보 | 전용 자료가 없다. |
| TR-SYS-04 | 시스템 benchmark의 workload·baseline·측정 오차를 통제해 연구 결론을 낸다. | D3 | TR-SYS-02, TR-SYS-03, CC-RES-02 | calculate, implement, interpret, design, transfer | — | 없음 | 트랙 선택 시 확보 | 전용 자료가 없다. |
| TR-EVAL-01 | 오염과 shortcut을 억제한 benchmark를 설계하고 타당성을 검증한다. | D3 | CC-EVAL-01, CC-RES-02 | explain, calculate, implement, interpret, design, transfer | — | 없음 | 트랙 선택 시 확보 | 전용 자료가 없다. |
| TR-EVAL-02 | judge 신뢰도와 adversarial safety 평가를 결합해 실패 모드를 찾는다. | D3 | CC-EVAL-02, CC-EVAL-03 | explain, implement, debug, interpret, design, transfer | — | 없음 | 트랙 선택 시 확보 | 전용 자료가 없다. |
| TR-EVAL-03 | representation·attention·attribution 기반 interpretability 가설을 실험한다. | D3 | CC-EVAL-01, CC-TRF-03, CC-RES-02 | explain, shape, implement, debug, interpret, design | context:SRC-KAM-02-03 | 없음 | 트랙 선택 시 확보 | tabular SHAP은 연구 맥락만 제공하며 LLM interpretability 자료가 아니다. |
| TR-EVAL-04 | 평가·해석 논문의 결과를 독립 재현하고 측정 한계를 보고한다. | D3 | TR-EVAL-01, TR-EVAL-03, CC-RES-03 | implement, debug, interpret, design, transfer | — | 없음 | 트랙 선택 시 확보 | 전용 자료가 없다. |
| TR-DATA-01 | dataset provenance·license·privacy 위험을 추적하고 release 결정을 설계한다. | D3 | CC-LLM-01, CC-EVAL-03 | explain, implement, interpret, design, transfer | — | 없음 | 트랙 선택 시 확보 | 전용 자료가 없다. |
| TR-DATA-02 | mixture·filtering·synthetic data·tokenizer 선택을 통제 실험으로 비교한다. | D3 | CC-LLM-01, CC-NLP-01, CC-RES-02 | calculate, implement, debug, interpret, design, transfer | — | 없음 | 트랙 선택 시 확보 | 전용 자료가 없다. |
| TR-DATA-03 | retrieval·RAG pipeline을 구현하고 검색·생성 오류를 분해 평가한다. | D3 | CC-NLP-02, CC-TRF-03, CC-EVAL-01 | explain, implement, debug, interpret, design, transfer | context:SRC-KAM-02-03 | 없음 | 트랙 선택 시 확보 | RAG 사례에서 SHAP을 언급할 뿐 retrieval을 가르치지 않는다. |
| TR-DATA-04 | data-centric ablation으로 데이터 품질·양·구성이 결과에 미치는 영향을 검증한다. | D3 | TR-DATA-02, CC-RES-02 | calculate, implement, interpret, design, transfer | — | 없음 | 트랙 선택 시 확보 | 전용 자료가 없다. |

## 5. 현재 강의자료 Registry

감사 범위는 세 과정 `INDEX.md`의 `강의 자료` 표에 있는 파일만이며 `course-provided-practice/`는 제외한다. 2026-08-27 기준 Markdown 본문 전체, 모든 로컬 그림 링크, 각 raster·SVG를 검사했고 PDF는 18쪽 전부 렌더해 육안 확인했다. 총 70개 자료, Markdown 참조 자산 241개(래스터 204개, SVG 37개), PDF 18쪽에서 누락되거나 열리지 않는 현재 파일은 없었다. 다만 아래 `limited` 세 건은 원본·변환 제약 때문에 내용 복구가 필요하다.

| Source ID | 정확한 경로 | 자료 형식 | SHA-256 | 무결성 | 감사 상태 | 감사일 | 비고 |
|---|---|---|---|---|---|---|---|
| SRC-KBM-01-01 | `materials/private/kant-basic-math/01-01_벡터의_정의와_기하학적_해석.md` | PDF 페이지 보존형 Markdown | `dc64b1fc6531ba45489c570ca240386f69f23beb78074c2dfdfe17a18ab45787` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-01-02 | `materials/private/kant-basic-math/01-02_내적과_코사인_유사도.md` | PDF 페이지 보존형 Markdown | `aa74571a130a71e75ccda6b0e4a41ed5125fcefa8178f2c1d55ec5888f124697` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-01-03 | `materials/private/kant-basic-math/01-03_행렬_연산과_딥러닝_레이어.md` | PDF 페이지 보존형 Markdown | `035a19731e5df38d382b87e6da3e53ef320ee314e9a2deaf9017d4b952b058e9` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-01-04 | `materials/private/kant-basic-math/01-04_특수_행렬과_행렬_연산_성질.md` | PDF 페이지 보존형 Markdown | `629498187fa5ca3909324e5e7668fd0363b8f3020bdb811e230c53a6d9988c81` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-02-01 | `materials/private/kant-basic-math/02-01_선형_변환의_기하학적_해석.md` | PDF 페이지 보존형 Markdown | `197ceb3f1004de72a9ffab7179a8a58e60fba743229800e293473d0803397feb` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-02-02 | `materials/private/kant-basic-math/02-02_벡터공간과_선형_독립.md` | PDF 페이지 보존형 Markdown | `8e5612dda842c8de502ebfa39bbd3d8b887c5baf0f2f07b8a47d848d1c32c544` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-02-03 | `materials/private/kant-basic-math/02-03_연립선형방정식과_행렬_해법.md` | PDF 페이지 보존형 Markdown | `e6ac1d7db7b30780f242119b451d37becc8a60b6af4f20591da9693b60953030` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-03-01 | `materials/private/kant-basic-math/03-01_고유값과_고유벡터.md` | PDF 페이지 보존형 Markdown | `8744fc2906b530991f44ebb02757099c63fcd4661ecf35bcc93d4c3bb028958e` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-03-02 | `materials/private/kant-basic-math/03-02_행렬_대각화와_PCA_구현.md` | PDF 페이지 보존형 Markdown | `5e5d755d75a9d701aec599065c0b2bbd5e42b0373bf07b5a929057aa13afcd83` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-03-03 | `materials/private/kant-basic-math/03-03_직교성과_최소제곱법.md` | PDF 페이지 보존형 Markdown | `91322e45369fe82059bdeedf8596dd44ade8f0e200054cef06577483335da7ad` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-04-01 | `materials/private/kant-basic-math/04-01_SVD의_구조와_원리.md` | PDF 페이지 보존형 Markdown | `3157566ff072b42c5cf992785eb026b4f6a14f5d981284e759f01da4e243b131` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-04-02 | `materials/private/kant-basic-math/04-02_SVD와_PCA_저랭크_응용.md` | PDF 페이지 보존형 Markdown | `adeaf26c81e6169be79e8486f0e796fafa8132dc0c875ee4fa9876437d125bb6` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-04-03 | `materials/private/kant-basic-math/04-03_선형대수_종합_미니_프로젝트.md` | PDF 페이지 보존형 Markdown | `9a826faea0120605d47d1174f8f3126237aaa9641ac87a9be5a6f16963123084` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-05-01 | `materials/private/kant-basic-math/05-01_벡터_행렬_텐서와_Shape.md` | PDF 페이지 보존형 Markdown | `c0dd25f7507175688102f07e9849ff4f078a60693fbbcf65a8ba699f27cd9411` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-05-02 | `materials/private/kant-basic-math/05-02_reshape_transpose_broadcasting_shape.md` | PDF 페이지 보존형 Markdown | `13b3f483cf163c81d8d406f043836eca397db9575ba7f02a29f80e808751666e` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-06-01 | `materials/private/kant-basic-math/06-01_Attention_score와_QK_t_shape.md` | PDF 페이지 보존형 Markdown | `931e1efdff027828a2576164baaa410dbdea134f82053e7fe5e6f0070c3a93e2` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-06-02 | `materials/private/kant-basic-math/06-02_Softmax_로그확률_Cross_Entropy.md` | PDF 페이지 보존형 Markdown | `822b4f4160a5d5681cfe537d316b0ae4dc1a4be732ac8048b7380eb885eb4f1c` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-07-01 | `materials/private/kant-basic-math/07-01_미분_Gradient_Gradient_Descent.md` | PDF 페이지 보존형 Markdown | `582d0e45125b61e752a8b9d1cfbcecc207205b6db03e12832289b36b384f215b` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KBM-07-02 | `materials/private/kant-basic-math/07-02_Chain_Rule과_Backpropagation.md` | PDF 페이지 보존형 Markdown | `07d5d4b8ee53a7b4e3aaa54e384126092dd65bf9a082688d500f695b86c4fd78` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KAM-01-01 | `materials/private/kant-advanced-machine-learning/01-01_문제_유형_데이터_분리_평가지표_리마인드.md` | PDF 페이지 보존형 Markdown | `9a2dc5db2e0daa29a8c3b83af7e41c96abf5264bb601cbfb5054473fff064d6d` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KAM-01-02 | `materials/private/kant-advanced-machine-learning/01-02_핵심_모델과_선택_기준_압축_정리.md` | PDF 페이지 보존형 Markdown | `a58807f4a2e10a9d10bb9dfd966a074c20a7a1b6721087bda0377aa5ea900690` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KAM-02-01 | `materials/private/kant-advanced-machine-learning/02-01_배깅과_랜덤포레스트.md` | HTML 토글 펼침 Markdown | `e2b0757ff006a4abdf6b0efed10730bee39d58d645d1ecc3b10a035c47280b50` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KAM-02-02 | `materials/private/kant-advanced-machine-learning/02-02_부스팅_계열_모델의_원리와_발전.md` | HTML 토글 펼침 Markdown | `6084d9358d24f48b5f96db420421d38137cc6c2b679c8588f6027d072d3eab70` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KAM-02-03 | `materials/private/kant-advanced-machine-learning/02-03_배깅_vs_부스팅_선택과_모델_해석_SHAP.md` | HTML 토글 펼침 Markdown | `2a79fe64405c6acc4b0303d1518e2bc5a26c0a73a5acb8640c88cf2803e8c45b` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KAM-03-01 | `materials/private/kant-advanced-machine-learning/03-01_편향_분산_트레이드오프와_과적합_과소적합_진단.md` | HTML 토글 펼침 Markdown | `1fc051b10f4663448a418847433d0d5ada03f2e95561e575d2402ab4d6f63a32` | limited | complete | 2026-08-20 | 수식 일부가 HTML 변환 과정에서 중복·훼손됨 |
| SRC-KAM-03-02 | `materials/private/kant-advanced-machine-learning/03-02_규제_L1_Lasso_L2_Ridge_ElasticNet.pdf` | PDF | `95a123f99e48a9d8d0399fecef7bebdf0d4b70aed07a6c8a776ab0c506eb3527` | limited | complete | 2026-08-20 | 18쪽 구버전은 완독·렌더 확인; INDEX에 신버전 이미지 1장 누락 기록 |
| SRC-KAM-04-01 | `materials/private/kant-advanced-machine-learning/04-01_데이터_불균형과_평가지표_왜곡.md` | HTML 토글 펼침 Markdown | `7ccb8c6b8855570e3e47f5c9df88078fb0621bfa3cfb3f6e3c54fc1c2a69a4bb` | limited | complete | 2026-08-20 | SMOTE·비용 수식 일부가 HTML 변환 과정에서 중복·훼손됨 |
| SRC-KAM-04-02 | `materials/private/kant-advanced-machine-learning/04-02_교차검증_전략과_데이터_누수_방지.md` | HTML 토글 펼침 Markdown | `7eae401632c30f6a6ca3fd9cc05807816db1b36d7948aace25dd93582521eb2f` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KAM-05-01 | `materials/private/kant-advanced-machine-learning/05-01_CV_기반_하이퍼파라미터_탐색과_공정한_후보_선정.md` | HTML 토글 펼침 Markdown | `e7215f8b9e37c24cd1619c4089f5ee1f2ada5cfa40a70dc35eaa516c64b57bb3` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KAM-05-02 | `materials/private/kant-advanced-machine-learning/05-02_누수_없이_학습하고_재사용하는_End-to-End_Pipeline.md` | HTML 토글 펼침 Markdown | `80b80c2c5ce91d713206475e67c81459c189a9496cd1ee9ea3a128b43371e7a5` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-01-00 | `materials/private/kant-deep-learning-basics/01-00_오프닝_딥러닝_기초_학습_로드맵.md` | HTML 토글 펼침 Markdown | `83787496645ab022b3b114e9103b87592f3cecab84d5387b5dec64273ae20a97` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-01-01 | `materials/private/kant-deep-learning-basics/01-01_머신러닝과_딥러닝의_차이.md` | HTML 토글 펼침 Markdown | `8a67681ddedb7b8da2f248183925acc2e7667be98eb7cebf1a9ab0149a1bc096` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-01-02 | `materials/private/kant-deep-learning-basics/01-02_데이터_모델_손실_최적화_평가_흐름.md` | HTML 토글 펼침 Markdown | `5219b3fcf6190b639eb3000651df348b9fa3f8c3fc64c26a9df9b3da3aa0a5a7` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-01-03 | `materials/private/kant-deep-learning-basics/01-03_딥러닝_문제_유형과_입출력_구조_설계.md` | HTML 토글 펼침 Markdown | `397b979aac6102e76e55a92a9c0dfcb13912f6f93d8a78c79b2db02456a0f9ac` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-01-04 | `materials/private/kant-deep-learning-basics/01-04_기본_코드_구조_읽기.md` | HTML 토글 펼침 Markdown | `81a325e1d76c0bbe08e209c1c74358d961b1ff22a00a20029824242a456cbb6f` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-02-01 | `materials/private/kant-deep-learning-basics/02-01_Tensor_생성과_dtype_shape_확인.md` | HTML 토글 펼침 Markdown | `64b51c35d0d2b4c3d0cd813694c4feb59e08783ffc198d94678a728e7c6b6c05` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-02-02 | `materials/private/kant-deep-learning-basics/02-02_Batch_dimension과_broadcasting.md` | HTML 토글 펼침 Markdown | `343bd57f9e364fd280a1afe12a3b8949421323356020ccd36e20149c277ed787` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-02-03 | `materials/private/kant-deep-learning-basics/02-03_CPU_GPU_device와_to_device.md` | HTML 토글 펼침 Markdown | `adb2b38aab63e7ea20436ab60a2de5c369edbeea01be3c17ada123b7ae37f3a6` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-02-04 | `materials/private/kant-deep-learning-basics/02-04_Shape_Device_오류_디버깅.md` | HTML 토글 펼침 Markdown | `d649878656851cc8b17931716ba7ed71a280c9081f765026b0e5ced74429dda0` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-03-01 | `materials/private/kant-deep-learning-basics/03-01_퍼셉트론과_선형_결정_경계.md` | HTML 토글 펼침 Markdown | `171bcd83dcdbb3c2623ee153cba800482da358f82f8988400389897a45b930be` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-03-02 | `materials/private/kant-deep-learning-basics/03-02_MLP의_입력층_은닉층_출력층.md` | HTML 토글 펼침 Markdown | `d20acae10499e57ef9bb26f14a0a112b1d043dac0f762023a279ac840ff8b7ef` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-03-03 | `materials/private/kant-deep-learning-basics/03-03_가중치_편향과_nn_Linear.md` | HTML 토글 펼침 Markdown | `8c446f84b4a0aacf98c2426d23575629ed27232105d9f61fdb1cba0115eec538` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-03-04 | `materials/private/kant-deep-learning-basics/03-04_입출력_차원_계산과_flatten.md` | HTML 토글 펼침 Markdown | `23aed119df3aec18653aed8707d915c0f369742c33378120f88047895f57b39c` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-03-05 | `materials/private/kant-deep-learning-basics/03-05_MLP_forward_미니_구현.md` | HTML 토글 펼침 Markdown | `921ae90e92ba56ec0695fd4e4c3d0c36b69d78a3b942b1fc9fc173e393191de2` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-04-01 | `materials/private/kant-deep-learning-basics/04-01_비선형성과_활성화_함수_필요성.md` | HTML 토글 펼침 Markdown | `185da5e7eec5045ea5dbba2c9eafd83fe09c8ab2573763d4ef3b8004ae36f53d` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-04-02 | `materials/private/kant-deep-learning-basics/04-02_ReLU의_역할과_사용_위치.md` | HTML 토글 펼침 Markdown | `084d67d1470e626a92997ccd2135fd9d56f2d47f71d58d6207d28fb8c64338da` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-04-03 | `materials/private/kant-deep-learning-basics/04-03_Sigmoid와_이진_분류_출력층.md` | HTML 토글 펼침 Markdown | `ed1c782bcb3814552fabe2504df29af3ad5bc22d06e1a9521b9c9186d6c1373c` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-04-04 | `materials/private/kant-deep-learning-basics/04-04_Softmax와_다중_분류_출력층.md` | HTML 토글 펼침 Markdown | `cd64126894afab51a819ffe9f57d0ca71995b94921b6b1d7a2908ebc86e78ab2` | complete | complete | 2026-08-20 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-05-01 | `materials/private/kant-deep-learning-basics/05-01_손실_함수의_역할과_목표_함수.md` | HTML 토글 펼침 Markdown | `ca86e2766341de080cf8ab3582911cd5744a44ca568450739d11eead13bce164` | complete | complete | 2026-08-21 | 본문 전체와 참조 자산 확인 |
| SRC-KDL-05-02 | `materials/private/kant-deep-learning-basics/05-02_회귀_이진_다중_분류_손실_선택.md` | HTML 토글 펼침 Markdown | `758689b2c7fa3852658c31d2aa51da2b5c570ca668b8f283c2fc86a496585e49` | complete | complete | 2026-08-21 | 본문 전체와 참조 자산 확인 |
| SRC-KDL-05-03 | `materials/private/kant-deep-learning-basics/05-03_SGD_Adam과_learning_rate.md` | HTML 토글 펼침 Markdown | `4c0dd39aaba5b769f76abc3aa16931458e8b0d1eeaefbf4202428516e512918a` | complete | complete | 2026-08-21 | 본문 전체와 참조 자산 확인 |
| SRC-KDL-05-04 | `materials/private/kant-deep-learning-basics/05-04_파라미터_업데이트_코드_흐름.md` | HTML 토글 펼침 Markdown | `4252a17a508aa5e90c8e496a18390efc1461d64ec5bb1f72a0c6a5f36d8c9210` | complete | complete | 2026-08-21 | 본문 전체와 참조 자산 확인 |
| SRC-KDL-06-01 | `materials/private/kant-deep-learning-basics/06-01_계산_그래프와_Chain_Rule.md` | HTML 토글 펼침 Markdown | `3753b7a9939583953871e7f5e4f01f366edd0d3c6ea139007ff23bda6a3b30c6` | complete | complete | 2026-08-25 | 본문 전체와 참조 자산 렌더 확인; backward 그림의 update 단계는 수업에서 정정 |
| SRC-KDL-06-02 | `materials/private/kant-deep-learning-basics/06-02_requires_grad와_Tensor_gradient.md` | HTML 토글 펼침 Markdown | `14b9d7c4e5a4296d0708590291388139d6948d426141b03de3a443254a997b4a` | complete | complete | 2026-08-25 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-06-03 | `materials/private/kant-deep-learning-basics/06-03_loss_backward와_grad_확인.md` | HTML 토글 펼침 Markdown | `1f730c0978d62f9898bed31bfa49e41b6b38c10b9eabcf0e768930b4c1287d39` | complete | complete | 2026-08-25 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-06-04 | `materials/private/kant-deep-learning-basics/06-04_zero_grad_backward_step_순서.md` | HTML 토글 펼침 Markdown | `21a8b379768c78cfaf642be9ad3dda2cb29cbd45bd7d6711991e3ac59630ca24` | complete | complete | 2026-08-25 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-06-05 | `materials/private/kant-deep-learning-basics/06-05_Autograd_디버깅과_안전한_평가_코드.md` | HTML 토글 펼침 Markdown | `c2c3d89385944821ad18bc1080de75d432acf460b1301e5664ff88c5f17811e1` | complete | complete | 2026-08-25 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-07-01 | `materials/private/kant-deep-learning-basics/07-01_Dataset과_DataLoader_역할.md` | HTML 토글 펼침 Markdown | `15d8477f1462f9553f1df9698f6160f7a453ad211f27505f9171a56c4175c686` | complete | complete | 2026-08-25 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-07-02 | `materials/private/kant-deep-learning-basics/07-02_TensorDataset과_Custom_Dataset.md` | HTML 토글 펼침 Markdown | `8b78b562b743e07917de9d738a691a8719ced7b649e3ea28f46cda9809040c4c` | complete | complete | 2026-08-25 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-07-03 | `materials/private/kant-deep-learning-basics/07-03_transform과_전처리_흐름.md` | HTML 토글 펼침 Markdown | `2bddf6da297fde40334205726856846b3dbf522c44161a132bd1182d0f76502a` | complete | complete | 2026-08-25 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-07-04 | `materials/private/kant-deep-learning-basics/07-04_batch_size_shuffle_train_valid_split.md` | HTML 토글 펼침 Markdown | `f68be4afabdc00c9d6d7f71d794255f04117f93af97aed9b505aa7b45db635c4` | complete | complete | 2026-08-25 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-07-05 | `materials/private/kant-deep-learning-basics/07-05_데이터_파이프라인_디버깅.md` | HTML 토글 펼침 Markdown | `90eaa381eaf79f28be1f5196f4142592fa4fd15be43ba4ebddd7a251159a0eb7` | complete | complete | 2026-08-25 | 본문 전체와 참조 자산 렌더 확인; 첫 batch 재사용 경계는 수업에서 정정 |
| SRC-KDL-08-01 | `materials/private/kant-deep-learning-basics/08-01_nn_Module_구조와_forward_설계.md` | HTML 토글 펼침 Markdown | `49320cf447e2ee79a203763126035271ddd826debf6790ad3394cbca0b202fc3` | complete | complete | 2026-08-27 | 본문 전체와 참조 자산 렌더 확인; 개요 그림과 실제 `model(x) -> __call__ -> forward` 호출 순서는 본문 설명을 기준으로 사용 |
| SRC-KDL-08-02 | `materials/private/kant-deep-learning-basics/08-02_MLP_모델_클래스_완성.md` | HTML 토글 펼침 Markdown | `926aa3df781e9983b9cbdad533ae3f902330d4b0113a653fe5dfe065a26046b0` | complete | complete | 2026-08-27 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-08-03 | `materials/private/kant-deep-learning-basics/08-03_loss와_optimizer_연결.md` | HTML 토글 펼침 Markdown | `9b45a84073b5e2c25c7df4dbe23682cbfb4e377ae24c44e243621a7102ddc9ab` | complete | complete | 2026-08-27 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-08-04 | `materials/private/kant-deep-learning-basics/08-04_train_loop_작성.md` | HTML 토글 펼침 Markdown | `2ec6a15904a1f1720c6a89e9b2ec2722fa5410a5e9f8054bf4b189318f7b9163` | complete | complete | 2026-08-27 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-08-05 | `materials/private/kant-deep-learning-basics/08-05_validation_loop_작성.md` | HTML 토글 펼침 Markdown | `7aad21b64f154eae3746626cbc54f53147d2d9135ab3d11e8c742c29191f7be5` | complete | complete | 2026-08-27 | 본문 전체와 참조 자산 렌더 확인 |
| SRC-KDL-08-06 | `materials/private/kant-deep-learning-basics/08-06_accuracy와_metric_누적.md` | HTML 토글 펼침 Markdown | `2ce49b778769c5e93f13305945d8febdc902b8c2a96f88c6625f25d433d0c026` | complete | complete | 2026-08-27 | 본문 전체와 참조 자산 렌더 확인; sample-weighted accuracy와 불균형 경계를 포함 |
| SRC-KDL-08-07 | `materials/private/kant-deep-learning-basics/08-07_epoch_단위_로그와_시각화.md` | HTML 토글 펼침 Markdown | `941935259715349c8e5a81cb4b149956a04fba4e27417aaa96530d81d0fa808d` | complete | complete | 2026-08-27 | 본문 전체와 참조 자산 렌더 확인; 왼쪽이 잘린 개요 raster의 정보는 본문·코드·SVG로 보존됨 |
| SRC-KDL-08-08 | `materials/private/kant-deep-learning-basics/08-08_MLP_종합_실습.md` | HTML 토글 펼침 Markdown | `61e45f90bc6a396c3b8dc784fdd7f9095cc1d18e3c3ff658efa2a34a2ce19d6d` | complete | complete | 2026-08-27 | 본문 전체와 참조 자산 렌더 확인; `best_state`는 메모리 내 model weight 보존이며 checkpoint/resume은 아님 |

## 6. 감사 중 발견된 주요 오류와 공백

### 즉시 정정할 내용

- `[정정]` `SRC-KBM-01-01`, **4. 정규화와 ML 특성 벡터의 의미**: 한 샘플 벡터 전체를 L2 norm으로 나누는 정규화는 특성별 단위·분산을 같게 만드는 scaling 또는 standardization과 다르다. 현재 설명은 둘을 혼동하므로 수업에서 분리한다.
- `[정정]` `SRC-KBM-01-02`, **2. 내적과 각도 및 3. 코사인 유사도의 값 해석**: cosine similarity는 두 벡터가 모두 nonzero일 때만 정의된다. 분모의 norm 중 하나라도 0이면 각도와 similarity가 미정의이고 제시된 NumPy 코드는 `NaN`을 만들 수 있으므로, `[-1, 1]` 범위 설명과 구현에 nonzero-norm 조건을 붙인다.
- `[정정]` `SRC-KBM-01-03`, **5페이지 신경망 계산 도식·표**: `X @ W + b`에서 `W`를 `(in_features, out_features)`로 두는 것은 수학적 표기로는 가능하지만, 이를 PyTorch `nn.Linear`의 저장 shape와 내부 계산이라고 설명한 부분은 틀렸다. `nn.Linear(in_features, out_features)`는 `weight`를 `(out_features, in_features)`로 저장하고 `X @ weight.T + bias`를 계산한다. 수업에서 수학적 `W` 관례와 framework parameter layout을 분리한다. 근거: [PyTorch `nn.Linear` 공식 문서](https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html).
- `[정정]` `SRC-KBM-01-04`, **5. 행렬식 존재 조건과 행렬식의 직관**: 수학적으로 singular는 determinant가 정확히 0인 경우다. 0에 가깝다는 사실만으로 singular라고 부르지 않으며 determinant 크기는 scale에 의존하므로 conditioning 판단을 대신하지 못한다.
- `[정정]` `SRC-KBM-02-03`, **4. 선형회귀와 정규방정식** 및 **이번 강의 핵심 정리 4**: overdetermined least-squares minimizer는 존재하지만 design matrix의 열이 rank-deficient이면 계수 해는 유일하지 않을 수 있다. explicit normal equation은 condition number도 악화시킬 수 있다.
- `[정정]` `SRC-KBM-04-01`, **2. U, Σ, Vᵀ의 의미**: full SVD의 `U` 전체가 column space의 기저이거나 `Vᵀ` 전체가 row space의 기저인 것은 아니다. nonzero singular value에 대응하는 left singular vector만 column space를, right singular vector만 row space를 span하고, 나머지는 각 ambient space의 직교기저를 완성한다.
- `[정정]` `SRC-KBM-04-02`, **2. sklearn PCA 내부 구현과 SVD 및 이번 강의 핵심 정리 1**: `PCA`는 solver에 따라 full·randomized·ARPACK SVD뿐 아니라 covariance matrix를 만드는 `covariance_eigh`도 사용할 수 있으므로 “covariance를 만들지 않는다”와 “sklearn도 내부적으로 SVD를 사용한다”는 단정에 solver 조건을 붙여야 한다. 근거: [scikit-learn PCA 공식 문서](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html).
- `[정정]` `SRC-KBM-03-02`, **2. PCA의 수학적 원리·표준화 심화·핵심 정리 4**; `SRC-KBM-04-02`, **3. 차원 축소 파이프라인**; `SRC-KBM-04-03`, **1. 데이터 분석 파이프라인 개관**: PCA는 feature를 center하지만 feature별 scaling은 자동으로 하지 않는다. PCA 전에 언제나 standardization해야 하는 것은 아니며, 단위 차이를 제거하려는지 원래 covariance 규모와 특성의 의미를 보존하려는지에 따라 결정한다. 근거: [scikit-learn PCA 공식 문서](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html).
- `[정정]` `SRC-KBM-04-02`, **5. 추천 시스템과 LoRA에서의 저랭크 아이디어**: LoRA는 trainable low-rank factor를 쓰지만 일반적인 LoRA 학습이 SVD를 계산하는 것은 아니다. 공통점은 저랭크 parameterization이지 같은 알고리즘이라는 뜻이 아니다. 근거: [LoRA 원 논문](https://arxiv.org/abs/2106.09685).
- `[정정]` `SRC-KBM-06-02`, **이번 강의 핵심 정리 4**: 정답 class의 cross entropy는 `log(p_true)`가 아니라 `-log(p_true)`다.
- `[정정]` `SRC-KBM-06-02`, **이해 점검 2**: 미래 token score에는 양의 무한대가 아니라 음의 무한대를 더해야 softmax 확률이 0이 된다.
- `[정정]` `SRC-KDL-05-01`, **손실 함수와 목표 함수 흐름 그림, 2-2**: prediction과 target은 loss function의 병렬 입력이며, 그림처럼 차례로 흘러가는 관계가 아니다. 또 scalar loss는 오차의 벌점을 나타낼 뿐 parameter 수정 방향을 직접 담지 않는다. 수정 방향은 `loss.backward()`가 계산한 gradient가 제공한다.
- `[정정]` `SRC-KDL-06-01`, **계산 그래프의 forward와 backward 흐름 그림**: 그림 끝의 parameter update는 backward 자체가 수행하는 단계가 아니다. backward는 gradient를 계산·누적하고 optimizer의 `step()`이 parameter를 갱신한다.
- `[정정]` `SRC-KDL-07-05`, **첫 batch 검사 코드**: `shuffle=True`인 loader에서 `next(iter(loader))`를 다시 호출하면 앞에서 출력한 batch와 다른 batch를 검사할 수 있다. 한 번 꺼낸 `(xb, yb)`를 shape·dtype·값 범위·유한성 검사에 재사용한다.

### 무결성 제약과 허용 가능한 보류

- `SRC-KAM-03-01`의 bias-variance 및 one-standard-error rule 수식 일부가 HTML 변환에서 중복·훼손됐다. 주변 설명과 그림은 읽을 수 있지만 정확한 식은 원본을 복구하기 전 그대로 근거로 쓰지 않는다.
- `SRC-KAM-03-02`의 현재 18쪽 PDF는 전체 텍스트 추출과 페이지 렌더가 가능하고 모든 페이지를 확인했다. 다만 과정 `INDEX.md`가 신버전 이미지 1장 누락 때문에 구버전을 유지한다고 명시하므로 `limited`이며 신버전 복구 뒤 재감사한다.
- `SRC-KAM-04-01`의 SMOTE 보간식과 비용식 일부가 HTML 변환에서 중복·훼손됐다. 그림·코드·서술은 남아 있지만 손상된 식은 독립 근거로 쓰지 않는다.
- `SRC-KBM-*`의 page-preserving Markdown은 일부 검색 텍스트에서 수식이 축약되지만 모든 원페이지 render가 존재하고 육안으로 읽힌다. 수식 감사와 수업에서는 검색 텍스트만 보지 않고 연결된 페이지 render를 함께 쓴다.
- `SRC-KBM-06-01`은 single-head attention까지만 다루고 multi-head, residual, normalization, FFN, positional encoding을 다음 단계로 명시적으로 보류한다. 이는 현재 강의 범위의 의도적 보류지만 `CC-TRF-01~03` 전체 충족으로 확대 해석하지 않는다.
- `SRC-KDL-06-02`의 `detach()` 설명은 graph 분리는 정확하지만 원본과 storage를 공유한다는 경계를 생략한다. 독립 복사가 필요할 때는 `detach().clone()`을 사용한다고 수업에서 보충한다.
- `SRC-KDL-06-05`의 anomaly detection 예시는 backward만 context로 감싼다. 실패 연산의 forward traceback까지 필요하면 forward와 loss 계산도 같은 context에서 실행한다고 보충한다.
- Chapter 6·7·8의 “주차 시작에 PDF를 올렸다”는 문장은 별도 로컬 PDF 링크를 제공하지 않는다. 현재 Markdown·자산 패키지는 완전하게 감사했지만, 그 문장이 가리키는 추가 원본의 존재 여부는 별도로 확인되기 전 provenance 근거로 세지 않는다.

### 커리큘럼 공백

- 현재 70강의 강점은 선형대수·tensor shape·MLP와 activation·손실·optimizer·autodiff·기본 데이터 파이프라인·train-validation-test 루프·기본 attention·전통 ML 평가와 leakage 방지다.
- 확률·통계 추론, NLP 전처리와 tokenizer, 완전한 Transformer·causal LM, pretraining·post-training, LLM 평가, 분산·추론 시스템, 논문 읽기·실험 설계·재현 보고는 직접 자료가 없거나 맥락 언급뿐이다.
- 딥러닝 기초 `SRC-KDL-01-00`은 14개 장의 향후 구성을 제시하지만 현재 registry에는 8개 장 40강만 있다. 등록되지 않은 미래 계획은 현재 자료 충족 근거로 세지 않는다.
- 전문 트랙은 모두 D3가 목표이며 현재 과정은 어떤 트랙도 직접 충족하지 않는다. 트랙을 선택한 뒤 해당 자료를 확보한다.

## 7. 갱신 규칙

1. ID는 의미를 바꾸거나 재사용하지 않는다. 성과가 새로 필요하면 새 ID를 추가한다.
2. 자료를 추가·교체하면 정확한 상대 경로와 SHA-256을 registry에 기록하고 해당 과정 `INDEX.md`와 양방향 일치를 확인한다.
3. 본문 전체, Markdown의 모든 로컬 자산, PDF의 모든 페이지를 확인하기 전에는 감사 상태를 `complete`로 두지 않는다.
4. 원본 누락 또는 변환 훼손이 있으면 무결성을 `limited`나 `blocked`로 두고 `충분` 판정의 단독 근거로 쓰지 않는다.
5. 역량 연결은 `primary`, `supporting`, `context` 중 하나로 명시한다. `context`만으로 `충분`을 부여하지 않는다.
6. 목표 깊이와 실제로 만들 수 있는 요구 근거를 비교해 충족도를 정한다. 자료가 바뀌면 관련 매핑과 오류·공백을 다시 감사한다.
7. 기본 구조 검증은 `python3 .agents/skills/coach-llm-research-study/scripts/validate_curriculum.py`로, 모든 private 자료·hash·INDEX parity를 포함한 검증은 같은 명령에 `--strict-sources`를 붙여 실행한다. 한 과정만 readiness 관점에서 검사할 때는 `--strict-sources --course-index materials/private/<course>/INDEX.md`를 함께 쓴다.
