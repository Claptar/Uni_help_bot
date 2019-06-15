import os
import random
import re

import numpy as np
import pandas as pd
import requests
import telebot
from telebot import types

import texting.texting_symbols
import timetable.timetable
from math_module import math_part

base_url = 'https://api.telegram.org/bot838117295:AAGUldfunZu6Cyx-kJkCucQuH3pCLBD4Jcg/'
TOKEN = '838117295:AAGUldfunZu6Cyx-kJkCucQuH3pCLBD4Jcg'
PATH = os.path.abspath('')
bot = telebot.TeleBot(TOKEN)
MESSAGE_NUM = 0
MESSAGE_COM = ''
Q_NUM = 0
PAR_NUM = 0
GROUP_NUM = ''
SUBJECT_NOW = ''
SUBJECTS_PATH = {
    'Матан': 'math',
    'Химия': 'chem_org'
}
SUBJECTS = {
    'Матан':
        {'Множество Rn': 1,
         'Предел и непрерывность': 2,
         'Дифференциальное исчисление в Rn': 3,
         'Интеграл Римана': 4,
         'Мера Жордана': 5,
         'Числовые ряды': 6},
    'Химия':
        {
            'Билеты 1-2': 1,
            'Билеты 3,5': 2,
            'Билеты 4,6': 3,
            'Билет 7': 4,
            'Билет 8': 5,
            'Билет 9': 6,
            'Билеты 10-11': 7,
            'Билет 12': 8,
            'Билет 13': 9,
            'Билет 14': 10,
            'Билет 15': 11,
            'Билет 16': 12,
            'Билет 17': 13,
            'Билет 18-19': 14,
            'Билет 20-21': 15,
            'Билет 22': 16,

        }
}

comms = ['help', 'start', 'flash_cards', 'figure_mnk', 'figure', 'mnk_constants', 'timetable', 'exam']

crazy_tokens = 0


@bot.message_handler(commands=['remove_button'])
def button_delete(message):
    try:
        keyboard = types.ReplyKeyboardRemove
        bot.send_message(message.chat.id, 'Убрал все кнопки !', reply_markup=keyboard)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Мне нечего убирать, никакой кнопки и так нет😉')


@bot.message_handler(commands=['help'])
def help_def(message):
    """
    Функция ловит сообщение с командой '/help' и присылает описание комманд бота
    :param message: telebot.types.Message
    :return:
    """
    bot.send_message(message.chat.id, 'Сейчас я расскажу, чем я могу тебе помочь ☺️\n'
                                      '/figure - Хочешь построить график по точкам ? Не вопрос !\n'
                                      '/figure_mnk - Хочешь построить график линеаризованный по МНК? Запросто !\n'
                                      '/mnk_constants - Нужно посчитать константы прямой по МНК? Я помогу !\n'
                                      '/timetable - Забыл расписание?) Бывает, пиши, я помогу 😉📱📱📱'
                                      '\n/exam - Подскажу расписание экзаменов, но ты сам захотел...'
                                      ' Я не люблю напоминать'
                                      'о плохом...\n'
                                      '/flash_cards - Давай сыграем в игру... Я тебе определение/формулировку, а '
                                      'ты попытайся вспомнить её. Как только вспомнишь/не вспомнишь нажимай "покажи"'
                                      'чтобы проверить себя\n'
                                      '/remove_button - Если что-то вдруг пошло не по плану, я уберу все кнопки')


@bot.message_handler(commands=['start'])
def start(message):
    """
    Функция ловит сообщение с коммандой '/start' и шлёт пользователю сообщение с приветсвием
    :param message: telebot.types.Message
    :return:
    """
    bot.send_message(message.chat.id, 'Привет-привет 🙃 Я очень люблю помогать людям,'
                                      ' напиши /help чтобы узнать, что я умею. ')


@bot.message_handler(commands=['flash_cards'])
def flash_cards(message):
    """
    Функция ловит сообщение с коммандой '/flash_cards' и запускает сессию этой функции
     отправляя кнопки с выбором предмета. Следующее сообщение отправляется в функцию subject
    :param message: telebot.types.Message
    :return:
    """
    bot.send_message(message.chat.id, 'Хочешь вспомнить парочку определений ?)📚📚')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in SUBJECTS.keys()])
    msg = bot.send_message(message.chat.id, 'Сначала выбери предмет', reply_markup=keyboard)
    bot.register_next_step_handler(msg, subject)


def subject(message):
    """
    Функция вызывается функцией start, в зависимости от выбора предмета пользователем функция предлагает
     параграфы этого предмета и вызывает функцию  paragraph()
    :param message: telebot.types.Message
    :return:
    """
    global Q_NUM, PATH, SUBJECT_NOW, SUBJECTS
    if message.text in SUBJECTS.keys():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in SUBJECTS[message.text].keys()])
        msg = bot.send_message(message.chat.id, 'Какой раздел ты хочешь поботать ?', reply_markup=keyboard)
        SUBJECT_NOW = message.text
        bot.register_next_step_handler(msg, paragraph)

    elif message.text == 'Выбрать другой параграф':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in SUBJECTS[SUBJECT_NOW].keys()])
        msg = bot.send_message(message.chat.id, 'Какой параграф ты хочешь поботать ?', reply_markup=keyboard)
        bot.register_next_step_handler(msg, paragraph)

    elif message.text == 'Всё, хватит' or message.text == 'В другой раз...':
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Возвращайся ещё !', reply_markup=keyboard)
        SUBJECT_NOW = ''

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Матан', 'В другой раз...']])
        msg = bot.send_message(message.chat.id, 'Извини, я тебя не понял, можешь повторить ?', reply_markup=keyboard)
        bot.register_next_step_handler(msg, subject)


def paragraph(message):
    """
    Функция вызывается функцией subject(). Она рандомно генерирует номер вопроса и присылает вопрос пользователю
    :param message: telebot.types.Message
    :return:
    """
    global Q_NUM, PATH, PAR_NUM, SUBJECTS, SUBJECT_NOW
    if (message.text in SUBJECTS[SUBJECT_NOW].keys()) or (message.text == 'Ещё'):
        if message.text in SUBJECTS[SUBJECT_NOW].keys():
            PAR_NUM = SUBJECTS[SUBJECT_NOW][message.text]
        questions = pd.read_excel(f'{PATH}/flash_cards/{SUBJECTS_PATH[SUBJECT_NOW]}/{PAR_NUM}/flash_data.xlsx',
                                  header=None)
        d = np.array(questions)
        Q_NUM = random.randint(0, len(d) - 1)
        question = d[Q_NUM, 0]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Покажи']])
        msg = bot.send_message(message.chat.id, question, reply_markup=keyboard)
        bot.register_next_step_handler(msg, answer)

    elif message.text == 'Всё, хватит' or message.text == 'В другой раз...':
        keyboard = types.ReplyKeyboardRemove()
        SUBJECT_NOW = ''
        bot.send_message(message.chat.id, 'Возвращайся ещё !', reply_markup=keyboard)

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Выбрать другой параграф', 'В другой раз...']])
        msg = bot.send_message(message.chat.id, 'Извини, я тебя не понял, можешь повторить ?', reply_markup=keyboard)
        bot.register_next_step_handler(msg, subject)


def answer(message):
    """
    Функция вызывается функцией paragraph(). Присылает пользователю ответ на вопрос.
    :param message: telebot.types.Message
    :return:
    """
    global Q_NUM, PAR_NUM
    if message.text == 'Покажи' or message.text == 'Покажи правильный ответ':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Ещё', 'Всё, хватит']])
        bot.send_message(message.chat.id, 'Правильный ответ:')
        with open(f'{PATH}/flash_cards/{SUBJECTS_PATH[SUBJECT_NOW]}/{PAR_NUM}/{Q_NUM + 1}.png', 'rb') as photo:
            msg = bot.send_photo(message.chat.id, photo, reply_markup=keyboard)
        bot.register_next_step_handler(msg, paragraph)
    elif message.text == 'Я не хочу смотреть ответ':
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ты не расстраивайся ! Все мы делаем ошибки...', reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Покажи правильный ответ', 'Я не хочу смотреть ответ']])
        msg = bot.send_message(message.chat.id,
                               'Извини, что-то не могу уловить твои мозговые волны... Попробуй ещё раз',
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, answer)


@bot.message_handler(commands=['figure_mnk'])
def figure_mnk(message):
    """
    Функция ловит сообщение с текстом '/figure_mnk'. Инициируется процесс рисования графика. Запускает функцию ax_x()
    :param message: telebot.types.Message
    :return:
    """
    global MESSAGE_COM
    bot.send_message(message.chat.id, 'Снова лабки делаешь ?) Ох уж эти линеаризованные графики !...'
                                      ' Сейчас быстренько всё построю, только тебе придётся ответить на пару вопросов'
                                      '😉. И не засиживайся, ложись спать))')
    msg = bot.send_message(message.chat.id, 'Скажи, как мне подписать ось х ?')
    MESSAGE_COM = 'figure_mnk'
    bot.register_next_step_handler(msg, ax_x)


@bot.message_handler(commands=['mnk_constants'])
def mnk_constants(message):
    """
    Функция ловит сообщение с текстом "/mnk_constants". Является первой функцией в сессии рисования графика.
    Вызывает ax_x()
    :param message: telebot.types.Message
    :return:
    """
    global MESSAGE_COM
    bot.send_message(message.chat.id, 'Хочешь узнать константы прямых по МНК ?)'
                                      ' Даа, непростая задача, так и быть, помогу тебе ! ')
    bot.send_message(message.chat.id, 'Пришли мне файл с данными вот в таком формате и всё будет готово😊')
    with open(f'{PATH}/math_module/example.jpg', 'rb') as photo:
        msg = bot.send_photo(message.chat.id, photo)
    MESSAGE_COM = 'mnk_constants'
    bot.register_next_step_handler(msg, date_mnk)


@bot.message_handler(commands=['figure'])
def figure(message):
    """
    Ловит сообщение с текстом "/figure". Является первой функцией в сессии рисования графика. Вызывает ax_x()
    :param message: telebot.types.Message
    :return:
    """
    global MESSAGE_COM
    MESSAGE_COM = 'figure'
    bot.send_message(message.chat.id, 'Ой, а что это у тебя за зависимость такая?) Мне даже самому интересно стало.'
                                      ' Сейчас быстренько всё построю, только тебе придётся ответить на пару вопросов'
                                      '😉))')
    msg = bot.send_message(message.chat.id, 'Скажи, как мне подписать ось х ?')
    bot.register_next_step_handler(msg, ax_x)


def ax_x(message):
    """
    Функция вызывается firure(), записывает введёное пользователем название оси Х
    :param message: telebot.types.Message
    :return:
    """
    math_part.LABEL_X = message.text
    msg = bot.send_message(message.chat.id, 'А, как мне подписать ось у ?')
    bot.register_next_step_handler(msg, ax_y)


def ax_y(message):
    """
    Функция вызывается ax_x(), записывает введённое пользователем название оси У, вызывает ax_y()
    :param message: telebot.types.Message
    :return:
    """
    math_part.LABEL_Y = message.text
    msg = bot.send_message(message.chat.id, 'Самое главное: как мне назвать график ?')
    bot.register_next_step_handler(msg, tit)


def tit(message):
    """
    Функция вызывается ax_x(), записывает введённое пользователем название графика, вызывает data_mnk()
    :param message:
    :return:
    """
    if message.text == 'Видимо не в этот раз ...':
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ну ладно... 😥', reply_markup=keyboard)
    else:
        if message.text == 'Попробую ещё раз':
            keyboard = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Давай попробуем ещё раз😔', reply_markup=keyboard)
        math_part.TITLE = message.text
        bot.send_message(message.chat.id, 'Пришли мне файл с данными вот в таком формате и всё будет готово😊')
        with open(f'{PATH}/math_module/example.jpg', 'rb') as photo:
            msg = bot.send_photo(message.chat.id, photo)
        bot.register_next_step_handler(msg, date_mnk)


def date_mnk(message):
    """
    Функция активирует рисование графика/линеаризованного графика/подсчёта констант и погрешностей, в зависимости от
    того, какая функция была написана пользователем.
    :param message:
    :return:
    """
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
            math_part.BOT_PLOT = True
            math_part.plots_drawer(src, math_part.LABEL_X, math_part.LABEL_Y, math_part.TITLE)
            with open('plot.png', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
            for i in range(0, len(a)):
                bot.send_message(message.chat.id, f"Коэффициенты {i + 1}-ой прямой:\n"
                                                  f" a = {a[i]} +- {d_a[i], 6}\n"
                                                  f" b = {b[i]} +- {d_b[i], 6}")
            os.remove('plot.png')
            math_part.BOT_PLOT = False
        elif MESSAGE_COM == 'figure':
            math_part.BOT_PLOT = True
            math_part.plot_drawer(src, math_part.LABEL_X, math_part.LABEL_Y, math_part.TITLE)
            with open('plot.png', 'rb') as photo:
                bot.send_document(message.chat.id, photo)
            os.remove('plot.png')
            math_part.BOT_PLOT = False
        elif MESSAGE_COM == 'mnk_constants':
            for i in range(0, len(a)):
                bot.send_message(message.chat.id, f"Коэффициенты {i + 1}-ой прямой:\n"
                                                  f" a = {a[i]} +- {d_a[i], 6}\n"
                                                  f" b = {b[i]} +- {d_b[i], 6}")
        os.remove(src)
        math_part.TITLE = ''
        math_part.LABEL_Y = ''
        math_part.LABEL_X = ''
    except Exception as e:
        print(e)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Попробую ещё раз', 'Видимо не в этот раз ...']])
        msg = bot.send_message(message.chat.id,
                               'Что-то не получилось... Проверь файл который ты прислал😨 ', reply_markup=keyboard)
        bot.register_next_step_handler(msg, tit)


@bot.message_handler(commands=['timetable'])
def get_group(message):
    """
    Функция ловит сообщение с текстом "/timetable".
    Отправляет пользователю вопрос о номере группы. Вызывает функцию get_weekday().
    :param message: telebot.types.Message
    :return:
    """
    if message.text == 'Ладно, сам посмотрю':
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, '😞', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Снова не можешь вспомнить какая пара следующая?)'
                                          'Ничего, я уже тут!')
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,
                         'Не подскажешь номер своей группы? (В формате Б00-000)', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_weekday)


def get_weekday(message):
    """
    Функция сохраняет номер группы и отправляет кнопки с выбором дня недели.
    Вызывает функцию get_schedule().
    :param message: telebot.types.Message
    :return:
    """
    global GROUP_NUM
    GROUP_NUM = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        *[types.KeyboardButton(name) for name in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']])
    msg = bot.send_message(message.chat.id, 'Расписание на какой день ты хочешь узнать?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, get_schedule)


def get_schedule(message):
    """
    Функция считывает день недели, вызывает функцию get_timetable из модуля timetable,
    отправляет пользователю раписание из файла.
    :param message: telebot.types.Message
    :return:
    """
    if message.text in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']:
        timetable.timetable.get_timetable(GROUP_NUM, message.text)
        f = open(f'{PATH}/timetable/class.txt')
        msg = ''
        for line in f:
            bot.send_message(message.chat.id, line)
            msg += line
        open(f'{PATH}/timetable/class.txt', 'w').close()
        if msg != '':
            keyboard = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Чем я ещё могу помочь?', reply_markup=keyboard)
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Попробую ещё раз', 'Ладно, сам посмотрю']])
            msg = bot.send_message(message.chat.id,
                                   'Что-то не получилось... Ты мне точно прислал номер группы в правильном формате ?',
                                   reply_markup=keyboard)
            bot.register_next_step_handler(msg, get_group)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Попробую ещё раз', 'Ладно, сам посмотрю']])
        msg = bot.send_message(message.chat.id,
                               'Какой интересный день недели, извини, я такого не знаю... ?',
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, get_group)


@bot.message_handler(commands=['exam'])
def ask_group(message):
    """
    Функция ловит сообщение с текстом '/exam'.
    Отправляет запрос о выборе группы и вызывает функцию get_exam_timetable().
    :param message: telebot.types.Message
    :return:
    """
    if message.text == 'Ладно, сам посмотрю':
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, '😞', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Не подскажешь номер своей группы? (В формате Б00-000)')
        bot.register_next_step_handler(message, get_exam_timetable)


def get_exam_timetable(message):
    """
    Функция считывает номер группы, вызывает функцию get_exam_timetable из модуля timetable,
    отправляет пользователю раписание экзаменов из файла.
    :param message: telebot.types.Message
    :return:
    """
    if message.text in texting.texting_symbols.groups:
        timetable.timetable.get_exam_timetable(message.text)
        f = open(f'{PATH}/timetable/exam.txt')
        for line in f:
            bot.send_message(message.chat.id, line)
        open(f'{PATH}/timetable/exam.txt', 'w').close()
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Попробую ещё раз', 'Ладно, сам посмотрю']])
        msg = bot.send_message(message.chat.id, 'Что-то не получилось... '
                                                'Ты мне точно прислал номер группы в правильном формате ?',
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, ask_group)


@bot.message_handler(content_types=['text'])
def chatting(message):
    """
    Функция запускается, если пользователь пишет любой незнакомый боту текст.
    :param message: any text
    :return: циклично возвращает одно вспомогательное сообщение, два смайлика,
    две цитаты, одну фотку собаки при последовательной отправке незнакомого текста
    """
    global crazy_tokens, PATH
    crazy_tokens += 1
    if crazy_tokens <= 1:
        bot.send_message(message.chat.id, 'Боюсь, я не совсем понимаю, о чём ты. \n'
                                          'Напиши /help, чтобы узнать, что я умею.\n')
    elif crazy_tokens <= 3:
        bot.send_message(message.chat.id, random.choice(texting.texting_symbols.emoji))
    elif crazy_tokens <= 5:
        bot.send_message(message.chat.id, random.choice(texting.texting_symbols.quotes))
    elif crazy_tokens == 6:
        doggy = get_image_url()
        '''
        API_LINK = 'http://api.forismatic.com/api/method=getQuote&format=text&lang=ru'
        cont = requests.post(API_LINK)
        print(cont.text)
        bot.send_message(message.chat.id, quote)
        '''

        bot.send_photo(message.chat.id, photo=doggy)
        crazy_tokens = 0


def get_url():
    """
    Функция получает ссылку на картинку собаки
    :return: ссылка на картинку
    """
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def get_image_url():
    """
    Функция проверяет расширение картинки с собакой
    :return: ссылка на картинку
    """
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url


bot.polling()
