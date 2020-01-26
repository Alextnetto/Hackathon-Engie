from PIL import Image

import pytesseract

from pdf2image import convert_from_path

import matplotlib
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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

    preco_celesc = fatura.crop((left, top, right, bottom))
    #fatura.show()
    '''cabecalho.show()
    preco_celesc.show()'''
    preco_celesc = pytesseract.image_to_string(preco_celesc).lower().split("\n")
    preco_celesc = preco_celesc[-1].split(" ")
    preco_celesc = list(map(int,preco_celesc))
    print(preco_celesc)

    left = 0
    top = height/2.7
    right = width/2
    bottom = height/2.63

    datas = fatura.crop((left, top, right, bottom))
    datas = pytesseract.image_to_string(datas).lower().split(" ")
    for i in range(len(datas)):
        datas[i] = datas[i][:3].upper()
    print(datas)



    left = 0.7 * width
    top = height/ 4.85
    right = 0.88 * width
    bottom = height / 4.65
    
    consumo = fatura.crop((left, top, right, bottom))
    consumo = pytesseract.image_to_string(consumo).lower().split(" ")


    print(consumo)
    cotacao_engie = [
        227.30,
        317.28,
        273.89,
        219.57,
        237.29,
        185.52,
        78.52,
        135.17,
        180.41,
        234.49,
        443.67,
        192.10
    ]

    
    cotacao_celesc = float(consumo[1].replace(",",".")) * 1000
    

    razao_economia = []

    for cotacao in cotacao_engie:
        razao = cotacao / cotacao_celesc
        razao_economia.append(razao)

    preco_engie = []

    for i in range(len(preco_celesc)):
        precoNovo = preco_celesc[i] * razao_economia[i]
        preco_engie.append(precoNovo)
    data = {
        "engie": preco_engie,
        "celesc": preco_celesc
    }

    df = pd.DataFrame(data)

    N = 12
    
    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, preco_celesc, width)
    p2 = plt.bar(ind, preco_engie, width)

    plt.ylabel('Preço')
    plt.title('Diferença de preço')
    plt.xticks(ind, datas)
    plt.legend((p1[0], p2[0]), ('Celesc', 'Engie'))

    plt.savefig('grafico.png')