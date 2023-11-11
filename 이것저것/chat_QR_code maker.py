import tkinter as tk
import qrcode
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk

class QRCodeMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Maker")

        self.label = tk.Label(root, text="Enter Link:")
        self.label.pack()

        self.link_entry = tk.Entry(root)
        self.link_entry.pack()

        self.generate_button = tk.Button(root, text="Generate QR Code", command=self.generate_qrcode)
        self.generate_button.pack()

        self.save_button = tk.Button(root, text="Save QR Code", command=self.save_qrcode)
        self.save_button.pack()

    def generate_qrcode(self):
        link = self.link_entry.get()
        if link:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(link)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            self.qr_image = img

            # Display the image using PIL
            self.qr_image_pil = ImageTk.PhotoImage(img)
            self.image_label = tk.Label(self.root, image=self.qr_image_pil)
            self.image_label.pack()

        else:
            messagebox.showerror("Error", "Please enter a valid link.")

    def save_qrcode(self):
        if hasattr(self, 'qr_image'):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.qr_image.save(file_path)
                messagebox.showinfo("Success", "QR Code saved successfully.")
        else:
            messagebox.showerror("Error", "Generate a QR code first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeMaker(root)
    root.mainloop()
