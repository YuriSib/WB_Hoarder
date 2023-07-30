import telebot

from main import second_save
from collecting import hoarder

bot = telebot.TeleBot('6419841809:AAFEiToc-LKefUbh7nkzEiusYGnHgA0NAK8')

@bot.message_handler(commands=['start'])
def main(message):
    chat_id = message.chat.id
    bot.reply_to(message, f"Your chat ID is: {chat_id}")

bot.send_message(674796107, "Произошло какое-то событие!")

bot.polling(none_stop=True)

original_table = 'original.xlsx'
compared_table = 'compared.xlsx'

hoarder()
second_save()
