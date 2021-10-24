import requests
from bs4 import BeautifulSoup
import csv
#библиотеки


URL = 'https://www.aviasales.ru/search/MOW2310AAQ29101?request_source=expired_search'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 OPR/80.0.4170.48', 'accept': '*/*'}
HOST = 'https://www.aviasales.ru'
TICKET = 'ticket.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='class')

    price = []
    for item in items:
             price.append({
            'price': item.find('div', class_='class').get_text(strip=True),
            'link': HOST + item.find('div', class_='class').get('href')
             })
    return price
#поиск всех билетов

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Цена', 'Ссылка'])
        for item in items:
            writer.writerow([item['price'], item['link']])
#сохрарение всего файла в эксель

def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        price = []
        save_file(price, TICKET)
    else:
        print('Error')


parse()
#процесс поиска

