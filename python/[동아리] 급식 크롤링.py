from sqlalchemy import text
import requests
from bs4 import BeautifulSoup
import pandas as pd

def daysmenu(year, month, day):
    url = f"http://www.daeseong.hs.kr/?act=lunch.main2&month={year}.{month:02d}.{day:02d}&code=1217"
    html = requests.get(url)

    parsed = BeautifulSoup(html.content, "html.parser")
    menu_names_div = parsed.select('div.menuName')
    menu_names_span = parsed.select('span')

    num = 1
    menus_breakfast = []
    menus_lunch = []
    menus_dinner = []

    for menu_name in menu_names_div + menu_names_span:
        if menu_name.get_text() == "본문내용 바로가기":
            break

        x = menu_name.get_text().splitlines()
        x.remove('')
        x.remove('')

        if num == 1:
            menus_breakfast.extend(x)
        elif num == 2:
            menus_lunch.extend(x)
        elif num == 3:
            menus_dinner.extend(x)

        num += 1

    data_dict ={
         '조식': menus_breakfast,
         '중식': menus_lunch,
         '석식': menus_dinner
     }

    return data_dict


def daymenu(year, month):
    data_dict = {}

    for day in range(1, 32):  # 월의 최대 일수에 맞춰 범위 설정 (일부 달은 31일까지 없으므로 예외 처리 필요)
        url = f"http://www.daeseong.hs.kr/?act=lunch.main2&month={year}.{month:02d}.{day:02d}&code=1217"
        html = requests.get(url)
        parsed = BeautifulSoup(html.content, "html.parser")

        menu_names_div = parsed.select('div.menuName')
        menu_names_span = parsed.select('span')
        num = 1
        menus_breakfast = []
        menus_lunch = []
        menus_dinner = []
        for menu_name in menu_names_div + menu_names_span:
            if menu_name.get_text() == "본문내용 바로가기":
                break
            x = menu_name.get_text().splitlines()
            x.remove('')
            x.remove('')
            if num == 1:
                menus_breakfast.extend(x)
            elif num == 2:
                menus_lunch.extend(x)
            elif num == 3:
                menus_dinner.extend(x)
            num += 1
        max_length = max(len(menus_breakfast), len(menus_lunch), len(menus_dinner))
         # 데이터 딕셔너리에 해당 날짜의 식단 정보 추가
        date_str = f"{year}-{month:02d}-{day:02d}"
        data_dict[date_str] ={
             '조식': menus_breakfast,
             '중식': menus_lunch,
             '석식': menus_dinner
         }

    df = pd.DataFrame(data_dict)
    df.to_excel(f'menu_{year}_{month}.xlsx', index=False)

    return data_dict

while True:
 choice= input("특정 날짜의 식단을 확인하시겠습니까? (y/n): ")
 if choice.lower() == 'y':
   # 사용자로부터 년, 월, 일을 입력받습니다.
  year_choice= int(input("년도를 입력하세요: "))
  month_choice= int(input("월을 입력하세요: "))
  day_choice= int(input("일을 입력하세요: "))
  a = daysmenu(year_choice,month_choice,day_choice)
  print('조식' + str(a.get('조식')))
  print('중식' + str(a.get('중식')))
  print('석식' + str(a.get('석식')))
 elif choice.lower() == 'n':
  choice2 = input("월별 식단 파일을 다운 받으시겠습니까? (y/n)")
  if choice2.lower() == 'y':
   year_input= int(input("연도를 입력하세요: "))
   month_input= int(input("월을 입력하세요: "))
   data_dict_result= daymenu(year_input, month_input)
   print(f"{year_input}년 {month_input}월 식단 정보:")
   print(data_dict_result)
  elif choice2.lower() == 'n':
   print("프로그램이 종료되었습니다.")
