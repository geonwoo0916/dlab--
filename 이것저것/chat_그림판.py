import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog
from PIL import Image, ImageTk

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("그림판")
        
        self.selected_color = "black"
        self.brush_size = 2
        
        self.create_menu()
        self.create_canvas()
        
        self.canvas.bind("<B1-Motion>", self.draw)
        
    def create_menu(self):
        menu_frame = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        color_button = tk.Button(menu_frame, text="색상 선택", command=self.select_color)
        color_button.pack(pady=10)
        
        brush_label = tk.Label(menu_frame, text="브러시 크기:")
        brush_label.pack()
        
        brush_slider = tk.Scale(menu_frame, from_=1, to=10, orient=tk.HORIZONTAL, command=self.set_brush_size)
        brush_slider.set(self.brush_size)
        brush_slider.pack()
        
        clear_button = tk.Button(menu_frame, text="캔버스 초기화", command=self.clear_canvas)
        clear_button.pack(pady=10)
        
        save_button = tk.Button(menu_frame, text="저장", command=self.save_image)
        save_button.pack()
        
    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
    def select_color(self):
        color = colorchooser.askcolor(title="색상 선택")[1]
        if color:
            self.selected_color = color
            
    def set_brush_size(self, size):
        self.brush_size = int(size)
        
    def draw(self, event):
        x, y = event.x, event.y
        self.canvas.create_oval(x - self.brush_size, y - self.brush_size, x + self.brush_size, y + self.brush_size, fill=self.selected_color, outline="")
        
    def clear_canvas(self):
        self.canvas.delete("all")
        
    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG 파일", "*.png"), ("모든 파일", "*.*")])
        if file_path:
            try:
                self.canvas.postscript(file="tmp.eps", colormode="color")
                img = Image.open("tmp.eps")
                img.save(file_path)
                messagebox.showinfo("저장", "이미지가 성공적으로 저장되었습니다.")
            except Exception as e:
                messagebox.showerror("에러", f"이미지 저장 중 에러가 발생했습니다:\n{str(e)}")

root = tk.Tk()
paint_app = PaintApp(root)
root.mainloop()
