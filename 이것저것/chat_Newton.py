import tkinter as tk
import time

class EnhancedNewtonsLawSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Newton's Law Simulation")

        self.canvas = tk.Canvas(self.root, width=1200, height=600)  # 크기를 조절
        self.canvas.pack()

        self.blue_circle = self.canvas.create_oval(50, 275, 100, 325, fill="blue")  # 가로로 배치
        self.red_circle = self.canvas.create_oval(1050, 275, 1100, 325, fill="red")  # 가로로 배치

        self.start_button = tk.Button(self.root, text="Start", command=self.start_simulation)
        self.start_button.pack()

        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_simulation)
        self.restart_button.pack()

        self.blue_force_scale = tk.Scale(self.root, from_=0, to=50, orient="horizontal", label="Blue Force")
        self.blue_force_scale.pack()
        self.red_force_scale = tk.Scale(self.root, from_=0, to=50, orient="horizontal", label="Red Force")
        self.red_force_scale.pack()

        self.acceleration = 1.0
        self.blue_mass = 10.0
        self.red_mass = 10.0
        self.blue_force = 10.0
        self.red_force = 10.0

        self.running = False

    def start_simulation(self):
        self.running = True
        while self.running:
            self.update_simulation()
            self.root.update()
            time.sleep(0.02)

    def update_simulation(self):
        self.blue_force = self.blue_force_scale.get()
        self.red_force = self.red_force_scale.get()
        
        blue_acceleration = self.blue_force / self.blue_mass
        red_acceleration = self.red_force / self.red_mass
        
        self.canvas.move(self.blue_circle, blue_acceleration, 0)  # 가로로 움직임
        self.canvas.move(self.red_circle, red_acceleration, 0)  # 가로로 움직임
        self.root.update()

    def restart_simulation(self):
        self.canvas.coords(self.blue_circle, 50, 275, 100, 325)
        self.canvas.coords(self.red_circle, 1050, 275, 1100, 325)
        self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedNewtonsLawSimulation(root)
    root.mainloop()
