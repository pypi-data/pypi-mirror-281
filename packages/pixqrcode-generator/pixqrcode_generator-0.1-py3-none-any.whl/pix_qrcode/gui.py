# pix_qrcode/gui.py

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from .generator import generate_pix_qrcode


def show_qr_code(image, qr_label):
    img = ImageTk.PhotoImage(image)
    qr_label.config(image=img)
    qr_label.image = img


def on_generate_click(pix_key_entry, amount_entry, merchant_name_entry, city_entry, description_entry, qr_label):
    pix_key = pix_key_entry.get()
    amount = amount_entry.get()
    merchant_name = merchant_name_entry.get()
    city = city_entry.get()
    description = description_entry.get()

    if not pix_key or not amount or not merchant_name or not city:
        messagebox.showerror("Erro", "Todos os campos exceto descrição são obrigatórios!")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Erro", "O valor deve ser um número!")
        return

    qr_image = generate_pix_qrcode(pix_key, amount, merchant_name, city, description)
    show_qr_code(qr_image, qr_label)


def run_gui():
    app = tk.Tk()
    app.title("Gerador de QR Code PIX")

    tk.Label(app, text="Chave PIX:").grid(row=0, column=0, sticky="e")
    pix_key_entry = tk.Entry(app)
    pix_key_entry.grid(row=0, column=1)

    tk.Label(app, text="Valor:").grid(row=1, column=0, sticky="e")
    amount_entry = tk.Entry(app)
    amount_entry.grid(row=1, column=1)

    tk.Label(app, text="Nome do Destinatário:").grid(row=2, column=0, sticky="e")
    merchant_name_entry = tk.Entry(app)
    merchant_name_entry.grid(row=2, column=1)

    tk.Label(app, text="Cidade:").grid(row=3, column=0, sticky="e")
    city_entry = tk.Entry(app)
    city_entry.grid(row=3, column=1)

    tk.Label(app, text="Descrição:").grid(row=4, column=0, sticky="e")
    description_entry = tk.Entry(app)
    description_entry.grid(row=4, column=1)

    generate_button = tk.Button(app, text="Gerar QR Code", command=lambda: on_generate_click(
        pix_key_entry, amount_entry, merchant_name_entry, city_entry, description_entry, qr_label))
    generate_button.grid(row=5, columnspan=2)

    qr_label = tk.Label(app)
    qr_label.grid(row=6, columnspan=2)

    app.mainloop()
