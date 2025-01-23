import matplotlib.pyplot as plt
import time
maxspeed = 10
a=0.05
class Car:
    def __init__(self, position, speed, sfd, mode, color,modtime1,modtime2):
        self.position = position
        self.speed = speed
        self.initial_speed = speed
        self.sfd = sfd
        self.mode = mode
        self.color = color
        self.modtime1 = modtime1
        self.modtime2 = modtime2

    def move(self):
        self.position += self.speed

def simulate_traffic(num_cars):
    plt.ion()
        # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]})
    colors = ['b', 'r', 'g', 'y', 'c', 'm', 'k']
    cars = [Car(100, 10, 100, 0, colors[i%len(colors)],0,0) for i in range(num_cars)]
    for i in range(num_cars):
        if i <= num_cars-2:
            cars[i+1].position = cars[i+1].sfd*i*-1
            ax1.plot(cars[i+1].position,1.5, 'o', color=cars[i].color)
    speeds = []
    speed1 = []
    speed2 = []
    speed3 = []
    speed4 = []
    speed5 = []
    speed6 = []
    speed7 = []
    x1 = 0
    while True:
        ax1.clear()
        ax2.clear()
        x1 += 1
        speeds.append((x1, cars[0].position))
        speed1.append((x1,cars[1].position))
        speed2.append((x1,cars[2].position))
        speed3.append((x1,cars[3].position))
        speed4.append((x1,cars[4].position))
        speed5.append((x1,cars[5].position))
        speed6.append((x1,cars[6].position))
        speed7.append((x1,cars[7].position))
        if x1==50:
            cars[0].modtime1 = 60
            cars[0].modtime2 = 80
        if x1 == cars[0].modtime1:
            cars[0].mode = 1
            k = 1
            h = 1
        if x1 == cars[0].modtime2:
            cars[0].mode = 2
            k = 1
            h = 1
        for i in range(num_cars):
            if i > 0 and cars[i-1].position - cars[i].position < 0:
                cars[i].speed = 0
            if i > 0 and cars[i-1].position - cars[i].position > cars[i].sfd:
                cars[i].mode = 2
                cars[i].modtime1 = x1
                k = 1
                h = 1
            if i > 0 and cars[i-1].position - cars[i].position < cars[i].sfd:
                cars[i].mode = 1
                cars[i].modtime2 = x1
                k = 1
                h = 1
            if cars[i].mode == 1:
                if i >0:
                    if cars[i-1].position - cars[i].position < cars[i].sfd:
                        k = 2*a*(x1-(cars[i].modtime1+cars[i].modtime2)/2)
                        cars[i].speed = max(cars[i].speed - k,0)
                    else:
                        cars[i].mode = 2
                        k = 1
                        h = 1
                else:
                    k = 2*a*(x1-(cars[i].modtime1+cars[i].modtime2)/2)
                    cars[i].speed = max(cars[i].speed + k,0)

            elif cars[i].mode == 2:
                if i > 0:
                    h = 2*a*(x1-(cars[i].modtime1+cars[i].modtime2)/2)
                else:
                    h = 2*a*(x1-(cars[i].modtime1+cars[i].modtime2)/2)
                cars[i].speed = min(cars[i].speed + h,maxspeed)
            if cars[i].speed == maxspeed:
                cars[i].mode = 0
                if (x1 - cars[i].modtime1) and i >0:
                    print(f"{i}번째 차 가속도 운동 시간 {x1 - cars[i].modtime1}")
                k = 1
                h = 1
            if cars[i].speed==0:
                cars[i].mode=2
                k = 1
                h = 1
            cars[i].move()
            ax1.plot(cars[i].position, 2, 'o', color=cars[i].color)
        
        # Plot speeds
        ax2.set_xlim(x1-100, x1)
        ax2.set_ylim(0, cars[0].position)
        x_values, y_values = zip(*speeds[-300:])
        x1_values, y1_values = zip(*speed1[-300:])
        x2_values, y2_values = zip(*speed2[-300:])
        x3_values, y3_values = zip(*speed3[-300:])
        x4_values, y4_values = zip(*speed4[-300:])
        x5_values, y5_values = zip(*speed4[-300:])
        x6_values, y6_values = zip(*speed4[-300:])
        x7_values, y7_values = zip(*speed4[-300:])
        ax2.plot(x_values, y_values, color='blue', alpha=1)
        ax2.plot(x1_values, y1_values, color='red', alpha=1)
        ax2.plot(x2_values, y2_values, color='green', alpha=1)
        ax2.plot(x3_values, y3_values, color='yellow', alpha=1)
        ax2.plot(x4_values, y4_values, color='c', alpha=1)
        ax2.plot(x5_values, y5_values, color='m', alpha=1)
        ax2.plot(x6_values, y6_values, color='k', alpha=1)
        ax2.plot(x7_values, y7_values, color='b', alpha=1)
        ax1.set_xlim(0, 5000)
        ax1.set_ylim(0, 3)
        ax1.set_title('Car Simulation')
        ax1.set_xlabel('Position')
        ax1.set_ylabel('Lane')
        plt.pause(0.00001)

        if all(car.position > 5000 for car in cars):
            break

    plt.ioff()
    plt.show()
simulate_traffic(20)
