# Materials

강의 자료와 강의에서 제공한 실습 자료를 보관합니다.

저작권이 있거나 비공개인 자료는 `materials/private/`에 두며, 이 경로는 Git에서 제외됩니다.

현재 로컬 자료:

```text
materials/private/kant-basic-math/  # Notion 기초 수학 19강
materials/private/kant-advanced-machine-learning/  # Notion 머신러닝 심화 11강
materials/private/kant-deep-learning-basics/  # Notion 딥러닝 기초 18강
```

각 과정 폴더의 장기 보관 형식은 읽기 쉬운 Markdown입니다. Notion의 접힌 내용은 모두 펼쳐 본문에 포함하고, 필요한 그림은 가까운 `assets/` 아래에 둡니다. PDF에서 변환한 자료는 검색 가능한 텍스트와 페이지별 무손실 렌더링을 함께 보존해 수식·도표·코드 배치를 다시 확인할 수 있게 합니다. 파일 목록과 원본 링크는 같은 폴더의 로컬 `INDEX.md`에 있습니다.

강의에서 제공한 실습은 다음처럼 강의 본문과 분리합니다.

```text
materials/private/<course>/course-provided-practice/
```

이 경로의 실습은 강의 원본의 일부입니다. 학습자나 저장소 스킬이 생성하는 최상위 `practice/` 결과물과 섞지 않습니다. 각 과정 `INDEX.md`의 강의 제공 실습 표는 `Practice path`, `Related lesson path`, `Variant`, `Format`, `Original` 열로 정확한 강의 관계를 기록합니다. 파일명이나 차시 번호가 비슷하다는 이유만으로 연결하지 않습니다.

매핑을 바꿀 때는 표의 모든 경로가 실제 파일을 가리키는지, 관련 강의와
variant가 원본 기준으로 정확한지 직접 확인합니다.

## 새 강의자료 등록

1. 비공개 강의는 `materials/private/<course>/`에 둡니다.
2. 장기 보관 파일은 `NN-NN_주제.md`처럼 강의 순서가 드러나는 안정적인 이름을 사용합니다.
3. 저장한 Notion HTML은 제목·본문·모든 토글·코드 들여쓰기·출력·표·링크·수식·그림을 보존한 펼침형 Markdown으로 재구성합니다.
4. PDF는 페이지별 검색 텍스트와 무손실 렌더링을 함께 생성하고, 전체 페이지를 시각적으로 확인합니다.
5. 원본 HTML 패키지나 PDF는 변환본의 개수·본문·자산 참조·페이지 렌더링 검증이 모두 성공한 뒤에만 삭제합니다. 누락이나 불확실성이 있으면 원본을 유지합니다.
6. 과정 폴더에 `INDEX.md`가 있다면 파일명, 자료 종류, 원본 위치를 함께 갱신합니다.

이 과정이 반복해서 번거로워질 때만 등록 스킬을 추가합니다. 지금은 별도 스킬 없이 위 절차를 사용합니다.

자료를 그대로 복사해 공개 노트로 만들지 않습니다. 공부한 날의 기록은 `til/`에 남기고, 오래 가져갈 개념만 `knowledge/`에 정리합니다.
