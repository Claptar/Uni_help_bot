import telebot
import requests
from telebot.types import Message

base_url = 'https://api.telegram.org/bot838117295:AAGUldfunZu6Cyx-kJkCucQuH3pCLBD4Jcg/'
TOKEN = '838117295:AAGUldfunZu6Cyx-kJkCucQuH3pCLBD4Jcg'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(func=lambda message: True)
def upper(message: Message):
    bot.reply_to(message, message.text.upper())


bot.polling()
