
import pandas as pd #pandas 라이브러리 함수들을 불러옴
import folium #folium 라이브러리 함수들을 불러옴

df=pd.read_excel("C:/Users/junhu/Workspace1/jung.xlsx") #엑셀 파일을 데이터프레임 타입으로 불러옴
df.dropna(inplace=True)#데이터프레임 값에 있는 필요없는 위치 값(행,열)을 없앰
pos=df[["이름","위도","경도"]].values #데이터프레임의 기준에 맞추어 데이터를 깔끔하게 정리함
map=folium.Map(location=[36.3319445, 127.4072666], zoom_start=20) #맵 열기
for data in pos:#반복문 시작
  folium.Marker([data[1],data[2]],tooltip=data[0],icon=folium.Icon(prefix='fa',icon='school', color = 'green')).add_to(map)
map.save("C:/Users/junhu/Workspace1/map1.html")#만든 맵 파일을 html 형식으로 저정함(저장 경로 지정)
map#만든 맵을 염

