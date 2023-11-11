import tkinter as tk
import time

class StopWatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stop Watch")

        self.running = False
        self.start_time = None
        self.elapsed_time = 0
        self.lap_times = []

        self.time_label = tk.Label(root, text="00:00:00.00", font=("Helvetica", 48))
        self.time_label.pack(padx=20, pady=20)

        self.start_button = tk.Button(root, text="Start", command=self.start_stop)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.lap_button = tk.Button(root, text="Lap", command=self.lap)
        self.lap_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack(side=tk.RIGHT, padx=10)

        self.lap_listbox = tk.Listbox(root, font=("Helvetica", 14), selectmode=tk.SINGLE)
        self.lap_listbox.pack(padx=20, pady=10)

        self.update()

    def update(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
        self.update_time_label()
        self.root.after(100, self.update)

    def update_time_label(self):
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        milliseconds = int((self.elapsed_time % 1) * 100)
        self.time_label.config(text=f"{minutes:02}:{seconds:02}.{milliseconds:02}")

    def start_stop(self):
        if self.running:
            self.running = False
            self.start_button.config(text="Start")
            self.lap_button.config(state=tk.DISABLED)
            self.lap_times.append(self.elapsed_time)
        else:
            self.running = True
            self.start_button.config(text="Stop")
            self.lap_button.config(state=tk.NORMAL)
            self.start_time = time.time() - self.elapsed_time

    def lap(self):
        if self.running:
            self.lap_times.append(self.elapsed_time)
            self.lap_listbox.insert(tk.END, self.format_time(self.elapsed_time))

    def reset(self):
        self.running = False
        self.start_time = None
        self.elapsed_time = 0
        self.lap_times = []
        self.start_button.config(text="Start")
        self.lap_button.config(state=tk.DISABLED)
        self.update_time_label()
        self.lap_listbox.delete(0, tk.END)

    def format_time(self, time):
        minutes = int(time // 60)
        seconds = int(time % 60)
        milliseconds = int((time % 1) * 100)
        return f"{minutes:02}:{seconds:02}.{milliseconds:02}"

root = tk.Tk()
app = StopWatchApp(root)
root.mainloop()
