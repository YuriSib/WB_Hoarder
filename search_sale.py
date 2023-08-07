import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time

from selenium.common.exceptions import SessionNotCreatedException, WebDriverException

from selenium_master import html_obj


def ya_search(qwery_, quantity):
    url = f'https://xmlstock.com/yandex/xml/?user=11362&key=2a81ea2bf46144411cc5e8c148f5fcfa&query=' \
          f'{quote("kuvalda.ru") + quote(qwery_)}' \
          f'&groupby=attr%3D%22%22.mode%3Dflat.groups-on-page%3D{quantity}.docs-in-group%3D1'
    response = requests.get(url)
    dirty_list_link = BeautifulSoup(response.text, features="xml").find_all('url')
    list_link = [link.text.strip('</url>') for link in dirty_list_link]
    link_vi = []
    link_ozon = []
    link_kuvalda = []
    for lnk in list_link:
        if 'vseinstrumenti.ru/product' in lnk and 'otzyvy' not in lnk:
            if len(link_vi) == 0:
                link_vi.append(lnk)
                link_vi = ''.join(link_vi)
        elif ('https://www.OZON.ru/product' in lnk or 'https://www.ozon.ru' in lnk)\
                and '/videos' not in lnk and '/features' not in lnk:
            if len(link_ozon) == 0:
                link_ozon.append(lnk)
                link_ozon = ''.join(link_ozon)
        elif 'https://www.kuvalda.ru/' in lnk and '/product' in lnk:
            if len(link_kuvalda) == 0:
                link_kuvalda.append(lnk)
                link_kuvalda = ''.join(link_kuvalda)

    return list_link, link_vi, link_ozon, link_kuvalda


def vi_sale(url):
    try:
        html = html_obj(url)
        soup = BeautifulSoup(html, 'lxml')
        sale_ = soup.find('div', class_='df5X3i').get_text(strip=True)
        sale_ = ''.join(filter(str.isdigit, sale_))
        name = soup.find('div', class_='pKTE7p').get_text(strip=True)
        return int(sale_), name
    except SessionNotCreatedException:
        print('Ошибка создания сессии!')
        return 0
    except WebDriverException:
        print('Долгое ожидание')
        return 0


def ozon_sale(url):
    try:
        html = html_obj(url)
        soup = BeautifulSoup(html, 'lxml')
        if '/reviews' in url:
            sale_ = soup.find('div', class_='qk3 k5q q6k').get_text(strip=True)
            name = soup.find('div', class_='y9k').get_text(strip=True)
        else:
            sale_ = soup.find('div', class_='s0k').get_text(strip=True)
            name = soup.find('div', class_='webProductHeading').get_text(strip=True)
        sale_ = ''.join(filter(str.isdigit, sale_))
        return int(sale_), name
    except SessionNotCreatedException:
        print('Ошибка создания сессии!')
        return 0
    except WebDriverException:
        print('Долгое ожидание')
        return 0


def kuvalda_sale(url):
    # proxies = {
    #     'http': 'http://1257420-all-country-DE:20h1gvhuvx@62.112.11.204:55071',
    # }
    response_ = requests.get(url)
    soup = BeautifulSoup(response_.text, 'lxml')
    sale_ = soup.find('div', class_='product-buy__price-value').get_text(strip=True)
    sale_ = ''.join(filter(str.isdigit, sale_))
    name = soup.find('div', class_='page-header__container container')\
        .get_text(strip=True)

    return int(sale_), name




# http = 'https://www.kuvalda.ru/catalog/2074/product-45565/'
# print(kuvalda_sale(http))

# qwery = 'Тепловая пушка электрическая ТЭПК-2000'
# sale = vi_sale(ya_search(qwery))
# print(sale)

