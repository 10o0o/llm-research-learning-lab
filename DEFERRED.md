# 보류 범위와 복귀 조건

현재 승인 경로에서 선택하지 않는 범위·역할·이유·관찰 가능한 복귀 조건이다. **미완료 보류는 완료나 불필요 판정이 아니다.** 기존 도움·실행·미확인 근거는 원 실습/회고와 [이행 전 북마크 인용](./practice/reviews/curriculum-transition.md)에 보존한다. 점수·학습 날짜·완료표·진도를 두지 않는다. 판본/행사 시기는 자료 식별 정보다.

범위는 [ROADMAP](./ROADMAP.md), 선수/자료는 [CURRICULUM](./CURRICULUM.md), 판단 근거는 [옛 의무 대응](./specs/001-employment-project-curriculum/research.md#r6-옛-의무의-새-역할)과 [선택 매핑](./specs/001-employment-project-curriculum/research/decision-matrix.md)이다. 조건이 생겨도 자동으로 시작하지 않고 실제 필요/범위 변경을 확인한다. 승인 범위 안의 통상 진행·필요 개념 설명에는 중복 승인을 요구하지 않는다.

| 기존 또는 추가 후보 범위 | 새 역할 | 제외·선택 이유 | 관찰 가능한 복귀 조건 |
| --- | --- | --- | --- |
| P0~P5 고정 순서·Phase 종료 시험·전환마다 공고 3~5건 | 의무 해제 | 취업 경로의 의무 해제; 프로젝트 기능과 지원 근거부터 확인 | 실제 지원 검토 시 읽은 공고와 자기 구현을 비교; 장기 확장은 공백·목표와 사용자 결정으로 선택 |
| MML 2~5·7, MIT 18.01SC, 깊은 행렬·미분·최적화 연습 | 사용처별 최소 설명·선택 | 필요한 개념 설명은 유지; 단원 전체·장말 연습을 선행 관문에서 제외 | 현재 코드의 벡터/텐서 계약, 유사도, 손실·gradient 또는 선택 논문의 유도를 설명하지 못할 때 해당 부분 |
| MIT 18.05 핵심 확률·LLN/CLT·추론, 전체 활동·R, Stat110/OpenIntro | 평가 전 최소 설명; 전체 활동/R 보류 | 표본·누수·지표·불확실성은 관련 평가 전에 설명; 전체 과정·R·상세 Bayes 계산은 보류 | 현재 비교의 독립성·변동·추론 해석 또는 다시 선택한 공식 활동에서 요구할 때; R은 해당 활동의 실제 요구 확인 후 |
| 기존 MLP 재현, makemore Parts 3~4와 exercises, Part 5 | 기존 근거 참고; AX gate 해제 | 기존 근거·미완료 보존; 첫 프로젝트의 필수 gate 해제 | 파인튜닝/장기 모델 작업에서 학습 루프·역전파·정규화 공백이 드러나거나 사용자가 해당 활동을 재선택할 때 |
| fast.ai Lesson 1~2와 이후 전체 수강 | 기존 근거 참고; 전체 수강 의무 없음 | 과거 수행·미검증 보존; 전체 수강 의무 없음 | 현재 과업의 모델 학습·추론·실행 흐름을 다른 설명으로 보강할 실제 필요가 있을 때 |
| CS229 Summer 2020 PS1~PS3 전체 written/coding, PS3 RL·ICA | notes 선택; 전체 PS/RL/ICA 보류 | 손실·일반화 설명은 필요한 만큼 선택; 전체 PS와 RL·ICA 문제는 보류 | 선택한 모델의 목적함수/최적화 공백 또는 실제 RL·ICA 작업이 필요하고 사용자가 공식 범위를 재선택할 때 |
| ISLP 5·6·8·13 본문·전체 labs | 평가/규제 절 선택; 전체 lab 의무 해제 | 분리·평가·규제 설명은 선택 참고; 전체 지정 장·lab 의무 해제 | 현재 모델 선택·오류·불확실성에 해결되지 않는 공백이 확인될 때 해당 절·연습 검토 |
| CS231n Spring 2024 L2~6·A2 Q1~Q3 및 나머지 CV | 진단 설명 선택; 공식 과제 보류 | 학습 진단 설명은 선택 참고; 공식 과제는 취업 경로 의무에서 제외 | 실제 학습·normalization·dropout·CV 공백이 생겨 해당 공식 활동을 재선택할 때 |
| CS224N Spring 2024 1246 A3 Q1(i)·A4 Q1~Q2, 나머지 과정·RNN/LSTM 필수 연결 | attention 설명 선택; 공식 과제 보류 | attention 설명은 필요 시 사용; written·programming·RNN/LSTM 전체를 선행 gate에서 제외 | 모델 입력·attention·position 또는 sequence 모델 비교의 실제 공백과 재선택이 있을 때 |
| Karpathy GPT·BPE, Raschka 전체 구현 | 필요 설명 선택; 중복 전체 구현 제외 | 필요한 설명만 선택; 같은 LM을 여러 번 전체 구현하는 의무 없음 | 장기 LM 내부 구현에서 현재 이해로 연결하지 못하는 부분이 있을 때; 공식 A1 중 타 구현 참고 금지는 유지 |
| CS336 A1 v26.0.3, A2 v26.1.3 | A1은 RE-02 대체; A2는 선택 | A1은 RE-02 자체 LM을 대체할 공식 구현 후보, A2는 RE-03 추론/시스템 대안의 선택 활동; AX/지원 gate 해제 | LM 내부 직접 구현 또는 측정 연구를 선택하고 관련 학습/평가·tensor/loss·attention 근거가 확인될 때; 자원·정책을 다시 확인 |
| Systems/Inference 고정 1순위, SFT/eval·DPO/RLVR, 연구 cycle | 한 전문화 기본안/대안과 질문 cycle | RE-03은 post-training/evaluation 기본안과 inference 대안 중 하나, RE-04는 독립 질문 하나; 여러 전문화 병렬 의무 해제 | 실제 병목·품질 문제·읽은 논문 질문·확인한 직무 요구에 따라 하나의 방향과 필요한 선수 선택 |
| P1 Kaggle 필수 및 다른 Phase 대회 | 모든 대회 의무 해제 | 모든 대회 의무 해제; 현재 프로젝트와 별도 경쟁 트랙을 강제하지 않음 | 실제 열린 대회·권리·자원이 현재 목표의 적용 확인에 적합하고 사용자가 선택할 때 |
| Phase별 백지 구현 목록·Deep-ML·시간제한 트랙 | 대표 확인/공백 보강 선택 | API 참고 실무 구현과 구분한 대표 확인만 유지; 별도 필수 트랙 해제 | 실제 관찰된 개념/구현 공백, 계획된 대표 확인 또는 사용자 회상 요청이 있을 때 |
| 주 60시간 의도·18/27/9/6 배분·KANT/알고리즘 시간·이전 달력 | 의무 일정·시간 배분 해제 | 의무 일정·성공 기준에서 제거; 기존 표현은 과거 북마크/이력으로만 구분 | 사용자가 시간 배분을 다시 요청하면 실제 확보 시간과 직접 수행을 보고 검토; 새 추적기·고정 예측은 만들지 않음 |
| 기존 MOD/MA/PC catalog의 필수·readiness 관계 | 역사적 참고; 현재 gate 해제 | 현재 경로 선택 권한 해제; 과거 설계·자료 감사 참고로 경계를 표시해 보존 | 필요한 역량을 참조할 때만 사용; 새 AX 단위를 옛 milestone 완료로 환산하지 않음 |
| 연속 사전분포·켤레 사전분포 상세 계산 | 상세 계산 보류 | 기본 prior/posterior/MAP·손실 연결과 모든 conjugate 계산은 다른 깊이 | 선택한 과제/논문이 해당 prior·posterior 계산/유도를 요구할 때 필요한 부분 |
| MML §7.3.3 볼록 켤레 추가 유도·증명 / 전권 | 추가 유도·증명/전권 보류 | Examples 7.7~7.9·Exercises 7.9~7.11과 전권은 현재 선행 관문이 아님 | 현재 최적화/논문이 쌍대·볼록 켤레 유도 또는 특정 수학 공백을 요구할 때 |
| CS229 최종 프로젝트·공식 시험 / 2018 영상 전부 | 전체 활동 보류; 설명 구간 선택 | Summer 2020 notes와 필요한 설명만 연결; 전체 수강/시험은 별도 범위 | 현재 목적함수/일반화 공백 또는 공식 프로젝트/시험 범위를 재선택할 때 |
| CS231n A1·A3·A2 Q4/Q5·전체 CV·Final Project | 공식 CV 과제 보류 | 텍스트 AX/한 LM과 전체 CV 과제를 중복 의무화하지 않음 | 실제 CV·vision encoder·CNN/normalization 문제와 사용자 범위 선택이 있을 때 |
| CS224N 나머지 written·programming·Final Project | 공식 과제 보류; 설명 구간 선택 | Spring 2024 1246의 과거 A3 Q1(i)·A4 Q1~Q2 written도 현재 gate가 아님 | 실제 word-vector·dependency parsing·encoder·attention/position·RNN/LSTM/seq2seq 공백과 해당 활동의 재선택; 1244 혼용 금지 |
| CS336 Assignment 3·4·5 전체 | 전체 과제 보류 | 전체 scaling/data/alignment 과제를 병렬 의무화하지 않음; 평가/오염 방지는 유지 | scaling·data·SFT/RL 질문이 요구하고 선수/권리/자원·선택이 확인될 때 |
| CS336 A2 B200·2/4/6 GPU·2 GPU DDP/FSDP / Triton backward OPTIONAL | 외부 benchmark 미수행; backward OPTIONAL | 단일 장치/CPU Gloo는 GPU scaling·공식 전체 완료가 아님; PyTorch/torch.compile backward 별개 | 질문/직무가 요구하고 VRAM·시간·장치 수·공식 hardware·비용과 별도 사용 권한이 확인될 때 |
| ISLP·Stat110·OpenIntro·MIT 18.01SC 전권/전체 과정 | 전권/전체 보류; 공백별 절 선택 | 표본/분리·추론·미적분의 현재 공백만 보강 | 현재 평가/논문의 계산·가정을 다른 설명 없이는 해석하지 못할 때 해당 절 |
| GP·ICA 추가 심화·넓은 RL 과정 | 보류; 필요 개념만 선택 | 별도 전체 과정을 AX 서비스·작은 LM의 공통 선수로 추가하지 않음. CS229 PS3 Q1 RL·Q6 ICA 자체의 보류와 추가 심화의 보류는 별개 | 선택한 논문·연구 질문이 GP·ICA 또는 policy gradient·reward·RL 평가를 실제 요구하고 관련 선수·활동 범위를 확인할 때 |
| Made With ML의 별도 프로젝트·전체 수강 | 별도 필수 프로젝트 해제; 공백별 참고 | AX-01~04에서 한 서비스의 평가·재현·품질을 연결하므로 기존 과정 프로젝트를 추가 의무로 두지 않음 | 실제 데이터·모델 변경·재현·production 설계 공백에 필요한 설명이 있고 해당 원문을 확인했을 때 필요한 구간 |
| Full Stack Deep Learning·Hugging Face LLM Course·smol-course·Agents Course 전체 / Google·기업 교육 등록 | 선택 구간만 참고; 전체/등록 보류 | 선택 구간 외 전체 수강·여러 framework·인증·Hub 게시/코드랩 전부는 의무 아님 | 선택 구간으로 해결되지 않는 실제 과업/운영 공백과 정확한 원문/활동이 확인될 때 |
| MIT 6.S191 전체 lab / fast.ai 전체 | 기초 설명 선택; 전체 lab/lesson 보류 | 필요 DL/sequence 설명과 기존 근거를 쓰며 전체 CV/RL/music·lesson은 의무 아님 | 실제 모델/학습/추론 workflow 공백이 특정 활동을 요구하고 정책/환경을 확인했을 때 |
| Karpathy makemore Part 5 — WaveNet | WaveNet 보류 | convolution sequence 전체가 현재 서비스/작은 Transformer의 공통 선수는 아님 | 실제 receptive field·convolution sequence 비교 질문과 선택이 있을 때 |
| 사내비 Q&A 재구현 | 기본 문제의 대체 후보 | 같은 역량의 대체 맥락 후보이며 원 코드/배포·팀 성과는 새 독립 구현이 아님 | 사용자 선호·문제·자료 권리·새 기여/평가 가능성 확인 후 같은 계약으로 맥락을 바꿀 때 |
| TF-IDF·키워드/BM25·dense/hybrid 모든 방식 | TF-IDF는 sparse 후보; 모든 방식 의무 없음 | sparse 후보 하나 대비 dense 또는 hybrid 하나만 기본 비교; TF-IDF는 필수 아님 | 실제 검색 오류/평가가 다른 방식을 비교할 이유를 제공할 때 |
| 분류기·분류 파인튜닝 | task-specific 선택 확장 | task-specific 확장; routing/라벨 없는 모든 AX의 필수 아님; 생성 SFT와 별개 | 실제 routing 실패·라벨/split·baseline·직무 요구·자원에서 학습 비교 가설이 생길 때 |
| LangChain 전체·LangGraph 전체·ADK 전체 / MCP | 기본 LangGraph 한 개; MCP 선택 | 한 framework 기본 LangGraph로 상태/도구 책임 학습; 모든 framework/프로토콜 순회는 의무 아님 | 실제 도구 표준화·연동/직무 요구와 직접 tool contract/권한 이해가 확인될 때 |
| multi-agent·A2A·장기 메모리·독립 벡터 DB 플랫폼 | multi-agent/플랫폼 보류 | 단일 workflow/agent·작은 검색으로 확인할 결과에 불필요한 복잡도를 추가하지 않음 | 해결 못한 분해/context/통신·규모 문제와 비교 지표·실패/비용 근거가 있을 때 |
| DPO/RLVR·대규모 사전학습·kernel/분산·data engineering 전체 | 한 전문화 외 선택 심화 후보 | 한 전문화 외 모든 심화를 동시에 요구하지 않음 | 질문이 방법을 요구하고 LM·목적함수·데이터/reward·최적화/평가 선수와 자원/권한을 확인할 때 |
| ASR/TTS·실시간 streaming·새 UI/범용 인프라 전체 | 목표 직무/문제에 따른 선택 확장 | 특정 업무 요건을 텍스트 AX 전체의 공통 선행으로 일반화하지 않음 | 실제 목표 JD/사용자 문제에 음성/streaming·운영/UX 공백이 있을 때 필요한 범위 |
| 별도 월별 논문 quota·전체 과제 재구현 | quota/전체 재구현 보류; 대표 확인 선택 | 논문/과목 수·모든 코드를 다시 쓰는 반복은 현재 단위 완료 기준이 아님 | RE-04 질문의 실제 논문 또는 대표/지연 확인에서 관찰한 구성요소 공백이 있을 때 |

## 재선택의 경계

재선택은 실제 목표/공백·자료 판본/접근·권리·환경/자원과 필요한 범위를 확인하는 결정이다. 선택해제와 불가 자원은 완료가 아니다. 보류된 전체 과제를 취업 경로의 숨은 선수로 적용하거나 짧은 보강을 새 승인 gate로 만들지 않는다. 과거 ID/hash·충족도/감사·미완료를 새 자료/학습 성과로 바꾸지 않는다.

공식 과제를 다시 고르면 AI/private/별도 환경·명령 정책과 Optional·Bonus를 유지한다. CS229 Summer 2020, CS231n Spring 2024, CS224N Spring 2024 archive 1246, CS336 A1 v26.0.3·A2 v26.1.3 판본과 기존 private clone을 보존한다. 자체 LM과 공식 A1은 대체 관계이며 AX/지원 gate가 아니다. A2 학습 profiling과 serving은 다르다. 유료 GPU/외부 게시·배포는 별도 권한을 따른다. [상세 정책](./.agents/references/learning-policies.md#course-specific-scope-and-assistance)을 직접 읽는다.
