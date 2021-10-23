import requests
from bs4 import BeautifulSoup
import csv
#библиотеки


HOST = 'https://www.aviasales.ru'
URL = 'https://www.aviasales.ru/search/MOW2310AAQ29101?request_source=search_form.explore_history&expected_price_value=6270&expected_price_currency=rub&expected_price_source=history&payment_method=all'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 OPR/80.0.4170.48', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
TICKET = 'ticket.csv'
#5 стр. обращение к сайту    6 стр. защита от проверки на бота

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
#получение данных в html формате

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='fade-enter-done')
    price=[]
    for item in items:
        price.append({
            'price': item.find('span', class_='price').get_text(strip=True),
            'link': HOST + item.find('a', class_='buy-button  button').get('href')
        })
        return price
#поиск всех билетов

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delattr(';'))
        writer.writerow(['Цена', 'Ссылка'])
        for item in items:
            writer.writerow(['price', 'link'])
#сохрарение всего файла в эксель

def parse():
    html = get_html(URL)
    price = []
    if html.status_code == 200:
        get_content(html.text)
        save_file(price, TICKET)
    else:
        print('error')
#процесс поиска