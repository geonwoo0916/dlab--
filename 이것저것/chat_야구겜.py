import tkinter as tk
from tkinter import messagebox
import random

class BaseballGameGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("숫자 야구 게임")

        self.secret_numbers = self.generate_number()
        self.life = 5
        self.guesses = []
        
        self.create_widgets()
        
    def generate_number(self):
        numbers = random.sample(range(1, 10), 3)
        return numbers
    
    def create_widgets(self):
        self.label = tk.Label(self.window, text="숫자 3개를 입력하세요 (1에서 9까지 중복되지 않는 숫자):")
        self.label.pack()
        
        self.entry = tk.Entry(self.window)
        self.entry.pack()
        
        self.button = tk.Button(self.window, text="제출", command=self.submit_guess)
        self.button.pack()
        
        self.result_label = tk.Label(self.window, text="")
        self.result_label.pack()
        
        self.life_label = tk.Label(self.window, text=f"남은 기회: {self.life}")
        self.life_label.pack()
        
        self.guesses_label = tk.Label(self.window, text="이전 기록:")
        self.guesses_label.pack()
        
        self.guesses_listbox = tk.Listbox(self.window)
        self.guesses_listbox.pack()
        
    def submit_guess(self):
        user_input = self.entry.get()
        numbers = []
        
        try:
            numbers = [int(num) for num in user_input]
            
            if len(numbers) != 3 or not all(1 <= num <= 9 for num in numbers) or len(set(numbers)) != 3:
                raise ValueError
        except ValueError:
            messagebox.showerror("오류", "입력이 잘못되었습니다. 다시 시도해주세요.")
            return
        
        strikes, balls = self.calculate_score(numbers)
        
        self.guesses.append((user_input, f"S: {strikes}, B: {balls}"))
        self.update_guesses_listbox()
        
        if strikes == 3:
            messagebox.showinfo("정답", "축하합니다! 정답을 맞추셨습니다.")
            self.window.destroy()
        else:
            self.result_label.config(text=f"S: {strikes}, B: {balls}")
            self.life -= 1
            self.life_label.config(text=f"남은 기회: {self.life}")
            
            if self.life == 0:
                messagebox.showinfo("게임 오버", f"기회를 모두 사용하셨습니다. 정답은 {self.secret_numbers[0]}, {self.secret_numbers[1]}, {self.secret_numbers[2]}입니다.")
                self.window.destroy()
        
        self.entry.delete(0, tk.END)
        
    def calculate_score(self, user_numbers):
        strikes = 0
        balls = 0
        
        for i in range(3):
            if user_numbers[i] == self.secret_numbers[i]:
                strikes += 1
            elif user_numbers[i] in self.secret_numbers:
                balls += 1
        
        return strikes, balls
    
    def update_guesses_listbox(self):
        self.guesses_listbox.delete(0, tk.END)
        for guess in self.guesses:
            self.guesses_listbox.insert(tk.END, f"입력: {guess[0]}, 결과: {guess[1]}")
        
    def start(self):
        self.window.mainloop()

game = BaseballGameGUI()
game.start()
