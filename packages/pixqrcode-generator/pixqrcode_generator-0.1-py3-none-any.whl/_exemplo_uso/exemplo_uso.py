from pix_qrcode import generate_pix_qrcode, save_pix_qrcode

pix_key = "22203015837"
amount = 100.00
merchant_name = "Jean Pires"
city = "San Francisco"
description = "Pagamento de Teste"

# Gerar QR Code
qr_image = generate_pix_qrcode(pix_key, amount, merchant_name, city, description)

# Salvar QR Code em um arquivo
save_pix_qrcode(qr_image, "qrcode.png")
