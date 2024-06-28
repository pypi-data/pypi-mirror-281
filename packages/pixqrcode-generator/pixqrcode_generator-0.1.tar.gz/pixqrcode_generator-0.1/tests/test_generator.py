
import unittest
from pix_qrcode.generator import generate_pix_qrcode


class TestPixQRCodeGenerator(unittest.TestCase):

    def test_generate_pix_qrcode(self):
        pix_key = "suachavepix"
        amount = 100.00
        merchant_name = "Seu Nome"
        city = "Sua Cidade"
        description = "Pagamento de Teste"

        qr_image = generate_pix_qrcode(pix_key, amount, merchant_name, city, description)
        self.assertIsNotNone(qr_image)


if __name__ == '__main__':
    unittest.main()

    #pix_key = "36285138800"
