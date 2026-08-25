# Practice

TIL에서 배운 내용을 직접 회상하고 구현하며, 실제 테스트 실패와 상태
변화를 해석한 증거를 둡니다.

## 산출물 형태

기초 수학, 작은 deterministic NumPy 계산, 독립적인 Tensor·Shape 확인처럼
재사용 모듈 경계가 학습 대상이 아닌 실습은 단일 Notebook을 사용합니다.

```text
practice/<area>/<topic>.ipynb
```

Notebook 안에서는 설명, 구현, 고정 fixture, 공개 검사, 결과 해석을
가까이 둡니다. 작은 학습·validation·checkpoint 흐름도 한 Notebook 안에서
완결합니다. 재사용 가능한 여러 모듈과 CI가 학습 대상인 별도 프로젝트를
사용자가 명시적으로 요청했을 때만 다중 파일 구조를 만듭니다.

Notebook은 자연스러운 목적과 요구사항, 작은 예, 단계별 힌트, 테스트
실행과 결과 해석을 안내합니다. 강의에서 배운 핵심 연산·판단만 TODO로
남기고 함수 시그니처, 반복 검증, 반환 조립, fixture와 bookkeeping은
기본으로 제공합니다. 따라서 제공된 helper와 scaffold는 완성 코드여도
되며 모든 함수를 통째로 `NotImplementedError`로 만들지 않습니다.

## 생성 원칙

`$suggest-learning-practice`에는 검토·저장을 마친 날짜별 TIL 경로를
정확히 전달합니다. `til/today.md`나 자동으로 고른 최신 TIL은 입력이
아닙니다. 실습은 TIL의 공백만 고치는 것이 아니라 주요 학습 성과 전체를
다음 action으로 바꿉니다.

- `implement`: 핵심 메커니즘 직접 구현
- `test`: 정상·경계·실패 계약 확인
- `debug`: 의도적으로 깨진 경계나 흐름 진단
- `interpret`: Shape, gradient, metric, output의 의미 설명
- `design`: API, 데이터 계약, 모델 출력이나 실험 조건 설계

설명을 잘했어도 직접 구현한 증거가 없으면 작은 `Core` 실습부터
시작합니다. `Applied`는 작은 현실 조건 하나를, `Advanced`는 기반 구현이
확인됐을 때만 ablation·민감도·실패 분석 같은 연구 질문 하나를 더합니다.

각 exercise는 하나의 주 개념과 최대 세 개의 학습자 작업만 다루며 다음
순서를 유지합니다.

```text
자연스러운 목적과 문제
→ 준비된 뼈대와 직접 완성할 부분
→ 모든 공개 검사 조건과 작은 예
→ 강의 핵심 연산·판단 구현
→ 바로 옆의 접힌 힌트
→ 공개 검사와 실패 진단
→ 결과의 의미와 한계 해석
```

힌트를 파일 아래쪽에 몰아두지 않습니다. 각 TODO 바로 앞에 `힌트 1`과
`힌트 2`를 접어 둡니다. 처음에는 `guided`, 익숙해지면 `partial`, 충분한
증거가 있는 뒤에는 `independent`로 비계를 줄이되 문제의 필수 조건은
끝까지 모두 공개합니다. 반드시 작성해야 하는 해석은 학습자 target으로
추적하고, 추적하지 않는 복습 메모는 선택 사항이며 완료 조건이 아니라고
밝힙니다.

## 강의 제공 실습

강의 제공 원본은 `materials/private/<course>/course-provided-practice/`에
남습니다. 각 과정 `INDEX.md`의 다음 열이 강의와 실습을 정확히 연결합니다.

```text
Practice path | Related lesson path | Variant | Format | Original
```

TIL에 링크된 정확한 강의와 일치하는 행만 자동으로 참고합니다. 원본은
learner evidence가 아닙니다. 기본·심화 자료의 starter, TODO, fixture,
check 경계를 먼저 감사하고 적절한 starter를 우선 보존합니다. 정답은
명세 확인과 임시 reference 실행에만 사용하며 답이나 가짜 출력을
Notebook에 복사하지 않습니다.

## 실행과 피드백

단일 Notebook은 setup을 한 번 실행한 뒤 현재 E번호의 구현 셀, fixture 셀,
`check_e01()` 형식의 검사 셀 순서로 실행합니다. 함수 수정 뒤에는 현재
구현 셀부터 다시 실행하면 됩니다.

미완성 핵심 지점에서만 `NotImplementedError`나 명시적 placeholder 실패가
정상입니다. 제공된 scaffold는 그대로 실행 가능해야 합니다. 막혔을 때
`$suggest-learning-practice`에 정확한 Notebook 경로를 주면 저장된 code와
실제 traceback을 기준으로 한 번에
가장 작은 blocker부터 안내합니다. 테스트 통과 뒤에도 결정적인 상태나
출력을 직접 설명해야 완료 증거가 됩니다.

[실습 Notebook 템플릿](./template.ipynb)은 위 구조의 Notebook 기준입니다.
실행하지 않은 결과를 기록하지 않고, 데이터셋·모델 가중치·API 키와 큰
출력 파일은 Git에 올리지 않습니다.
