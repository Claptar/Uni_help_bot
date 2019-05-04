import os
import telebot
from telebot.types import Message
import math_part


base_url = 'https://api.telegram.org/bot838117295:AAGUldfunZu6Cyx-kJkCucQuH3pCLBD4Jcg/'
TOKEN = '838117295:AAGUldfunZu6Cyx-kJkCucQuH3pCLBD4Jcg'
bot = telebot.TeleBot(TOKEN)
MESSAGE_NUM = 0
MESSAGE_COM = ''


@bot.message_handler(commands=['help'])
def mnk_constants(message):
    bot.send_message(message.chat.id, 'Сейчас я расскажу чем я могу тебе помочь ☺️\n'
                                      '/figure - Хочешь построить график по точкам ? Не вопрос !\n'
                                      '/figure_mnk - Хочешь построить график линеаризованный по мнк ? Запросто !\n'
                                      '/mnk_constants - Нужно посчитать константы прямой по мнк ? Я помогу !\n'
                                      '/schedule - Забыл расписание ?) Бывает, пиши, я помогу 😉📱📱📱')


@bot.message_handler(commands=['start'])
def mnk_constants(message):
    bot.send_message(message.chat.id, 'Привет-привет 🙃 Я очень люблю помогать людям,'
                                      ' напиши /help чтобы узнать, что я умею. ')


@bot.message_handler(commands=['figure'])
def mnk_constants(message):
    global MESSAGE_NUM, MESSAGE_COM
    bot.send_message(message.chat.id, 'Ой, а что это у тебя за зависимость такая?) Мне даже самому интересно стало.'
                                      ' Сейчас быстренько всё построю, только тебе придётся ответить на пару вопросов'
                                      '😉))')
    bot.send_message(message.chat.id, 'Скажи, как мне подписать ось х ?')
    MESSAGE_NUM = 1
    MESSAGE_COM = 'figure'


@bot.message_handler(commands=['figure_mnk'])
def mnk_constants(message):
    global MESSAGE_NUM, MESSAGE_COM
    bot.send_message(message.chat.id, 'Снова лабки делаешь ?) Ох уж эти линеаризованные графики !...'
                                      ' Сейчас быстренько всё построю, только тебе придётся ответить на пару вопросов'
                                      '😉. И не засиживайся, ложись спать))')
    bot.send_message(message.chat.id, 'Скажи, как мне подписать ось х ?')
    MESSAGE_NUM = 1
    MESSAGE_COM = 'figure_mnk'


@bot.message_handler(commands=['mnk_constants'])
def mnk_constants(message):
    global MESSAGE_COM
    bot.send_message(message.chat.id, 'Хочешь узнать константы прямых по МНК ?) Даа, непростая задача, так и быть,'
                                      'помогу тебе ! Только пришли мне данные вот в таком формате 😉')
    with open('example.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    MESSAGE_COM = 'mnk_constants'


@bot.message_handler(commands=['schedule'])
def schedule(message):
    bot.send_message(message.chat.id, 'Снова не можешь вспомнить номер кабинета или какая следующая пара ?)'
                                      'Ничего, я уже тут !')
    with open('schedule.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(func=lambda message: True)
def figure_prepare(message: Message):
    global MESSAGE_NUM
    if MESSAGE_NUM == 1:
        math_part.LABEL_X = message.text
        bot.send_message(message.chat.id, 'А, как мне подписать ось у ?')
        MESSAGE_NUM += 1
    elif MESSAGE_NUM == 2:
        math_part.LABEL_Y = message.text
        bot.send_message(message.chat.id, 'Самое главное: как мне назвать график ?')
        MESSAGE_NUM += 1
    elif MESSAGE_NUM == 3:
        math_part.TITLE = message.text
        bot.send_message(message.chat.id, 'А теперь пришли файл с данными вот в таком формате')
        with open('example.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)


@bot.message_handler(func=lambda message: True, content_types='document')
def document_getter(message: Message):
    global MESSAGE_COM, MESSAGE_NUM
    file_id = message.json.get('document').get('file_id')
    file_path = bot.get_file(file_id).file_path
    downloaded_file = bot.download_file(file_path)
    src = message.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    a, b, d_a, d_b = math_part.mnk_calc(src)

    if MESSAGE_COM == 'figure_mnk':

        math_part.plots_drawer(src, math_part.LABEL_X, math_part.LABEL_Y, math_part.TITLE)

        with open('plot.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)

        for i in range(0, len(a)):
            bot.send_message(message.chat.id, f'Коэффициенты {i + 1}-ой прямой:\n'
            f' a = {round(a[i], 3)} +- {round(d_a[i], 3)}\n'
            f' b = {round(b[i], 3)} +- {round(d_b[i], 3)}')
        os.remove('plot.jpg')

    elif MESSAGE_COM == 'figure':

        math_part.plot_drawer(src, math_part.LABEL_X, math_part.LABEL_Y, math_part.TITLE)

        with open('plot.jpg', 'rb') as photo:

            bot.send_photo(message.chat.id, photo)

        os.remove('plot.jpg')

    elif MESSAGE_COM == 'mnk_constants':

        for i in range(0, len(a)):

            bot.send_message(message.chat.id, f'Коэффициенты {i + 1}-ой прямой:\n'
            f' a = {round(a[i], 3)} +- {round(d_a[i], 3)}\n'
            f' b = {round(b[i], 3)} +- {round(d_b[i], 3)}')

    os.remove(src)
    math_part.TITLE = ''
    math_part.LABEL_Y = ''
    math_part.LABEL_X = ''
    MESSAGE_NUM = 0


bot.polling()
