import telebot
import os

from main import save_in_excel, pars_and_save
from collecting import hoarder
from table_compared import compared

bot = telebot.TeleBot('6419841809:AAFEiToc-LKefUbh7nkzEiusYGnHgA0NAK8')


@bot.message_handler(commands=['start'])
def test(message):
    chat_id = message.chat.id
    bot.reply_to(message, f"Your chat ID is: {chat_id}")


bot.send_message(674796107, "Произошло какое-то событие!")


original_table = 'original.xlsx'
compared_table = 'compared.xlsx'


while True:
    pars_and_save(compared_table)
    list_dumping = compared(original_table, compared_table, 1)
    for product in list_dumping:
        bot.send_message(674796107, f'Товар: {product[0]}, id: {product[1]} \n упал в цене на {product[2]} %. \n'
                                    f'Было: {product[3]} руб., стало: {product[4]} руб.')
    os.remove(compared_table)


bot.polling(none_stop=True)