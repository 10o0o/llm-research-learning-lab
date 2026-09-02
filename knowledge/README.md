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

문서는 학습 일기가 아니라 개념 참고 자료처럼 작성합니다. `핵심 요약`과 `개념 정리`를 기본으로 두고, `개념 정리` 안을 정의·원리·수식과 Shape·다른 개념과의 차이 같은 `###` 소제목으로 필요한 만큼 나눕니다. 긴 회고형 문장보다 짧은 설명, 목록, 표, 수식과 Shape 흐름을 우선합니다. 예제·적용·주의점은 개념을 다시 이해하거나 잘못 사용하는 것을 막을 때만 추가합니다.

학습 과정에서 생긴 일시적인 질문, 다음에 실험할 내용, 자세한 코드와 출력은 각각 TIL과 `practice/`에 둡니다. 학습 증거는 무엇을 knowledge에 반영할지 판단하는 기준이지, 지식 문서 안에 증명 기록으로 반복해서 남길 내용은 아닙니다. 독립 문서로 나뉜 개념이 직접 연결될 때는 `관련 기록`에 knowledge 링크를 남깁니다.

GPT가 가르쳐준 설명 자체는 아직 내 지식으로 간주하지 않습니다. 내가 다시 설명하거나 계산·질문·실행 결과로 이해를 드러낸 뒤, 실제로 이해한 범위만 반영합니다. 하루에 새 문서가 생기지 않아도 정상이며, 같은 개념이 있다면 새 파일 대신 기존 문서를 갱신합니다.

[지식 문서 템플릿](./template.md)을 사용할 수 있습니다. 명시적으로
`$update-learning-knowledge`를 사용할 때도 현재 대화의 학습자 설명·계산이나
정확히 지정한 실행·해석 artifact만 입력으로 삼습니다. 한 번에 0~3개만
갱신하며 새 내용이 없으면 `NO_CHANGE`가 정상입니다. 관련 TIL, 실습,
원본 자료 링크는 실제로 다시 찾아볼 가치가 있을 때만 추가합니다.

```bash
python3 .agents/skills/update-learning-knowledge/scripts/validate_knowledge.py \
  knowledge/<area>/<concept>.md
```

Knowledge 수정은 commit이나 push를 자동으로 허용하지 않습니다.
