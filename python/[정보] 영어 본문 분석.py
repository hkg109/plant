import pandas as pd
from wordcloud import WordCloud
from matplotlib import font_manager, rc
from collections import Counter
import tkinter as tk
from tkinter import messagebox, ttk
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import os
import re

# 다운로드: nltk 데이터 (처음 실행 시 필요)
nltk.download('punkt')
nltk.download('stopwords')

# 한글 폰트 설정
font_paths = [
    "C:/Windows/Fonts/NanumGothic.ttf",  # Windows 기본 경로
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"  # Linux 기본 경로
]
font_path = next((path for path in font_paths if os.path.exists(path)), None)
if font_path:
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)
else:
    font_name = 'Arial'
    print("한글 폰트를 찾을 수 없어 기본 폰트를 사용합니다.")
    rc('font', family=font_name)

# 데이터 전처리 함수
def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # 영어 문자와 공백만 남기기 (., 같은 특수 문자 제거)
    words = word_tokenize(text.lower())  # 소문자 변환 및 토큰화
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
    return filtered_words

# 문장 길이 분석
def sentence_lengths(text):
    sentences = sent_tokenize(text)
    lengths = [len(word_tokenize(re.sub(r'[^a-zA-Z\s]', '', sentence))) for sentence in sentences]
    return sentences, lengths

# 단어 빈도 분석
def word_frequency(words):
    word_counts = Counter(words)
    return word_counts

# WordCloud 생성 함수
def generate_wordcloud(words):
    wordcloud = WordCloud(font_path=font_path, background_color='white', width=500, height=500).generate(' '.join(words))
    return wordcloud

# tkinter UI
root = tk.Tk()
root.title("텍스트 분석 도구")
root.geometry("900x600")
root.configure(bg="#4A90E2")

# 분석 결과 표시
results_frame = tk.Frame(root, bg="#FFFFFF", relief=tk.RAISED, borderwidth=2)
results_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# WordCloud 표시 함수
def display_wordcloud(wordcloud):
    wordcloud_canvas = tk.Canvas(results_frame, width=500, height=500, bg="white")
    wordcloud_canvas.pack()

    # WordCloud 이미지를 파일로 저장하고 로드
    wordcloud.to_file("wordcloud.png")
    wordcloud_image = tk.PhotoImage(file="wordcloud.png")
    wordcloud_canvas.create_image(250, 250, image=wordcloud_image)
    wordcloud_canvas.image = wordcloud_image

# 결과 업데이트 함수
def update_results(sentences, word_counts):
    # 총 문장 수 표시
    sentence_label = tk.Label(results_frame, text=f"총 문장 수: {len(sentences)}", bg="white", font=("Arial", 14))
    sentence_label.pack(pady=10)

    # 빈출 단어 표시
    top_words = word_counts.most_common(10)
    keyword_label = tk.Label(results_frame, text="핵심 키워드 (상위 3): " + ", ".join([word for word, _ in top_words[:3]]), bg="white", font=("Arial", 14))
    keyword_label.pack(pady=10)

    words_frame = tk.Frame(results_frame, bg="white", relief=tk.SOLID, borderwidth=1)
    words_frame.pack(pady=10, padx=5, fill=tk.BOTH)

    word_label = tk.Label(words_frame, text="빈출 단어 및 횟수:", bg="white", font=("Arial", 12))
    word_label.pack(anchor="w", pady=5)

    for word, count in top_words:
        tk.Label(words_frame, text=f"{word}: {count}", bg="white", font=("Arial", 10), anchor="w").pack(pady=2, padx=5)

# 분석 버튼 동작
def analyze_text():
    text = text_box.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("경고", "텍스트를 입력하세요!")
        return

    filtered_words = preprocess_text(text)
    sentences, _ = sentence_lengths(text)
    word_counts = word_frequency(filtered_words)

    wordcloud = generate_wordcloud(filtered_words)
    display_wordcloud(wordcloud)
    update_results(sentences, word_counts)

# UI 구성
label = tk.Label(root, text="텍스트를 입력하세요", bg="#4A90E2", fg="white", font=("Arial", 16))
label.pack(pady=10)

text_box = tk.Text(root, height=10, width=70, font=("Arial", 12))
text_box.pack(pady=10)

analyze_button = tk.Button(root, text="분석하기", command=analyze_text, bg="#50E3C2", fg="black", font=("Arial", 14))
analyze_button.pack(pady=10)

root.mainloop()
