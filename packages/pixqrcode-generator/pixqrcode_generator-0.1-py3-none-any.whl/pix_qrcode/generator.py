# pix_qrcode/generator.py

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


def save_pix_qrcode(image, filepath):
    image.save(filepath)
