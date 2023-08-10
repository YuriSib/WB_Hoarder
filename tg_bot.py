import telebot
import os
import time

from main import pars_and_save, changes_prise_in_table, find_value_row, timing
from table_compared import compared, timing_decorator
from search_sale import vi_sale, ozon_sale, kuvalda_sale, ya_search

bot = telebot.TeleBot('6419841809:AAFEiToc-LKefUbh7nkzEiusYGnHgA0NAK8')


@bot.message_handler(commands=['start'])
def test(message_):
    chat_id = message_.chat.id
    bot.reply_to(message_, f"Your chat ID is: {chat_id}")


def handle_exceptions(bot_):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                bot_.send_message(674796107, "Бот выключен вручную.")
            except Exception:
                bot_.send_message(674796107, "Бот был выключен из-за ошибки!")
                raise Exception
        return wrapper
    return decorator


def message(name, id_, percent_, old_price, new_price, other_price_, mp_name):
        bot.send_message(674796107, f'Товар: {name}, \n id: {id_} \n '
                                    f'упал в цене на {percent_}%. \n'
                                    f'Было: {old_price} руб., стало: {new_price}руб.\n'
                                    f'На {mp_name} найден похожий товар,\n'
                                    f'стоимость: {other_price_} рублей \n'
                                    f' разница {(other_price_ - new_price) / new_price * 100}%')


@handle_exceptions(bot)
def collecting(url, original, compared_, percent, sleep):
    if os.path.exists(original):
        if os.path.exists(compared_):
            os.remove(compared_)
        pars_and_save(url, compared_)
        list_dumping = compared(original_table, compared_, percent)
        print(f'Позиций к обработке : {len(list_dumping)}')
        count_position = 0
        for product in list_dumping:
            count_position += 1
            print(f'Идет обработка {count_position} позиции, осталось {len(list_dumping) - count_position}')
            row = product[5] + 2
            links, link_vi, link_ozon, link_kuvalda = ya_search(product[0], 50)
            price = kuvalda_sale(link_kuvalda) if link_kuvalda != [] else False
            if price:
                if price > product[4] * 1.3:
                    message(product[0], product[1], product[2], product[3], product[4], price, 'Кувалде')
                    changes_prise_in_table(original, row, 3, product[4])
                else:
                    changes_prise_in_table(original, row, 3, price)
            else:
                price = vi_sale(link_vi) if link_vi != [] else False
                if price:
                    if price > product[4] * 1.3:
                        message(product[0], product[1], product[2], product[3], product[4], price, 'ВсеИнструменты')
                        changes_prise_in_table(original, row, 3, product[4])
                    else:
                        changes_prise_in_table(original, row, 3, price)
                else:
                    price = ozon_sale(link_ozon) if link_ozon != [] else 0
                    if price:
                        if price > product[4] * 1.3:
                            message(product[0], product[1], product[2], product[3], product[4], price, 'Озоне')
                            changes_prise_in_table(original, row, 3, product[4])
                        else:
                            changes_prise_in_table(original, row, 3, price)
                    else:
                        changes_prise_in_table(original, row, 3, product[4])
        sleep_min = int(sleep / 60)
        print(f'Итерация завершена, ожидание, {sleep_min} минут.')
        for min_ in range(1, sleep_min + 1):
            time.sleep(60)
            print(f'До новой итерации осталось: {sleep_min - min_} мин.')
    else:
        pars_and_save(url, original)
        sleep_min = int(sleep / 60)
        print(f'Ожидание: {sleep_min} минут.')
        for min_ in range(1, sleep_min + 1):
            time.sleep(60)
            print(f'До новой итерации осталось: {sleep_min - min_} мин.')


original_table = 'original.xlsx'
compared_table = 'compared.xlsx'
interskol_1 = 'interskol_1.xlsx'
interskol_2 = 'interskol_2.xlsx'

url_1 = f'https://catalog.wb.ru/catalog/repair10/catalog?appType=1&cat=128968&curr=rub&dest=-1257786&page=1&' \
        f'regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&uclusters=0' \
        f'headers=headers&page='
url_2 = 'https://catalog.wb.ru/brands/%D0%B8/catalog?appType=1&brand=9084&curr=rub&dest=-1257786&' \
        'regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&' \
        'uclusters=0headers=headers&page='


while True:
    bot.send_message(674796107, "Бот запущен!")
    collecting(url_1, original_table, compared_table, 20, 300)
    collecting(url_2, interskol_1, interskol_2, 20, 300)

