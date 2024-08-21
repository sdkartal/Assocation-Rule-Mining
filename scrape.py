import requests
from bs4 import BeautifulSoup
import pandas as pd
import time  # Gecikme için


tarifler_listesi = []

for sayfa in range(1, 46):
    if sayfa == 1:
        url = "https://www.nefisyemektarifleri.com/kategori/tarifler/et-yemekleri/?nytorderby=archive-populer#"
    else:
        url = f"https://www.nefisyemektarifleri.com/kategori/tarifler/et-yemekleri/page/{sayfa}/?nytorderby=archive-populer"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tarif_linkleri = soup.find_all('a', class_='title', href=True)

    for tarif_link in tarif_linkleri[:23]:
        tarif_adi = tarif_link.text.strip()
        tarif_url = tarif_link['href']

        tarif_response = requests.get(tarif_url)
        tarif_soup = BeautifulSoup(tarif_response.text, 'html.parser')

        malzemeler_listesi = tarif_soup.find('ul', class_='recipe-materials')
        malzemeler = []

        if malzemeler_listesi is not None:
            for malzeme in malzemeler_listesi.find_all('li', itemprop='recipeIngredient'):
                malzemeler.append(malzeme.text.strip())
        else:
            malzemeler.append("Malzeme listesi bulunamadı.")

        tarifler_listesi.append({
            'Tarif Adı': tarif_adi,
            'Malzemeler': ', '.join(malzemeler)
        })

        time.sleep(1)

tarifler_df = pd.DataFrame(tarifler_listesi) # 1036 tane veri çektik.
tarifler_df.to_csv('tarifler_45_sayfa.csv', index=False, encoding='utf-8-sig')
