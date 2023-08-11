import requests

proxies = {
    'http': 'http://1257420-all-country-DE:20h1gvhuvx@62.112.11.204:55071',
}


def get_category(url, page):
    # url = f'https://catalog.wb.ru/catalog/repair10/catalog?appType=1&limit=100&cat=128968&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&uclusters=0&page={page}'
    # url = f'https://catalog.wb.ru/catalog/repair10/catalog?appType=1&cat=128968&curr=rub&dest=-1257786&page=1&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&uclusters=0headers=headers&page={page}'
    url = f'{url}{page}'

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.ru',
        'Referer': 'https://www.wildberries.ru/catalog/dlya-remonta/instrumenty-i-osnastka/sverlenie-dolblenie-zakruchivanie',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(url=url, headers=headers, proxies=proxies, timeout=60)

    return response.json()


def prepare_items(response):
    products = []

    products_raw = response.get('data', {}).get('products', None)

    if products_raw != None and len(products_raw) > 0:
        for product in products_raw:
            if float(product.get('salePriceU', None)) / 100 > 1000:
                products.append({
                    'Бренд': product.get('brand', None),
                    'Наименование': product.get('name', None),
                    'Цена со скидкой': float(product.get('salePriceU', None)) / 100 if
                    product.get('salePriceU', None) != None else None,
                    'Артикул, id': product.get('id', None),
                })

    return products


def hoarder(url, page):
    response = get_category(url, page)
    products = prepare_items(response)

    return products
