# TIL

날짜별로 당시의 학습을 돌아보기 위한 역사 기록입니다.

```text
til/YYYY/MM/YYYY-MM-DD.md
```

TIL은 수업의 gate나 자동 산출물이 아닙니다. 사용자가 현재 대화,
`til/today.md`의 draft, 또는 exact practice artifact를 지정해 저장을
요청할 때만 작성합니다.

확인 가능한 범위 안에서 다음 내용을 개념 중심으로 정리합니다.

1. 배운 개념과 핵심 정의
2. 성립 조건, 작동 원리, 한계
3. 학습자가 직접 설명하거나 적용한 예
4. 실제 실행하고 해석한 결과
5. 다시 찾을 가치가 있는 source, practice, knowledge 링크

Tutor 설명, 파일 존재, green test만으로 학습자 이해를 꾸미지 않습니다.
사용자가 실제로 남긴 불확실성은 standalone 기록의 `남은 질문`에 보존할
수 있습니다.

`til/today.md`는 ignored manual scratchpad입니다. 자동으로 읽거나 비우지
않으며, 사용할 때는 사용자가 정확히 지정합니다.

작성한 날짜별 파일은 다음 standalone validator로 확인할 수 있습니다.

```bash
python3 .agents/skills/save-today-til/scripts/validate_til.py til/YYYY/MM/YYYY-MM-DD.md
```

TIL 작성 요청은 파일 편집만 허용합니다. Commit과 push는 각각 별도 요청이
필요합니다. TIL은 당시의 기록이고, `knowledge/`는 현재의 reusable
understanding입니다.
