# 레퍼런스 교육과정 비교와 사용할 범위

**조회일: 2026-10-19.** 공식 과정 소개·선수·목차·실습 유형을 비교했다. 전체 강의 시청·문항 검토·스타터 확보·실행·수료를 확인한 것은 아니다. 실제 수업 전에는 사용할 정확한 절·영상·활동과 도움 정책을 확인한다. 아래 10개는 비교 대상이며 열 개의 필수 수강 트랙이 아니다.

## 비교한 공식 교육과정

| ID·공식 출처·판본 | 확인한 선수와 실습/프로젝트 | 접근·제약·이번 선택 |
| --- | --- | --- |
| REF-01 · [MIT 6.S191 — Introduction to Deep Learning, 2026](https://introtodeeplearning.com/) | 기본 행렬 연산·미분/chain rule, Python은 도움. L1 DL·L2 sequence, 비전·생성·RL·LLM, Python/music·얼굴 탐지·LLM fine-tuning labs와 프로젝트 제안 | 현재 공식 메인 본문에서 2026 일정·목차 확인. 공개 무료 자료. `/2026/` archive URL은 접근 실패해 검증 경로로 쓰지 않음. RE-01에 L1 및 필요한 sequence 설명을 선택; CV/RL/music 전체 lab은 제외 |
| REF-02 · [Stanford CS336 — Language Modeling from Scratch, Spring 2026](https://cs336.stanford.edu/) | Python·PyTorch·DL·systems·선형대수·확률 선수. tokenizer/LM, profiling/분산, scaling, data, SFT/RL 과제로 구성. 구현량이 큼 | 공개 syllabus·AI/기존 코드 정책 확인. 강의 L1~3·12~15를 RE-02~04의 모델/데이터/평가 참고로 선택; L10은 추론 대안. 모든 A1~A5 이수는 요구하지 않음. 공식 과제 선택 시 기존 private 공간·pin·AI/명령 제한 유지 |
| REF-03 · [Full Stack Deep Learning — LLM Bootcamp, April 2023](https://fullstackdeeplearning.com/llm-bootcamp/) | Python 경험, ML 또는 backend/frontend 경험이 도움. 앱 출시·LLM foundations·prompting·augmented LMs·UX·LLMOps와 walkthrough. 연속 필수 과제 평가는 소개에서 확인되지 않음 | 무료 녹화. 사이트 자체가 도구 변화 경고. AX-01·02·04에서 제품 흐름·UX·운영 원리만 선택; 옛 API/모델을 현재 기준으로 쓰거나 walkthrough 실행을 직접 구현으로 세지 않음 |
| REF-04 · [Hugging Face — LLM Course, 상시 개정판](https://huggingface.co/learn/llm-course/en/chapter1/1) | Python, 입문 DL 권장. PyTorch 선행 지식 자체는 필수 아님. Transformers·fine-tuning·datasets·tokenizers·data curation·LLM 학습 등의 실습 | 공개 무료. RE-01은 Ch2~3·5, RE-02는 필요한 Ch1·6, RE-03은 Ch10~11을 선택 참고. Hub 게시·인증·12장 전체 이수는 요구하지 않음 |
| REF-05 · [Hugging Face — smol-course, 상시 개정판](https://huggingface.co/learn/smol-course/unit0/1) · [Chat Templates](https://huggingface.co/learn/smol-course/unit1/2) | Python·ML·PyTorch·Transformer 기반 권장. instruction tuning/SFT·평가·DPO·VLM, 실습과 프로젝트. 개별 주제는 독립 선수 확인 필요 | 공개 읽기와 모델 실행 자원/계정은 구별. 목차와 sidebar의 번호가 달라 **주제명** 기준 참조. RE-03 기본은 chat template·SFT/PEFT·domain evaluation; DPO/RL/VLM 전체는 보류. 실행 전에 모델·VRAM·플랜/비용 확인 |
| REF-06 · [Hugging Face — AI Agents Course, 상시 개정판](https://huggingface.co/learn/agents-course/en/unit0/introduction) · [Unit 2.3 LangGraph](https://huggingface.co/learn/agents-course/en/unit2/langgraph/introduction) | 기본 Python·LLM. Unit1 도구/행동/관찰·메시지, Unit2 프레임워크, RAG use case, benchmark final과 관측/평가 bonus. 사전 구성 Spaces와 실습 | 공개 무료 읽기. AX-01·03의 주 참고로 Unit1과 프레임워크 **하나**(기본안 LangGraph) 선택. 예제는 강한 외부 API 모델 접근을 요구하므로 그대로 실행하지 않음. 전체 framework·인증·leaderboard·Hub 게시 의무 없음 |
| REF-07 · [Google — 5-Day AI Agents Intensive, 2025 안내](https://blog.google/innovation-and-ai/technology/developers-tools/ai-agents-intensive/) · [2025-12-18 회고](https://blog.google/innovation-and-ai/technology/developers-tools/ai-agents-intensive-recap/) | 공식 안내/회고가 architecture·tools·memory·evaluation·production, whitepaper·codelab·capstone을 명시 | 2025 행사 종료 후 자습 가이드로 전환. [Kaggle guide](https://www.kaggle.com/learn-guide/5-day-agents)는 root 브라우저에서 0줄로 반환되어 세부 코드랩 원문 검토로 세지 않음. AX coverage 비교용; ADK/계정/API/2026 별도 행사를 필수로 합치지 않음 |
| REF-08 · [NAVER 커넥트재단 — Boostcamp AI Tech 8기, 2025–26](https://boostcamp.connect.or.kr/program_ai.html) · [모집 안내](https://boostcamp.connect.or.kr/guide_ai.html) | Python/수학·ML pre-course, 공통 AI Core 9주, CV/NLP/추천 중 하나의 AI Production 12주. 모델·serving·최적화·MLOps 프로젝트 | 2025-09-01~2026-02-11 기수로 현재 종료된 사례. 전일제·선발 과정. 핵심 기반→한 도메인→production을 연결하는 구성 참고; 그 시간표·선발 과목·GPU 지원을 개인 경로에 복제하거나 다음 기수 모집을 주장하지 않음 |
| REF-09 · [LG — Aimers 9기 과정·해커톤 설명](https://www.lg.co.kr/media/release/30586) | 공식 2026-09-21 보도자료의 과정 표: tabular ML·수학·지도학습·최적화/시계열·LLM 적용/평가. 산업 실데이터 예측 과제와 코드·성능·구두 발표 | 소개·목차와 실제 문제 연결을 확인했으며 강의 원문을 검토한 것은 아님. AX의 현장 문제/평가와 RE-01의 실험 설명 참고; 전 강의·경진대회 참가·특정 스포츠 예측을 의무화하지 않음 |
| REF-10 · [KT — AIVLE School 교육 소개](https://aivle.kt.co.kr/home/main/introMain?mcd=HM01001000) · [10기 지원 안내](https://aivle.kt.co.kr/home/main/applyMain?mcd=MC00000051) | 기업 문제 발굴→해결의 실무/프로젝트형 소개. 학력·연령·미취업 등 지원 자격 안내. [2024 공식 보고서](https://corp.kt.com/archive/ipgrpt/attach/now/FACTBOOK.pdf)는 과거 6개월/840h 구성 설명 | 현 기수의 세부 모듈·비용은 공개 내용만으로 확정 불가. 과거 보고서 수치를 2026년 현행 시간/비용으로 쓰지 않음. 비교 참고만, 신청·비용·단기 보조 강좌 대체를 권하지 않음 |

## 채택할 학습 구성

| 경로 | 기준 자료와 사용할 구간 | 선택하지 않는 범위 |
| --- | --- | --- |
| AX: 한 업무 서비스를 점진적으로 구현 | REF-06의 기초·도구·한 framework, REF-03의 앱 흐름·augmented LM·UX/LLMOps. 2026 공식 아키텍처/평가 자료로 기술 가정 보정 | HF 여러 framework 전체, Google codelab 전부, 2023 API 복사, 인증/학원 등록을 완료 조건으로 삼지 않음 |
| RE-01: 학습·검증을 해석하는 모델 실험 | REF-01의 DL 기초와 REF-04의 학습·데이터 관련 절; 기존 학습자의 MLP 근거와 대조해 공백만 보강 | 입문 DL·수학 전체를 AX 전에 이수, CV/RL 실습 전부, 같은 MLP 강의 전체 반복 |
| RE-02: 작은 LM 하나의 내부 구현 | REF-02의 tokenization·PyTorch/resource·architecture·data/eval 강의 범위. 기본은 자체 프로젝트 하나, 공식 A1을 고르면 같은 구현을 대체 | 자체 LM 전체 구현 후 A1 전체를 또 요구, A1 선택 없이 공식 완료 주장, 다른 과제 전부를 숨은 선수로 복원 |
| RE-03: post-training/evaluation 기본안 또는 inference 대안 | 기본 REF-05의 chat template·SFT/PEFT·평가와 REF-04 관련 절; 대안 REF-02의 inference/systems 설명 | DPO·RLVR·VLM·kernel·분산 벤치마크를 모두 병렬 의무화 |
| RE-04: 질문 하나의 독립 실험·재현 | REF-02의 데이터/평가·후속학습 범위를 바탕으로 RE-03에서 생긴 질문 하나를 고름. 논문은 실제 읽고 나서 해당 주장·실험을 제한 | 논문 quota, 읽지 않은 논문 요약·결과, 자원 없는 대규모 수치 재현, 새로운 성능 향상/독창성 보장 |

## 자료 선택의 한계

이 설계는 어느 한 학교의 공인 학위나 기업의 수료 자격을 대체하지 않는다. 과정 소개가 말하는 폭넓은 역량과 실제 개별 실습을 끝낸 증거를 구분한다. Google guide·MIT archive처럼 열리지 않은 경로는 접근 제한을 기록했으며 제목만으로 강의 내용을 가르치지 않는다. 자료를 선택했다고 다운로드·계정 등록·환경 설치·모델 실행·게시가 승인되는 것도 아니다.
