# 임베딩 학습 (Word 2 Vec)

1. 영어 Word2Vec
2. 한국어 Word2Vec



* URI 데이터로 이벤트아이디 구성
* window_size별로 잘라서 다음 uri 예측
* Deeplog log_key 모델 training 파트
* predict 파트 (valid data에 대해서 슬라이딩 윈도우를 진행한뒤 예측 로그 도출해내는 것)



### 데이터 구조도

* 부서별 (uri_seq)
  * 이벤트 ID (uri 종류) - 시간 순 배치



### 진행 예정

* 부서별 직급별 개인별 혹은 혼합에 무엇으로 할지 분류 조건 선정
* sql 데이터로 event ID 구성
* 문장 임베딩 포함해서 진행
* parameter vector 모델 알아보기
* log anomaly 구현

