import os
import random
import re
import numpy as np
import pandas as pd
import requests
import telebot
from telebot import types

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
Q_LIST = []
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
    global Q_NUM, PATH, PAR_NUM, SUBJECTS, SUBJECT_NOW, Q_SEQUENCE
    if (message.text in SUBJECTS[SUBJECT_NOW].keys()) or (message.text == 'Ещё'):
        if message.text in SUBJECTS[SUBJECT_NOW].keys():
            PAR_NUM = SUBJECTS[SUBJECT_NOW][message.text]
        # импортирую список вопросов
        questions = pd.read_excel(f'{PATH}/flash_cards/{SUBJECTS_PATH[SUBJECT_NOW]}/{PAR_NUM}/flash_data.xlsx',
                                  header=None)
        # преобразования списка в numpy массив
        questions = np.array(questions)
        if not Q_SEQUENCE:
            i = 0
            for q in questions:
                Q_SEQUENCE.append(i)
                i += 1
            random.shuffle(Q_SEQUENCE)
        Q_NUM = Q_SEQUENCE[0]
        Q_SEQUENCE.pop(0)
        question = questions[Q_NUM, 0]
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