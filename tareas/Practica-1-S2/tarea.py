# -*- coding: utf-8 -*-

import requests
import pandas as pd
from bs4 import BeautifulSoup

link1 = 'https://articulo.mercadolibre.com.mx/MLM-1535773709-bocina-jbl-go-3-portatil-con-bluetooth-black-_JM#position=10&search_layout=stack&type=item&tracking_id=962d5d16-fea7-46ed-bd1e-ee164dcc86d4'
link2 = 'https://www.radioshack.com.mx/store/Categor%C3%ADa/Todas/Audio-y-video/Audio/Bocinas/Bocina-Bluetooth-JBL-GO-3-Negro/p/100038831'
link3 = 'https://www.cyberpuerta.mx/Audio-y-Video/Audio-y-MP3/Bocinas/JBL-Bocina-Portatil-Go-3-Bluetooth-Inalambrico-4-2W-RMS-Negro-Resistente-al-Agua.html'

r1 = requests.get(link1)
r2 = requests.get(link2)
r3 = requests.get(link3)

print(r1)
print(r2)
print(r3)

html2 = BeautifulSoup(r2.text, "html.parser")
html1 = BeautifulSoup(r1.text, "html.parser")
html3 = BeautifulSoup(r3.text, "html.parser")

preciosM = html1.find('span', {'class' : 'andes-money-amount__fraction'})
producto1 = html1.find('h1',{'class' : 'ui-pdp-title'})
PreciosR = html2.find('span', {'id' : 'price1'})
producto2 = html2.find('h1', {'class': 'p-name'})
PreciosC = html3.find('span', {'class','priceText'})
producto3 = html3.find('h1',{'class' : 'detailsInfo_right_title'})

nomprod1 = producto1.getText()
nomprod2 = producto2.getText()
nomprod3 = producto3.getText()

precio1 = float(preciosM.getText().replace(',', '').replace('$', ''))
precio2 = float(PreciosR.getText())
precio3 = float(PreciosC.getText().replace('$', '').replace(',', ''))

data = {'Precio': [precio1, precio2, precio3], 'Enlace': ['Mercado Libre', 'Radio Shack', 'Cyber Puerta'], 'Producto':[nomprod1, nomprod2, nomprod3]}
df = pd.DataFrame(data)

# Guardar el DataFrame en un archivo CSV
df.to_csv('datos_productos.csv', index=False, encoding='ISO-8859-1 ')

print(df)
precio_minimo = df['Precio'].min()
print(f"El precio mínimo es: {precio_minimo}")
