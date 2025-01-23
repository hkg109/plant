import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import tkinter as tk
from tkinter import ttk

# 뉴스 크롤링 함수
def fetch_news():
    url = "https://news.naver.com/section/100"  # IT/과학 섹션
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 뉴스 제목과 링크 추출
    news_list = []
    for item in soup.select(".sa_text a.sa_text_title"):
        title = item.get_text(strip=True)
        link = item['href']
        if not link.startswith("http"):
            link = "https://news.naver.com" + link
        news_list.append({"title": title, "link": link})
    return news_list

# 텍스트 마이닝 및 워드클라우드 생성
def analyze_and_visualize(news_list):
    all_text = " ".join([news['title'] for news in news_list])
    words = all_text.split()
    
    # 단어 빈도 계산
    word_freq = Counter(words)
    
    # 워드클라우드 생성
    wordcloud = WordCloud(
        font_path="NanumGothic.ttf",  # 한글 폰트 경로 설정
        background_color="white",
        width=800,
        height=400,
        colormap="Greens"  # 초록색 계열 컬러맵
    ).generate_from_frequencies(word_freq)
    
    # 워드클라우드 시각화
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("뉴스 헤드라인 워드클라우드",font="NanumGothic", fontsize=20)
    plt.show()

    return word_freq.most_common(10)

# UI 업데이트 함수
def update_ui():
    news_list = fetch_news()
    if not news_list:
        print("뉴스 데이터를 가져오지 못했습니다.")
        return
    
    # 텍스트 마이닝 및 워드클라우드
    top_words = analyze_and_visualize(news_list)
    
    # 테이블 초기화
    for row in table.get_children():
        table.delete(row)
    
    # 테이블에 데이터 추가
    for news in news_list:
        table.insert("", "end", values=(news['title'], news['link']))

# 뉴스 기사 열기 함수
def open_news(event):
    selected_item = table.selection()
    if selected_item:
        item_data = table.item(selected_item)
        link = item_data['values'][1]
        import webbrowser
        webbrowser.open(link)

# GUI 생성
root = tk.Tk()
root.title("뉴스 분석")
root.geometry("900x600")
root.configure(bg="#e6ffe6")  # 초록색 배경

# 제목
title_label = tk.Label(root, text="뉴스 헤드라인 분석", bg="#e6ffe6", fg="#006400", font=("NanumGothic", 20, "bold"))
title_label.pack(pady=10)

# 버튼
fetch_button = ttk.Button(root, text="뉴스 분석 실행", command=update_ui)
fetch_button.pack(pady=10)

# 테이블
columns = ("헤드라인", "링크")
table = ttk.Treeview(root, columns=columns, show="headings")
table.heading("헤드라인", text="헤드라인")
table.heading("링크", text="링크")
table.column("헤드라인", width=600)
table.column("링크", width=250)
table.pack(fill="both", expand=True)

# 헤드라인 클릭 시 뉴스 링크 열기
table.bind("<Double-1>", open_news)

# 메인 루프 실행
root.mainloop()
