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


## `PPOMPPU`

### 해외직구 게시판 첫글 확인

```python
>> from crawler import PPU
>> ppu = PPU()
>> # 추후 단일 키워드가 아닌 리스트형태로 체크할 수 있게 패치예정
>> ppu.get_forum_oversea_title('할인')
```
