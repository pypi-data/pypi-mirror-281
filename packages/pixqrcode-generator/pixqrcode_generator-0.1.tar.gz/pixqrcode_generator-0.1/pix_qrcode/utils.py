# pix_qrcode/utils.py

def save_qrcode_image(image, filepath):
    """
    Salva a imagem do QR Code em um arquivo.

    :param image: Imagem do QR Code a ser salva.
    :param filepath: Caminho do arquivo onde a imagem será salva.
    """
    image.save(filepath)
