import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import requests
import random
import time
from datetime import datetime

class LanguageLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("언어 학습 도우미")
        self.root.geometry("400x600")
        self.root.configure(bg="#f0f0f0")  # 배경색 설정

        self.vocab = {}
        self.quiz_history = []
        self.score = 0  # 점수 초기화

        self.load_vocab()
        self.create_widgets()

    def create_widgets(self):
        # 영단어 추가 버튼
        self.add_english_word_button = tk.Button(self.root, text="영단어 추가", command=self.add_english_word, width=20, height=2, bg="#4CAF50", fg="white")
        self.add_english_word_button.pack(pady=10)

        # 한국어 단어 추가 버튼
        self.add_korean_word_button = tk.Button(self.root, text="한국어 단어 추가", command=self.add_korean_word, width=20, height=2, bg="#2196F3", fg="white")
        self.add_korean_word_button.pack(pady=10)

        # 단어 목록 보기 버튼
        self.view_vocab_button = tk.Button(self.root, text="단어 목록 보기", command=self.view_vocab, width=20, height=2, bg="#FFC107", fg="black")
        self.view_vocab_button.pack(pady=10)

        # 단어 목록 초기화 버튼
        self.clear_vocab_button = tk.Button(self.root, text="단어 목록 초기화", command=self.clear_vocab, width=20, height=2, bg="#F44336", fg="white")
        self.clear_vocab_button.pack(pady=10)

        # 퀴즈 시작 버튼
        self.start_quiz_button = tk.Button(self.root, text="퀴즈 시작", command=self.start_quiz, width=20, height=2, bg="#673AB7", fg="white")
        self.start_quiz_button.pack(pady=10)

        # 전적 보기 버튼
        self.view_history_button = tk.Button(self.root, text="전적 보기", command=self.view_history, width=20, height=2, bg="#FF9800", fg="white")
        self.view_history_button.pack(pady=10)

        # 점수 표시
        self.score_label = tk.Label(self.root, text=f"점수: {self.score}", font=("Arial", 14), bg="#f0f0f0")
        self.score_label.pack(pady=10)

        # 종료 버튼
        self.exit_button = tk.Button(self.root, text="종료", command=self.exit_app, width=20, height=2, bg="#9E9E9E", fg="white")
        self.exit_button.pack(pady=10)

    def add_english_word(self):
        word = simpledialog.askstring("영단어 추가", "영단어를 입력하세요:")
        
        if word:
            meaning = self.get_meaning(word)  # 뜻 자동 검색
            if meaning:
                self.vocab[word] = meaning
                self.save_vocab()
                messagebox.showinfo("단어 추가", f"{word} -> {meaning}이(가) 추가되었습니다.")
            else:
                messagebox.showerror("단어 추가", "뜻을 찾을 수 없습니다.")

    def get_meaning(self, english_word):
        url = f"https://api.mymemory.translated.net/get?q={english_word}&langpair=en|ko"
        try:
            response = requests.get(url)
            data = response.json()
            if data['responseData']:
                return data['responseData']['translatedText']
        except Exception as e:
            print(f"Error fetching translation: {e}")
        return None

    def add_korean_word(self):
        word = simpledialog.askstring("한국어 단어 추가", "한국어 단어를 입력하세요:")
        
        if word:
            english_word = self.get_english_word(word)
            if english_word:
                self.vocab[word] = english_word
                self.save_vocab()
                messagebox.showinfo("단어 추가", f"{word} -> {english_word}이(가) 추가되었습니다.")
            else:
                messagebox.showerror("단어 추가", "영단어를 찾을 수 없습니다.")

    def get_english_word(self, korean_word):
        url = f"https://api.mymemory.translated.net/get?q={korean_word}&langpair=ko|en"
        try:
            response = requests.get(url)
            data = response.json()
            if data['responseData']:
                return data['responseData']['translatedText']
        except Exception as e:
            print(f"Error fetching translation: {e}")
        return None

    def view_vocab(self):
        vocab_list = "\n".join([f"{word}: {meaning}" for word, meaning in self.vocab.items()])
        if vocab_list:
            messagebox.showinfo("단어 목록", vocab_list)
        else:
            messagebox.showinfo("단어 목록", "단어가 없습니다.")

    def clear_vocab(self):
        if messagebox.askyesno("단어 목록 초기화", "정말로 단어 목록을 초기화하시겠습니까?"):
            self.vocab.clear()
            self.save_vocab()
            messagebox.showinfo("단어 목록 초기화", "단어 목록이 초기화되었습니다.")

    def start_quiz(self):
        if not self.vocab:
            messagebox.showwarning("퀴즈 시작", "단어가 없습니다. 먼저 단어를 추가하세요.")
            return
        
        self.score = 0  # 점수 초기화
        self.score_label.config(text=f"점수: {self.score}")  # 점수 레이블 업데이트

        num_questions = simpledialog.askinteger("퀴즈 설정", "퀴즈에 포함할 단어 수를 입력하세요:", minvalue=1, maxvalue=len(self.vocab))
        if num_questions is None:
            return
        
        questions = random.sample(list(self.vocab.items()), num_questions)
        start_time = datetime.now()  # 퀴즈 시작 시간 기록

        for korean_word, english_word in questions:
            if not self.ask_question(english_word, korean_word):
                self.score -= 1

        end_time = datetime.now()  # 퀴즈 종료 시간 기록
        duration = (end_time - start_time).seconds  # 퀴즈 소요 시간 (초)

        # 퀴즈 전적에 추가
        self.quiz_history.append({
            "date": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "score": self.score,
            "num_questions": num_questions,
            "duration": duration
        })
        self.save_history()
        messagebox.showinfo("퀴즈 완료", f"퀴즈가 완료되었습니다! 최종 점수: {self.score} (소요 시간: {duration}초)")

    def ask_question(self, english_word, korean_word):
        answer = simpledialog.askstring("퀴즈", f"{english_word}의 뜻은?")
        timer_start = time.time()
        
        while True:
            if answer is None:
                return False  # 사용자가 취소 버튼을 누른 경우
            elif time.time() - timer_start > 10:  # 10초 제한시간
                messagebox.showwarning("시간 초과", "시간이 초과되었습니다!")
                return False
            elif answer.strip().lower() == korean_word.lower():
                self.score += 1  # 점수 +1
                self.score_label.config(text=f"점수: {self.score}")  # 점수 레이블 업데이트
                messagebox.showinfo("정답", "정답입니다!")
                return True
            else:
                answer = simpledialog.askstring("퀴즈", f"틀렸습니다. 다시 시도하세요: {english_word}의 뜻은?")

    def view_history(self):
        if not self.quiz_history:
            messagebox.showinfo("전적 보기", "퀴즈 전적이 없습니다.")
            return
        
        history_text = "\n".join([f"날짜: {entry['date']}, 점수: {entry['score']}, 단어 수: {entry['num_questions']}, 소요 시간: {entry['duration']}초" for entry in self.quiz_history])
        messagebox.showinfo("퀴즈 전적", history_text)

    def save_vocab(self):
        with open("vocab.json", "w", encoding="utf-8") as f:
            json.dump(self.vocab, f, ensure_ascii=False, indent=4)

    def load_vocab(self):
        if os.path.exists("vocab.json"):
            with open("vocab.json", "r", encoding="utf-8") as f:
                self.vocab = json.load(f)

    def save_history(self):
        with open("quiz_history.json", "w", encoding="utf-8") as f:
            json.dump(self.quiz_history, f, ensure_ascii=False, indent=4)

    def exit_app(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = LanguageLearningApp(root)
    root.mainloop()