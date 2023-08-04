import telebot
import os
import time

from selenium.common.exceptions import InvalidArgumentException

from main import save_in_excel, pars_and_save, changes_prise_in_table, find_value_row
from collecting import hoarder
from table_compared import compared
from search_sale import vi_sale, ya_search

bot = telebot.TeleBot('6419841809:AAFEiToc-LKefUbh7nkzEiusYGnHgA0NAK8')


@bot.message_handler(commands=['start'])
def test(message):
    chat_id = message.chat.id
    bot.reply_to(message, f"Your chat ID is: {chat_id}")


def collecting(original, compared_, percent, sleep):
    bot.send_message(674796107, "Бот запущен!")
    if os.path.exists(original):
        while True:
            # if os.path.exists(compared_table):
            #     os.remove(compared_)
            # pars_and_save(compared_)
            list_dumping = compared(original_table, compared_, percent)
            for product in list_dumping:
                try:
                    vi_price = vi_sale(ya_search(product[0]))
                    if vi_price > product[4]:
                        bot.send_message(674796107, f'Товар: {product[0]}, \n id: {product[1]} \n '
                                                    f'упал в цене на {product[2]}%. \n'
                                                    f'Было: {product[3]} руб., стало: {product[4]}руб.\n'
                                                    f'Цена на ВсеИнструменты: {vi_price} руб.,'
                                                    f' разница {(vi_price - product[0]) / product[0] * 100}%')
                    else:
                        row = find_value_row(original, product[1])
                        changes_prise_in_table(original, row, 3, product[4])
                except InvalidArgumentException:
                    print('Не удалось найти товар!')
                    bot.send_message(674796107, f'Товар: {product[0]}, \n id: {product[1]} \n '
                                                f'упал в цене на {product[2]}%. \n'
                                                f'Было: {product[3]} руб., стало: {product[4]}руб.\n')

            time.sleep(sleep)
    else:
        pars_and_save(original)
        time.sleep(sleep)


original_table = 'original.xlsx'
compared_table = 'compared.xlsx'

collecting(original_table, compared_table, 20, 1200)


bot.polling(none_stop=True)