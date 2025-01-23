import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

def speices(birth, replication, death):  # Birth, Replication, Death
    name = []
    name.append([birth, replication, death])
    return name

def per(percentage):
    chance = random.random()  # 0.0 이상 1.0 미만의 실수 반환
    return chance < (percentage / 100.0)

# 개체수 Birth, Replication, Death 
a = speices(80, 50, 10)
b = speices(0, 100, 20)
allspeices = [a, b]  # 리스트 생성 수정

# 그래프 초기 설정
plt.ion()

# 그래프 생성
fig, ax = plt.subplots()

# 초기 데이터
x1 = []
y = [[] for _ in range(len(allspeices))]  # 초기 y 데이터 설정
simulation = True
simultaiontime = 0
plt.xlabel('Time', labelpad=10)
plt.ylabel('N', labelpad=10)

max_capacity = 1500
colors = ['blue', 'orange', 'green']  # 종별 색상 설정
sigman = 0
i = 0
for c in range(5):  # 자연발생
    allspeices[i].append([allspeices[i][0][0], allspeices[i][0][1], allspeices[i][0][2]])
i=1
for c in range(5):  # 자연발생
    allspeices[i].append([allspeices[i][0][0], allspeices[i][0][1], allspeices[i][0][2]])
while simulation:
    n=0
    for i in range(len(allspeices)):  # 자연발생
        if per(allspeices[n][0][0]) == True:
            allspeices[n].append([allspeices[n][0][0], allspeices[n][0][1], allspeices[n][0][2]])  # 0으로 초기화
        n+=1
    n = 0
    for i in range(len(allspeices)):  # 복제 및 사망
        for k in range(len(allspeices[n])):
            if (len(allspeices[n]) > 1):
                if per(allspeices[n][0][2]) == True:  # 사망 조건 수정
                    if len(allspeices[n]) > 2:  # 비어있지 않을 때만 pop
                        allspeices[n].pop(0)
                else:
                    if n > 0:
                        if len(allspeices[n-1]) > 2:
                            allspeices[n-1].pop(0)
                            if per(allspeices[n][0][1]):
                                allspeices[n].append([allspeices[n][0][0], allspeices[n][0][1], allspeices[n][0][2]])
                        else:
                            if len(allspeices[n]) > 2:
                                allspeices[n].pop(0)
                    else:
                        if per(allspeices[n][0][1]):
                            allspeices[n].append([allspeices[n][0][0], allspeices[n][0][1], allspeices[n][0][2]])
    # y 데이터 업데이트
        n += 1
    for r in range(len(y)):
        y[r].append(len(allspeices[r]))

    ax.clear()
    x1.append(simultaiontime)
    # 그래프 그리기
    for z in range(len(y)):
        ax.plot(x1, y[z], color=colors[z], alpha=1, label=f'Species {z+1}')  # 각 종별 색상 지정
    ax.set_xlim(1,simultaiontime)
    ax.set_ylim(0,30)
    plt.legend()  # 범례 추가
    plt.show()
    plt.pause(0.001)
    simultaiontime += 1
    time.sleep(0.001)
    if simultaiontime == 300:
        simulation = False
        plt.savefig(f'C:/Users/junhu/OneDrive/바탕 화면/evolution/lotka{simultaiontime}.png', dpi=500)  # 이미지 저장
