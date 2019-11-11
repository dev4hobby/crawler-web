# Web Crawler

## `Naver`

```python3
>> from crawler import Naver
>> naver = Naver()
```

### 카페 글 리스트

```python3
>> naver.get_cafe_post('중고나라','맥북 프로 2016')
```

### 실시간 검색어

```python3
>> naver.get_trends(rank=10, age=20) # default rank: 20
```

### 실시간 날씨

```python3
>> naver.get_weather('인계동', raw_option=False)
현재 경기도 수원시 팔달구 인계동의 기온은 13도 입니다. 
[ 흐림, 어제보다 7˚ 높아요 ]

>> naver.get_weather('인계동')
['경기도 수원시 팔달구 인계동', '13', '흐림, 어제보다 7˚ 높아요']
```


## `Google`

### 검색된 이미지 데이터

```python3
>> from crawler import Google
>> google = Google()
>> google.get_images('kitten','2')
```

---

- 2019_11_11_`dev : in progress`
- 지역별 미세먼지, 날씨 등 생활 정보 기능 구현중