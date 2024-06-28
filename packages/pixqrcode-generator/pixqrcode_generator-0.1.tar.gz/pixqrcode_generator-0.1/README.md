# pix_qrcode

Biblioteca para gerar QR Codes de pagamentos via PIX.

## Descrição

pypix-qrcode é uma biblioteca Python que facilita a geração de QR Codes para pagamentos via PIX. Este projeto oferece uma maneira simples e eficiente de criar QR Codes compatíveis com o sistema de pagamentos instantâneos brasileiro. Além disso, inclui uma interface gráfica para facilitar a geração e visualização dos QR Codes.

Funcionalidades:

> Geração de QR Codes de PIX a partir de chave PIX, valor, nome do destinatário e cidade.
> Suporte para descrição opcional da transação.
> Interface gráfica simples baseada em Tkinter para entrada de dados e visualização de QR Codes.
> Fácil integração em aplicações Python.

## Como Usar:

## Instalação

```bash
pip install pix_qrcode
````

## Exemplo de Uso Programático

```bash
from pypix_qrcode import generate_pix_qrcode, save_pix_qrcode

pix_key = "suachavepix"
amount = 100.00
merchant_name = "Seu Nome"
city = "Sua Cidade"
description = "Pagamento de Teste"

# Gerar QR Code
qr_image = generate_pix_qrcode(pix_key, amount, merchant_name, city, description)

# Salvar QR Code em um arquivo
save_pix_qrcode(qr_image, "qrcode.png")
Executar a Interface Gráfica
python
Copiar código
from pypix_qrcode import run_gui

run_gui()
Contribuição:
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.
````
## Licença:
Este projeto está licenciado sob a licença MIT.

## Contato:
Para perguntas e suporte, entre em contato em jdrpires@gmail.com