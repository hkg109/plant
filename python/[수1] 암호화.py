def letter_to_number(letter):
    # 알파벳을 숫자로 매핑하는 사전
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return alphabet.index(letter) + 1
    # 주어진 알파벳 문자를 숫자로 변환하여 반환하는 함수입니다.
    # 예시: 'a' -> 1, 'b' -> 2, ..., 'z' -> 26

def number_to_letter(number):
    # 숫자를 알파벳으로 매핑하는 사전
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return alphabet[number - 1]
    # 주어진 숫자를 알파벳 문자로 변환하여 반환하는 함수입니다.
    # 예시: 1 -> 'a', 2 -> 'b', ..., 26 -> 'z'

def sentence_to_numbers(sentence):
    # 문장을 단어 단위로 나눔
    words = sentence.split()
    number_words = []

    for word in words:
        number_word = ''
        for letter in word:
            if letter.isalpha():  # 알파벳만 변환
                number_word += str(letter_to_number(letter.lower()))
        number_words.append(number_word)

    return ' '.join(number_words)
    # 문장을 숫자로 변환하는 함수입니다.
    # 각 단어의 알파벳 문자를 숫자로 변환하여 반환합니다.
    # 예시: "hello world" -> "85121215 231518124"

def sentence_to_numbers2(sentence):
    # 문장을 단어 단위로 나눔
    words = sentence.split()
    number_words = []

    for word in words:
        number_word = ''
        for letter in word:
            if letter.isalpha():  # 알파벳만 변환
                if letter_to_number(letter.lower()) + input_key > 26:
                    number_word += number_to_letter(letter_to_number(letter.lower()) + input_key - 26)
                else:
                    number_word += number_to_letter(letter_to_number(letter.lower()) + input_key)
        number_words.append(number_word)

    return ' '.join(number_words)
    # 알파벳 문자를 숫자로 변환한 후 주어진 키를 더하여 다시 알파벳 문자로 변환하는 함수입니다.
    # 키를 더한 값이 26을 초과하면 26을 빼줍니다.
    # 예시: "abc", 키=3 -> "def"

def numbers_to_sentence(number_sentence, input_key):
    # 숫자 문장을 단어 단위로 나눔
    number_words = number_sentence.split()
    letter_words = []

    for number_word in number_words:
        letter_word = ''
        for letter in number_word:
            if letter.isalpha():  # 알파벳만 변환
                number = letter_to_number(letter.lower()) - input_key
                if number < 1:
                    number += 26
                letter_word += number_to_letter(number)
        letter_words.append(letter_word)

    return ' '.join(letter_words)
    # 숫자로 변환된 문장을 주어진 키를 사용하여 다시 알파벳 문자로 변환하는 함수입니다.
    # 예시: "def", 키=3 -> "abc"

def sentence_to_numbers3(sentence):
    number_pairs = []
    i = 0
    sentence = sentence.replace(" ","")
    while i < len(sentence):
        if i + 1 < len(sentence):
            pair = sentence[i:i+2]
            i += 2
        else:
            pair = sentence[i]
            i += 1
        
        number_pair = ''
        for letter in pair:
            if letter.isalpha():  # 알파벳만 변환
                number_pair += "{:02d}".format(letter_to_number(letter.lower()))
        number_pairs.append(number_pair)
    
    return ' '.join(number_pairs)
    # 문장을 두 자리 숫자로 변환하여 반환하는 함수입니다.
    # 예시: "hello world" -> "08 05 12 12 15 23 15 18 12 04"

def numbers_to_sentence2(numbers):
    words = numbers.split()
    sentence = ''
    
    for number_word in words:
        for i in range(0, len(number_word), 2):
            number = int(number_word[i:i+2])
            sentence += number_to_letter(number)
    
    return sentence
    # 두 자리 숫자로 변환된 문장을 다시 알파벳 문자로 변환하여 반환하는 함수입니다.
    # 예시: "08 05 12 12 15 23 15 18 12 04" -> "hello world"

def xGCD(a, b):
    # {g, {x, y}}를 반환합니다. ax + by = g
    if b == 0:
        return (a, (1, 0))
    g, (x, y) = xGCD(b, a % b)
    return (g, (y, x - (a // b) * y))
    # 확장 유클리드 알고리즘을 사용하여 a와 b의 최대공약수(gcd)와
    # ax + by = gcd를 만족하는 x와 y를 반환하는 함수입니다.

def mod_inverse(a, mod):
    g, (x, y) = xGCD(a, mod)
    if g > 1:
        return -1
    return (x + mod) % mod
    # 모듈러 역수를 계산하는 함수입니다.
    # a * x ≡ 1 (mod mod)를 만족하는 x를 반환합니다.
    # 예시: a=3, mod=11 -> 4 (왜냐하면 3 * 4 ≡ 1 (mod 11))

def modular_exponentiation(base, exponent, mod):
    result = 1
    base = base % mod
    while exponent > 0:
        if (exponent % 2) == 1:
            result = (result * base) % mod
        exponent = exponent >> 1
        base = (base * base) % mod
    return result
    # 모듈러 제곱을 계산하는 함수입니다.
    # base^exponent % mod를 효율적으로 계산합니다.
    # 예시: base=2, exponent=10, mod=5 -> 4 (왜냐하면 2^10 % 5 = 1024 % 5 = 4)

def exponentiate_numbers(number_sentence, key, mod):
    number_words = number_sentence.split()
    exponentiated_words = []

    for number_word in number_words:
        number = int(number_word)
        exponentiated_number = modular_exponentiation(number, key, mod)  # 제곱 후 모듈러 연산
        exponentiated_word = "{:04d}".format(exponentiated_number)
        exponentiated_words.append(exponentiated_word)
    
    return ' '.join(exponentiated_words)
    # 숫자 문장을 키와 모듈러 값을 사용하여 모듈러 제곱 연산을 수행하는 함수입니다.


# 예제 입력
while True:
    answer = input("전치암호화 / 지수암호화 / 전치복호화 / 지수복호화 : ")
    if answer == '전치암호화':
        input_sentence = input("평문을 입력해주세요 : ")
        print("P: " + sentence_to_numbers(input_sentence))
        input_key= int(input("키를 입력해주세요 : "))
        print("C: " + sentence_to_numbers2(input_sentence))
        print("C: " + sentence_to_numbers(sentence_to_numbers2(input_sentence)))
    elif answer == '전치복호화':
        input_sentence = input("암호문을 입력해주세요: ")
        input_key = int(input("키를 입력해주세요 : "))
        decrypted_sentence = numbers_to_sentence(input_sentence, input_key)
        print("P: " + decrypted_sentence)
    elif answer == '지수암호화':
        input_sentence = input("평문을 입력해주세요: ")
        print("P: " + sentence_to_numbers3(input_sentence))
        print("P: " + numbers_to_sentence2(sentence_to_numbers3(input_sentence)))
        key = int(input("키를 입력해주세요 : "))
        mod = int(input("모듈러 수를 입력해주세요 : "))
        exponentiated_sentence = exponentiate_numbers(sentence_to_numbers3(input_sentence), key, mod)
        print("C: " + exponentiated_sentence)
        inverse = mod_inverse(key, mod-1)
        print("P: " + exponentiate_numbers(exponentiated_sentence, inverse, mod))
        print("P: " + numbers_to_sentence2(exponentiate_numbers(exponentiated_sentence, inverse, mod)))
    elif answer == '지수복호화':
        input_sentence = input("암호문을 입력해주세요: ")
        key = int(input("키를 입력해주세요 : "))
        mod = int(input("모듈러 수를 입력해주세요 : "))
        inverse = mod_inverse(key, mod-1)
        print("P: " + numbers_to_sentence2(exponentiate_numbers(input_sentence, inverse, mod)))