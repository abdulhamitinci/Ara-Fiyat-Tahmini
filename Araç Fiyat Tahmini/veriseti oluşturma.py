import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_data_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    veri = []
    tablo = soup.find('table', {'class': 'table listing-table w100'})
    if tablo:
        satırlar = tablo.find_all('tr')

        for satır in satırlar:
            sütunlar = satır.find_all('td')
            sütunlar = [sütun.text.strip() for sütun in sütunlar]
            
            if len(sütunlar) >= 6:
                yil = sütunlar[3]
                km = sütunlar[4]
                renk = sütunlar[5]
                eski_fiyat = sütunlar[6]
                
                fiyat_tag = satır.find('span', {'class': 'listing-oldprice no-wrap db tdlt'})
                yeni_fiyat = fiyat_tag.text.strip() if fiyat_tag else eski_fiyat
                
                veri.append([yil, km, renk, yeni_fiyat])
    
    return veri

def get_data_from_multiple_pages(base_url, start_page=1, end_page=1):
    all_data = []
    for page in range(start_page, end_page + 1):
        url = f"{base_url}?page={page}"
        page_data = get_data_from_page(url)
        all_data.extend(page_data)
    return all_data

# Kullanıcıdan input alma
marka = input("Marka: ").strip().replace(" ", "-").lower()
model = input("Model: ").strip().replace(" ", "-").lower()
motor = input("Motor: ").strip().replace(" ", "-").lower()
sınıf = input("Sınıf: ").strip().replace(" ", "-").lower()
base_url = f"https://www.arabam.com/ikinci-el/otomobil/{marka}-{model}-{motor}-{sınıf}"

# Verileri toplama
veriler = get_data_from_multiple_pages(base_url, start_page=1, end_page=3)

# Veriyi DataFrame'e dönüştürme
df = pd.DataFrame(veriler, columns=['Yıl', 'Kilometre', 'Renk', 'Fiyat'])

# Veri temizleme ve tür dönüşümü
df['Yıl'] = pd.to_numeric(df['Yıl'], errors='coerce')
df['Kilometre'] = pd.to_numeric(df['Kilometre'].str.replace('.', ''), errors='coerce')
df['Fiyat'] = pd.to_numeric(df['Fiyat'].str.replace(' TL', '').str.replace('.', ''), errors='coerce')

# Önemli sütunlarda NaN değerleri olan satırları kaldırma
df.dropna(subset=['Yıl', 'Kilometre', 'Fiyat'], inplace=True)

# DataFrame'i Excel'e kaydetme
df.to_excel('output.xlsx', index=False)

print("Veriler başarıyla 'output.xlsx' dosyasına kaydedildi.")
