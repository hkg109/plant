import numpy as np
import matplotlib.pyplot as plt

# 세제곱 함수 정의
def f(x):
    return (x - 2) ** 2

# 세제곱 함수의 도함수(기울기) 정의
def df(x):
    return 3 * (x - 2) 

# 경사하강법 함수
def gradient_descent(starting_point, learning_rate, num_iterations):
    x = starting_point
    history = [x]  # 최적화 경로 기록용 리스트

    for _ in range(num_iterations):
        x -= learning_rate * df(x)  # 경사 하강
        history.append(x)

    return x, history

# 초기값과 파라미터 설정
starting_point = 0.0  # 시작점
learning_rate = 0.1   # 학습률
num_iterations = 20   # 반복 횟수

# 경사하강법 실행
optimal_x, history = gradient_descent(starting_point, learning_rate, num_iterations)

# 결과 출력
print(f"최적의 x 값: {optimal_x}")
print(f"최적화 경로: {history}")

# 함수와 최적화 경로 시각화
x_values = np.linspace(-1, 5, 100)
y_values = f(x_values)

plt.plot(x_values, y_values, label='f(x) = (x - 2)^2')
plt.scatter(history, f(np.array(history)), color='red', label='경사하강법 경로')
plt.title('경사하강법을 이용한 세제곱 함수 최적화')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.axhline(0, color='black', lw=0.5, ls='--')
plt.axvline(2, color='green', lw=0.5, ls='--', label='최솟값 위치 (x=2)')
plt.legend()
plt.grid()
plt.show()
