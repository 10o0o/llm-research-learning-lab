---
title: "학습한 모델의 저장과 추론"
updated: 2026-09-22
tags:
  - neural-network
  - inference
---

# 학습한 모델의 저장과 추론

## 핵심 요약

학습한 모델을 다시 사용하려면 모델 구조와 학습된 파라미터를 보존해야 한다.
추론은 해당 가중치로 예측하며 가중치를 갱신하지 않는다.

## 개념 정리

모델 구조만 있으면 학습으로 얻은 값이 사라지고, 파라미터만 있으면 그 값을
어떤 구조에 적용해야 하는지 별도로 알아야 한다. fastai의 export는 구조와
가중치에 더해 추론에 필요한 데이터 처리 설정을 보존한다.

학습용 무작위 증강은 일반적인 추론에 그대로 적용하지 않는다.
다만 크기 조절·정규화처럼 입력을 모델에 맞추는 전처리와 출력 인덱스의
클래스 대응은 필요하다. 증강 생략은 모든 전처리를 생략한다는 뜻이 아니다.

## 주의점

저장 파일이 존재하는 것과 새 환경에서 불러오기·예측이 성공하는 것은 다르다.
필요한 라이브러리와 사용자 정의 함수 등의 호환성은 별도로 확인한다.
여기서 말하는 export는 추론용 보존이며 학습 재개 상태 전체의 보장을 뜻하지 않는다.

## 관련 기록

- Practice: [fast.ai 책 2장 회고](../../practice/deep-learning/fastai-book02-production.md)
- Source: [fastbook 2장, Using the Model for Inference](https://github.com/fastai/fastbook/blob/master/02_production.ipynb)
