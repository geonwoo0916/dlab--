import tkinter as tk
from tkinter import messagebox
import random

# 게임 설정
WIDTH = 10
HEIGHT = 10
MINES = 10

# 게임 상태
game_over = False
mines = set()
revealed = set()

# Tkinter 초기화
root = tk.Tk()
root.title("지뢰 게임")

# 지뢰 생성
def create_mines():
    global mines
    mines = set()
    while len(mines) < MINES:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        mines.add((x, y))

# 인접한 셀의 지뢰 개수 계산
def count_adjacent_mines(x, y):
    count = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            nx, ny = x + dx, y + dy
            if (nx, ny) in mines:
                count += 1
    return count

# 셀 클릭 이벤트 처리
def cell_click(x, y):
    global game_over, revealed

    if game_over:
        return

    if (x, y) in mines:
        # 게임 오버
        game_over = True
        messagebox.showinfo("게임 오버", "지뢰를 클릭했습니다. 새로운 게임을 시작하세요.")
        create_mines()
        revealed = set()
        game_over = False
    else:
        # 셀 주변의 지뢰 개수 표시
        count = count_adjacent_mines(x, y)
        revealed.add((x, y))
        if count == 0:
            # 인접한 빈 셀들도 자동으로 표시
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and (nx, ny) not in revealed:
                        cell_click(nx, ny)
        update_cells()

# 셀 업데이트
def update_cells():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if (x, y) in revealed:
                count = count_adjacent_mines(x, y)
                cell_text = str(count) if count > 0 else ""
                buttons[x][y].config(text=cell_text)
            else:
                buttons[x][y].config(text="")

# 지뢰 게임 보드 생성
buttons = []
for x in range(WIDTH):
    row = []
    for y in range(HEIGHT):
        button = tk.Button(root, width=2, height=1, command=lambda x=x, y=y: cell_click(x, y))
        button.grid(row=x, column=y)
        row.append(button)
    buttons.append(row)

# 게임 시작
create_mines()
update_cells()

root.mainloop()
