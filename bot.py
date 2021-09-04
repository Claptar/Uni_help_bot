from telebot import types
from data_constructor import psg
from math_module import math_part
from koryavov import kor

import os
import random
import re
import numpy as np
import pandas as pd
import requests
import telebot
import texting.texting_symbols
import timetable.timetable
import datetime

token = os.environ["TOKEN"]  # Токен для бота берётся из переменных окружения
bot = telebot.TeleBot(token)
MESSAGE_NUM = 0
MESSAGE_COM = ""
Q_NUM = 0
PAR_NUM = 0
GROUP_NUM = ""
COURSE_NUM = 0
SUBJECT_NOW = ""
Q_SEQUENCE = []
SUBJECTS_PATH = {"Матан": "math", "Химия": "chem_org"}
SUBJECTS = {
    "Матан": {
        "Множество Rn": 1,
        "Предел и непрерывность": 2,
        "Дифференциальное исчисление в Rn": 3,
        "Интеграл Римана": 4,
        "Мера Жордана": 5,
        "Числовые ряды": 6,
    },
    "Химия": {
        "Билеты 1-2": 1,
        "Билеты 3,5": 2,
        "Билеты 4,6": 3,
        "Билет 7": 4,
        "Билет 8": 5,
        "Билет 9": 6,
        "Билеты 10-11": 7,
        "Билет 12": 8,
        "Билет 13": 9,
        "Билет 14": 10,
        "Билет 15": 11,
        "Билет 16": 12,
        "Билет 17": 13,
        "Билет 18-19": 14,
        "Билет 20-21": 15,
        "Билет 22": 16,
        "Билет 24": 17,
        "Билет 25": 18,
        "Билет 26": 19,
        "Билет 27": 20,
        "Билет 23": 21,
        "Билет 34": 22,
        "Билет 35": 23,
        "Билет 36": 24,
    },
}


comms = ["help", "start", "plot", "timetable", "exam"]  # Comands list

crazy_tokens = 0
ANSW_ID = 0

# Plot constants
PLOT_MESSEGE = 0
PLOT_BUTTONS = [
    "Название графика",
    "Подпись осей",
    "Кресты погрешностей",
    "Готово",
    "MНК",
]


@bot.message_handler(commands=["help"])
def help_def(message):
    """
    Функция ловит сообщение с командой '/help' и присылает описание комманд бота
    :param message: telebot.types.Message
    :return:
    """
    bot.send_message(
        message.chat.id,
        "Сейчас я расскажу, чем я могу тебе помочь ☺️\n"
        "/plot — Получил данные на лабе и уже хочешь построить график? Запросто!\n"
        "/timetable — Забыл расписание?) Бывает, пиши, я помогу 😉📱\n"
        "/exam — Подскажу расписание экзаменов, но ты сам захотел... "
        " Я не люблю напоминать "
        "о плохом...\n"
        "/koryavov — Подскажу номер страницы с этой задачей по физике в Корявове."
        "Информация берётся с замечательного сайта mipt1.ru \n"
        "/profile — Опечатка в номере курса или группы? Нажимай, сейчас исправим)\n"
        "/custom — Не ходишь на лекции или есть факультативы ?"
        "Измени расписание под себя !",
    )


@bot.message_handler(commands=["profile"])
def choose_edit(message):
    """
    Функция ловит сообщение с командой '/profile' и спрашивает у пользователя
    какие данные он хочет изменить в базе данных
    :param message:
    :return:
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        *[
            types.KeyboardButton(name)
            for name in ["Номер курса", "Номер группы", "Выход"]
        ]
    )  # кнопки c номерами семестров
    try:
        student = psg.get_student(message.chat.id)
        msg = bot.send_message(
            message.chat.id,
            f"Сейчас у тебя указано, что ты учишься на {student[1]} курсе "
            f"в {student[0]} группе."
            f" Что именно ты хочешь изменить?",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(msg, edit_values)
    except Exception as e:
        print("АШИПКА")
        print(e)
        bot.send_message(
            os.environ["ADMIN_1"],
            f"Посмотри логи у чувака"
            f" user = {message.from_user} id={message.chat.id}"
            f" пошла по пизде 109 строчка...",
        )
        bot.send_message(
            os.environ["ADMIN_2"],
            f"Посмотри логи у чувака"
            f" user = {message.from_user} id={message.chat.id}"
            f" пошла по пизде 109 строчка...",
        )
        bot.send_message(
            message.chat.id,
            "Извини, что-то пошло не так, команда устранения ошибок уже взялась за дело,"
            " попробуй эту функцию позже) Чтобы проблема решилась быстрее"
            " ты можешь написать @Error404NF",
        )


def edit_values(message):
    if message.content_type == "text":
        if message.text == "Номер курса":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in [1, 2, 3, 4, 5, "Выход"]]
            )
            msg = bot.send_message(
                message.chat.id, "Введи номер своего курса", reply_markup=keyboard
            )
            bot.register_next_step_handler(msg, edit_course)
        elif message.text == "Номер группы":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
            msg = bot.send_message(
                message.chat.id, "Введи номер своей группы", reply_markup=keyboard
            )
            bot.register_next_step_handler(msg, edit_group)
        elif message.text == "Выход":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Передумал? Ну ладно...", reply_markup=keyboard
            )
            bot.send_sticker(
                message.chat.id,
                "CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ",
            )
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[
                    types.KeyboardButton(name)
                    for name in ["Номер курса", "Номер группы", "Выход"]
                ]
            )
            msg = bot.send_message(
                message.chat.id, "Что-то не так, давай ещё раз", reply_markup=keyboard
            )
            bot.register_next_step_handler(msg, edit_values)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[
                types.KeyboardButton(name)
                for name in ["Номер курса", "Номер группы", "Выход"]
            ]
        )
        msg = bot.send_message(
            message.chat.id, "Что-то не так, давай ещё раз", reply_markup=keyboard
        )
        bot.register_next_step_handler(msg, edit_values)


def edit_course(message):
    if message.content_type == "text":
        if message.text == "Выход":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Передумал? Ну ладно...", reply_markup=keyboard
            )
            bot.send_sticker(
                message.chat.id,
                "CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ",
            )
        elif message.text.isdigit():
            psg.update_course(message.chat.id, int(message.text))
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Всё готово, проверяй)", reply_markup=keyboard
            )
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in [1, 2, 3, 4, 5, "Выход"]]
            )
            msg = bot.send_message(
                message.chat.id,
                "Что-то не так, выбери номер курса ещё раз",
                reply_markup=keyboard,
            )
            bot.register_next_step_handler(msg, edit_course)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in [1, 2, 3, 4, 5, "Выход"]])
        msg = bot.send_message(
            message.chat.id,
            "Что-то не так, выбери номер курса ещё раз",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(msg, edit_course)


def edit_group(message):
    if message.content_type == "text":
        if message.text == "Выход":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Передумал? Ну ладно...", reply_markup=keyboard
            )
            bot.send_sticker(
                message.chat.id,
                "CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ",
            )
        else:
            psg.update_group_num(message.chat.id, message.text)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Всё готово, проверяй)", reply_markup=keyboard
            )
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
        msg = bot.send_message(
            message.chat.id,
            "Что-то не так, введи номер своей группы ещё раз",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(msg, edit_group)


@bot.message_handler(commands=["koryavov"])
def koryavov1(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        *[types.KeyboardButton(name) for name in [1, 2, 3, 4, 5, "Выход"]]
    )  # кнопки c номерами семестров
    msg = bot.send_message(
        message.chat.id,
        "Выбери номер семестра общей физики: \n"
        "1) Механика \n"
        "2) Термодинамика \n"
        "3) Электричество \n"
        "4) Оптика\n"
        "5) Атомная и ядерная физика",
        reply_markup=keyboard,
    )
    bot.register_next_step_handler(msg, task_number)


def task_number(message):
    if message.content_type == "text":
        if message.text.isdigit() and 1 <= int(message.text) <= 5:
            kor.SEM = int(message.text)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
            msg = bot.send_message(
                message.chat.id,
                "Отлично, напиши теперь номер задачи",
                reply_markup=keyboard,
            )
            bot.register_next_step_handler(msg, task_page)
        elif message.text == "Выход":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Передумал? Ну ладно...", reply_markup=keyboard
            )
            bot.send_sticker(
                message.chat.id,
                "CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ",
            )
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in [1, 2, 3, 4, 5, "Выход"]]
            )  # кнопки c номерами семестров
            msg = bot.send_message(
                message.chat.id, "Что-то не так, давай ещё раз. Выбери номер семестра:"
            )
            bot.register_next_step_handler(msg, task_number)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[types.KeyboardButton(name) for name in [1, 2, 3, 4, 5, "Выход"]]
        )  # кнопки c номерами семестров
        msg = bot.send_message(
            message.chat.id, "Что-то не так, давай ещё раз. Выбери номер семестра:"
        )
        bot.register_next_step_handler(msg, task_number)


def task_page(message):
    if message.content_type == "text":
        if math_part.is_digit(message.text):
            kor.TASK = message.text
            reply = "Информация взята с сайта mipt1.ru \n\n" + kor.kor_page(
                kor.SEM, kor.TASK
            )
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(message.chat.id, reply, reply_markup=keyboard)
        elif message.text == "Выход":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Передумал? Ну ладно...", reply_markup=keyboard
            )
            bot.send_sticker(
                message.chat.id,
                "CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ",
            )
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
            msg = bot.send_message(
                message.chat.id,
                "Что-то не так, давай ещё раз. Введи номер задачи.",
                reply_markup=keyboard,
            )
            bot.register_next_step_handler(msg, task_page)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
        msg = bot.send_message(
            message.chat.id,
            "Что-то не так, давай ещё раз. Введи номер задачи.",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(msg, task_page)


@bot.message_handler(commands=["start"])
def check(message):
    data = psg.read_data()
    if message.chat.id in data.index:
        pass
    else:
        psg.insert_data(message.chat.id, "Б00-228", 0)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[types.KeyboardButton(name) for name in range(1, 6)]
        )  # кнопки c номерами курсов
        msg = bot.send_message(
            message.chat.id,
            "Привет-привет 🙃 Давай знакомиться! Меня зовут A2."
            " Можешь рассказать мне немного о себе,"
            " чтобы я знал, как могу тебе помочь?"
            " Для начала выбери номер своего курса.",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(msg, group_num)


def group_num(message):
    if (message.text.isdigit()) and (1 <= int(message.text) <= 5):
        psg.update_course(message.chat.id, int(message.text))
        keyboard = types.ReplyKeyboardRemove()
        msg = bot.send_message(
            message.chat.id,
            "Отлично, а теперь не подскажешь номер своей группы?\n"
            "(В формате Б00–228 или 777, как в расписании)",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(msg, end)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[types.KeyboardButton(name) for name in range(1, 6)]
        )  # кнопки c номерами курсов
        msg = bot.send_message(
            message.chat.id,
            "Выбери номер курса из предложенных, пожалуйста)",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(msg, group_num)


def end(message):
    psg.update_group_num(message.chat.id, message.text)
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )  # кнопки для получения расписания на сегодня или завтра
    keyboard.add(*[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]])
    bot.send_message(
        message.chat.id,
        "Отлично, вот мы и познакомились 🙃 Я очень люблю помогать людям,"
        " напиши /help чтобы узнать, что я умею. ",
        reply_markup=keyboard,
    )


@bot.message_handler(commands=["pb"])
def pb(message):
    bot.send_message(message.chat.id, "Хочешь вспомнить парочку определений?)📚📚")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in SUBJECTS.keys()])
    msg = bot.send_message(
        message.chat.id, "Сначала выбери предмет", reply_markup=keyboard
    )
    bot.register_next_step_handler(msg, sub)


def sub(message):
    """
    Функция вызывается функцией start, в зависимости от выбора предмета пользователем функция предлагает
     параграфы этого предмета и вызывает функцию  paragraph()
    :param message: telebot.types.Message
    :return:
    """
    global Q_NUM, SUBJECT_NOW, SUBJECTS
    if message.text in SUBJECTS.keys():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[types.KeyboardButton(name) for name in SUBJECTS[message.text].keys()]
        )
        msg = bot.send_message(
            message.chat.id, "Какой раздел ты хочешь поботать?", reply_markup=keyboard
        )
        SUBJECT_NOW = message.text
        bot.register_next_step_handler(msg, par)

    elif message.text == "Выбрать другой параграф":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[types.KeyboardButton(name) for name in SUBJECTS[SUBJECT_NOW].keys()]
        )
        msg = bot.send_message(
            message.chat.id, "Какой параграф ты хочешь поботать?", reply_markup=keyboard
        )
        bot.register_next_step_handler(msg, par)

    elif message.text == "Всё, хватит" or message.text == "В другой раз...":
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Возвращайся ещё!", reply_markup=keyboard)
        SUBJECT_NOW = ""

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[types.KeyboardButton(name) for name in ["Матан", "В другой раз..."]]
        )
        msg = bot.send_message(
            message.chat.id,
            "Извини, я тебя не понял, можешь, пожалуйста, повторить?",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(msg, sub)


def par(message):
    """
    Функция вызывается функцией subject(). Она рандомно генерирует номер вопроса и присылает вопрос пользователю
    :param message: telebot.types.Message
    :return:
    """
    global Q_NUM, PAR_NUM, SUBJECTS, SUBJECT_NOW
    path = os.path.abspath("")
    if (message.text in SUBJECTS[SUBJECT_NOW].keys()) or (message.text == "Ещё"):
        if message.text in SUBJECTS[SUBJECT_NOW].keys():
            PAR_NUM = SUBJECTS[SUBJECT_NOW][message.text]
        questions = pd.read_excel(
            f"{path}/flash_cards/{SUBJECTS_PATH[SUBJECT_NOW]}/{PAR_NUM}/flash_data.xlsx",
            header=None,
        )
        d = np.array(questions)
        for i in range(0, len(d)):
            Q_NUM = i
            question = d[Q_NUM, 0]
            bot.send_message(message.chat.id, question)
            with open(
                f"{path}/flash_cards/{SUBJECTS_PATH[SUBJECT_NOW]}/{PAR_NUM}/{Q_NUM + 1}.png",
                "rb",
            ) as photo:
                bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=["flash_cards"])
def flash_cards(message):
    """
    Функция ловит сообщение с коммандой '/flash_cards' и запускает сессию этой функции
     отправляя кнопки с выбором предмета. Добавляется inline-клавиатура, нажатие кнопок которой
     передаются дальше в callback_query_handler
    :param message: telebot.types.Message
    :return:
    """
    bot.send_message(message.chat.id, "Хочешь вспомнить парочку определений?)📚📚")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        *[
            types.InlineKeyboardButton(text=name, callback_data=name)
            for name in SUBJECTS.keys()
        ]
    )
    bot.send_message(message.chat.id, "Сначала выбери предмет", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda c: c.data in SUBJECTS.keys())
def subject(c):
    """
    Функция ловит callback с названием предмета и изменяет
     это сообщение на предложение выбора разделов.
    :param c: telebot.types.CallbackQuery
    :return:
    """
    global Q_NUM, SUBJECT_NOW, SUBJECTS
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        *[
            types.InlineKeyboardButton(text=name, callback_data=name)
            for name in SUBJECTS[c.data].keys()
        ]
    )
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text="Какой раздел ты хочешь поботать?",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    SUBJECT_NOW = c.data


@bot.callback_query_handler(func=lambda c: (SUBJECT_NOW != "") or (c.data == "Ещё"))
def paragraph(c):
    """
    Функция ловит callback с названием раздела выбранного ранее предмета
    и изменяет это сообщение на вопрос из этого раздела.
    :param c: telebot.types.CallbackQuery
    :return:
    """
    global Q_NUM, PAR_NUM, SUBJECTS, SUBJECT_NOW, Q_SEQUENCE
    path = os.path.abspath("")
    if ANSW_ID:
        bot.delete_message(c.message.chat.id, ANSW_ID)
    if c.data in SUBJECTS[SUBJECT_NOW].keys():
        PAR_NUM = SUBJECTS[SUBJECT_NOW][c.data]
    # импортирую список вопросов
    questions = pd.read_excel(
        f"{path}/flash_cards/{SUBJECTS_PATH[SUBJECT_NOW]}/{PAR_NUM}/flash_data.xlsx",
        header=None,
    )
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
    keyboard.add(
        *[
            types.InlineKeyboardButton(text=name, callback_data=name)
            for name in ["Покажи"]
        ]
    )
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=question,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda c: c.data == "Покажи")
def answer(c):
    """
    Функция ловит callback с текстом "Покажи". Присылает пользователю ответ на вопрос.
    :param c: telebot.types.CallbackQuery
    :return:
    """
    global Q_NUM, PAR_NUM, ANSW_ID
    path = os.path.abspath("")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        *[
            types.InlineKeyboardButton(text=name, callback_data=name)
            for name in ["Ещё", "Всё, хватит"]
        ]
    )
    with open(
        f"{path}/flash_cards/{SUBJECTS_PATH[SUBJECT_NOW]}/{PAR_NUM}/{Q_NUM + 1}.png",
        "rb",
    ) as photo:
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="Правильный ответ",
            parse_mode="Markdown",
            reply_markup=keyboard,
        )
        msg = bot.send_photo(c.message.chat.id, photo)
        ANSW_ID = msg.message_id


@bot.callback_query_handler(func=lambda c: c.data == "Всё, хватит")
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
        text="Возвращайся ещё 😉",
        parse_mode="Markdown",
    )
    bot.delete_message(c.message.chat.id, ANSW_ID)


@bot.message_handler(commands=["plot"])
def plot(message):
    """
    Функция ловит сообщение с текстом '/plot'. Инициируется процесс рисования графика. Запускает функцию ax_x()
    :param message: telebot.types.Message
    :return:
    """
    global MESSAGE_COM
    bot.send_message(
        message.chat.id,
        "Снова лабки делаешь?) Ох уж эти графики!..."
        " Сейчас быстренько всё построю, только тебе придётся ответить на пару вопросов"
        "😉. И не засиживайся, ложись спать)",
    )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ["Без названия", "Выход"]])
    msg = bot.send_message(
        message.chat.id,
        "Как мы назовём график?"
        " Если не хочешь давать ему название,"
        " то нажми кнопку ниже 😉",
        reply_markup=keyboard,
    )
    MESSAGE_COM = "plot"
    bot.register_next_step_handler(msg, tit)


def tit(message):
    """
    Функция вызывается ax_x(), записывает введённое пользователем название графика, вызывает data_mnk()
    :param message: сообщение пользователя
    :return:
    """
    global MESSAGE_COM
    if message.content_type == "text":
        if message.text == "Выход":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Передумал? Ну ладно...", reply_markup=keyboard
            )
            bot.send_sticker(
                message.chat.id,
                "CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ",
            )
        elif message.text == "Без названия":
            math_part.TITLE = ""
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ["✅", "❌", "Выход"]])
            msg = bot.send_message(
                message.chat.id, "Прямую по МНК строим?", reply_markup=keyboard
            )
            bot.register_next_step_handler(msg, mnk)
        else:
            math_part.TITLE = message.text
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ["✅", "❌", "Выход"]])
            msg = bot.send_message(
                message.chat.id, "Прямую по МНК строим?", reply_markup=keyboard
            )
            bot.register_next_step_handler(msg, mnk)

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["Без названия"]])
        msg = bot.send_message(
            message.chat.id,
            "Я тебя не понял... Напиши ещё раз название графика."
            " Если не хочешь давать ему название,"
            " то нажми кнопку ниже 😉",
            reply_markup=keyboard,
        )
        MESSAGE_COM = "plot"
        bot.register_next_step_handler(msg, tit)


def mnk(message):
    """
    Функция вызывается tit(), записывается выбор пользователя: строить мнк прямую или нет. Вызывает
    :param message: сообщение пользователя
    :return:
    """
    if message.content_type == "text":
        if message.text == "Выход":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Передумал? Ну ладно...", reply_markup=keyboard
            )
            bot.send_sticker(
                message.chat.id,
                "CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ",
            )
        elif message.text == "✅":
            math_part.ERROR_BAR = True
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ["0.0/0.0"]])
            msg = bot.send_message(
                message.chat.id,
                "Пришли данные для крестов погрешностей по осям х и y в"
                ' формате "123.213/123.231", если кресты не нужны, то'
                " нажми на кнопку ниже",
                reply_markup=keyboard,
            )
            bot.register_next_step_handler(msg, error_bars)
        elif message.text == "❌":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
            with open("files/Example.xlsx", "rb") as example:
                bot.send_document(message.chat.id, example)
            msg = bot.send_message(
                message.chat.id,
                "Пришли .xlsx файл с данными как в example.xlsx, и всё будет готово",
                reply_markup=keyboard,
            )
            bot.register_next_step_handler(msg, date_mnk)
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ["✅", "❌", "Выход"]])
            msg = bot.send_message(
                message.chat.id,
                "Извини, повтори ещё раз... Прямую по МНК строим?",
                reply_markup=keyboard,
            )
            bot.register_next_step_handler(msg, mnk)

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["✅", "❌", "Выход"]])
        msg = bot.send_message(
            message.chat.id,
            "Извини, повтори ещё раз... Прямую по МНК строим?",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(msg, mnk)


def error_bars(message):
    if message.content_type == "text":
        if message.text == "Выход":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Передумал? Ну ладно...", reply_markup=keyboard
            )
            bot.send_sticker(
                message.chat.id,
                "CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ",
            )
        try:
            math_part.ERRORS = list(map(float, message.text.split("/")))
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
            with open("files/Example.xlsx", "rb") as expl:
                bot.send_document(message.chat.id, expl)
            msg = bot.send_message(
                message.chat.id,
                "Пришли .xlsx файл с данными как в example.xlsx и всё будет готово",
                reply_markup=keyboard,
            )
            bot.register_next_step_handler(msg, date_mnk)
        except Exception as e:
            print(e)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ["0.0/0.0"]])
            msg = bot.send_message(
                message.chat.id,
                "Не могу распознать формат данных( Давай ещё раз. "
                "Пришли данные для крестов погрешностей по осям х и y в "
                'формате "123.213/123.231", если кресты не нужны, то'
                " нажми на кнопку ниже",
                reply_markup=keyboard,
            )
            bot.register_next_step_handler(msg, error_bars)
    else:
        math_part.ERROR_BAR = True
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["0.0/0.0"]])
        msg = bot.send_message(
            message.chat.id,
            "Ты прислал что-то не то( Давай ещё раз. "
            "Пришли данные для крестов погрешностей по осям х и y в "
            'формате "123.213/123.231", если кресты не нужны, то'
            " нажми на кнопку ниже",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(msg, error_bars)


def date_mnk(message):
    """
    Функция активирует рисование графика/линеаризованного графика/подсчёта констант и погрешностей, в зависимости от
    того, какая функция была написана пользователем.
    :param message:
    :return:
    """
    if message.content_type == "text":
        if message.text == "Выход":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Передумал? Ну ладно...", reply_markup=keyboard
            )
            bot.send_sticker(
                message.chat.id,
                "CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ",
            )
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
            msg = bot.send_message(
                message.chat.id,
                "Ты точно прислал .xlsx файл? Давай ещё раз! "
                "Пришли .xlsx файл с данными, и всё будет готово",
                reply_markup=keyboard,
            )
            bot.register_next_step_handler(msg, date_mnk)
    elif message.content_type == "document":
        if message.document.file_name == "Example.xlsx":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
            msg = bot.send_message(
                message.chat.id,
                "Переименуй файл, пожалуйста🥺 И присылай снова, я подожду",
                reply_markup=keyboard,
            )
            bot.send_sticker(
                message.chat.id,
                "CAACAgIAAxkBAAMDXj8HbU7hkvX2ou3kfBAsN6kHtKcAAsUFAAL6C7YIqZjbAAHdPGrWGAQ",
            )
            bot.register_next_step_handler(msg, date_mnk)
        else:
            try:
                file_id = message.json.get("document").get("file_id")
                file_path = bot.get_file(file_id).file_path
                downloaded_file = bot.download_file(file_path)
                FILE_NAME = message.document.file_name
                with open(FILE_NAME, "wb") as new_file:
                    new_file.write(downloaded_file)
                a, b, d_a, d_b = math_part.mnk_calc(FILE_NAME)
                math_part.BOT_PLOT = True
                math_part.plots_drawer(
                    FILE_NAME,
                    math_part.TITLE,
                    math_part.ERRORS[0],
                    math_part.ERRORS[1],
                    math_part.ERROR_BAR,
                )
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(
                    *[
                        types.KeyboardButton(name)
                        for name in ["На сегодня", "На завтра"]
                    ]
                )
                bot.send_message(
                    message.chat.id, "Принимай работу!)", reply_markup=keyboard
                )
                with open("plot.png", "rb") as photo:
                    bot.send_document(message.chat.id, photo)
                if math_part.ERROR_BAR:
                    for i in range(0, len(a)):
                        bot.send_message(
                            message.chat.id,
                            f"Коэффициенты {i + 1}-ой прямой:\n"
                            f" a = {a[i]} +- {d_a[i]}\n"
                            f" b = {b[i]} +- {d_b[i]}",
                        )
                with open("plot.pdf", "rb") as photo:
                    bot.send_document(message.chat.id, photo)
                os.remove("plot.pdf")
                os.remove("plot.png")
                math_part.BOT_PLOT = False
                if FILE_NAME != "Example.xlsx":
                    os.remove(FILE_NAME)
                math_part.TITLE = ""
                math_part.ERRORS = [0, 0]
                math_part.ERROR_BAR = False
            except Exception as e:
                os.remove(FILE_NAME)
                print(e)
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
                msg = bot.send_message(
                    message.chat.id,
                    "Ты точно прислал .xlsx файл как в примере? Давай ещё раз!",
                    reply_markup=keyboard,
                )
                bot.register_next_step_handler(msg, date_mnk)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
        msg = bot.send_message(
            message.chat.id,
            "Ты точно прислал .xlsx файл? Давай ещё раз! "
            "Пришли .xlsx файл с данными, и всё будет готово",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(msg, date_mnk)


@bot.message_handler(func=lambda message: message.text in ["На сегодня", "На завтра"])
def get_start_schedule(message):
    """
    Функция ловит сообщение с текстом "Расписание на сегодня/завтра".
    Узнает номер дня недели сегодня/завтра и по этому значению обращается в функцию timetable_by_group().
    :return:
    """
    try:
        student = psg.get_student(message.chat.id)
    except Exception as e:
        print("АШИПКА")
        print(e)
        bot.send_message(
            os.environ["ADMIN_1"],
            f"Посмотри логи у чувака"
            f" user = {message.from_user} id={message.chat.id}"
            f" пошла по пизде 706 строчка...",
        )
        bot.send_message(
            os.environ["ADMIN_2"],
            f"Посмотри логи у чувака"
            f" user = {message.from_user} id={message.chat.id}"
            f" пошла по пизде 706 строчка...",
        )
        bot.send_message(
            message.chat.id,
            "Извини, что-то пошло не так, команда устранения ошибок уже взялась за дело,"
            " попробуй эту функцию позже) Чтобы проблема решилась быстрее"
            " ты можешь написать @Error404NF",
        )
        return "Что-то пошло по пизде"

    if timetable.timetable.check_group(student[0], student[1]):
        # список дней для удобной конвертации номеров дней недели (0,1, ..., 6) в их названия
        week = tuple(
            [
                "Понедельник",
                "Вторник",
                "Среда",
                "Четверг",
                "Пятница",
                "Суббота",
                "Воскресенье",
            ]
        )
        today = (
            datetime.datetime.today().weekday()
        )  # today - какой сегодня день недели (от 0 до 6)
        if message.text == "На сегодня":  # расписание на сегодня
            schedule = timetable.timetable.timetable_by_group(
                student[1], student[0], week[today]
            )
            STRING = ""  # "строка" с расписанием, которую отправляем сообщением
            for (
                row
            ) in (
                schedule.iterrows()
            ):  # проходимся по строкам расписания, приплюсовываем их в общую "строку"
                # время пары - жирный + наклонный шрифт, название пары на следующей строке
                string: str = (
                    "<b>" + "<i>" + row[0] + "</i>" + "</b>" + "\n" + row[1][0]
                )
                STRING += string + "\n\n"  # между парами пропуск (1 enter)
            bot.send_message(
                message.chat.id, STRING, parse_mode="HTML"
            )  # parse_mode - чтобы читал измененный шрифт
            keyboard = types.ReplyKeyboardMarkup(
                resize_keyboard=True
            )  # кнопки для получения расписания на сегодня или завтра
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Чем ещё я могу помочь?", reply_markup=keyboard
            )
        elif message.text == "На завтра":  # расписание на завтра
            tomorrow = 0  # номер дня завтра, если это воскресенье (6), то уже стоит
            if today in range(6):  # если не воскресенье, то значение today + 1
                tomorrow = today + 1
            # тест на рандомной группе
            schedule = timetable.timetable.timetable_by_group(
                student[1], student[0], week[tomorrow]
            )
            STRING = ""  # "строка" с расписанием, которую отправляем сообщением
            for (
                row
            ) in (
                schedule.iterrows()
            ):  # проходимся по строкам расписания, приплюсовываем их в общую "строку"
                # время пары - жирный + наклонный шрифт, название пары на следующей строке
                string: str = (
                    "<b>" + "<i>" + row[0] + "</i>" + "</b>" + "\n" + row[1][0]
                )
                STRING += string + "\n\n"  # между парами пропуск (1 enter)
            bot.send_message(
                message.chat.id, STRING, parse_mode="HTML"
            )  # parse_mode - чтобы читал измененный шрифт
            keyboard = types.ReplyKeyboardMarkup(
                resize_keyboard=True
            )  # кнопки для получения расписания на сегодня или завтра
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Чем ещё я могу помочь?", reply_markup=keyboard
            )
    else:
        bot.send_message(
            message.chat.id,
            "Не могу найти расписание для указанных тобой номера курса и группы 😞 "
            "Нажми /profile чтобы проверить корректность данных.",
        )


@bot.message_handler(commands=["timetable"])
def get_course(message):
    """
    Функция ловит сообщение с текстом "/timetable".
    Отправляет пользователю вопрос о номере курса. Вызывает функцию get_group()
    :param message: telebot.types.Message
    :return:
    """
    if message.text == "/timetable":  # инициализация блока
        bot.send_message(
            message.chat.id,
            "Снова не можешь вспомнить, какая пара следующая? :) " "Ничего, я уже тут!",
        )
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[types.KeyboardButton(name) for name in range(1, 4)]
        )  # кнопки c номерами курсов
        keyboard.add(
            *[types.KeyboardButton(name) for name in [4, 5, "Выход"]]
        )  # кнопка для выхода из функции
        msg = bot.send_message(
            message.chat.id, "Не подскажешь номер курса?", reply_markup=keyboard
        )
        bot.register_next_step_handler(msg, get_group)
    elif (
        message.text == "Ладно, сам посмотрю"
    ):  # если после ошибки в считывании данных пришло сообщение о выходе:
        keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=True
        )  # кнопки для получения расписания на сегодня или завтра
        keyboard.add(
            *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
        )
        bot.send_message(
            message.chat.id,
            "Без проблем! " "Но ты это, заходи, если что :)",
            reply_markup=keyboard,
        )
        # стикос "Ты заходи есчо"
        bot.send_sticker(
            message.chat.id,
            "CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ",
        )
    elif (
        message.text == "Попробую ещё раз"
    ):  # если после ошибки в считывании данных в других функциях пришло
        # сообщение попробовать ввести значения еще раз
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[types.KeyboardButton(name) for name in range(1, 4)]
        )  # то же, что и в блоке инициализации
        keyboard.add(*[types.KeyboardButton(name) for name in [4, 5, "Выход"]])
        msg = bot.send_message(
            message.chat.id, "Не подскажешь номер курса?", reply_markup=keyboard
        )
        bot.register_next_step_handler(msg, get_group)


def get_group(message):
    """
    Функция сохраняет номер курса и отправляет пользователю вопрос о номере группы.
    Вызывает функцию get_weekday().
    :param message: telebot.types.Message
    :return:
    """
    global COURSE_NUM  # вызываем глобальную переменную с номером курса
    if (
        message.content_type == "text"
    ):  # проверка типа сообщения, является ли оно текстовым, а не файлом
        if (
            message.text == "Выход"
        ):  # если из функции get_course() пришло сообщение о выходе
            keyboard = types.ReplyKeyboardMarkup(
                resize_keyboard=True
            )  # кнопки для получения расписания на сегодня или завтра
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Передумал? Ну ладно...", reply_markup=keyboard
            )
            # стикос "Ты заходи есчо"
            bot.send_sticker(
                message.chat.id,
                "CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ",
            )
        elif message.text in map(str, range(1, 6)):  # если прилетел номер курса
            COURSE_NUM = int(message.text)  # запоминаем номер курса (число)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[
                    types.KeyboardButton(name)
                    for name in ["Моя группа", "Выход"]  # кнопка для выхода из функции
                ]
            )
            bot.send_message(
                message.chat.id,  # просим пользователя ввести номер группы
                "Не подскажешь номер группы?\n"
                "(В формате Б00–228 или 777, как в расписании)",
                reply_markup=keyboard,
            )
            bot.register_next_step_handler(message, get_weekday)
        elif (
            message.text == "Ладно, сам посмотрю"
        ):  # если после ошибки в считывании данных пришло сообщение о выходе:
            keyboard = types.ReplyKeyboardMarkup(
                resize_keyboard=True
            )  # кнопки для получения расписания на сегодня или завтра
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id,
                "Без проблем! " "Но ты это, заходи, если что :)",
                reply_markup=keyboard,
            )
            # стикос "Ты заходи есчо"
            bot.send_sticker(
                message.chat.id,
                "CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ",
            )
        elif (
            message.text == "Попробую ещё раз"
        ):  # если после ошибки в считывании данных в других функциях пришло
            # сообщение попробовать ввести значения еще раз
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[
                    types.KeyboardButton(name)
                    for name in ["Моя группа", "Выход"]  # кнопка для выхода из функции
                ]
            )
            bot.send_message(
                message.chat.id,  # просим пользователя ввести номер группы
                "Не подскажешь номер группы?\n"
                "(В формате Б00–228 или 777, как в расписании)",
                reply_markup=keyboard,
            )
            bot.register_next_step_handler(message, get_weekday)
        else:  # если сообщение не "Выход" и не номер курса, то говорим об ошибке и отправляем в get_course()
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[
                    types.KeyboardButton(name)
                    for name in [
                        "Попробую ещё раз",
                        "Ладно, сам посмотрю",  # первая кнопка - ввод данных заново, вторая - выход
                    ]
                ]
            )
            msg = bot.send_message(
                message.chat.id,
                "Что-то не получилось... Ты мне точно прислал номер курса в правильном "
                "формате?",
                reply_markup=keyboard,
            )
            bot.register_next_step_handler(msg, get_course)
    else:  # если сообщение не является текстом, то говорим об ошибке формата и отправляем в get_course()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[
                types.KeyboardButton(name)
                for name in ["Попробую ещё раз", "Ладно, сам посмотрю"]
            ]
        )
        msg = bot.send_message(
            message.chat.id,
            "Что-то не получилось... Ты мне точно прислал номер курса в правильном "
            "формате?",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(msg, get_course)


def get_weekday(message):
    """
    Функция сохраняет номер группы и отправляет кнопки с выбором дня недели.
    Вызывает функцию get_schedule().
    :param message: telebot.types.Message
    :return:
    """
    global GROUP_NUM, COURSE_NUM  # глобальные переменные
    if message.content_type == "text":  # проверяем, является ли сообщение текстовым
        if message.text == "Выход":  # если из get_group() прилетело сообщение о выходе
            keyboard = types.ReplyKeyboardMarkup(
                resize_keyboard=True
            )  # кнопки для получения расписания на сегодня или завтра
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Передумал? Ну ладно...", reply_markup=keyboard
            )
            bot.send_sticker(
                message.chat.id,
                "CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ",
            )
        elif (
            message.text == "Ладно, сам посмотрю"
        ):  # если после ошибки в считывании данных пришло сообщение о выходе:
            keyboard = types.ReplyKeyboardMarkup(
                resize_keyboard=True
            )  # кнопки для получения расписания на сегодня или завтра
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id,
                "Без проблем! " "Но ты это, заходи, если что :)",
                reply_markup=keyboard,
            )
            # стикос "Ты заходи есчо"
            bot.send_sticker(
                message.chat.id,
                "CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ",
            )
        elif message.text == "Попробую ещё раз":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # дни недели для тыков и кнопка для выхода (строки выбраны по размеру слов)
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["Понедельник", "Вторник"]]
            )
            keyboard.add(*[types.KeyboardButton(name) for name in ["Среда", "Четверг"]])
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["Пятница", "Суббота"]]
            )
            keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
            bot.send_message(
                message.chat.id,
                "Расписание на какой день ты хочешь узнать?",
                reply_markup=keyboard,
            )
            bot.register_next_step_handler(message, get_schedule)
        elif message.text == "Моя группа":
            GROUP_NUM = psg.get_student(message.chat.id)[0]
            if timetable.timetable.check_group(GROUP_NUM, COURSE_NUM):
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                # дни недели для тыков и кнопка для выхода (строки выбраны по размеру слов)
                keyboard.add(
                    *[types.KeyboardButton(name) for name in ["Понедельник", "Вторник"]]
                )
                keyboard.add(
                    *[types.KeyboardButton(name) for name in ["Среда", "Четверг"]]
                )
                keyboard.add(
                    *[types.KeyboardButton(name) for name in ["Пятница", "Суббота"]]
                )
                keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
                bot.send_message(
                    message.chat.id,
                    "Расписание на какой день ты хочешь узнать?",
                    reply_markup=keyboard,
                )
                bot.register_next_step_handler(message, get_schedule)
            else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(
                    *[
                        types.KeyboardButton(name)
                        for name in ["Попробую ещё раз", "Ладно, сам посмотрю"]
                    ]
                )
                msg = bot.send_message(
                    message.chat.id,
                    "Что-то не получилось... Ты мне точно прислал номер группы в правильном"
                    " формате?",
                    reply_markup=keyboard,
                )
                bot.register_next_step_handler(msg, get_group)
        else:
            GROUP_NUM = message.text
            if timetable.timetable.check_group(GROUP_NUM, COURSE_NUM):
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                # дни недели для тыков и кнопка для выхода (строки выбраны по размеру слов)
                keyboard.add(
                    *[types.KeyboardButton(name) for name in ["Понедельник", "Вторник"]]
                )
                keyboard.add(
                    *[types.KeyboardButton(name) for name in ["Среда", "Четверг"]]
                )
                keyboard.add(
                    *[types.KeyboardButton(name) for name in ["Пятница", "Суббота"]]
                )
                keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
                bot.send_message(
                    message.chat.id,
                    "Расписание на какой день недели ты хочешь узнать?",
                    reply_markup=keyboard,
                )
                bot.register_next_step_handler(message, get_schedule)
            else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(
                    *[
                        types.KeyboardButton(name)
                        for name in ["Попробую ещё раз", "Ладно, сам посмотрю"]
                    ]
                )
                msg = bot.send_message(
                    message.chat.id,
                    "Что-то не получилось... Ты мне точно прислал номер группы в правильном"
                    " формате?",
                    reply_markup=keyboard,
                )
                bot.register_next_step_handler(msg, get_group)
    else:  # если сообщение не текстовое, то говорим об ошибке формата, отсылаем в функцию get_group()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[
                types.KeyboardButton(name)
                for name in ["Попробую ещё раз", "Ладно, сам посмотрю"]
            ]
        )
        msg = bot.send_message(
            message.chat.id,
            "Что-то не получилось... Ты мне точно прислал номера группы в правильном "
            "формате?",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(msg, get_group)


pd.options.display.max_colwidth = 100


def get_schedule(message):
    """
    Функция, выдающая расписание на нужный день недели.
    :param message: telebot.types.Message
    :return:
    """
    global COURSE_NUM, GROUP_NUM
    if message.content_type == "text":  # проверка типа сообщения - текст или нет
        if (
            message.text == "Выход"
        ):  # если из функции get_group() прилетело сообщение о выходе
            keyboard = types.ReplyKeyboardMarkup(
                resize_keyboard=True
            )  # кнопки для получения расписания на сегодня или завтра
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Передумал? Ну ладно...", reply_markup=keyboard
            )
            bot.send_sticker(
                message.chat.id,
                "CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ",
            )
        elif message.text in [
            "Понедельник",
            "Вторник",
            "Среда",
            "Четверг",
            "Пятница",
            "Суббота",
        ]:  # если прилетел день недели
            schedule = timetable.timetable.timetable_by_group(
                COURSE_NUM, GROUP_NUM, message.text
            )
            STRING = ""  # проходимся по всем строчкам расписания, записываем в STRING готовое сообщение,
            # которое отправим пользователю ( см. функцию get_start_schedule() )
            for row in schedule.iterrows():
                string: str = (
                    "<b>" + "<i>" + row[0] + "</i>" + "</b>" + "\n" + row[1][0]
                )
                STRING += string + "\n\n"
            bot.send_message(message.chat.id, STRING, parse_mode="HTML")
            keyboard = types.ReplyKeyboardMarkup(
                resize_keyboard=True
            )  # кнопки для получения расписания на сегодня или завтра
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
            )
            bot.send_message(
                message.chat.id, "Чем ещё я могу помочь?", reply_markup=keyboard
            )
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[
                    types.KeyboardButton(name)
                    for name in ["Попробую ещё раз", "Ладно, сам посмотрю"]
                ]
            )
            msg = bot.send_message(
                message.chat.id,
                "Что-то не получилось... Ты мне точно прислал день недели в правильном "
                "формате?",
                reply_markup=keyboard,
            )
            bot.register_next_step_handler(msg, get_weekday)
    else:  # если сообщение не текстовое, то говорим об ошибке формате
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[
                types.KeyboardButton(name)
                for name in ["Попробую ещё раз", "Ладно, сам посмотрю"]
            ]
        )
        msg = bot.send_message(
            message.chat.id,
            "Что-то не получилось... Ты мне точно прислал день недели в правильном "
            "формате?",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(msg, get_weekday)


@bot.message_handler(commands=["exam"])
def ask_group(message):
    """
    Функция ловит сообщение с текстом '/exam'.
    Отправляет запрос о выборе группы и вызывает функцию get_exam_timetable().
    :param message: telebot.types.Message
    :return:
    """
    bot.send_message(message.chat.id, "Ещё не время... Но ты не забывай...")
    bot.send_sticker(
        message.chat.id,
        "CAACAgIAAxkBAAMEXj8IxnJkYATlpAOTkJyLiXH2u0UAAvYfAAKiipYBsZcZ_su45LkYBA",
    )


def get_exam_timetable(message):
    """
    Функция считывает номер группы, вызывает функцию get_exam_timetable из модуля timetable,
    отправляет пользователю раписание экзаменов из файла.
    :param message: telebot.types.Message
    :return:
    """
    if message.text in texting.texting_symbols.groups:
        path = os.path.abspath("")
        timetable.timetable_old.get_exam_timetable(message.text)
        f = open(f"{path}/timetable/exam.txt")
        for line in f:
            bot.send_message(message.chat.id, line)
        open(f"{path}/timetable/exam.txt", "w").close()
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[
                types.KeyboardButton(name)
                for name in ["Попробую ещё раз", "Ладно, сам посмотрю"]
            ]
        )
        msg = bot.send_message(
            message.chat.id,
            "Что-то не получилось... "
            "Ты мне точно прислал номер группы в правильном формате ?",
            reply_markup=keyboard,
        )
        bot.register_next_step_handler(msg, ask_group)


@bot.message_handler(commands=["god_voice"])
def get_message_text(message):
    pers_id = message.chat.id
    admins = [
        int(os.environ["ADMIN_1"]),
        int(os.environ["ADMIN_2"]),
        int(os.environ["ADMIN_3"]),
    ]
    if pers_id in admins:
        msg = bot.send_message(
            message.chat.id, 'Пришли мне сообщение в формате "chat_id/message_text"'
        )
        bot.register_next_step_handler(msg, send_message)
    else:
        bot.send_message(
            message.chat.id,
            "Боюсь, я не совсем понимаю, о чём ты. \n"
            "Напиши /help, чтобы узнать, что я умею.\n",
        )


def send_message(message):
    try:
        chat_id = int(message.text.split("/")[0])
        text = message.text.split("/")[1]
        bot.send_message(chat_id, text)
        bot.send_message(message.chat.id, "Готово")
    except Exception as e:
        bot.send_message(message.chat.id, "Попробуй ещё раз")
        print(e)


@bot.message_handler(content_types=["text"])
def chatting(message):
    """
    Функция запускается, если пользователь пишет любой незнакомый боту текст.
    :param message: any text
    :return: циклично возвращает одно вспомогательное сообщение, два смайлика,
    две цитаты, одну фотку собаки при последовательной отправке незнакомого текста
    """
    global crazy_tokens
    crazy_tokens += 1
    if crazy_tokens <= 1:
        bot.send_message(
            message.chat.id,
            "Боюсь, я не совсем понимаю, о чём ты. \n"
            "Напиши /help, чтобы узнать, что я умею.\n",
        )
    elif crazy_tokens <= 3:
        bot.send_message(message.chat.id, random.choice(texting.texting_symbols.emoji))
    elif crazy_tokens <= 5:
        bot.send_message(message.chat.id, random.choice(texting.texting_symbols.quotes))
    elif crazy_tokens == 6:
        doggy = get_image_url()
        """
        API_LINK = 'http://api.forismatic.com/api/method=getQuote&format=text&lang=ru'
        cont = requests.post(API_LINK)
        print(cont.text)
        bot.send_message(message.chat.id, quote)
        """

        bot.send_photo(message.chat.id, photo=doggy)
        crazy_tokens = 0


def get_url():
    """
    Функция получает ссылку на картинку собаки
    :return: ссылка на картинку
    """
    contents = requests.get("https://random.dog/woof.json").json()
    url = contents["url"]
    return url


def get_image_url():
    """
    Функция проверяет расширение картинки с собакой
    :return: ссылка на картинку
    """
    allowed_extension = ["jpg", "jpeg", "png"]
    file_extension = ""
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url


bot.polling(none_stop=True)
