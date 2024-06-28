import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode


def generate_pix_qrcode(pix_key, amount, merchant_name, city, description=None):
    payload_format_indicator = "00"
    point_of_initiation_method = "01"
    merchant_account_information = f"26{len(pix_key):02d}{pix_key}"
    merchant_category_code = "0000"
    transaction_currency = "986"
    transaction_amount = f"{amount:.2f}"
    country_code = "BR"
    merchant_name_field = f"{merchant_name.upper():<25}"
    merchant_city_field = f"{city.upper():<15}"
    additional_data_field = f"05{len(description):02d}{description}" if description else ""

    payload = (f"{payload_format_indicator}01{point_of_initiation_method}"
               f"{merchant_account_information}"
               f"{merchant_category_code}{transaction_currency}"
               f"{transaction_amount}{country_code}"
               f"{merchant_name_field}{merchant_city_field}{additional_data_field}")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(payload)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img


def show_qr_code(image):
    img = ImageTk.PhotoImage(image)
    qr_label.config(image=img)
    qr_label.image = img


def on_generate_click():
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
    show_qr_code(qr_image)


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

generate_button = tk.Button(app, text="Gerar QR Code", command=on_generate_click)
generate_button.grid(row=5, columnspan=2)

qr_label = tk.Label(app)
qr_label.grid(row=6, columnspan=2)

app.mainloop()
