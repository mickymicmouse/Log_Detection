# DataFrame 메소드

* value_counts()
  * unique한 값들의 개수 반환
* unique()
  * 중복 없이 도메인 값 반환
* describe()
  * 요약 정리

```shell
count      860736
unique         82
top       UNKNOWN
freq       500872
Name: dept_name, dtype: object
```

* info()
  * 각 컬럼별 타입과 null 여부, 개수 반환

```shell
RangeIndex: 860736 entries, 0 to 860735
Data columns (total 53 columns):
 #   Column                 Non-Null Count   Dtype  
---  ------                 --------------   -----  
 0   Unnamed: 0             860736 non-null  int64 
```

* columns
  * 데이터프레임의 컬럼을 리스트 형식으로 반환
* `list(set(col)-set(remove_col))`
  * 데이터 프레임 컬럼에서 삭제하고 싶은 컬럼 제거 (차집합 효과)
* sort_values(by=[컬럼명], axis = 0, ascending = False)
  * 데이터 프레임 정렬
  * axis = 0 -> 열을 기준으로
  * ascending=False -> 내림차순

