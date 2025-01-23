import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NewtonsLawSimulation(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Newton's Law Simulation")
        self.geometry("1200x800")

        self.velocity_data = []
        self.time_data = []
        self.acceleration_data = []

        self.create_widgets()
        self.create_graph()

    def create_widgets(self):
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill=tk.X, side=tk.TOP)

        self.inertia_button = ttk.Button(self.button_frame, text="Start Simulation", command=self.show_inertia_simulation)
        self.inertia_button.pack(side=tk.LEFT)

        self.reset_button = ttk.Button(self.button_frame, text="Reset", command=self.reset_simulation)
        self.reset_button.pack(side=tk.LEFT)

        self.simulation_frame = ttk.Frame(self)
        self.simulation_frame.pack(fill=tk.BOTH, expand=True, pady=20)

    def create_graph(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 4))
        self.canvas_graph = FigureCanvasTkAgg(self.fig, master=self)  # `master=self` to place it in the main window
        self.canvas_graph.draw()
        self.canvas_graph.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def update_graphs(self):
        self.ax1.clear()
        self.ax2.clear()

        self.ax1.plot(self.time_data, self.velocity_data, label="Velocity (m/s)")
        self.ax1.set_title("Velocity-Time Graph")
        self.ax1.set_xlabel("Time (s)")
        self.ax1.set_ylabel("Velocity (m/s)")
        self.ax1.legend()

        self.ax2.plot(self.time_data, self.acceleration_data, label="Acceleration (m/s²)")
        self.ax2.set_title("Acceleration-Time Graph")
        self.ax2.set_xlabel("Time (s)")
        self.ax2.set_ylabel("Acceleration (m/s²)")
        self.ax2.legend()

        self.canvas_graph.draw()

    def show_inertia_simulation(self):
        for widget in self.simulation_frame.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.simulation_frame, width=1000, height=200)
        self.canvas.pack()

        # 수평면 생성
        self.ground = self.canvas.create_rectangle(0, 120, 1200, 125, fill="black")

        # 물체 생성
        self.object = self.canvas.create_rectangle(10, 100, 30, 120, fill="blue")

        self.force_label = ttk.Label(self.simulation_frame, text="Force (N):")
        self.force_label.pack()
        self.force_entry = ttk.Entry(self.simulation_frame)
        self.force_entry.pack()

        self.mass_label = ttk.Label(self.simulation_frame, text="Mass (kg):")
        self.mass_label.pack()
        self.mass_entry = ttk.Entry(self.simulation_frame)
        self.mass_entry.pack()

        self.time_label = ttk.Label(self.simulation_frame, text="Time of Force Applied (s):")
        self.time_label.pack()
        self.time_entry = ttk.Entry(self.simulation_frame)
        self.time_entry.pack()

        self.start_button = ttk.Button(self.simulation_frame, text="Start", command=self.start_inertia_simulation)
        self.start_button.pack()

    def start_inertia_simulation(self):
        try:
            # 사용자 입력 값 가져오기
            force = float(self.force_entry.get())
            mass = float(self.mass_entry.get())
            time_of_force = float(self.time_entry.get())

            # 가속도 계산 (F = m*a -> a = F/m)
            acceleration = force / mass

            # 초기 속도 및 위치, 시뮬레이션을 위한 시간 간격 및 총 시간 초기화
            velocity = 0
            position = 0
            delta_time = 0.01
            total_time = 0

            # 데이터 저장을 위한 리스트 초기화
            self.velocity_data.clear()
            self.time_data.clear()
            self.acceleration_data.clear()

            # 물체가 수평면의 끝에 도달하거나 사용자가 설정한 시간이 지날 때까지 반복
            while position < 1000:
                # 힘이 가해지는 동안 가속도 적용
                if total_time <= time_of_force:
                    velocity += acceleration * delta_time
                else:
                    acceleration = 0

                # 위치 업데이트
                position += velocity * delta_time
                # 총 시간 업데이트
                total_time += delta_time

                # 그래픽스 업데이트 - 물체를 움직이는 부분
                self.canvas.coords(self.object, 10 + position, 100, 30 + position, 120) # 수정된 부분

                # 데이터 추가
                self.time_data.append(total_time)
                self.velocity_data.append(velocity)
                self.acceleration_data.append(acceleration)

                # 시간, 거리, 속도 정보 업데이트
                self.canvas.delete("info")
                self.canvas.create_text(900, 20, text=f"Time: {total_time:.2f} s", tags="info")
                self.canvas.create_text(900, 40, text=f"Distance: {position:.2f} m", tags="info")
                self.canvas.create_text(900, 60, text=f"Velocity: {velocity:.2f} m/s", tags="info")

                # 그래프 업데이트
                self.update_graphs()
                self.canvas.update()

        except ValueError:
            messagebox.showerror("Input Error", "Force, Mass, and Time of Force Applied must be numbers.")



    def reset_simulation(self):
            # 시뮬레이션 프레임 내부의 위젯을 모두 제거합니다.
        for widget in self.simulation_frame.winfo_children():
            widget.destroy()

            # 그래프 데이터를 초기화합니다.
        self.velocity_data.clear()
        self.time_data.clear()
        self.acceleration_data.clear()

            # 그래프도 초기화합니다.
        self.ax1.clear()
        self.ax2.clear()
        self.canvas_graph.draw()

            # 위젯을 다시 생성합니다.
        self.create_widgets()

if __name__ == "__main__":
    app = NewtonsLawSimulation()
    app.mainloop()
