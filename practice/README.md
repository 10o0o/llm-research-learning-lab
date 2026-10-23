# Practice

학습자의 구현·실행·해석과 도움 범위를 구별해 보관합니다.

## 현재 실습

[문의 보조 Python 실습](./ai-apps/README.md)에 현재 코드의 파일 역할과 CLI가 있습니다.
실제 재개 위치·다음 독립 행동은 [STATE](../STATE.md)만 정합니다. Python 본체 하나를
기준으로 필요한 모듈을 분리하고, 탐색·시각화에는 선택적으로 notebook을 사용합니다.
다중 파일 구조는 재사용 경계가 필요할 때 늘리며 먼저 큰 패키지를 만들지 않습니다.

## 보관한 실습

- [makemore Part 3 회고](./deep-learning/makemore-part3.md): 초기화 비교·첫 backward
  관찰·저자 진단 사본·평가용 변환의 실행과 도움을 구분했다. 공식 구현과 출력이
  포함된 노트북 네 개는 비공개 영역에 바이트 그대로 보관했다.

- [MML 7장 회고](./math/mml-ch07-continuous-optimization.md): 최적화의 직접 설명과 튜터 유도, 공식 연습의 수행·보류를 구분했다. 빈 노트북은 그대로 유지했다.

- [MML 5장 회고](./math/mml-ch05-vector-calculus.md): 편미분·야코비안·자동미분·Hessian·Taylor 설명과 선택 공식 연습의 도움·미수행을 구분했다. 빈 작업 노트북은 새 보관본을 만들지 않았다.

- [MML 4장 회고](./math/mml-ch04-matrix-decompositions.md): 본문·선택 연습의 직접 설명과 계산, 튜터 계산, 보류 증명을 구분했다. 빈 작업 노트북은 새 보관본을 만들지 않았다.

- [MML 2장 회고](./math/mml-ch02-linear-algebra.md): 대화 계산·설명과 교정,
  미완료 연습을 구분했다. 빈 작업 노트북은 새 보관본을 만들지 않았다.

- [fast.ai 책 2장 회고](./deep-learning/fastai-book02-production.md): 곰 분류기 학습과
  저장·추론, 데이터 검토와 공식 복습. 위젯·공개 배포 등 미완료를 남겼다.
  책 원문이 포함된 노트북은 비공개 영역에 바이트 그대로 보존했다.

- [fast.ai Lesson 1 이미지 실습 회고](./deep-learning/fastai-lesson1-images.md) ·
  [책 1장 회고와 미완료 범위](./deep-learning/fastai-book01-intro.md):
  분류·분할 실행, 개념 복습, 중단된 IMDb와 미수행 예시를 구분했습니다.
  원문·사진이 포함된 노트북 두 개는 비공개 영역에 바이트 동일하게 보존했습니다.

- [MLP E02 초기화·수동 SGD 보관본](./deep-learning/makemore-mlp-e02-initialization-training.ipynb) ·
  [회고와 다음 학습 준비](./deep-learning/makemore-mlp-e02-initialization-training.md):
  초기 손실, backward와 갱신의 분리, 같은 배치 10회 학습. 당시 미완료였던
  E01·E03의 후속 실험은 아래 보관본에 있습니다.
- [MLP E01·E03 실험 보관본](./deep-learning/makemore-mlp-e01-e03.ipynb) ·
  [회고](./deep-learning/makemore-mlp-e01-e03.md): 학습률 비교, 논문 읽기,
  직접 연결 비교와 단일 seed의 해석 한계.
- [MLP 학습·평가 재구현 보관본](./deep-learning/makemore-mlp-training-recall.ipynb) ·
  [회고](./deep-learning/makemore-mlp-training-recall.md): 준비 코드 제공과 API 보조를
  구분한 학습자 구현, 실행 결과와 입력·정답 대응 설명.

- [micrograd 구현과 공식 exercises](./deep-learning/micrograd.ipynb):
  `Value` 자동미분, 뉴런·MLP 학습, 미분 검산, `ExerciseValue`의 softmax·로그 loss,
  PyTorch 비교를 담은 코드·출력 보관본입니다. 강의 따라 구현한 부분과 공식
  exercises의 직접 시도·피드백 수정, 보충 예제가 함께 들어 있습니다.
  관련 개념은 [knowledge 안내](../knowledge/README.md)에 연결했습니다.
- 루트의 `main.ipynb`는 다음 학습을 위한 작업 공간입니다. 과거 실습을
  확인할 때는 위 보관본을 사용합니다.
- [makemore bigram 보관본](./deep-learning/makemore-bigrams.ipynb) ·
  [챕터 회고](./deep-learning/makemore-bigrams.md): counting bigram/trigram,
  분할·smoothing, 인덱싱·cross-entropy, sampling/greedy 실험입니다.
  원본은 수정·재실행하지 않았으며, 문법 오류와 저장 출력의 한계는 회고에 명시했습니다.

## 준비·피드백·보관

현재 승인 활동의 환경·허용 시작 자료는 튜터가 [준비 책임](../.agents/references/learning-policies.md#learning-setup-and-starting-materials)에
따라 준비합니다. 위 준비 범위 외의 파일 생성·수정은 명시 요청이나 확인된 챕터
마무리의 권한을 따릅니다. 기본 대상 구현·실행·첫 해석은 학습자 몫이며, 자체 프로젝트의
현재 명시적 위임은 [소유권 정책](../.agents/references/learning-policies.md#learner-ownership-and-evidence)에
따라 보조 수행으로 구분합니다. 피드백은 실제 파일·저장 출력·첫 해석을 함께 봅니다.
노트북은 `scripts/nbpeek.py`로 관련 셀만 읽고, 보관본을 재실행하거나 과거 오류를 지우지 않습니다.

확인된 실제 챕터 전환의 보관·회고·초안 기반 knowledge·검증 후 초기화·로컬 커밋은
[finish-chapter](../.agents/skills/finish-chapter/SKILL.md)의 절차를 따릅니다.
`$finish-chapter` / `이번 챕터 정리해줘`로도 호출합니다. AX/RE 단위 완료나 일반 `완료`는
챕터 마무리·기록·초기화·Git 권한이 아닙니다. 기록 권한은 [기록 정책](../.agents/references/recordkeeping-policies.md)에 있습니다.

## 위치와 공개 범위

자체 코드의 현재 위치는 `practice/ai-apps/`입니다. 별도 서비스 repo로 계속 발전시킬 때는
[ROADMAP](../ROADMAP.md#초기-개발-공간과-서비스의-지속-발전)의 환경·권리·원본 보존·기여 경계를
확인합니다. 예전 후보 경로는 새 작업 공간을 자동 생성하는 지시가 아닙니다.
[이행 전 북마크 인용](./reviews/curriculum-transition.md)도 현재 재개를 선택하지 않습니다.

KANT 제공 원본은 `materials/private/<course>/course-provided-practice/`, 개인 작업 사본과
결과는 `practice/private/kant-live-labs/<프로젝트>/`로 구분해 공개 Git에서 제외합니다.
원자료와 강사 완성본은 학습자의 새 독립 구현이 아닙니다.

MIT 18.05 문제 세트 답안과 CS229·CS231n·CS224N·CS336 공식 과제 답안은
written·코드·노트북·저장 출력 모두 별도 비공개 작업 공간에 둡니다. 공식 원문·답안·
저작권 자료·개인/고객 정보·비밀정보·큰 데이터/가중치는 공개 Git에 자동 추가하지 않습니다.

## 공식 실습을 재선택할 때

현재 승인 범위는 [ROADMAP](../ROADMAP.md), 선수·자료는 [CURRICULUM](../CURRICULUM.md),
보류 이유는 [DEFERRED](../DEFERRED.md), 판본·도움·명령·환경·비공개 제한은
[공식 과제 정책](../.agents/references/official-course-policies.md)을 따릅니다.
실제 원문·starter·exercises/assignments 요구를 확인하고 Optional·Bonus는 선택,
미실행 요구는 미완료로 남깁니다. 완성 노트북 실행·AI 예제·KANT 자료가 선택한 공식
실습을 대신하지 않습니다. 대화 설명을 영상 시청으로, 로컬 검사를 대학 공식 채점으로
표현하지 않습니다. 기존 metadata·저장 출력·도움 이력은 당시 산출물로 보존합니다.
API 문서 참고 실무 구현과 무보조 회상·지연 전이는 별도 근거입니다.
