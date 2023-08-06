import telebot
import os
import time
from openpyxl import Workbook, load_workbook

from selenium.common.exceptions import InvalidArgumentException

from main import save_in_excel, pars_and_save, changes_prise_in_table, find_value_row, timing
from collecting import hoarder
from table_compared import compared, timing_decorator
from search_sale import vi_sale, ya_search

bot = telebot.TeleBot('6419841809:AAFEiToc-LKefUbh7nkzEiusYGnHgA0NAK8')


@bot.message_handler(commands=['start'])
def test(message):
    chat_id = message.chat.id
    bot.reply_to(message, f"Your chat ID is: {chat_id}")


def message(name, id_, percent_, old_price, new_price, other_price_, mp_name):
    bot.send_message(674796107, f'Товар: {name}, \n id: {id_} \n '
                                f'упал в цене на {percent_}%. \n'
                                f'Было: {old_price} руб., стало: {new_price}руб.\n'
                                f'Цена на {mp_name}: {other_price_} руб.,'
                                f' разница {(other_price_ - new_price) / new_price * 100}%')


def collecting(original, compared_, percent, sleep):
    bot.send_message(674796107, "Бот запущен!")
    if os.path.exists(original):
        while True:
            # if os.path.exists(compared_):
            #     os.remove(compared_)
            # pars_and_save(compared_)
            list_dumping = compared(original_table, compared_, percent)
            for product in list_dumping:
                row = find_value_row(original, product[1])
                link_vi, link_ozon = ya_search(product[0], 50)
                vi_price = vi_sale(link_vi) if link_vi != [] else 0
                if vi_price == 0:
                    ozon_price = vi_sale(link_ozon) if link_ozon != [] else 0
                else:
                    ozon_price = 0
                if vi_price != 0:
                    changes_prise_in_table(original, row, 3, vi_price)
                    if vi_price > product[4]:
                        message(product[0], product[1], product[2], product[3], product[4], vi_price, 'ВсеИнструменты')
                    else:
                        changes_prise_in_table(original, row, 3, product[4])
                elif ozon_price != 0:
                    changes_prise_in_table(original, row, 3, ozon_price)
                    if ozon_price > product[4]:
                        message(product[0], product[1], product[2], product[3], product[4], vi_price, 'Ozon')
                    else:
                        row = find_value_row(original, product[1])
                        changes_prise_in_table(original, row, 3, product[4])
                else:
                    changes_prise_in_table(original, row, 3, product[4])
                    message(product[0], product[1], product[2], product[3], product[4], 0, 'Не найдено')

            time.sleep(sleep)
    else:
        pars_and_save(original)
        time.sleep(sleep)


original_table = 'original.xlsx'
compared_table = 'compared.xlsx'

collecting(original_table, compared_table, 20, 1200)


bot.polling(none_stop=True)