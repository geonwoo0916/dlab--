import tkinter as tk
import tkinter.font
import time
from tkinter import messagebox as msg
import numpy as np
import pygame.mixer


TILE_SIZE = 24      # 지뢰찾기 게임의 타일 크기를 지정

class GameBoard:        # 게임 보드 클래스 생성
    def __init__(self, w, h, mine, frame):      # 게임판의 가로, 세로, 지뢰의 수, 게임판이 표시될 프레임
        self.imgFlag = tk.PhotoImage(file='flag.png')
        self.imgWrongFlag = tk.PhotoImage(file='wrongflag.png')
        self.imgMine = tk.PhotoImage(file='mine.png')
        self.imgFlaggedMine = tk.PhotoImage(file='flaggedmine.png')
        self.imgtime = tk.PhotoImage(file='clock.png')     # 게임에 사용되는 5종의 이미지 불러옴
        self.board = tk.Frame(frame)        # 게임보드의 타일들을 포함할 프레임 'board' 생성
        self.board.pack()
        self.tileLeft = w * h - mine        # 게임에 승리하기 위해 클릭해야 하는 타일의 수를 저장
        self.mine = mine                    # 지뢰의 수를 저장
        self.flag = 0                       # 사용된 깃발의 수를 저장
        self.disabled = False               # 게임 승리, 패배, 일시정지 시에 True
        self.time = 60

        self.button_sound = "click_button.mp3"  # 소리
        # self.bgm_sound = "긴장브금.mp3"
        self.boom_sound = "boom.mp3"

 
        self.width = w
        self.height = h                     # 게임 판의 가로, 세로 타일 수
 
        self.dataBoard = np.zeros(self.width * self.height, dtype='i')
        self.dataBoard[:mine] = 9
        np.random.shuffle(self.dataBoard)
        self.dataBoard = self.dataBoard.reshape(self.width, self.height)        # 2d-array(w x h)에 지뢰를 9개 무작위 배치
 
        for x in range(self.width):
            for y in range(self.height):
                self.dataBoard[x][y] = self.boardCheck(x, y)        # dataBoard 9가 아닌(지뢰가 없는) 타일에 인접 지뢰 수 저장
 
        self.tileFrame = [[0] * self.height for _ in range(self.width)]
        self.tileBack = [[0] * self.height for _ in range(self.width)]
        self.tileBtn = [[0] * self.height for _ in range(self.width)]
        self.tileBtnImg = [[0] * self.height for _ in range(self.width)]  # 타일별 프레임, 라벨, 버튼, 변수 초기화

    def play_sounds(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.button_sound)
        pygame.mixer.music.play()
    
    # def bgm_sounds(self):
    #     pygame.mixer.init()
    #     pygame.mixer.music.load(self.bgm_sound)
    #     pygame.mixer.music.play(-1)

    def boom_sounds(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.boom_sound)
        pygame.mixer.music.play()
    
    # 클래스 GameBoard 내부에 새로운 메서드 추가
    def update_time(self):
        if not self.disabled and self.time > 0:
            #print( self.time )
            self.time -= 1
            timeCnt.configure(text=' 남은 시간 : %d' % self.time)
            mainWindow.after(1000, self.update_time)  # 1초 후에 다시 업데이트
        elif self.time == 0 :
            self.lose()
        # if self.time <= 30:
        #     self.bgm_sounds()

    # def hint(self) :
    # # 1. root window 게임판 힌트 버튼 추가 (t kinter)
    # # 2. 1번 작업한 gui 에다 hint 함수 command 처리
    # # 3. hint 함수 만들기

    def hint(self):
        if self.time <= 30:     # self.time이 30초일 때 힌트 기능 실행
            for x_ in range(self.width):
                for y_ in range(self.height):
                    if self.dataBoard[x_][y_] == 9 and self.tileBtn[x_][y_].winfo_ismapped():
                        self.tileBtn[x_][y_].pack_forget()
                        self.tileBack[x_][y_].pack(fill=tk.BOTH, expand=tk.YES)                 # 지뢰가 존재하는 칸 보여줌
            mainWindow.after(500, self.hide_hint)  # 1초 후에 hide_hint 메서드 호출

    def hide_hint(self):
        for x_ in range(self.width):
            for y_ in range(self.height):
                if self.dataBoard[x_][y_] == 9 and self.tileBack[x_][y_].winfo_ismapped():
                    self.tileBack[x_][y_].pack_forget()
                    self.tileBtn[x_][y_].pack(fill=tk.BOTH, expand=tk.YES)

    def boardCheck(self, x, y):     # dataBoard[x][y] 칸의 지뢰여부 또는 인접지뢰 수를 출력
        if self.dataBoard[x][y] == 9:
            return 9        # dataBoard[x][y] == 9 이면 그대로 반환

        relativeCoord = ((1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))      # 주변 칸의 상대좌표
        result = 0
        for crd in relativeCoord:
            if 0 <= x + crd[0] < self.width and 0 <= y + crd[1] < self.height:  # 주변 칸의 좌표가 유효한지 확인
                if self.dataBoard[x + crd[0]][y + crd[1]] == 9:                 # 주변 칸의 데이터가 9인지 확인
                    result += 1
        return result       # dataBoard[x][y] != 9 이면 인접 지뢰 수 반환

    def boardActivate(self):        # __init__에서 구성된 보드를 부모 프레임에 표시
        for x in range(self.width):
            for y in range(self.height):        # 보드의 모든 타일에 대하여
                self.tileFrame[x][y] = tk.Frame(self.board, width=TILE_SIZE, height=TILE_SIZE, padx=0, pady=0, relief='sunken', bd=1)
                self.tileFrame[x][y].pack_propagate(False)
                self.tileFrame[x][y].grid(column=x, row=y)      # 타일의 사이즈를 가진 작은 프레임 생성
 
                backText = self.dataBoard[x][y]
                if backText == 0:
                    self.tileBack[x][y] = tk.Label(self.tileFrame[x][y], text='')
                elif backText == 9:
                    self.tileBack[x][y] = tk.Label(self.tileFrame[x][y], text='', image=self.imgMine)
                else:
                    self.tileBack[x][y] = tk.Label(self.tileFrame[x][y], text=backText)     # 타일의 데이터에 따라 빈칸, 이미지, 숫자 라벨 구성 (패킹하지 않음)
 
                self.tileBtn[x][y] = tk.Button(self.tileFrame[x][y], command=(lambda x_=x, y_=y: self.boardClick(x_, y_)), bd=1)
                self.tileBtn[x][y].bind('<Button-3>', (lambda event, x_=x, y_=y: self.boardRightClick(x_, y_)))
                self.tileBtn[x][y].pack(fill=tk.BOTH, expand=tk.YES)                        # 각 타일에 버튼 생성, command 지정 및 우클릭 이벤트 바인드

    def boardClick(self, x, y):     # x, y 좌표의 타일이 클릭되었을 때 호출
        self.play_sounds()
        if not self.disabled:       # 보드가 활성화 되어있으면,
            self.tileBtn[x][y].pack_forget()
            self.tileBack[x][y].pack(fill=tk.BOTH, expand=tk.YES)       # 버튼을 언패킹. 지뢰 그림, 인접 지뢰 숫자 등을 포함한 라벨 패킹
 
            if self.dataBoard[x][y] == 9:
                self.tileBack[x][y].configure(background='RED', relief='flat')
                self.boom_sounds()
                self.lose()     # 지뢰를 클릭했다면, 클릭한 칸의 배경을 붉게하고, 게임 종료
            else:
                self.tileLeft -= 1      # 지뢰가 아니라면 클리어까지 남은 타일 수를 1 감소
                if self.tileLeft == 0:
                    self.win()          # 클리어 까지 남은 타일의 수가 0이 되면 게임에서 승리
 
                if self.dataBoard[x][y] == 0:       # 인접 지뢰 숫자가 0인 타일에서 주변 타일로 재귀호출
                    relativeCoord = ((1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))
                    for crd in relativeCoord:
                        if 0 <= x + crd[0] < self.width and 0 <= y + crd[1] < self.height and self.tileBtn[x + crd[0]][y + crd[1]].winfo_ismapped():
                            self.boardClick(x + crd[0], y + crd[1])     # 유효한 인접 타일 중 클릭되지 않은 타일을 자동으로 클릭
 
            if self.tileBtnImg[x][y] == 1:      # 깃발이 사용된 칸을 클릭한 것이면, 우클릭 이벤트를 발생 (사용된 깃발 수 관리를 위해)
                self.boardRightClick(x, y)
    
            # print( self.time )
            if self.time <= 0:
                timeCnt.configure(text=' 시간이 다 되었습니다!', foreground='red')
                timeCnt.configure(text=' 남은 시간 : %d' % (self.time), foreground='black')      # 남은 시간의 수를 안내
                self.lose()
            # else:
            #     timeCnt.configure(text=' 남은 시간 : %d' % (self.time), foreground='black')      # 남은 시간의 수를 안내


    def boardRightClick(self, x, y):        # x, y 좌표의 타일이 우클릭되었을 때 호출
        self.play_sounds()
        if not self.disabled:               # 보드가 활성화 되어있으면,
            self.tileBtnImg[x][y] = (self.tileBtnImg[x][y] + 1) % 3
            if self.tileBtnImg[x][y] == 0:
                self.tileBtn[x][y].configure(image='', text='')
            elif self.tileBtnImg[x][y] == 1:
                self.tileBtn[x][y].configure(image=self.imgFlag, text='')
                self.flag += 1
            else:
                self.tileBtn[x][y].configure(image='', text='?')        # 타일의 버튼 이미지를 [0 : 표시하지 않음, 1 : 깃발, 2 : 물음표]로 표시함
                self.flag -= 1                                          # 우클릭 횟수에 따라 사용된 깃발 수를 관리
            if self.mine-self.flag < 0:
                flagCnt.configure(text=' 깃발을 너무 많이 사용했습니다!', foreground='red')                  # 지뢰의 수보다 깃발을 많이 사용하면 안내
            else:
                flagCnt.configure(text=' 남은 지뢰 : %d' % (self.mine-self.flag), foreground='black')      # 남은 지뢰(깃발)의 수를 안내

    def win(self):
        winLose.configure(text='WIN!!!', foreground='blue')
        self.disabled = True        # 승리시 승리 메시지 출력, 게임판 비활성화

    def lose(self):                                                                         # 패배시
        for x_ in range(self.width):
            for y_ in range(self.height):
                if self.dataBoard[x_][y_] == 9 and self.tileBtn[x_][y_].winfo_ismapped():
                    self.tileBtn[x_][y_].pack_forget()
                    self.tileBack[x_][y_].pack(fill=tk.BOTH, expand=tk.YES)                 # 지뢰가 존재하는 칸 보여줌
 
                    if self.tileBtnImg[x_][y_] == 1:
                        self.tileBack[x_][y_].configure(image=self.imgFlaggedMine)          # 올바르게 사용한 플래그 위치 표시
 
                elif self.tileBtnImg[x_][y_] == 1:
                    self.tileBtn[x_][y_].configure(image=self.imgWrongFlag, text='')        # 잘못 사용한 플래그 위치 표시
        winLose.configure(text='LOSE...', foreground='red')
        self.disabled = True        # 패배시 패배 메시지 출력, 게임판 비활성화
 
    def unpackBoard(self):
        self.board.pack_forget()        # 화면에서 게임판 지우기
 
 
def gameLevel():
    if game is not None:
        game.disabled = True
    newGameWindow.deiconify()       # 새 게임 대화상자를 화면에 표시, 게임판 비활성화
 
def gameLevelCancel():
    if game is not None:
        game.disabled = False
    newGameWindow.withdraw()        # 새 게임 대화상자를 화면에서 숨김, 게임판 활성화

# gameStart 함수 수정
def gameStart(frame):
    winLose.configure(text='')  # 승, 패 안내 초기화
    newGameWindow.withdraw()  # 새 게임 대화상자 닫음
    global game  # 전역변수 game 사용

    if game is not None:
        game.unpackBoard()  # 실행 중이던 게임이 있으면 화면에서 지움

    if level.get() == 0:
        w = 9
        h = 9
        mine = 10
        
    elif level.get() == 1:
        w = 16
        h = 16
        mine = 40
    else:
        w = 30
        h = 16
        mine = 99
    game = GameBoard(w, h, mine, frame)  # 사용자가 선택한 레벨에 따라 게임보드 생성
    game.boardActivate()  # 활성화

    mainWindow.geometry('%dx%d+%d+%d' % ((w + 1) * TILE_SIZE, (h + 1) * TILE_SIZE + 64,
                                         (scrW - (w + 1) * TILE_SIZE) / 2, (scrH - (h + 1) * TILE_SIZE - 64) / 2))
    mainFrame.configure(width=(w + 1) * TILE_SIZE, height=(h + 1) * TILE_SIZE)  # 화면의 사이즈와 위치 조정

    flagCnt.configure(text=' 남은 지뢰 : %d' % game.mine)
    timeCnt.configure(text=' 남은 시간 : %d' % game.time)  # 시간 초기값 설정

    uiPlace(w, h)
    game.disabled = False  # ui 재설정 및 게임 활성화
 
    if game is not None:
        game.unpackBoard()      # 실행 중이던 게임이 있으면 화면에서 지움
    
    game_time = 0
    if level.get() == 0:
        w = 9
        h = 9
        mine = 10
        game_time = 60  # 쉬움 레벨: 60초
    elif level.get() == 1:
        w = 16
        h = 16
        mine = 40
        game_time = 60*5  # 쉬움 레벨: 300초
    else:
        w = 30
        h = 16
        mine = 99
        game_time = 60*10  # 쉬움 레벨: 600초
    game = GameBoard(w, h, mine, frame)     # 사용자가 선택한 레벨에 따라 게임보드 생성
    game.boardActivate()                    # 활성화
    game.time = game_time
    game.update_time()  # 시간 업데이트 시작
 
    mainWindow.geometry('%dx%d+%d+%d' % ((w + 1) * TILE_SIZE, (h + 1) * TILE_SIZE + 64, (scrW - (w + 1) * TILE_SIZE) / 2, (scrH - (h + 1) * TILE_SIZE - 64) / 2))
    mainFrame.configure(width=(w + 1) * TILE_SIZE, height=(h + 1) * TILE_SIZE)      # 화면의 사이즈와 위치 조정
 
    flagCnt.configure(text=' 남은 지뢰 : %d' % game.mine)
    uiPlace(w, h)
    game.disabled = False       # ui 재설정 및 게임 활성화
 
def uiPlace(w, h):
    flagCnt.place(y=8)
    timeCnt.place(x=w * TILE_SIZE / 2 + TILE_SIZE / 4, y=8)
    mainFrame.place(y=32)
    newGameBtn.place(x=6, y=(h + 1) * TILE_SIZE + 32)
    hintBtn.place(x=w * TILE_SIZE / 2.5, y=(h + 1) * TILE_SIZE + 32)  # 힌트 버튼 위치
    quitGameBtn.place(x=w*TILE_SIZE-12, y=(h + 1) * TILE_SIZE + 32)
    winLose.place(x=w * TILE_SIZE / 2, y=(h + 1) * TILE_SIZE + 32)      # mainWindow 의 위젯들 배치
 
game = None
 
def quitGame():
    if msg.askokcancel('지뢰찾기', '게임을 종료하시겠습니까?'):
        mainWindow.destroy()        # 게임종료 대화상자를 표시, 게임종료
 
mainWindow = tk.Tk()
scrW = mainWindow.winfo_screenwidth()
scrH = mainWindow.winfo_screenheight()
mainWindow.geometry('%dx%d+%d+%d' % (10 * TILE_SIZE, 10 * TILE_SIZE + 64, (scrW - 10 * TILE_SIZE)/2, (scrH - 10 * TILE_SIZE - 64)/2))
mainWindow.resizable(False, False)
mainWindow.title('지뢰 찾기')
mainWindow.lift()       # mainWindow tk 윈도우를 생성, 초기설정
 
mainWindow.protocol("WM_DELETE_WINDOW", quitGame)       # 창 닫기 버튼 클릭 시 quitGame 함수 호출
 
defaultFont = tk.font.Font(family='맑은 고딕', size=10, weight='bold')
mainWindow.option_add("*Font", defaultFont)             # mainWindow 기본 폰트 지정
 
newGameWindow = tk.Toplevel(mainWindow)
newGameWindow.geometry('344x200+%d+%d' % ((scrW - 344)/2, (scrH - 200)/2))
newGameWindow.resizable(False, False)
newGameWindow.title('새 게임')
newGameWindow.wm_attributes("-topmost", 1)      # 새 게임 대화상자 윈도우를 생성, 초기설정
newGameWindow.protocol("WM_DELETE_WINDOW", gameLevelCancel)         # 새 게임 대화상자의 창 닫기 버튼을 gamelevelCancel 에 연결
 
""" 새 게임 대화상자의 GUI 구성 """
 
levelLabel = tk.Label(newGameWindow, text='난이도를 선택해 주세요!')
levelLabel.grid(column=0, row=0)

level = tk.IntVar()
newGameEasy = tk.Radiobutton(newGameWindow, text='쉬움\t\t  (9x9 보드 / 지뢰 10개))', variable=level, value=0)
newGameMedium = tk.Radiobutton(newGameWindow, text='중간\t\t(16x16 보드 / 지뢰 40개)', variable=level, value=1)
newGameHard = tk.Radiobutton(newGameWindow, text='어려움\t\t(30x16 보드 / 지뢰 99개)', variable=level, value=2)
gameStartBtn = tk.Button(newGameWindow, text='게임 시작', command=lambda: gameStart(mainFrame))       # 난이도 선택 라디오 버튼 및 게임시작 버튼 생성

newGameEasy.grid(column=0, row=1, padx=16)
newGameMedium.grid(column=0, row=2, padx=16)
newGameHard.grid(column=0, row=3, padx=16)
gameStartBtn.grid(column=0, row=5, padx=0, pady=16)     # 난이도 선택 라디오 버튼 및 게임시작 버튼 배치
 
""" mainWindow 의 GUI 구성 """

imgFlagCnt = tk.PhotoImage(file='flag.png')
imgTimeCnt = tk.PhotoImage(file='clock.png')
imgHintCnt = tk.PhotoImage(file='hint.png')
flagCnt = tk.Label(mainWindow, image=imgFlagCnt, text=' 남은 지뢰 : 10', compound='left')       # 남은 지뢰 수 표시 라벨 생성
timeCnt = tk.Label(mainWindow, image=imgTimeCnt, text=' 남은 시간 : 60', compound='left')

mainFrame = tk.Frame(mainWindow, width=10 * TILE_SIZE, height=10 * TILE_SIZE, padx=11, pady=11, relief='sunken', bd=1)
mainFrame.pack_propagate(False)     # 게임이 들어갈 mainFrame 생성
 
newGameBtn = tk.Button(mainWindow, text='새 게임', command=gameLevel)
quitGameBtn = tk.Button(mainWindow, text=' X ', command=quitGame, foreground='red')     # 게임종료 버튼 생성
hintBtn = tk.Button(mainWindow, image=imgHintCnt, command=lambda:game.hint())  # 힌트 버튼 생성
 
winLoseFont = tk.font.Font(family='맑은 고딕', size=14, weight='bold')
winLose = tk.Label(mainWindow, text='', anchor=tk.CENTER, font=winLoseFont)         # 승, 패 표시 라벨 생성

uiPlace(9, 9)       # mainWindow 위젯 배치 함수

mainWindow.mainloop()
