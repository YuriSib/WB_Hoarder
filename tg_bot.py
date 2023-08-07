import telebot
import os
import time
from openpyxl import Workbook, load_workbook

from selenium.common.exceptions import InvalidArgumentException

from main import save_in_excel, pars_and_save, changes_prise_in_table, find_value_row, timing
from collecting import hoarder
from table_compared import compared, timing_decorator
from search_sale import vi_sale, ozon_sale, kuvalda_sale, ya_search

bot = telebot.TeleBot('6419841809:AAFEiToc-LKefUbh7nkzEiusYGnHgA0NAK8')


@bot.message_handler(commands=['start'])
def test(message_):
    chat_id = message_.chat.id
    bot.reply_to(message_, f"Your chat ID is: {chat_id}")


def message(name, id_, percent_, old_price, new_price, other_price_, mp_name, shops_name):
    bot.send_message(674796107, f'Товар: {name}, \n id: {id_} \n '
                                f'упал в цене на {percent_}%. \n'
                                f'Было: {old_price} руб., стало: {new_price}руб.\n'
                                f'На {mp_name} найдено: {shops_name},\n'
                                f'стоимость: {other_price_} рублей \n'
                                f' разница {(other_price_ - new_price) / new_price * 100}%')


def collecting(original, compared_, percent, sleep):
    bot.send_message(674796107, "Бот запущен!")
    if os.path.exists(original):
        while True:
            # if os.path.exists(compared_):
            #     os.remove(compared_)
            # pars_and_save(compared_)
            list_dumping = compared(original_table, compared_, percent)
            print(f'Позиций к обработке : {len(list_dumping)}')
            count_position = 0
            for product in list_dumping:
                count_position += 1
                print(f'Идет обработка {count_position} позиции, осталось {len(list_dumping) - count_position}')
                # чтобы код работал быстрее, нужно сделать в нумерацию строк в таблице, тогда не
                # придется вызывать функцию find_value_row
                row = find_value_row(original, product[1])
                links, link_vi, link_ozon, link_kuvalda = ya_search(product[0], 50)
                price, name = kuvalda_sale(link_kuvalda) if link_kuvalda != [] else 0
                if price > product[4]:
                    message(product[0], product[1], product[2], product[3], product[4], price, 'Кувалде', name)
                else:
                    changes_prise_in_table(original, row, 3, price)
                if price == 0:
                    price, name = vi_sale(link_vi) if link_vi != [] else 0
                    if price > product[4]:
                        message(product[0], product[1], product[2], product[3], product[4], price, 'ВсеИнструменты', name)
                    else:
                        changes_prise_in_table(original, row, 3, price)
                if price == 0:
                    price, name = ozon_sale(link_ozon) if link_ozon != [] else 0
                    if price > product[4]:
                        message(product[0], product[1], product[2], product[3], product[4], price, 'Озон', name)
                    else:
                        changes_prise_in_table(original, row, 3, price)
                if price == 0:
                    changes_prise_in_table(original, row, 3, product[4])
            sleep_min = int(sleep / 60)
            print(f'Итерация завершена, ожидание, {sleep_min} минут.')
            for min_ in range(1, sleep_min + 1):
                time.sleep(60)
                print(f'До новой итерации осталось: {sleep_min - min_} мин.')
            time.sleep(sleep)
    else:
        pars_and_save(original)
        sleep_min = int(sleep / 60)
        print(f'Ожидание: {sleep_min} минут.')
        for min_ in range(1, sleep_min + 1):
            time.sleep(60)
            print(f'До новой итерации осталось: {sleep_min - min_} мин.')


original_table = 'original.xlsx'
compared_table = 'compared.xlsx'

try:
    collecting(original_table, compared_table, 20, 600)
except KeyboardInterrupt:
    bot.send_message(674796107, "Бот выключен вручную.")
except Exception:
    bot.send_message(674796107, "Бот был выключен из-за ошибки!")
    raise Exception

bot.polling(none_stop=True)