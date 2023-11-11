import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import qrcode
from PIL import Image, ImageTk
import cv2

class QRCodeVendingMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Vending Machine")

        # Initialize balance
        self.balance = 0

        # Product data
        self.products = {
            "짜장면": {"price": 6000, "quantity": 5, "image": "짜장면.png"},
            "짬뽕": {"price": 7000, "quantity": 3, "image": "짬뽕.png"},
            "탕수육": {"price": 12000, "quantity": 10, "image": "탕수육.png"},
            "볶음밥": {"price": 8000, "quantity": 8, "image": "볶음밥.png"}
        }

        # Create UI elements
        self.balance_label = ttk.Label(root, text=f"잔액: {self.balance} 원")
        self.qr_label = ttk.Label(root, text="QR 코드를 스캔하세요")
        self.purchase_button = ttk.Button(root, text="구매하기", command=self.purchase_product)
        self.charge_button = ttk.Button(root, text="돈 충전", command=self.charge_balance)
        self.select_image_button = ttk.Button(root, text="이미지 선택", command=self.select_image)

        # Display UI elements
        self.balance_label.pack()
        self.qr_label.pack()
        self.purchase_button.pack()
        self.charge_button.pack()
        self.select_image_button.pack()

    def update_balance_label(self):
        self.balance_label.config(text=f"잔액: {self.balance} 원")

    def purchase_product(self):
        selected_product = self.qr_label["text"]
        if selected_product in self.products:
            product = self.products[selected_product]
            if product["quantity"] > 0 and self.balance >= product["price"]:
                self.balance -= product["price"]
                product["quantity"] -= 1
                self.update_balance_label()
                messagebox.showinfo("구매 완료", f"{selected_product} 구매되었습니다.")
            elif product["quantity"] == 0:
                messagebox.showinfo("품절", f"{selected_product} 품절되었습니다.")
            else:
                messagebox.showinfo("잔액 부족", "잔액이 부족합니다.")

    def charge_balance(self):
        # Use cv2 to scan QR code
        cap = cv2.VideoCapture(0)
        qr_code_detector = cv2.QRCodeDetector()

        while True:
            ret, frame = cap.read()
            if ret:
                decoded_text, points, _ = qr_code_detector.detectAndDecodeMulti(frame)

                if decoded_text:
                    scanned_amount = int(decoded_text)
                    self.balance += scanned_amount
                    self.update_balance_label()
                    messagebox.showinfo("충전 완료", f"{scanned_amount} 원이 충전되었습니다.")
                    print(self.balance)
                    break

            cv2.imshow("QR Code Scanner", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        print(file_path)
        if file_path:
            self.scan_image(file_path)

    def scan_image(self, image_path):
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        qr_code_detector = cv2.QRCodeDetector()
        decoded_text, points, _ = qr_code_detector.detectAndDecodeMulti(gray)

        if decoded_text:
            scanned_amount = int(decoded_text)
            self.balance += scanned_amount
            self.update_balance_label()
            messagebox.showinfo("충전 완료", f"{scanned_amount} 원이 충전되었습니다.")
        else:
            messagebox.showerror("오류", "유효한 QR 코드가 아닙니다.")

def main():
    root = tk.Tk()
    app = QRCodeVendingMachine(root)
    root.mainloop()

if __name__ == "__main__":
    main()
