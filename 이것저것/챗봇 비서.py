import tkinter as tk 
from PIL import ImageTk, Image 
import bardapi
import os

os.environ["_BARD_API_KEY"]="XwiTWzq0E8xSIVuXhoU4eEV_jIcWwrIlIMPXT2i4xnWzuMDXsAFU7ilhD-ZvZ3bvpI7Tjg."


class ChatWidget(tk.Frame):
    def __init__(self, parent, profile_image_path, nickname, message, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        profile_image = ImageTk.PhotoImage(Image.open(profile_image_path).resize((50, 50)))
        profile_label = tk.Label(self, image=profile_image)
        profile_label.image = profile_image
        profile_label.grid(row=0, column=0, rowspan=2, padx=5)

        nickname_label = tk.Label(self, text=nickname, font=("Helvetica", 12, "bold"))
        nickname_label.grid(row=0, column=1, sticky="w")

        message_label = tk.Label(self, text=message, wraplength=300)
        message_label.grid(row=1, column=1, sticky="w")


def send_message():
    message = input_entry.get()             # 디자인
    chat_widget = ChatWidget(message_list_frame, "./profile_image.png", "파란이", message)
    chat_widget.pack(fill=tk.X, padx=10, pady=10)
    input_entry.delete(0, tk.END)           # 여기까지 디자인
    chat_model = bardapi.core.Bard()        # 바드에서 받음
    if message == "" :                      # 공백일 때 에러 출력
        add_received_message('잠시 에러가 발생했는데 다시 해주세요.')
    else:                                   # 답변이 있을 때 답변
        # response = chat_model.get_answer("넌 최고의 작가야, 무조건 내가 말하는 부분에 대해 시 한편을 작성해봐." + message)
        response = chat_model.get_answer(message)
        add_received_message(response['content'])

def add_received_message(message):          # 챗봇 답변
    chat_widget = ChatWidget(message_list_frame, "./dlab_profile.png", "디랩 비서", message) 
    chat_widget.pack(fill=tk.X, padx=10, pady=10)

window = tk.Tk()    # tk.Tk()를 사용하여 새로운 윈도우를 생성합니다.
window.title("깨톡방")    # 윈도우의 제목을 "깨톡방"으로 설정합니다. 
window.geometry("500x700")    # 윈도우의 크기를 500x800 픽셀로 설정합니다. 
window.resizable(False, False)    # 윈도우의 크기 조절을 비활성화합니다. 
scrollbar = tk.Scrollbar(window)    # 오른쪽에 스크롤바를 생성합니다. 
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)    # message_list_canvas이라는 캔버스 위젯을 생성합니다. 이 캔버스는 채팅 메시지 목록을 표시하기 위한 용도로 사용됩니다. 
message_list_canvas = tk.Canvas(window)    # message_list_frame이라는 프레임 위젯을 생성합니다. 이 프레임은 캔버스의 내용을 감싸는 역할을 합니다. 
message_list_canvas.pack(fill=tk.BOTH, expand=True)    # message_list_canvas에 수직 스크롤바를 적용합니다. 스크롤바와 캔버스를 연결합니다. 
message_list_frame = tk.Frame(message_list_canvas)     # message_list_frame을 캔버스의 시작점에 위치시킵니다. 
message_list_canvas.config(yscrollcommand=scrollbar.set)   # 스크롤바 설정
scrollbar.config(command=message_list_canvas.yview)    # y축을 스크롤하게 명령
message_list_canvas.create_window((0, 0), window=message_list_frame, anchor="nw")   # 윈도우 생성 및 메시지 언더바 리스트 프레임 심음
# Tkinter를 사용하여 간단한 채팅 애플리케이션의 윈도우를 생성하는 부분입니다. 
input_frame = tk.Frame(window)
input_frame.pack(fill=tk.X)
input_entry = tk.Entry(input_frame)
input_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
send_button = tk.Button(input_frame, text="전송")
send_button.pack(side=tk.RIGHT)
send_button.config(command=send_message)

def configure_canvas(event):
    message_list_canvas.configure(scrollregion=message_list_canvas.bbox("all"))

message_list_frame.bind('<Configure>', configure_canvas)

add_received_message("안녕하세요, 무엇을 도와드릴까요?")
# message_list_frame.bind('<Configure>',
# message_list_canvas.configure(scrollregion=message_list_canvas.bbox("all")))
window.mainloop()