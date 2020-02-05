import os
import random
import re

import numpy as np
import pandas as pd
import requests
import telebot
from telebot import types

import texting.texting_symbols
from math_module import math_part

import timetable.timetable
import datetime

# Токен бота.
base_url = 'https://api.telegram.org/bot893576564:AAFGQbneULhW7iUIsLwqJY3WZpFPe78oSR0/'
TOKEN = '893576564:AAFGQbneULhW7iUIsLwqJY3WZpFPe78oSR0'
PATH = os.path.abspath('')
bot = telebot.TeleBot(TOKEN)
FILE_NAME = ''
MESSAGE_NUM = 0
MESSAGE_COM = ''
Q_NUM = 0
PAR_NUM = 0
GROUP_NUM = ''
COURSE_NUM = 0
SUBJECT_NOW = ''
Q_SEQUENCE = []
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
            'Билет 24': 17,
            'Билет 25': 18,
            'Билет 26': 19,
            'Билет 27': 20,
            'Билет 23': 21,
            'Билет 34': 22,
            'Билет 35': 23,
            'Билет 36': 24

        }
}

comms = ['help', 'start', 'flash_cards', 'plot', 'timetable', 'exam']  # Comands list

crazy_tokens = 0
ANSW_ID = 0

# Plot constants
PLOT_MESSEGE = 0
PLOT_BUTTONS = ['Название графика', 'Подпись осей', 'Кресты погрешностей', 'Готово', 'MНК']


@bot.message_handler(commands=['help'])
def help_def(message):
    """
    Функция ловит сообщение с командой '/help' и присылает описание комманд бота
    :param message: telebot.types.Message
    :return:
    """
    bot.send_message(message.chat.id, 'Сейчас я расскажу, чем я могу тебе помочь ☺️\n'
                                      '/plot - Получил данные на лабе и уже хочешь построить график ? Запросто !\n'
                                      '/timetable - Забыл расписание?) Бывает, пиши, я помогу 😉📱📱📱'
                                      '\n/exam - Подскажу расписание экзаменов, но ты сам захотел...'
                                      ' Я не люблю напоминать'
                                      'о плохом...\n'
                                      '/flash_cards - Давай сыграем в игру... Я тебе определение/формулировку, а '
                                      'ты попытайся вспомнить её. Как только вспомнишь/не вспомнишь нажимай "покажи"'
                                      'чтобы проверить себя\n')


@bot.message_handler(commands=['start'])
def start(message):
    """
    Функция ловит сообщение с коммандой '/start' и шлёт пользователю сообщение с приветсвием
    :param message: telebot.types.Message
    :return:
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # кнопки для получения расписания на сегодня или завтра
    keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
    bot.send_message(message.chat.id, 'Привет-привет 🙃 Я очень люблю помогать людям,'
                                      ' напиши /help чтобы узнать, что я умею. ', reply_markup=keyboard)


@bot.message_handler(commands=['pb'])
def pb(message):
    bot.send_message(message.chat.id, 'Хочешь вспомнить парочку определений ?)📚📚')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in SUBJECTS.keys()])
    msg = bot.send_message(message.chat.id, 'Сначала выбери предмет', reply_markup=keyboard)
    bot.register_next_step_handler(msg, sub)


def sub(message):
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
        bot.register_next_step_handler(msg, par)

    elif message.text == 'Выбрать другой параграф':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in SUBJECTS[SUBJECT_NOW].keys()])
        msg = bot.send_message(message.chat.id, 'Какой параграф ты хочешь поботать ?', reply_markup=keyboard)
        bot.register_next_step_handler(msg, par)

    elif message.text == 'Всё, хватит' or message.text == 'В другой раз...':
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Возвращайся ещё !', reply_markup=keyboard)
        SUBJECT_NOW = ''

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Матан', 'В другой раз...']])
        msg = bot.send_message(message.chat.id, 'Извини, я тебя не понял, можешь повторить ?', reply_markup=keyboard)
        bot.register_next_step_handler(msg, sub)


def par(message):
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
        for i in range(0, len(d)):
            Q_NUM = i
            question = d[Q_NUM, 0]
            bot.send_message(message.chat.id, question)
            with open(f'{PATH}/flash_cards/{SUBJECTS_PATH[SUBJECT_NOW]}/{PAR_NUM}/{Q_NUM + 1}.png', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['flash_cards'])
def flash_cards(message):
    """
    Функция ловит сообщение с коммандой '/flash_cards' и запускает сессию этой функции
     отправляя кнопки с выбором предмета. Добавляется inline-клавиатура, нажатие кнопок которой
     передаются дальше в callback_query_handler
    :param message: telebot.types.Message
    :return:
    """
    bot.send_message(message.chat.id, 'Хочешь вспомнить парочку определений ?)📚📚')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in SUBJECTS.keys()])
    bot.send_message(message.chat.id, 'Сначала выбери предмет', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data in SUBJECTS.keys())
def subject(c):
    """
    Функция ловит callback с названием предмета и изменяет
     это сообщение на предложение выбора разделов.
    :param c: telebot.types.CallbackQuery
    :return:
    """
    global Q_NUM, PATH, SUBJECT_NOW, SUBJECTS
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in SUBJECTS[c.data].keys()])
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text='Какой раздел ты хочешь поботать ?',
        parse_mode='Markdown',
        reply_markup=keyboard)
    SUBJECT_NOW = c.data


@bot.callback_query_handler(func=lambda c: (SUBJECT_NOW != '') or (c.data == 'Ещё'))
def paragraph(c):
    """
    Функция ловит callback с названием раздела выбранного ранее предмета
    и изменяет это сообщение на вопрос из этого раздела.
    :param c: telebot.types.CallbackQuery
    :return:
    """
    global Q_NUM, PATH, PAR_NUM, SUBJECTS, SUBJECT_NOW, Q_SEQUENCE
    if ANSW_ID:
        bot.delete_message(c.message.chat.id, ANSW_ID)
    if c.data in SUBJECTS[SUBJECT_NOW].keys():
        PAR_NUM = SUBJECTS[SUBJECT_NOW][c.data]
    # импортирую список вопросов
    questions = pd.read_excel(f'{PATH}/flash_cards/{SUBJECTS_PATH[SUBJECT_NOW]}/{PAR_NUM}/flash_data.xlsx',
                              header=None)
    # преобразования списка в numpy массив
    questions = np.array(questions)
    if not Q_SEQUENCE:
        i = 0
        for _ in questions:
            Q_SEQUENCE.append(i)
            i += 1
        random.shuffle(Q_SEQUENCE)
    Q_NUM = Q_SEQUENCE[0]
    Q_SEQUENCE.pop(0)
    question = questions[Q_NUM, 0]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Покажи']])
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=question,
        parse_mode='Markdown',
        reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data == 'Покажи')
def answer(c):
    """
    Функция ловит callback с текстом "Покажи". Присылает пользователю ответ на вопрос.
    :param c: telebot.types.CallbackQuery
    :return:
    """
    global Q_NUM, PAR_NUM, ANSW_ID
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Ещё', 'Всё, хватит']])
    with open(f'{PATH}/flash_cards/{SUBJECTS_PATH[SUBJECT_NOW]}/{PAR_NUM}/{Q_NUM + 1}.png', 'rb') as photo:
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text='Правильный ответ',
            parse_mode='Markdown',
            reply_markup=keyboard)
        msg = bot.send_photo(c.message.chat.id, photo)
        ANSW_ID = msg.message_id


@bot.callback_query_handler(func=lambda c: c.data == 'Всё, хватит')
def stop_cards(c):
    """
    Функция ловит callback с текстом "Всё, хватит". Завершает сеанс игры.
    :param c: telebot.types.CallbackQuery
    :return:
    """
    global ANSW_ID
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text='Возвращайся ещё 😉',
        parse_mode='Markdown')
    bot.delete_message(c.message.chat.id, ANSW_ID)


@bot.message_handler(commands=['plot'])
def plot(message):
    """
    Функция ловит сообщение с текстом '/plot'. Инициируется процесс рисования графика. Запускает функцию ax_x()
    :param message: telebot.types.Message
    :return:
    """
    global MESSAGE_COM
    bot.send_message(message.chat.id, 'Снова лабки делаешь ?) Ох уж эти графики !...'
                                      ' Сейчас быстренько всё построю, только тебе придётся ответить на пару вопросов'
                                      '😉. И не засиживайся, ложись спать))')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Без названия', 'Выход']])
    msg = bot.send_message(message.chat.id, 'Как мы назовём график ?'
                                            ' Если не хочешь называть нажми кнопку ниже 😉', reply_markup=keyboard)
    MESSAGE_COM = 'plot'
    bot.register_next_step_handler(msg, tit)


def tit(message):
    """
    Функция вызывается ax_x(), записывает введённое пользователем название графика, вызывает data_mnk()
    :param message: сообщение пользователя
    :return:
    """
    global MESSAGE_COM
    if message.content_type == 'text':
        if message.text == 'Выход':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
            bot.send_message(message.chat.id, 'Передумал ? Ну ладно...', reply_markup=keyboard)
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ')
        elif message.text == 'Без названия':
            math_part.TITLE = ''
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['✅', '❌', 'Выход']])
            msg = bot.send_message(message.chat.id, 'Прямую по МНК строим ?', reply_markup=keyboard)
            bot.register_next_step_handler(msg, mnk)
        else:
            math_part.TITLE = message.text
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['✅', '❌', 'Выход']])
            msg = bot.send_message(message.chat.id, 'Прямую по МНК строим ?', reply_markup=keyboard)
            bot.register_next_step_handler(msg, mnk)

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Без названия']])
        msg = bot.send_message(message.chat.id, 'Я тебя не понял... Напиши ещё раз название графика !'
                                                ' Если не хочешь называть нажми кнопку ниже 😉', reply_markup=keyboard)
        MESSAGE_COM = 'plot'
        bot.register_next_step_handler(msg, tit)


def mnk(message):
    """
    Функция вызывается tit(), записывается выбор пользователя: строить мнк прямую или нет. Вызывает
    :param message: сообщение пользователя
    :return:
    """
    if message.content_type == 'text':
        if message.text == 'Выход':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
            bot.send_message(message.chat.id, 'Передумал ? Ну ладно...', reply_markup=keyboard)
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ')
        elif message.text == '✅':
            math_part.ERROR_BAR = True
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['0.0/0.0']])
            msg = bot.send_message(message.chat.id, 'Пришли данные для крестов погрешностей по осям х и y в '
                                                    'формате "123.213/123.231", если кресты не нужны,'
                                                    ' нажми на кнопку ниже', reply_markup=keyboard)
            bot.register_next_step_handler(msg, error_bars)
        elif message.text == '❌':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])
            with open('Example.xlsx', 'rb') as example:
                bot.send_document(message.chat.id, example)
            msg = bot.send_message(message.chat.id,
                                   'Пришли xlsx файл с данными как в example.xlsx и всё будет готово',
                                   reply_markup=keyboard)
            bot.register_next_step_handler(msg, date_mnk)
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['✅', '❌', 'Выход']])
            msg = bot.send_message(message.chat.id, 'Извини, повтори ещё раз... Прямую по МНК строим ?',
                                   reply_markup=keyboard)
            bot.register_next_step_handler(msg, mnk)

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['✅', '❌', 'Выход']])
        msg = bot.send_message(message.chat.id, 'Извини, повтори ещё раз... Прямую по МНК строим ?',
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, mnk)


def error_bars(message):
    if message.content_type == 'text':
        if message.text == 'Выход':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
            bot.send_message(message.chat.id, 'Передумал ? Ну ладно...', reply_markup=keyboard)
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ')
        try:
            math_part.ERRORS = list(map(float, message.text.split('/')))
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])
            with open('Example.xlsx', 'rb') as expl:
                bot.send_document(message.chat.id, expl)
            msg = bot.send_message(message.chat.id,
                                   'Пришли xlsx файл с данными как в example.xlsx и всё будет готово',
                                   reply_markup=keyboard)
            bot.register_next_step_handler(msg, date_mnk)
        except Exception as e:
            print(e)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['0.0/0.0']])
            msg = bot.send_message(message.chat.id,
                                   'Не могу распознать формат данных( Давай ещё раз. '
                                   'Пришли данные для крестов погрешностей по осям х и y в '
                                   'формате "123.213/123.231", если кресты не нужны,'
                                   ' нажми на кнопку ниже', reply_markup=keyboard)
            bot.register_next_step_handler(msg, error_bars)
    else:
        math_part.ERROR_BAR = True
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['0.0/0.0']])
        msg = bot.send_message(message.chat.id, 'Ты прислал что-то не то( Давай ещё раз. '
                                                'Пришли данные для крестов погрешностей по осям х и y в '
                                                'формате "123.213/123.231", если кресты не нужны,'
                                                ' нажми на кнопку ниже', reply_markup=keyboard)
        bot.register_next_step_handler(msg, error_bars)


def date_mnk(message):
    """
    Функция активирует рисование графика/линеаризованного графика/подсчёта констант и погрешностей, в зависимости от
    того, какая функция была написана пользователем.
    :param message:
    :return:
    """
    global FILE_NAME
    if message.content_type == 'text':
        if message.text == 'Выход':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
            bot.send_message(message.chat.id, 'Передумал ? Ну ладно...', reply_markup=keyboard)
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ')
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])
            msg = bot.send_message(message.chat.id,
                                   'Ты точно прислал xlsx файл ? Давай ещё раз ! '
                                   'Пришли xlsx файл с данными и всё будет готово', reply_markup=keyboard)
            bot.register_next_step_handler(msg, date_mnk)
    elif message.content_type == 'document':
        try:
            file_id = message.json.get('document').get('file_id')
            file_path = bot.get_file(file_id).file_path
            downloaded_file = bot.download_file(file_path)
            FILE_NAME = message.document.file_name
            with open(FILE_NAME, 'wb') as new_file:
                new_file.write(downloaded_file)
            a, b, d_a, d_b = math_part.mnk_calc(
                FILE_NAME)  # TODO разделить рассчёт погрешностей констант и рассчёт самих констант
            math_part.BOT_PLOT = True
            math_part.plots_drawer(FILE_NAME, math_part.TITLE, math_part.ERRORS[0], math_part.ERRORS[1], math_part.ERROR_BAR)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
            bot.send_message(message.chat.id, 'Принимай работу !)', reply_markup=keyboard)
            with open('plot.pdf', 'rb') as photo:
                bot.send_document(message.chat.id, photo)
            if math_part.ERROR_BAR:
                for i in range(0, len(a)):
                    bot.send_message(message.chat.id, f"Коэффициенты {i + 1}-ой прямой:\n"
                                                      f" a = {a[i]} +- {d_a[i], 6}\n"
                                                      f" b = {b[i]} +- {d_b[i], 6}")
            os.remove('plot.pdf')
            with open('plot.png', 'rb') as photo:
                bot.send_document(message.chat.id, photo)
            os.remove('plot.png')
            math_part.BOT_PLOT = False
            os.remove(FILE_NAME)
            math_part.TITLE = ''
            math_part.ERRORS = [0, 0]
            math_part.ERROR_BAR = False
        except Exception as e:
            os.remove(FILE_NAME)
            print(e)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])
            msg = bot.send_message(message.chat.id,
                                   'Ты точно прислал xlsx файл как в примере ? Давай ещё раз !', reply_markup=keyboard)
            bot.register_next_step_handler(msg, date_mnk)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])
        msg = bot.send_message(message.chat.id,
                               'Ты точно прислал xlsx файл ? Давай ещё раз ! '
                               'Пришли xlsx файл с данными и всё будет готово', reply_markup=keyboard)
        bot.register_next_step_handler(msg, date_mnk)


@bot.message_handler(func=lambda message: message.text in ['На сегодня', 'На завтра'])
def get_start_schedule(message):
    """
    Функция ловит сообщение с текстом "Расписание на сегодня/завтра".
    Узнает номер дня недели сегодня/завтра и по этому значению обращается в функцию get_schedule_by_group()?.
    :return:
    """
    # список дней для удобной конвертации номеров дней недели (0,1, ..., 6) в их названия
    week = tuple(['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'])
    today = datetime.datetime.today().weekday()  # today - какой сегодня день недели (от 0 до 6)
    if message.text == 'На сегодня':  # расписание на сегодня
        # проверка работы функции на рандомной группе
        schedule = timetable.timetable.timetable_by_group(3, '7113', week[today])
        STRING = ''  # "строка" с расписанием, которую отправляем сообщением
        for row in schedule.iterrows():  # проходимся по строкам расписания, приплюсовываем их в общую "строку"
            # время пары - жирный + наклонный шрифт, название пары на следующей строке
            string: str = '<b>' + '<i>' + row[0] + '</i>' + '</b>' + '\n' + row[1][0]
            STRING += string + '\n\n'  # между парами пропуск (1 enter)
        bot.send_message(message.chat.id, STRING, parse_mode='HTML')  # parse_mode - чтобы читал измененный шрифт
        keyboard = types.ReplyKeyboardRemove()  # убираем клавиатуру
        bot.send_message(message.chat.id, 'Чем ещё я могу помочь?', reply_markup=keyboard)
    elif message.text == 'На завтра':  # расписание на завтра
        tomorrow = 0  # номер дня завтра, если это воскресенье (6), то уже стоит
        if today in range(6):  # если не воскресенье, то значение today + 1
            tomorrow = today + 1
        # тест на рандомной группе
        schedule = timetable.timetable.timetable_by_group(3, '7113', week[tomorrow])
        STRING = ''  # "строка" с расписанием, которую отправляем сообщением
        for row in schedule.iterrows():  # проходимся по строкам расписания, приплюсовываем их в общую "строку"
            # время пары - жирный + наклонный шрифт, название пары на следующей строке
            string: str = '<b>' + '<i>' + row[0] + '</i>' + '</b>' + '\n' + row[1][0]
            STRING += string + '\n\n'  # между парами пропуск (1 enter)
        bot.send_message(message.chat.id, STRING, parse_mode='HTML')  # parse_mode - чтобы читал измененный шрифт
        keyboard = types.ReplyKeyboardRemove()  # сворачиваем клавиатуру
        bot.send_message(message.chat.id, 'Чем ещё я могу помочь?', reply_markup=keyboard)


@bot.message_handler(commands=['timetable'])
def get_course(message):
    """
    Функция ловит сообщение с текстом "/timetable".
    Отправляет пользователю вопрос о номере курса. Вызывает функцию get_group()
    :param message: telebot.types.Message
    :return:
    """
    if message.text == '/timetable':  # инициализация блока
        bot.send_message(message.chat.id, 'Снова не можешь вспомнить какая пара следующая? :) '
                                          'Ничего, я уже тут!')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in range(1, 7)])  # кнопки c номерами курсов
        keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])  # кнопка для выхода из функции
        msg = bot.send_message(message.chat.id, 'Не подскажешь номер своего курса?', reply_markup=keyboard)
        bot.register_next_step_handler(msg, get_group)
    elif message.text == 'Ладно, сам посмотрю':  # если после ошибки в считывании данных пришло сообщение о выходе:
        keyboard = types.ReplyKeyboardRemove()  # убираем кнопки
        bot.send_message(message.chat.id, 'Без проблем! '
                                          'Но ты это, заходи, если что :)',
                         reply_markup=keyboard
                         )
        # стикос "Ты заходи есчо"
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ')
    elif message.text == 'Попробую ещё раз':  # если после ошибки в считывании данных в других функциях пришло
        # сообщение попробовать ввести значения еще раз
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in range(1, 7)])  # то же, что и в блоке инициализации
        keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])
        msg = bot.send_message(message.chat.id, 'Не подскажешь номер своего курса?', reply_markup=keyboard)
        bot.register_next_step_handler(msg, get_group)


def get_group(message):
    """
    Функция сохраняет номер курса и отправляет пользователю вопрос о номере группы.
    Вызывает функцию get_weekday().
    :param message: telebot.types.Message
    :return:
    """
    global COURSE_NUM  # вызываем глобальную переменную с номером курса
    if message.content_type == 'text':  # проверка типа сообщения, является ли оно текстовым, а не файлом
        if message.text == 'Выход':  # если из функции get_course() пришло сообщение о выходе
            keyboard = types.ReplyKeyboardRemove()  # убираем кнопки
            bot.send_message(message.chat.id, 'Передумал ? Ну ладно...', reply_markup=keyboard)
            # стикос "Ты заходи есчо"
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ')
        elif message.text in map(str, range(1, 7)):  # если прилетел номер курса
            COURSE_NUM = int(message.text)  # запоминаем номер курса (число)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in ['Выход']  # кнопка для выхода из функции
                  ]
            )
            bot.send_message(message.chat.id,  # просим пользователя ввести номер группы
                             'Не подскажешь номер своей группы? (В формате L0N–YFx или YFx)',
                             reply_markup=keyboard)
            bot.register_next_step_handler(message, get_weekday)
        else:  # если сообщение не "Выход" и не номер курса, то говорим об ошибке и отправляем в get_course()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in [
                'Попробую ещё раз', 'Ладно, сам посмотрю'  # первая кнопка - ввод данных заново, вторая - выход
            ]
                           ]
                         )
            msg = bot.send_message(message.chat.id,
                                   'Что-то не получилось... Ты мне точно прислал номер курса?',
                                   reply_markup=keyboard)
            bot.register_next_step_handler(msg, get_course)
    else:  # если сообщение не является текстом, то говорим об ошибке формата и отправляем в get_course()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Попробую ещё раз', 'Ладно, сам посмотрю']])
        msg = bot.send_message(message.chat.id,
                               'Что-то не получилось... Ты мне точно прислал номера курса в правильном '
                               'формате?',
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, get_course)


def get_weekday(message):
    """
    Функция сохраняет номер группы и отправляет кнопки с выбором дня недели.
    Вызывает функцию get_schedule().
    :param message: telebot.types.Message
    :return:
    """
    if message.content_type == 'text':  # проверяем, является ли сообщение текстовым
        if message.text == 'Выход':  # если из get_group() прилетело сообщение о выходе
            keyboard = types.ReplyKeyboardRemove()  # убираем кнопки
            bot.send_message(message.chat.id, 'Передумал ? Ну ладно...', reply_markup=keyboard)
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ')
        else:  # иначе запоминаем текст сообщения (проверку на формат текста не делал)
            global GROUP_NUM  # глобальная переменная - номер группы
            GROUP_NUM = message.text
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in [  # дни недели для тыков и кнопка для выхода
                    'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Выход'
                ]
                  ]
            )
            bot.send_message(message.chat.id, 'Расписание на какой день ты хочешь узнать?', reply_markup=keyboard)
            bot.register_next_step_handler(message, get_schedule)
    else:  # если сообщение не текстовое, то говорим об ошибке формата, отсылаем в функцию get_course()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Попробую ещё раз', 'Ладно, сам посмотрю']])
        msg = bot.send_message(message.chat.id,
                               'Что-то не получилось... Ты мне точно прислал номера курса и группы в правильном '
                               'формате?',
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, get_course)


pd.options.display.max_colwidth = 100


def get_schedule(message):
    """
    Функция, выдающая расписание на нужный день недели.
    :param message: telebot.types.Message
    :return:
    """
    if message.content_type == 'text':  # проверка типа сообщения - текст или нет
        if message.text == 'Выход':  # если из функции get_group() прилетело сообщение о выходе
            keyboard = types.ReplyKeyboardRemove()  # убираем кнопки
            bot.send_message(message.chat.id, 'Передумал ? Ну ладно...', reply_markup=keyboard)
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ')
        else:  # иначе проверяем, есть ли расписание для этой группы в файле
            schedule = timetable.timetable.timetable_by_group(COURSE_NUM, GROUP_NUM, message.text)
            if schedule.empty:  # если расписание пустое, то говорим об ошибке формата, просим ввести данные заново
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(*[types.KeyboardButton(name) for name in ['Попробую ещё раз', 'Ладно, сам посмотрю']])
                msg = bot.send_message(message.chat.id,
                                       'Что-то не получилось... Ты мне точно прислал номера курса и группы в правильном'
                                       ' формате?',
                                       reply_markup=keyboard)
                bot.register_next_step_handler(msg, get_course)  # да-да, отсылаем в самую первую функцию)))
            else:  # иначе переводим табличку с расписанием на день (pd.Series) в pd.DataFrame
                schedule = schedule.to_frame()
                STRING = ''  # проходимся по всем строчкам расписания, записываем в STRING готовое сообщение,
                # которое отправим пользователю ( см. функцию get_start_schedule() )
                for row in schedule.iterrows():
                    string: str = '<b>' + '<i>' + row[0] + '</i>' + '</b>' + '\n' + row[1][0]
                    STRING += string + '\n\n'
                bot.send_message(message.chat.id, STRING, parse_mode='HTML')
                keyboard = types.ReplyKeyboardRemove()  # убираем клаву, спрашиваем, чем можем быть еще полезны
                bot.send_message(message.chat.id, 'Чем ещё я могу помочь?', reply_markup=keyboard)
    else:  # если сообщение не текстовое, то говорим об ошибке формате
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Попробую ещё раз', 'Ладно, сам посмотрю']])
        msg = bot.send_message(message.chat.id,
                               'Что-то не получилось... Ты мне точно прислал номера курса и группы в правильном '
                               'формате?',
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, get_course)  # ну и последний разок сходим в самую первую функцию)


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
        timetable.timetable_old.get_exam_timetable(message.text)
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
