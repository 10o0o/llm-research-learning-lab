---
title: "입력과 정답의 대응"
updated: 2026-09-22
tags:
  - classification
  - train-dev-test
---

# 입력과 정답의 대응

## 핵심 요약

지도학습에서는 입력마다 그 입력에 해당하는 정답을 연결해야 한다.
정답을 얻는 규칙은 데이터의 실제 저장 방식에 맞아야 한다.

## 개념 정리

사진이 클래스별 폴더에 들어 있다면 상위 폴더 이름을 라벨로 사용할 수 있다.
fastai의 parent_label은 이 규칙을 구현한다. 모든 사진이 같은 폴더에 있다면
폴더 이름은 클래스를 구분하지 못하므로 다른 정답 출처가 필요하다.

CSV에 파일명과 라벨이 있다면 파일명을 기준으로 해당 라벨을 연결한다.
파일 목록과 CSV 행 순서가 같다고 가정하지 않는다. 라벨 누락이나 같은 파일명의
충돌이 있으면 올바른 대응을 먼저 확인해야 한다.

## 예제 또는 적용

black 폴더의 곰 사진은 폴더 규칙으로 black 라벨을 얻을 수 있다.
그러나 black·grizzly·teddy 사진을 모두 images 폴더에 모으면 같은 규칙은
모든 사진에 images를 반환한다. 이 경우 파일명별 정답 표를 조회해야 한다.

## 관련 기록

- Practice: [fast.ai 책 2장 회고](../../practice/deep-learning/fastai-book02-production.md)
- Source: [fastbook 2장, From Data to DataLoaders](https://github.com/fastai/fastbook/blob/master/02_production.ipynb)
