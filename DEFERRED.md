# 보류 자료

이 문서는 **현재 경로에서 뺀 자료의 목록과 다시 꺼낼 조건**입니다. 여기 있는
항목은 완료된 것도, 불필요하다고 판정된 것도 아닙니다. 모두 **미완료 보류**이며
`ROADMAP.md`의 Phase 예산 안에서 1순위 전문화에 직접 기여하지 않기 때문에 뺐습니다.

이 문서는 진도나 완료 여부를 기록하지 않습니다. 복귀 조건이 실제로 발생하면
Agent가 해당 항목을 제안하고, 사용자가 승인한 뒤에만 `STATE.md`를 바꿉니다.
**어떤 조건도 자동으로 학습을 시작하지 않습니다.** 보류 항목을 꺼낼 때는 그
항목 전체가 아니라 그 시점에 필요한 범위만 꺼냅니다.

## 읽는 법

- **무엇**: 자료와 범위
- **왜 뺐나**: 현재 경로에서 제외한 판단 근거
- **무엇을 열어 주나**: 이 자료가 실제로 가능하게 하는 것
- **복귀 조건**: 이것이 관찰되면 다시 제안한다

---

## 1. CS224N Spring 2024 (A1~A4, Final Project)

[CS224N Spring 2024](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html) ·
[AI Tools Policy](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1246/index.html) ·
[공개 영상](https://www.youtube.com/playlist?list=PLoROMvodv4rOaMFbaqxPDoLWjDaRAdP9D)

과정 전체를 통째로 뺀 것이 아니라 항목별로 판단했습니다. 복귀할 때도 과제 하나
전체가 아니라 아래에 적힌 부분만 꺼냅니다. 공식 AI 정책은 복귀 시점에도 그대로
적용됩니다.

### A1 — Word Vectors (word2vec, co-occurrence SVD)

- **왜 뺐나**: embedding이 학습되는 원리는 makemore Part 2에서 이미 직접
  구현했습니다. word2vec의 negative sampling과 SVD 기반 embedding은 역사적으로
  중요하지만 decoder-only LM의 추론 성능과 직접 연결되지 않습니다.
- **무엇을 열어 주나**: 분포 가설, embedding 공간의 기하, 사전학습 embedding의 평가
- **복귀 조건**: embedding 품질 자체를 평가·비교해야 하는 작업이 생길 때.
  또는 2순위 트랙(Evaluation)에서 표현 학습을 다룰 때

### A2 — Dependency Parsing과 신경망 수기 미분

- **왜 뺐나**: dependency parsing은 고전 NLP 구조 예측이며 현재 경로에 연결
  지점이 없습니다. written 파트의 수기 backpropagation은 **Karpathy Part 4가
  더 깊게 대체**하므로 손실이 없습니다.
- **무엇을 열어 주나**: 구문 구조, transition-based parsing
- **복귀 조건**: 구조 예측 과제를 직접 다루게 될 때. 현재 목표 경로에서는
  발생하지 않을 가능성이 높습니다

### A3 — Seq2Seq NMT, Attention 변형, Beam Search, Subword

- **왜 뺐나**: encoder-decoder 기계번역은 decoder-only 추론 최적화와 구조가
  다릅니다. attention 자체는 Karpathy "Let's build GPT"와 CS336 A1이 다룹니다.
- **무엇을 열어 주나**: **beam search와 디코딩 전략**. 이 부분만은 추론
  최적화와 직접 관련이 있습니다. greedy·sampling·beam의 품질/지연 trade-off는
  `P4`에서 실제로 측정하게 됩니다
- **복귀 조건**: `P4`에서 디코딩 전략을 비교할 때 **A3의 beam search 부분만**
  발췌해서 사용. 번역 과제 전체는 꺼내지 않습니다

### A4 — Transformer 자기지도학습과 Fine-tuning

- **왜 뺐나**: Transformer 사전학습 구현은 CS336 A1이 더 엄밀하고 공식 테스트도
  있습니다. 범위가 겹칩니다.
- **무엇을 열어 주나**: fine-tuning 절차, 사전학습과 downstream task의 연결
- **복귀 조건**: 2순위 트랙(Post-training: SFT, LoRA)에 진입할 때.
  그때는 CS336 A5(Alignment)가 더 나은 선택일 수 있으므로 함께 비교합니다

### Final Project — 공식 BERT 프로젝트

- **왜 뺐나**: BERT는 encoder-only입니다. 1순위 전문화의 대상인 autoregressive
  decoder 추론(KV cache, prefill/decode 분리, continuous batching)이 BERT에는
  존재하지 않습니다. 3~4주를 쓰고도 목표 역량에 닿지 않습니다.
- **무엇을 열어 주나**: 완결된 연구 프로젝트 경험, 논문 수준의 보고
- **복귀 조건**: 연구 프로젝트 경험 자체가 필요해질 때. 단 그 시점에는
  `P4`의 추론 최적화 프로젝트가 같은 역할을 하면서 1순위 전문화에 직접
  기여하므로, **`P4`를 파이널 프로젝트로 대체하는 것이 기본 판단**입니다

---

## 2. Karpathy makemore Part 5 — WaveNet

- **왜 뺐나**: dilated causal convolution으로 문맥을 늘리는 구조이며,
  Transformer 계열 추론 최적화와 이어지지 않습니다. 계층적 구조를 쌓는 감각은
  Part 3·4에서 충분히 얻습니다.
- **무엇을 열어 주나**: convolution 기반 sequence 모델, 계층적 receptive field
- **복귀 조건**: convolution 기반 아키텍처를 실제로 다뤄야 할 때.
  현재 경로에서는 발생하지 않을 가능성이 높습니다

---

## 3. 통계 추론 — Stat110 후반부, 신뢰구간·bootstrap·가설검정

`CURRICULUM.md`의 `CC-PROB-02`(likelihood·MLE), `CC-STAT-01`, `CC-STAT-02`.
Stat110 2판은 Chapter 1~4만 채택한 상태입니다.

- **왜 뺐나**: 지금 당장의 구현을 막고 있지 않습니다. 선수로 먼저 쌓기보다
  실제로 필요해지는 지점에서 보충하는 편이 정착이 잘 됩니다.
- **무엇을 열어 주나**:
  - **MLE**: cross-entropy 최소화가 왜 최대가능도 추정인지. 지금은 "손실을
    줄인다"로 쓰고 있지만 추정 이론으로 다시 읽으면 학습 목적 함수 선택을
    설명할 수 있게 됩니다
  - **신뢰구간·bootstrap·가설검정**: 벤치마크 결과 비교. **측정 없이는
    최적화를 주장할 수 없고, 분산과 신뢰구간 없이는 측정을 주장할 수 없습니다**
- **복귀 조건**:
  - MLE는 `P2`에서 학습 목적 함수를 다룰 때 **수업 내 보충**으로 처리
  - 신뢰구간·bootstrap·가설검정은 **`P3` 진입 직전에 필수로 보충**합니다.
    `P3`는 커널 최적화의 개선폭을 보고하는 구간이고, "3% 빨라졌다"가 노이즈인지
    실제 개선인지 구분하지 못하면 결과를 신뢰할 수 없습니다. 이 항목은
    보류 목록 중 **유일하게 일정이 정해진 복귀**입니다

---

## 4. RNN·LSTM 심화

`knowledge/deep-learning/rnn-lstm-sequence-classification.md`와
`practice/deep-learning/rnn-lstm-*.ipynb`로 이미 한 차례 다뤘습니다.

- **왜 뺐나**: 순환 구조의 state·gate는 확인했고, 그 이상은 Transformer 경로에
  기여하지 않습니다. 추가 심화 목표를 만들지 않습니다.
- **무엇을 열어 주나**: 순차 처리와 병렬 처리의 대비. `P3`에서 Transformer가
  왜 학습에서 병렬화되는지 설명할 때 좋은 대조군입니다
- **복귀 조건**: 별도 학습으로 꺼내지 않고, 필요할 때 기존 노트를 대조에만 씁니다.
  state space model·Mamba 계열을 다루게 되면 그때 재검토합니다

---

## 5. Hugging Face LLM Course

- **왜 뺐나**: 라이브러리 사용법 중심이며, 지금은 직접 구현으로 배우는 구간입니다.
  먼저 배우면 추상화 뒤에 있는 것을 보지 않게 됩니다.
- **무엇을 열어 주나**: 실무 표준 도구 체인, `transformers`·`tokenizers`의 관례
- **복귀 조건**: `P4`에서 vLLM·TGI 같은 실제 서빙 구현을 읽을 때.
  자기 구현을 마친 뒤에 보면 대조 학습이 됩니다

---

## 6. CS229, MIT 6.S191, Kaggle 프로젝트

- **왜 뺐나**: CS229와 6.S191은 이미 "참고 자료"로만 지정돼 있고 별도 완강
  목표가 없습니다. Kaggle 프로젝트는 `ROADMAP.md`의 "필요할 때" 항목이며
  1순위 전문화에 기여하지 않습니다.
- **무엇을 열어 주나**: 고전 ML 이론(CS229), 전체 조망(6.S191), 실전 데이터
  파이프라인과 error analysis(Kaggle)
- **복귀 조건**: CS229·6.S191은 특정 수학 설명이 필요할 때 해당 강의만 발췌.
  Kaggle은 2순위 트랙(Evaluation)에서 failure analysis를 다룰 때 재검토

---

## 7. 2순위 전문화 — Post-training과 Evaluation

`ROADMAP.md` endpoint `TR-MOD-03`, `TR-EVAL-02`, `TR-EVAL-05`.

- **왜 뺐나**: 순서의 문제입니다. 1순위를 먼저 끝냅니다.
- **무엇을 열어 주나**: SFT, LoRA, preference optimization, 평가 설계,
  failure analysis, contamination 점검
- **복귀 조건**: `P4` 완료 후. 그 시점에 CS336 A4(Data)·A5(Alignment)와
  CS224N A4를 함께 비교해 경로를 다시 설계합니다

---

## 갱신 규칙

1. 항목을 뺄 때는 **왜 뺐나**와 **복귀 조건**을 반드시 함께 적습니다.
   조건 없는 보류는 사실상 삭제이므로 허용하지 않습니다.
2. 보류 항목을 꺼낼 때는 항목 전체가 아니라 필요한 범위만 꺼내고,
   꺼낸 범위를 이 문서에 표시하지 않습니다. 진행 상태는 `STATE.md`만 가집니다.
3. 이 문서는 완료·날짜·점수·mastery를 기록하지 않습니다.
4. 복귀 조건이 발생했는지 판단하는 근거는 학습자의 실제 구현·실행·해석이며,
   Agent의 설명이나 파일 존재가 아닙니다.
