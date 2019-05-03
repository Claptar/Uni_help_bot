import telebot
from telebot.types import Message

base_url = 'https://api.telegram.org/bot838117295:AAGUldfunZu6Cyx-kJkCucQuH3pCLBD4Jcg/'
TOKEN = '838117295:AAGUldfunZu6Cyx-kJkCucQuH3pCLBD4Jcg'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(func=lambda message: True)
def upper(message: Message):
    if message.document is not None:
        bot.send_message(message.chat.id, 'Это документ')
    if message.text is not None:
        bot.send_message(message.chat.id, 'Это текст')


@bot.message_handler(func=lambda message: True, content_types='document')
def document_getter(message: Message):
    if message.document is not None:
        bot.send_message(message.chat.id, 'Это документ')
    file_id = message.json.get('document').get('file_id')
    file_path = bot.get_file(file_id).file_path
    downloaded_file = bot.download_file(file_path)
    src = '/home/claptar/PycharmProjects/MNK-Tool/down/' + message.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)


bot.polling()
