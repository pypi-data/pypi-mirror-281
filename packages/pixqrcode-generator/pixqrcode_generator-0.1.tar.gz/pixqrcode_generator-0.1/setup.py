from setuptools import setup, find_packages

setup(
    name='pixqrcode-generator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'qrcode[pil]',
        'Pillow'
    ],
    description='Biblioteca para gerar QR Codes de pagamentos via PIX',
    author='Seu Nome',
    author_email='seuemail@exemplo.com',
    url='https://github.com/username/pixqrcode-generator',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
