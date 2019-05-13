import os
import random
import telebot
from telebot.types import Message
from telebot import types
import pandas as pd
import numpy as np
import math_part
import exam_timetable


base_url = 'https://api.telegram.org/bot838117295:AAGUldfunZu6Cyx-kJkCucQuH3pCLBD4Jcg/'
TOKEN = '838117295:AAGUldfunZu6Cyx-kJkCucQuH3pCLBD4Jcg'
PATH = os.path.abspath('')
bot = telebot.TeleBot(TOKEN)
MESSAGE_NUM = 0
MESSAGE_COM = ''
Q_NUM = 0

comms = ['help', 'start', 'flash_cards', 'figure_mnk', 'figure', 'mnk_constants', 'timetable', 'exam']

crazy_tokens = 0
emoji = ['😀','😬','😁','😂','😃','👿','😈','😴','🤧','🤢','🤮','🤒','🤕','😷','🤐','🤯','😲','😵','🤩','😭','😓','🤤','😪','😥','😢','😧','😦','😄','🤣','😅','😆','😇','😉','😊','🙂','🙃','☺','😋','😌','😍','😘','😗','😙','😚','🤪','😜','😝','😛','🤑','😎','🤓','🧐','🤠','🤗','🤡','😏','😶','😐','😑','😒','🙄','🤨','🤔','🤫','🤭','🤥','😳','😞','😟','😠','😡','🤬','😔','😕','🙁','☹','😣','😖','😫','😩','😤','😮','😱','😨','😰','😯','😦','😧','😢','😥','😪','🤤','😓','😭','🤩']


@bot.message_handler(commands=['help'])
def help_def(message):
    bot.send_message(message.chat.id, 'Сейчас я расскажу чем я могу тебе помочь ☺️\n'
                                      '/figure - Хочешь построить график по точкам ? Не вопрос !\n'
                                      '/figure_mnk - Хочешь построить график линеаризованный по мнк ? Запросто !\n'
                                      '/mnk_constants - Нужно посчитать константы прямой по мнк ? Я помогу !\n'
                                      '/timetable - Забыл расписание ?) Бывает, пиши, я помогу 😉📱📱📱'
                                      '\n/exam - Подскажу расписание экзаменов, но ты сам захотел...'
                                      ' Я не люблю напоминать'
                                      'о плохом...\n'
                                      '/flash_cards - Давай сыграем в игру... Я тебе определение/формулировку, а ты мне'
                                      '"знаю/не знаю.')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет-привет 🙃 Я очень люблю помогать людям,'
                                      ' напиши /help чтобы узнать, что я умею. ')


@bot.message_handler(commands=['flash_cards'])
def start(message):
    bot.send_message(message.chat.id, 'Хочешь вспомнить парочку определений ?)📚📚')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Матан']])
    msg = bot.send_message(message.chat.id, 'Сперва выбери предмет', reply_markup=keyboard)
    bot.register_next_step_handler(msg, subject)


def subject(message):
    global Q_NUM, PATH
    if (message.text == 'Матан') or (message.text == 'Ещё'):
        Q_NUM = random.randint(0, 13)
        questions = pd.read_excel(f'{PATH}/flash_cards/math/flash_data.xlsx', header=None)
        d = np.array(questions)
        question = d[Q_NUM, 0]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Покажи']])
        msg = bot.send_message(message.chat.id, question, reply_markup=keyboard)
        bot.register_next_step_handler(msg, answer)
    if message.text == 'Всё, хватит':
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Возвращайся ещё !', reply_markup=keyboard)


def answer(message):
    global Q_NUM
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Ещё', 'Всё, хватит']])
    bot.send_message(message.chat.id, 'Правильный ответ:')
    with open(f'{PATH}/flash_cards/math/{Q_NUM + 1}.png', 'rb') as photo:
        msg = bot.send_photo(message.chat.id, photo, reply_markup=keyboard)
    bot.register_next_step_handler(msg, subject)


@bot.message_handler(commands=['figure_mnk'])
def figure_mnk(message):
    global MESSAGE_COM
    bot.send_message(message.chat.id, 'Снова лабки делаешь?) Ох уж эти линеаризованные графики!...'
                                      'Сейчас быстренько всё построю, только тебе придётся ответить на пару вопросов'
                                      '😉. И не засиживайся, ложись спать))')
    msg = bot.send_message(message.chat.id, 'Скажи, как мне подписать ось х?')
    MESSAGE_COM = 'figure_mnk'
    bot.register_next_step_handler(msg, ax_x)


@bot.message_handler(commands=['mnk_constants'])
def mnk_constants(message):
    global MESSAGE_COM
    msg = bot.send_message(message.chat.id, 'Хочешь узнать константы прямых по МНК ?)'
                                            ' Даа, непростая задача, так и быть, помогу тебе!')
    MESSAGE_COM = 'mnk_constants'
    bot.register_next_step_handler(msg, tit)


@bot.message_handler(commands=['figure'])
def figure(message):
    global MESSAGE_COM
    MESSAGE_COM = 'figure'
    bot.send_message(message.chat.id, 'Ой, а что это у тебя за зависимость такая?) Мне даже самому интересно стало.'
                                      ' Сейчас быстренько всё построю, только тебе придётся ответить на пару вопросов'
                                      '😉))')
    msg = bot.send_message(message.chat.id, 'Скажи, как мне подписать ось х ?')
    bot.register_next_step_handler(msg, ax_x)


def ax_x(message):
    math_part.LABEL_X = message.text
    msg = bot.send_message(message.chat.id, 'А как мне подписать ось у ?')
    bot.register_next_step_handler(msg, ax_y)


def ax_y(message):
    math_part.LABEL_Y = message.text
    msg = bot.send_message(message.chat.id, 'Самое главное: как мне назвать график ?')
    bot.register_next_step_handler(msg, tit)


def tit(message):
    if message.text == 'Видимо не в этот раз ...':
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ну ладно... 😥', reply_markup=keyboard)
    else:
        if message.text == 'Попробую ещё раз':
            keyboard = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Давай попробуем ещё раз😔', reply_markup=keyboard)
        math_part.TITLE = message.text
        bot.send_message(message.chat.id, 'Отправь мне файл с данными вот в таком формате, и всё будет готово😊')
        with open('example.jpg', 'rb') as photo:
            msg = bot.send_photo(message.chat.id, photo)
        bot.register_next_step_handler(msg, date_mnk)


def date_mnk(message):
    try:
        global MESSAGE_COM
        file_id = message.json.get('document').get('file_id')
        file_path = bot.get_file(file_id).file_path
        downloaded_file = bot.download_file(file_path)
        src = message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        a, b, d_a, d_b = math_part.mnk_calc(src)

        if MESSAGE_COM == 'figure_mnk':

            math_part.plots_drawer(src, math_part.LABEL_X, math_part.LABEL_Y, math_part.TITLE)

            with open('plot.png', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)

            for i in range(0, len(a)):
                bot.send_message(message.chat.id, f'Коэффициенты {i + 1}-ой прямой:\n'
                f' a = {round(a[i], 3)} +- {round(d_a[i], 3)}\n'
                f' b = {round(b[i], 3)} +- {round(d_b[i], 3)}')
            os.remove('plot.png')

        elif MESSAGE_COM == 'figure':

            math_part.plot_drawer(src, math_part.LABEL_X, math_part.LABEL_Y, math_part.TITLE)

            with open('plot.png', 'rb') as photo:

                bot.send_photo(message.chat.id, photo)

            os.remove('plot.png')

        elif MESSAGE_COM == 'mnk_constants':

            for i in range(0, len(a)):
                bot.send_message(message.chat.id, f'Коэффициенты {i + 1}-ой прямой:\n'
                f' a = {round(a[i], 3)} +- {round(d_a[i], 3)}\n'
                f' b = {round(b[i], 3)} +- {round(d_b[i], 3)}')
        os.remove(src)
        math_part.TITLE = ''
        math_part.LABEL_Y = ''
        math_part.LABEL_X = ''
    except Exception as e:
        print(e)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Попробую ещё раз', 'Видимо не в этот раз ...']])
        msg = bot.send_message(message.chat.id,
                               'Что-то не получилось... Проверь файл, который ты прислал😨 ', reply_markup=keyboard)
        bot.register_next_step_handler(msg, tit)


@bot.message_handler(commands=['timetable'])
def schedule(message):
    bot.send_message(message.chat.id, 'Снова не можешь вспомнить номер кабинета или какая следующая пара?)'
                                      'Ничего, я уже тут!')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['1 группа', 'Общее расписание']])
    msg = bot.send_message(message.chat.id, 'Чьё расписание ты хочешь узнать?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, answer)


def answer(message):
    if (message.text == '1 группа'):
        bot.send_message(message.chat.id, 'Держи!')
        with open('timetable_for_our_group.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, 'Держи!')
        with open('timetable_for_all.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    keyboard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Чем я ещё могу помочь?', reply_markup=keyboard)


@bot.message_handler(commands=['exam'])
def ask_group(message):
    bot.send_message(message.chat.id, 'А из какой ты группы?')
    bot.register_next_step_handler(message, get_exam_timetable)


def get_exam_timetable(message):
    exam_timetable.get_timetable(message.text)
    f = open('exam.txt')
    for line in f:
        bot.send_message(message.chat.id, line)
    open('exam.txt', 'w').close()


# Если отправить боту просто текст или незнакомую команду, то он ответит так:
@bot.message_handler(content_types=['text'])
def chatting(message):
    global crazy_tokens
    crazy_tokens += 1
    if crazy_tokens <= 2:
        bot.send_message(message.chat.id, 'Боюсь, я не совсем понимаю, о чём ты. \n' 
                                          'Напиши /help, чтобы узнать, что я умею.\n')
    elif crazy_tokens <= 7:
        bot.send_message(message.chat.id, random.choice(emoji))
    elif crazy_tokens == 8:
        bot.send_message(message.chat.id, random.choice(emoji))
        crazy_tokens = 0


bot.polling()
