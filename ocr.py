from PIL import Image

import pytesseract

from pdf2image import convert_from_path


pages = convert_from_path('faturaPDF.pdf', 500)


for page in pages:
    page.save('fatura.jpg', 'JPEG')

fatura = Image.open(r"fatura.jpg")

print(fatura.size)
width, height = fatura.size
left = 0
top = 0
right = width
bottom = height/15

cabecalho = fatura.crop((left, top, right, bottom))


distruibuidora = pytesseract.image_to_string(cabecalho).lower()

if "celesc" in distruibuidora:

    left = 0
    top = height/2.8
    right = width/2
    bottom = height/2.55

    historico = fatura.crop((left, top, right, bottom))
    fatura.show()
    cabecalho.show()
    historico.show()
    historico = pytesseract.image_to_string(historico).lower().split("\n")
    print(historico[-1])
