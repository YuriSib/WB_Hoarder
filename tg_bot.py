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


def message(name, id_, percent_, old_price, new_price, other_price_, mp_name):
        bot.send_message(674796107, f'Товар: {name}, \n id: {id_} \n '
                                    f'упал в цене на {percent_}%. \n'
                                    f'Было: {old_price} руб., стало: {new_price}руб.\n'
                                    f'На {mp_name} найден похожий товар,\n'
                                    f'минимальная стоимость: {other_price_} рублей \n'
                                    f' разница {(other_price_ - new_price) / new_price * 100}%')


def sleep(time_):
    print(f'Итерация завершена, ожидание, {time_} минут.')
    for min_ in range(1, time_ + 1):
        time.sleep(60)
        print(f'До новой итерации осталось: {time_ - min_} мин.')


def collecting(url, original, compared_, percent):
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
            price_kuvalda = kuvalda_sale(link_kuvalda) if link_kuvalda != [] else 99999
            price_vi = vi_sale(link_vi) if link_vi != [] else 99999
            # price_ozon = ozon_sale(link_ozon) if link_ozon != [] else 99999
            price = min(price_kuvalda, price_vi)
            if price != 99999:
                if price > product[4] * 1.25:
                    message(product[0], product[1], product[2], product[3], product[4], price, 'Маркетплейсах')
                    changes_prise_in_table(original, row, 3, product[4])
                else:
                    changes_prise_in_table(original, row, 3, price) if price < product[4] else \
                        changes_prise_in_table(original, row, 3, product[4])
            else:
                changes_prise_in_table(original, row, 3, product[4])
    else:
        pars_and_save(url, original)


original_table, compared_table = 'original.xlsx', 'compared.xlsx'
zubr1_1, zubr1_2 = 'zubr1_1.xlsx', 'zubr1_2.xlsx'
zubr2_1, zubr2_2 = 'zubr2_1.xlsx', 'zubr2_2.xlsx'
interskol1, interskol2 = 'interskol1.xlsx', 'interskol2.xlsx'
sturm1, sturm2 = 'sturm1.xlsx', 'sturm2.xlsx'
resanta1, resanta2 = 'resanta1.xlsx', 'resanta2.xlsx'
denzel1, denzel2 = 'denzel1.xlsx', 'denzel2.xlsx'



url_1 = f'https://catalog.wb.ru/catalog/repair10/catalog?appType=1&cat=128968&curr=rub&dest=-1257786&page=1&' \
        f'regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&uclusters=0' \
        f'headers=headers&page='
url_interskol = 'https://catalog.wb.ru/brands/%D0%B8/catalog?appType=1&brand=9084&curr=rub&dest=-1257786&' \
        'regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&' \
        'uclusters=0headers=headers&page='
url_zubr_1 = 'https://catalog.wb.ru/brands/%D0%B7/catalog?appType=1&brand=54220&curr=rub&dest=-1257786&fsupplier=67861;' \
             '218978&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=rate&sort=rate&spp=0' \
             '&subject=2221;2224&page='
url_zubr_2 = 'https://catalog.wb.ru/brands/%D0%B7/catalog?appType=1&brand=54220&curr=rub&dest=-1257786&fsupplier=67861;' \
             '218978&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&sort=rate' \
             '&spp=0&subject=1569;3748;2540;770;1164;4998;926;4080;2441;2297;3717;1165;1166;1169;2070;4084;2668;2995;' \
             '2183;1318;2194;4160;3968;2550;986;2341;1362;1168;1337;2197;1170;1171&page='
url_sturm = 'https://catalog.wb.ru/brands/s/catalog?appType=1&brand=36933&curr=rub&dest=-1257786&regions=80,38,83,4,' \
            '64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&page='
url_resanta = 'https://catalog.wb.ru/brands/%D1%80/catalog?appType=1&brand=15488&curr=rub&dest=-1257786&regions=' \
               '80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&page='
url_denzel = 'https://catalog.wb.ru/brands/d/catalog?appType=1&brand=46232&curr=rub&dest=-1257786&regions=' \
             '80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&sort=popular&spp=0&page='


bot.send_message(674796107, "Бот запущен!")

try:
    while True:
        collecting(url_1, original_table, compared_table, 10)
        collecting(url_zubr_1, zubr1_1, zubr1_2, 10)
        collecting(url_zubr_2, zubr2_1, zubr2_2, 10)
        collecting(url_interskol, interskol1, interskol2, 10)
        collecting(url_sturm, sturm1, sturm2, 10)
        collecting(url_resanta, resanta1, resanta2, 10)
        collecting(url_denzel, denzel1, denzel2, 10)
        sleep(15)
except KeyboardInterrupt:
    bot.send_message(674796107, "Бот выключен вручную.")
except Exception:
    bot.send_message(674796107, "Бот был выключен из-за ошибки!")
    raise Exception
