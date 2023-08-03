import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time

from selenium_master import html_obj


def ya_search(qwery_):
    url = f'https://xmlstock.com/yandex/xml/?user=11362&key=2a81ea2bf46144411cc5e8c148f5fcfa&query={quote(qwery_)}' \
          f'&groupby=attr%3D%22%22.mode%3Dflat.groups-on-page%3D50.docs-in-group%3D1'
    response = requests.get(url)
    dirty_list_link = BeautifulSoup(response.text, features="xml").find_all('url')
    list_link = [link.text.strip('</url>') for link in dirty_list_link]
    link_vi = []
    for lnk in list_link:
        if 'vseinstrumenti.ru/product' in lnk and 'otzyvy' not in lnk:
            if len(link_vi) == 0:
                link_vi.append(lnk)
                link_vi = ''.join(link_vi)

    return link_vi


def vi_sale(url):
    html = html_obj(url)
    soup = BeautifulSoup(html, 'lxml')
    sale_ = soup.find('div', class_='df5X3i').get_text(strip=True)

    return sale_


# qwery = 'Труборасширитель VST-22 для труб 38, 12, 58, 34, 78'
# sale = vi_sale(ya_search(qwery))
# print(sale)

