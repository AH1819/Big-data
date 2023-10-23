import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def scrape_data(link):
    try:
        response = requests.get(link)
        response.raise_for_status()  # Check for any HTTP request errors

        html = BeautifulSoup(response.text, "html.parser")
        return html
    except requests.exceptions.RequestException as e:
        print(f"Error while making a request: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

linkP = 'https://www.artic.edu/collection?artist_ids=José%20Clemente%20Orozco'
link1 = 'https://www.artic.edu/artworks/49614/zapatistas'
link2 = 'https://www.artic.edu/artworks/97430/mexican-peasants-working'
link3 = 'https://www.artic.edu/artworks/52708/the-conqueror'

html1 = scrape_data(linkP)
html2 = scrape_data(link1)
html3 = scrape_data(link2)
html4 = scrape_data(link3)

if html1 and html2 and html3 and html4:
    print("OK")

    NomA = html1.find('a', {'class': 'tag f-tag-2 tag--quaternary tag--l'})
    NomAuthor = NomA.getText()

    datos = html1.find_all('a', {'class': 'm-listing__link'})
    links = []
    title1 = []

    for i in datos:
        result = i.get('href')
        Titulo = i.getText('strong', {'class': 'title f-list-7'})
        title = Titulo.split(',')[0].strip()
        links.append(result)
        title1.append(title)

    data = {'Enlace': [links[3], links[6], links[11]], 'Titulo': [title1[3], title1[6], title1[11]]}
    df = pd.DataFrame(data)

    title = f'Colección de pinturas del muralista: {NomAuthor}'

    df.to_csv('DatosPinturas.csv', index=False)

    with open('DatosPinturas.csv', 'r') as file:
        filedata = file.read()

    with open('DatosPinturas.csv', 'w') as file:
        file.write(f"{title}\n")
        file.write(filedata)

    print("primera parte \n")
    print(df)
    print("\n")

    Art1 = html2.find('dd', {'itemprop': 'creator'}).getText().replace('\n', '')

    tit1 = html2.find('dd', {'itemprop': 'name'}).getText().replace('\n', '')

    place1 = html2.find('dd', {'itemprop': 'locationCreated'}).getText().replace('\n', '')

    date1 = html2.find('dd', {'itemprop': 'dateCreated'}).getText().replace('\n', '')

    dimension1 = html2.find('dd', {'itemprop': 'size'}).getText().replace('\n', '')

    Art2 = html3.find('dd', {'itemprop': 'creator'}).getText().replace('\n', '')

    tit2 = html3.find('dd', {'itemprop': 'name'}).getText().replace('\n', '')

    place2 = html3.find('dd', {'itemprop': 'locationCreated'}).getText().replace('\n', '')

    date2 = html3.find('dd', {'itemprop': 'dateCreated'}).getText().replace('\n', '')

    dimension2 = html3.find('dd', {'itemprop': 'size'}).getText().replace('\n', '')

    Art3 = html4.find('dd', {'itemprop': 'creator'}).getText().replace('\n', '')

    tit3 = html4.find('dd', {'itemprop': 'name'}).getText().replace('\n', '')

    place3 = html4.find('dd', {'itemprop': 'locationCreated'}).getText().replace('\n', '')

    date3 = html4.find('dd', {'itemprop': 'dateCreated'}).getText().replace('\n', '')

    pattern = r'\d{4}–\d{4}'
    match = re.search(pattern, date3)

    fecha = match.group()

    dimension3 = html4.find('dd', {'itemprop': 'size'}).getText().replace('\n', '')

    data = {'Artist': [Art1, Art2, Art3], 'Title': [tit1, tit2, tit3], 'Date': [date1, date2, fecha],
            'Dimensions': [dimension1, dimension2, dimension3], 'link': [link1, link2, link3]}
    df = pd.DataFrame(data)

    print(df)

    df.to_csv('datos.csv', index=False, encoding="utf-8-sig")

else:
    print('ERROR')
