# Knowledge

지금 내가 알고 있고 설명할 수 있는 내용을 개념별로 모아두는 지식 베이스입니다.

```text
knowledge/<area>/<concept>.md
```

예:

```text
knowledge/math/vector.md
knowledge/math/numpy-axis-broadcasting.md
knowledge/ml/data-split.md
knowledge/deep-learning/backpropagation.md
knowledge/llm/attention.md
knowledge/systems/kv-cache.md
```

파일명에는 날짜를 넣지 않습니다. 새롭게 이해하거나 잘못 알고 있던 점을 발견하면 같은 문서를 고쳐서 **현재의 가장 좋은 이해**만 남깁니다.

모든 TIL을 옮길 필요는 없습니다. 다시 사용할 개념이나 다른 학습의 기반이 되는 내용만 정리합니다. 한 문서에는 독립적으로 다시 찾거나 보충할 가치가 있는 개념 하나를 담습니다. 같은 날 배웠더라도 벡터 정규화와 NumPy broadcasting처럼 서로 따로 재사용할 개념은 문서를 나누고, 하나의 정의·수식·예제는 불필요하게 여러 파일로 쪼개지 않습니다.

문서는 학습 일기가 아니라 개념 참고 자료처럼 작성합니다. `핵심 요약`과 `개념 정리`를 기본으로 두고, `개념 정리` 안을 정의·원리·수식과 Shape·다른 개념과의 차이 같은 `###` 소제목으로 필요한 만큼 나눕니다. 핵심 요약은 정의, 목적과 핵심 성립 조건을 짧게 제시하고, 자세한 근거와 절차는 본문에 둡니다. 문서나 요약의 길이에 임의의 상한을 두지 않습니다. 예제·적용·주의점은 개념을 독립적으로 복원하거나 오용을 막는 데 필요할 때 추가합니다.

학습 과정에서 생긴 일시적인 질문, 다음에 실험할 내용, 자세한 코드와 출력은 각각 TIL과 `practice/`에 둡니다. 학습 증거는 반영 범위를 정하는 근거로 사용하되, 실행했다거나 검사를 통과했다는 회고만 개념 예제에 반복하지 않습니다. 예제에는 문서만 읽어도 이해할 수 있도록 필요한 입력, 조건, 계산 결과와 해석을 함께 둡니다. 관련 수치, 입력, 한계와 실습 링크는 개념을 복원하는 데 필요하면 보존합니다. 문법 검사나 녹색 테스트는 문서 형식과 실행 상태를 확인할 뿐, 설명의 의미가 정확하거나 학습자가 개념을 이해했다는 증거가 아닙니다. 독립 문서로 나뉜 개념이 직접 연결될 때는 `관련 기록`에 knowledge 링크를 남깁니다.

GPT가 가르쳐준 설명 자체는 아직 내 지식으로 간주하지 않습니다. 내가 다시 설명하거나 계산·질문·실행 결과로 이해를 드러낸 뒤, 실제로 이해한 범위만 반영합니다. 근거에서 참고 문장 하나만 고치는 데 그치지 않고 관련 문서 전체를 읽어 용어, 요약, 예제, 주의점과 링크가 서로 맞는지 확인합니다. 하루에 새 문서가 생기지 않아도 정상이며, 같은 개념이 있다면 새 파일 대신 기존 문서를 갱신합니다. 기존 tag를 우선 재사용하며 tag 수에 임의의 제한을 두지 않습니다.

비공개 원본의 내부 경로는 knowledge의 링크나 본문에 넣지 않습니다. 저자·자료명·판본·장·절·강의명처럼 다시 식별하는 데 필요한 정보를 일반 텍스트 참고문헌으로 남깁니다. 공개된 공식 URL이 있으면 함께 링크할 수 있습니다. 원본의 비공개 여부와 공개 링크의 유무는 지식 내용의 검증 여부를 대신하지 않습니다.

[지식 문서 템플릿](./template.md)을 사용할 수 있습니다. 명시적으로
`$update-learning-knowledge`를 사용할 때도 현재 대화의 학습자 설명·계산이나
정확히 지정한 실행·해석 artifact만 입력으로 삼습니다. 단독 스킬에서는 한 번에
0~3개만 갱신하며 새 내용이 없으면 `NO_CHANGE`가 정상입니다. 관련 TIL,
실습과 출처는 실제로 다시 찾아볼 가치가 있을 때만 추가합니다.

```bash
python3 .agents/skills/update-learning-knowledge/scripts/validate_knowledge.py \
  knowledge/<area>/<concept>.md
```

단독 knowledge 수정 요청은 commit이나 push를 자동으로 허용하지 않습니다.
[`$finish-chapter`](../.agents/skills/finish-chapter/SKILL.md)는 명시적으로
챕터 보관·회고·지식 갱신과 로컬 커밋까지 묶은 요청입니다. 이 경우에는 3개
제한 없이 해당 챕터의 확인된 개념을 검토하지만, 새 내용이 없는 문서를
억지로 만들지 않습니다. STATE는 전체 교체안 승인 후 반영하며 push는 하지 않습니다.

## Micrograd에서 연결한 개념

MLP에서 다시 연결한 초기화·수동 SGD는
[E02 회고](../practice/deep-learning/makemore-mlp-e02-initialization-training.md)와
[보관본](../practice/deep-learning/makemore-mlp-e02-initialization-training.ipynb)에 있습니다.
[MLP 초기화와 경사하강](./deep-learning/mlp-and-gradient-descent.md),
[backward와 실제 갱신](./deep-learning/multiclass-training-loop.md)을 함께 참고합니다.

다시 읽을 때는 아래 순서로 연결할 수 있습니다. 구현과 실행 출력은
[micrograd 실습 보관본](../practice/deep-learning/micrograd.ipynb)에 있습니다.

| 개념 | 다시 확인할 내용 |
|---|---|
| [도함수와 수치 미분](./math/derivatives-and-finite-differences.md) | 부호·크기, 편미분, 미분 규칙, 전진·중앙 차분 |
| [계산 그래프와 역전파](./deep-learning/computational-graph-autograd.md) | Value, 클로저, 위상 순서, 누적, 객체와 숫자 구분 |
| [MLP 구성과 경사하강 학습](./deep-learning/mlp-and-gradient-descent.md) | 뉴런·층·파라미터 수, loss, 초기화·역전파·업데이트 |
| [Softmax와 음의 로그우도 손실](./deep-learning/softmax-negative-log-likelihood.md) | 정답 확률, 연산 구현, PyTorch 비교 |

배치 학습·검증으로 연결할 때는 기존
[다중분류 학습 반복과 autograd](./deep-learning/multiclass-training-loop.md)를 참고합니다.

## Makemore bigram에서 연결한 개념

[챕터 회고](../practice/deep-learning/makemore-bigrams.md)에서 질문·수정·
도움·실험 한계를, [실습 보관본](../practice/deep-learning/makemore-bigrams.ipynb)에서
당시 코드와 출력을 확인할 수 있습니다.

| 개념 | 다시 확인할 내용 |
|---|---|
| [문자 n-gram 언어 모델](./llm/character-ngram-models.md) | 현재/다음 문자 ID, 빈도표, 문맥별 확률 |
| [데이터 분할과 평활화 계수 선택](./ml/data-split-and-smoothing.md) | 이름 단위 분할, train 집계, dev 선택, test 한계 |
| [행렬곱과 one-hot 행 선택](./math/matrix-multiplication-linear-layer.md) | ID 목록으로 여러 가중치 행 가져오기 |
| [Softmax와 NLL](./deep-learning/softmax-negative-log-likelihood.md) | 정답 확률, 배치 인덱싱, 안정적인 cross-entropy |
| [샘플링과 탐욕적 생성](./llm/sampling-and-greedy.md) | 확률 추출과 최대 선택, seed, 이름별 초기화 |
