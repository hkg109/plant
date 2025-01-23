from bs4 import BeautifulSoup
import nltk, string, random, requests, re,tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

def get_synonyms_antonyms(word):
    url = f"https://www.merriam-webster.com/thesaurus/{word}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
    except Exception as e:
        print(f"Error occurred while fetching data from thesaurus: {e}")
        return [], []

    synonyms = []
    antonyms = []
    
    synonyms_tag = soup.find("meta", attrs={"name": "twitter:description", "content": True})
    if synonyms_tag:
        synonyms_content = synonyms_tag["content"]
        synonyms_start_index = synonyms_content.find("Synonyms for")
        if synonyms_start_index != -1:
            synonyms_start_index += len("Synonyms for")
            synonyms_end_index = synonyms_content.find("Antonyms of")
            synonyms_str = synonyms_content[synonyms_start_index: synonyms_end_index].strip()
            synonyms = [s.strip() for s in synonyms_str.split(",")]
    
    antonyms_tag = soup.find("meta", attrs={"name": "twitter:description", "content": True})
    if antonyms_tag:
        antonyms_content = antonyms_tag["content"]
        antonyms_start_index = antonyms_content.find("Antonyms of")
        if antonyms_start_index != -1:
            antonyms_start_index += len("Antonyms of")
            antonyms_str = antonyms_content[antonyms_start_index:].strip()
            antonyms = [a.strip() for a in antonyms_str.split(",")]
    
    return synonyms, antonyms

def get_meaning(word):
    url = f"https://dic.daum.net/search.do?q={word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    meaning = ""
    meaning_tag = soup.find("span", class_="txt_search")
    if meaning_tag:
        meaning = meaning_tag.get_text(strip=True)
    
    return meaning


def transform_sentence_game(sent1):
    stopwords = nltk.corpus.stopwords.words('english') + list(string.punctuation)

    # 문장을 단어로 토큰화
    tokens1 = nltk.word_tokenize(sent1)

    # 불용어 제거
    tokens2 = [t for t in tokens1 if t.lower() not in stopwords and t not in string.punctuation]

    # 랜덤하게 단어 선택
    random_word = random.choice(tokens2)

    # 선택된 단어의 유의어와 반의어를 찾음
    synonyms, antonyms = get_synonyms_antonyms(random_word)
    # 선택된 단어를 원래 문장에서 유의어로 대체
    new_word = random.choice([random_word] + synonyms + antonyms) if synonyms or antonyms else random_word
    if new_word in synonyms:
        req = "o"
    elif new_word in antonyms:
        req = "x"
    else:
        req = "o"
    new_word = new_word.replace(';', '')
    new_word = new_word.replace(':', '')
    new_sent = sent1.replace(random_word, new_word) if synonyms else sent1
    # 결과 출력
    print(f"입력문장: {sent1}")
    print(f"변형된 문장: {new_sent}")
    print(f"정답은 {req}입니다")
    random_mean = get_meaning(random_word)
    new_mean = get_meaning(new_word)
    return sent1, new_sent, req,random_mean,new_mean



def create_questions():
    global qus, window
    qus = []
    window.destroy()
    engw = simpledialog.askstring("Input", "지문을 입력하세요:")
    # 구두점을 기준으로 문장을 분리합니다.
    sent = re.split('[.!?]', engw)
    for i in sent:
        if i:  # 비어있는 문장은 제외합니다.
            a, b, c, d, e= transform_sentence_game(i.strip())
            qus.append([a,b,c,d,e])
    load_question()

def menu():
    global window
    window.destroy()
    window = Tk()
    window.title("메뉴")
    window.geometry("300x100")
    button = Button(window, text="지문 입력하기", command=create_questions)
    button2 = Button(window, text="유의어/반의어 찾기", command=create_santo)
    button.pack(side=TOP, padx=10, pady=10)
    button2.pack(side=BOTTOM, padx=10, pady=10)
    window.mainloop()

def create_santo():
    global window
    window.destroy()
    wword = simpledialog.askstring("Input", "단어를 입력하세요:")
    s, a = get_synonyms_antonyms(wword)
    window = Tk()
    window.title(f"{wword}의 유의어/반의어")
    window.geometry("900x200")
    label = Label(window, text=f"{wword} 의 유의어/반의어는 다음과 같습니다\n\n 유의어 : {s}\n\n 반의어 : {a}")
    label.pack()
    button = Button(window, text="메뉴로 돌아가기", command=menu)
    button.pack(side=RIGHT, padx=10, pady=10)
    window.mainloop()

window = Tk()
window.title("메뉴")
window.geometry("300x100")
button = Button(window, text="지문 입력하기", command=create_questions)
button2 = Button(window, text="유의어/반의어 찾기", command=create_santo)
button.pack(side=TOP, padx=10, pady=10)
button2.pack(side=BOTTOM, padx=10, pady=10)
window.mainloop()

n = 0
window = None




def next_question(ox):
    global n, window
    if qus[n][2] == ox:
        messagebox.showinfo("결과", f"정답입니다!\n원래 단어 뜻 : {qus[n][3]}\n변형 단어 뜻 : {qus[n][4]}")
    else:
        messagebox.showinfo("결과", f"오답입니다!\n원래 단어 뜻 : {qus[n][3]}\n변형 단어 뜻 : {qus[n][4]}")
    if window is not None:
        window.destroy()
    n += 1
    if n < len(qus):
        load_question()

def load_question():
    global n, window
    window = Tk()
    window.title("영어 지문 변형문제")
    window.geometry("1300x300")

    # 문장을 끊어서 보여주도록 수정
    original_text = "원래 문장 :\n" + '\n'.join(qus[n][0].split(', '))
    transformed_text = "변형된 문장:\n" + '\n'.join(qus[n][1].split(', '))
    label = Label(window, text="변형된 문장이 원래 문장과 유사한 의미를 띄고 있나요?\n\n"+original_text + "\n\n" + transformed_text)

    label.pack()
    button = Button(window, text="O", command=lambda: next_question("o"))
    button.pack(side=LEFT, padx=300, pady=50)
    button.config(background = "green",width = 6, height = 3)
    button2 = Button(window, text="X", command=lambda: next_question("x"))
    button2.pack(side=RIGHT, padx=300, pady=50)
    button2.config(background = "red",width = 6, height = 3)
    window.mainloop()

load_question()