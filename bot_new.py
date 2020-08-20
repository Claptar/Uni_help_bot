import os
import logging
import pickle

import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from math_module import math_part
from koryavov import kor
from data_constructor import psg
import datetime

logging.basicConfig(level=logging.INFO)

API_TOKEN = '893576564:AAHxlCPFCfcewfz2_0rlygYfJzCbhz4HYJs'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Start(StatesGroup):
    group = State()
    custom = State()


class Profile(StatesGroup):
    choose = State()
    group = State()
    custom = State()


class Timetable(StatesGroup):
    choose = State()
    another_group = State()
    weekday = State()


class Koryavov(StatesGroup):
    sem_num_state = State()
    sem_num = 0
    task_num_state = State()
    task_num = 0


class Custom(StatesGroup):
    existing = State()
    new = State()
    weekday = State()
    time = State()
    edit = State()
    again = State()


class Plots(StatesGroup):
    title_state = State()
    title = ''
    mnk_state = State()
    mnk = False
    error_bars_state = State()
    errors = []
    plot_state = State()


def today_tomorrow_keyboard():
    """
    Кнопки для получения расписания на сегодня или завтра.
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
    return keyboard


def schedule_string(schedule: pd.DataFrame):
    """
    Строка с расписанием, которую отправляет бот.
    """
    STRING = ''  # "строка" с расписанием, которую отправляем сообщением
    for row in schedule.iterrows():  # проходимся по строкам расписания, приплюсовываем их в общую "строку"
        # время пары - жирный + наклонный шрифт, название пары на следующей строке
        string: str = '<b>' + '<i>' + row[0] + '</i>' + '</b>' + '\n' + row[1][0]
        STRING += string + '\n\n'  # между парами пропуск (1 enter)
    # parse_mode - чтобы читал измененный шрифт
    return STRING


@dp.message_handler(Text(equals='Выход'), state='*')
async def user_exit(message: types.Message, state: FSMContext):
    """
    Функция, выполняющая выход по желанию пользователя (на любой стадии).
    """
    current_state = await state.get_state()  # проверка, что запущено хотя бы какое-то из состояний
    if current_state is None:
        return

    await bot.send_message(
        message.chat.id,
        'Без проблем! Но ты это, заходи, если что 😉',
        reply_markup=today_tomorrow_keyboard()
    )
    # стикос "Ты заходи есчо"
    await bot.send_sticker(
        message.chat.id,
        'CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ'
    )
    # При выходе выключаем машину состояний
    await state.finish()


@dp.message_handler(Text(equals=['На сегодня', 'На завтра']))
async def send_today_tomorrow_schedule(message):
    """
    Функция ловит сообщение с текстом 'На сегодня/завтра'.
    Возвращает расписание на этот день, вызывает функцию timetable.timetable_by_group().
    По умолчанию, если у этого пользователя есть кастомное расписание, выдает его,
    иначе - расписание группы пользователя.
    """
    # список дней для удобной конвертации номеров дней недели (0, 1, ..., 6) в их названия
    week = tuple(['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'])
    today = datetime.datetime.today().weekday()  # today - какой сегодня день недели (от 0 до 6)
    tomorrow = today + 1 if today in range(6) else 0  # номер дня для завтра, если это воскресенье (6), то 0
    day = today if message.text == 'На сегодня' else tomorrow  # выбор дня в зависимости от запроса
    table = psg.send_timetable(
        custom=True,
        my_group=False,
        chat_id=message.chat.id
    )
    if table:  # если пользователь есть в базе
        if table[0]:  # проверка, есть ли у этого пользователя кастомное расписание в базе данных
            schedule = pickle.loads(table[0])[week[day]].to_frame()
            await bot.send_message(  # отправляем расписание
                message.chat.id,
                schedule_string(schedule),
                parse_mode='HTML'
            )
        else:  # если у этого пользователя нет кастомного расписания в базе данных, отправляем расписание группы
            table = psg.send_timetable(
                custom=False,
                my_group=True,
                chat_id=message.chat.id
            )
            if table:  # если пользователь есть в базе
                schedule = pickle.loads(table[0])[week[day]].to_frame()
                await bot.send_message(  # отправляем расписание
                    message.chat.id,
                    schedule_string(schedule),
                    parse_mode='HTML'
                )
        await bot.send_message(
            message.chat.id,
            'Чем ещё я могу помочь?',
            reply_markup=today_tomorrow_keyboard()
        )
    else:  # если в базе данных нет этого пользователя (или произошла ошибка)
        await bot.send_message(
            message.chat.id,
            'Что-то пошло не так, попробуй еще раз позже, пожалуйста)\n'
            'Если мы с тобой еще не знакомы, то скорей пиши /start!',
            reply_markup=today_tomorrow_keyboard()
        )


@dp.message_handler(commands=['help'])
async def help_def(message: types.Message):
    """
    Функция ловит сообщение с командой '/help' и присылает описание комманд бота.
    """
    with open('files/help.txt', encoding='utf-8', mode='r') as f:
        text = f.read()
    await bot.send_message(message.chat.id, text)


@dp.message_handler(commands='start')
async def start_initiate(message: types.Message):
    """
    Функция ловит сообщение с командой '/start' и приветствует пользователя.
    """
    if psg.check_user_group(message.chat.id):  # если пользователь уже есть в базе данных
        await bot.send_message(
            message.chat.id,
            'Привет-привет! 🙃\nМы уже с тобой знакомы 😉 '
            'Напиши /help, чтобы я напомнил тебе, что я умею)',
            reply_markup=today_tomorrow_keyboard()
        )
    else:  # пользователя нет в базе данных
        await Start.group.set()  # изменяем состояние на Start.group
        await bot.send_message(
            message.chat.id,
            'Привет-привет! 🙃\nДавай знакомиться! Меня зовут A2. '
            'Можешь рассказать мне немного о себе, '
            'чтобы я знал, чем могу тебе помочь?'
        )
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Уже не учусь', 'Выход']])
        await bot.send_message(  # 'Уже не учусь' - вариант для выпускников
            message.chat.id,
            ' Не подскажешь номер своей группы?\n'
            '(В формате Б00–228 или 777, как в расписании)',
            reply_markup=keyboard
        )


@dp.message_handler(state=Start.group)
async def start_proceed_group(message: types.Message, state: FSMContext):
    """
    Функция принимает значение номера группы и проверяет, есть ли такая группа в базе.
    Если группы нет в базе данных (или произошла какая-то ошибка), то функция просит ввести номер группы заново.
    Если группа есть в базе данных, информация о пользователе заносится в таблицу User, а пользователю
    отправляется запрос, нужно ли ему кастомное расписание.
    """
    (group, text) = (
        'ALUMNI',
        'Привет достопочтенному выпускнику! 👋'
    ) if message.text == 'Уже не учусь' else (  # разные варианты для выпускника и студента
        message.text,
        'Отлично, вот мы и познакомились 🙃'
    )
    if psg.insert_user(message.chat.id, group):  # группа есть в базе, добавление пользователя прошло успешно
        async with state.proxy() as data:
            data['group'] = group
        await Start.custom.set()  # меняем состояние на Start.custom
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Хочу', 'Не хочу']])
        await bot.send_message(  # запрос о кастомном расписании
            message.chat.id,
            text + '\nЕсли хочешь получить возможность использовать '
                   'кастомное расписание, нажми на нужную кнопку внизу.',
            reply_markup=keyboard
        )
    else:  # группы нет в базе (или произошла какая-то ошибка), просим повторить ввод
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Уже не учусь', 'Выход']])
        await bot.send_message(
            message.chat.id,
            'Что-то пошло не так, введи номер своей группы ещё раз, пожалуйста)',
            reply_markup=keyboard
        )


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT,
                    content_types=types.message.ContentType.ANY, state=Start.group)
async def start_proceed_group_invalid_type(message: types.Message):
    """
    Функция просит ввести номер группы заново, если формат ввода номера группы неправильный.
    """
    await message.reply("Пришли номер группы в верном формате, пожалуйста)")


@dp.message_handler(Text(equals=['Хочу', 'Не хочу']), state=Start.custom)
async def start_proceed_custom(message: types.Message, state: FSMContext):
    """
    Функция принимает ответ пользователя, нужно ли ему кастомное расписание, заносит заготовку
    в базу данных, если ответ положительный.
    """
    if message.text == 'Не хочу':  # ответ пользователя отрицательный
        await bot.send_message(
            message.chat.id,
            'Хорошо, но не забывай, что ты всегда можешь вернуться, '
            'если захочешь опробовать его в деле 😉\n'
            'Чтобы вызвать кастомное расписание, напиши /custom.'
        )
        await bot.send_message(  # в любом случае пишем про /help
            message.chat.id,
            'А теперь скорее пиши /help, чтобы узнать, '
            'чем еще я могу помочь тебе!',
            reply_markup=today_tomorrow_keyboard()
        )
    elif message.text == 'Хочу':  # ответ пользователя положительный
        async with state.proxy() as data:
            group = data['group']
        # если номер группы верный (по идее должно быть выполнено)
        # и добавление заготовки расписания прошло успешно
        if psg.update_user(message.chat.id, group, update_custom=True):
            await bot.send_message(
                message.chat.id,
                'Отлично, все получилось 🙃\n'
                'Теперь ты можешь использовать кастомное расписание! '
                'Чтобы вызвать его, напиши /custom.'
            )
            await bot.send_message(
                message.chat.id,
                'А теперь скорее пиши /help, чтобы узнать, '
                'чем еще я могу помочь тебе!',
                reply_markup=today_tomorrow_keyboard()
            )
        else:
            await bot.send_message(
                message.chat.id,
                'Что-то пошло не так, попробуй еще раз позже, пожалуйста)\n'
                'Чтобы настроить кастомное расписание, напиши /custom.'
            )
            await bot.send_message(
                message.chat.id,
                'Не расстраивайся! Напиши /help, чтобы узнать, '
                'чем еще я могу помочь тебе!',
                reply_markup=today_tomorrow_keyboard()
            )
    await state.finish()  # в любом случае останавливаем машину состояний


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT
                    or message.text not in ['Хочу', 'Не хочу'],
                    content_types=types.message.ContentType.ANY, state=Start.custom)
async def start_proceed_custom_invalid(message: types.Message):
    """
    Функция просит выбрать из вариант из предложенных, если формат ввода неправильный.
    """
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


@dp.message_handler(commands='profile')
async def edit_initiate(message: types.Message):
    """
    Функция ловит сообщение с командой '/profile' и спрашивает у пользователя,
    хочет ли он изменить группу, закрепленную за ним.
    """
    cur_group = psg.check_user_group(message.chat.id)
    if cur_group:
        await Profile.choose.set()  # изменяем состояние на Profile.choose
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Да', 'Нет', 'Выход']])
        if cur_group[0] == 'ALUMNI':
            await bot.send_message(
                message.chat.id,
                f'Сейчас у тебя указано, что ты – выпускник. '
                'Ты хочешь изменить это значение на номер группы?',
                reply_markup=keyboard
            )
        else:
            await bot.send_message(
                message.chat.id,
                f'Сейчас у тебя указано, что ты учишься в группе {cur_group[0]}. '
                'Ты хочешь изменить это значение?',
                reply_markup=keyboard
            )
    else:
        await bot.send_message(
            message.chat.id,
            'Что-то пошло не так, попробуй еще раз позже, пожалуйста)\n'
            'Если мы с тобой еще не знакомы, то скорей пиши /start!',
            reply_markup=today_tomorrow_keyboard()
        )


@dp.message_handler(Text(equals=['Да', 'Нет']), state=Profile.choose)
async def edit_proceed_choose(message: types.Message, state: FSMContext):
    """
    Функция принимает ответ пользователя, хочет ли он поменять значение группы
    и просит пользователя ввести желаемый номер группы.
    """
    if message.text == 'Да':  # положительный ответ, запрос о вводе номера группы
        await Profile.group.set()  # изменяем состояние на Profile.group
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Уже не учусь', 'Выход']])
        await bot.send_message(
            message.chat.id,
            'Введи номер группы, пожалуйста)',
            reply_markup=keyboard
        )
    elif message.text == 'Нет':  # отрицательный ответ
        await bot.send_message(
            message.chat.id,
            'Я рад, что тебя все устраивает 😉',
            reply_markup=today_tomorrow_keyboard()
        )
        await state.finish()  # выключаем машину состояний


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT
                    or message.text not in ['Да', 'Нет', 'Выход'],
                    content_types=types.message.ContentType.ANY, state=Profile.choose)
async def edit_proceed_choose_invalid(message: types.Message):
    """
    Функция просит выбрать из вариант из предложенных, если формат ввода неправильный.
    """
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


@dp.message_handler(state=Profile.group)
async def edit_proceed_group(message: types.Message, state: FSMContext):
    """
    Функция ловит ответ пользователя с номером группы, если обновление удалось сделать,
    посылает пользователю запрос, хочет ли он изменить свое кастомное расписание.
    :param message:
    :param state:
    :return:
    """
    # получилось обновить номер группы, запрос о изменении кастомного расписания
    group = 'ALUMNI' if message.text == 'Уже не учусь' else message.text
    if psg.update_user(message.chat.id, group, update_custom=False):
        async with state.proxy() as data:
            data['group'] = group
        await Profile.custom.set()  # изменяем состояние на Profile.custom
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Хочу', 'Не хочу']])
        await bot.send_message(
            message.chat.id,
            'Все готово) Ты хочешь поменять кастомное '
            'расписание на расписание новой группы?',
            reply_markup=keyboard
        )
    else:  # номера группы нет в базе (или произошла какая-то ошибка)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Уже не учусь', 'Выход']])
        await bot.send_message(  # просим пользователя ввести номер группы еще раз
            message.chat.id,
            'Что-то пошло не так, введи номер своей группы ещё раз, пожалуйста)',
            reply_markup=keyboard
        )


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT,
                    content_types=types.message.ContentType.ANY, state=Profile.group)
async def edit_proceed_group_invalid_type(message: types.Message):
    """
    Функция просит ввести номер группы заново, если формат ввода номера группы неправильный.
    """
    await message.reply("Пришли номер группы в верном формате, пожалуйста)")


@dp.message_handler(Text(equals=['Хочу', 'Не хочу']), state=Profile.custom)
async def edit_proceed_custom(message: types.Message, state: FSMContext):
    if message.text == 'Не хочу':  # если пришел отрицательный ответ
        await bot.send_message(
            message.chat.id,
            'Я рад, что тебя все устраивает 😉',
            reply_markup=today_tomorrow_keyboard()
        )
    elif message.text == 'Хочу':  # если пришел положительный ответ, то изменяем кастомное расписание
        async with state.proxy() as data:
            group = data['group']
        if psg.update_user(message.chat.id, group, update_custom=True):
            await bot.send_message(
                message.chat.id,
                'Отлично, все получилось 🙃\n'
                'Чтобы вызвать кастомное расписание, напиши /custom.',
                reply_markup=today_tomorrow_keyboard()
            )
        else:  # если произошла ошибка при обновлении расписания
            await bot.send_message(
                message.chat.id,
                'Что-то пошло не так, попробуй еще раз позже, пожалуйста)\n'
                'Чтобы настроить кастомное расписание, напиши /custom.',
                reply_markup=today_tomorrow_keyboard()
            )
    await state.finish()


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT
                    or message.text not in ['Хочу', 'Не хочу'],
                    content_types=types.message.ContentType.ANY, state=Profile.custom)
async def edit_proceed_custom_invalid(message: types.Message):
    """
    Функция просит выбрать из вариант из предложенных, если формат ввода неправильный.
    """
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


@dp.message_handler(commands='koryavov')
async def koryavov(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in [1, 2, 3, 4, 5, 'Выход']])  # кнопки c номерами семестров
    await bot.send_message(message.chat.id, 'Выбери номер семестра общей физики: \n'
                                            '1) Механика \n'
                                            '2) Термодинамика \n'
                                            '3) Электричество \n'
                                            '4) Оптика\n'
                                            '5) Атомная и ядерная физика', reply_markup=keyboard)
    await Koryavov.sem_num_state.set()


@dp.message_handler(lambda message: message.text.isdigit(), state=Koryavov.sem_num_state)
async def sem_num(message: types.Message):
    Koryavov.sem_num = int(message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])
    await bot.send_message(message.chat.id, 'Отлично, напиши теперь номер задачи', reply_markup=keyboard)
    await Koryavov.task_num_state.set()


# If some invalid input
@dp.message_handler(state=Koryavov.sem_num_state)
async def kor_sem_inv_input(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in [1, 2, 3, 4, 5, 'Выход']])  # кнопки c номерами семестров
    await bot.send_message(message.chat.id, 'Что-то не так, давай ещё раз. Выбери номер семестра:')


@dp.message_handler(lambda message: math_part.is_digit(message.text), state=Koryavov.task_num_state)
async def task_page(message: types.Message, state: FSMContext):
    Koryavov.task_num = message.text
    reply = 'Информация взята с сайта mipt1.ru \n\n' + kor.kor_page(Koryavov.sem_num, Koryavov.task_num)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
    await bot.send_message(message.chat.id, reply, reply_markup=keyboard)
    await state.finish()


# If some invalid input
@dp.message_handler(state=Koryavov.task_num_state)
async def kor_task_inv_input(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])
    await bot.send_message(message.chat.id, 'Что-то не так, давай ещё раз. Введи номер задачи.', reply_markup=keyboard)


@dp.message_handler(commands='timetable')
async def timetable_initiate(message: types.Message):
    """
    Функция ловит сообщение с текстом "/timetable".
    Отправляет пользователю вопрос, расписание своей или другой группы ему нужно.
    """
    await Timetable.choose.set()  # ставим состояние Timetable.choose
    await bot.send_message(
        message.chat.id,
        'Снова не можешь вспомнить, какая пара следующая?\n'
        'Ничего, я уже тут! 😉'
    )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Кастомное', 'Моя группа']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Другая группа', 'Выход']])
    await bot.send_message(
        message.chat.id,
        'Выбери, пожалуйста, какое расписание тебе нужно)',
        reply_markup=keyboard
    )


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT
                    or message.text not in ['Кастомное', 'Моя группа', 'Другая группа', 'Выход'],
                    state=Timetable.choose, content_types=types.message.ContentType.ANY)
async def timetable_proceed_choose_invalid(message: types.Message):
    """
    Функция просит пользователя выбрать вариант из списка ['Кастомное', 'Моя группа', 'Другая группа', 'Выход'],
    если сообщение не содержит никакую из этих строк (+ проверка типа сообщения).
    """
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


@dp.message_handler(Text(equals=['Другая группа']), state=Timetable.choose)
async def timetable_proceed_choose(message: types.Message):
    """
    Функция ловит сообщение с текстом 'Другая группа' и отправляет пользователю вопрос о номере группы.
    """
    await Timetable.another_group.set()  # изменяем состояние на Timetable.another_group
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])  # кнопка для выхода из функции
    await bot.send_message(
        message.chat.id,  # просим пользователя ввести номер группы
        'Не подскажешь номер группы?\n'
        '(В формате Б00–228 или 777, как в расписании)',
        reply_markup=keyboard
    )


@dp.message_handler(state=Timetable.another_group)
async def timetable_proceed_another_group(message: types.Message, state: FSMContext):
    """
    Функция принимает сообщение с номером группы и проверяет его. Если все хорошо, то отправляет
    пользователю запрос о дне недели. Если произошла какая-то ошибка, то функция просит пользователя
    ввести номер группы еще раз.
    """
    table = psg.send_timetable(custom=False, my_group=False, another_group=message.text)
    if table:
        await Timetable.weekday.set()  # изменяем состояние на Timetable.weekday
        async with state.proxy() as data:
            data['schedule'] = pickle.loads(table[0])  # записываем расписание
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # дни недели для тыков и кнопка для выхода (строки выбраны по размеру слов)
        keyboard.add(*[types.KeyboardButton(name) for name in ['На неделю']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Понедельник', 'Вторник']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Среда', 'Четверг']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Пятница', 'Суббота']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Воскресенье', 'Выход']])
        await bot.send_message(
            message.chat.id,
            'Расписание на какой день недели ты хочешь узнать?',
            reply_markup=keyboard
        )
    else:  # номера группы нет в базе (или произошла какая-то ошибка)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])
        await bot.send_message(  # просим пользователя ввести номер группы еще раз
            message.chat.id,
            'Что-то пошло не так, введи номер своей группы ещё раз, пожалуйста)',
            reply_markup=keyboard
        )


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT,
                    state=Timetable.another_group,
                    content_types=types.message.ContentType.ANY)
async def timetable_proceed_another_group_invalid_type(message: types.Message):
    """
    Функция просит ввести номер группы заново, если формат ввода неправильный.
    """
    await message.reply("Пришли номер группы в верном формате, пожалуйста)")


@dp.message_handler(Text(equals=['Кастомное', 'Моя группа']), state=Timetable.choose)
async def timetable_proceed_my_group_custom(message: types.Message, state: FSMContext):
    """
    Функция принимает сообщение от пользователя с запросом нужного ему варианта расписания.
    Отправляет пользователю вопрос о нужном дне недели. В случае ошибки отправляет пользователю
    сообщение о необходимости редактирования номера группы или кастомного расписания.
    """
    table = (psg.send_timetable(  # нужное пользователю расписание
        custom=True, my_group=False, chat_id=message.chat.id
    ) if message.text == 'Кастомное' else psg.send_timetable(
        custom=False, my_group=True, chat_id=message.chat.id
    )
             )
    if table:  # если расписание было найдено
        if table[0]:
            await Timetable.weekday.set()  # изменяем состояние на Timetable.weekday
            async with state.proxy() as data:
                data['schedule'] = pickle.loads(table[0])  # записываем расписание
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # дни недели для тыков и кнопка для выхода (строки выбраны по размеру слов)
            keyboard.add(*[types.KeyboardButton(name) for name in ['На неделю']])
            keyboard.add(*[types.KeyboardButton(name) for name in ['Понедельник', 'Вторник']])
            keyboard.add(*[types.KeyboardButton(name) for name in ['Среда', 'Четверг']])
            keyboard.add(*[types.KeyboardButton(name) for name in ['Пятница', 'Суббота']])
            keyboard.add(*[types.KeyboardButton(name) for name in ['Воскресенье', 'Выход']])
            await bot.send_message(
                message.chat.id,
                'Расписание на какой день недели ты хочешь узнать?',
                reply_markup=keyboard
            )
        else:
            await bot.send_message(
                message.chat.id,
                'Не могу найти твое кастомное расписание 😞\n'
                'Нажми /custom чтобы проверить корректность данных.',
                reply_markup=today_tomorrow_keyboard()
            )
            await state.finish()
    else:  # если в базе данных нет этого пользователя (или произошла ошибка)
        await bot.send_message(
            message.chat.id,
            'Что-то пошло не так, попробуй еще раз позже, пожалуйста)\n'
            'Если мы с тобой еще не знакомы, то скорей пиши /start!',
            reply_markup=today_tomorrow_keyboard()
        )
        await state.finish()  # в случае ошибки выключаем машину состояний


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT
                    or message.text not in ['На неделю', 'Понедельник', 'Вторник', 'Среда',
                                            'Четверг', 'Пятница', 'Суббота', 'Воскресенье', 'Выход'],
                    state=Timetable.weekday,
                    content_types=types.message.ContentType.ANY)
async def timetable_proceed_weekday_invalid(message: types.Message):
    """
    Функция просит пользователя выбрать вариант из списка ['На неделю', 'Понедельник', 'Вторник', 'Среда',
                                                           'Четверг', 'Пятница', 'Суббота', 'Воскресенье', 'Выход'],
    если сообщение не содержит никакую из этих строк.
    """
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


@dp.message_handler(Text(equals=['На неделю', 'Понедельник', 'Вторник', 'Среда',
                                 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']),
                    state=Timetable.weekday)
async def timetable_return_schedule(message: types.Message, state: FSMContext):
    """
    Функция отправляет расписание на выбранный день недели.
    """
    async with state.proxy() as data:
        schedule = data['schedule']  # берем расписание из памяти
        data.clear()
    if message.text != 'На неделю':  # расписание на 1 день
        await bot.send_message(  # отправляем расписание
            message.chat.id,
            schedule_string(schedule[message.text].to_frame()),
            parse_mode='HTML'
        )
    else:  # расписание на неделю (на каждый из 7 дней)
        for day in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']:
            await bot.send_message(  # отправляем расписание
                message.chat.id,
                schedule_string(schedule[day].to_frame()),
                parse_mode='HTML'
            )

    await bot.send_message(
        message.chat.id,
        'Чем ещё я могу помочь?',
        reply_markup=today_tomorrow_keyboard()
    )
    await state.finish()  # выключаем машину состояний


@dp.message_handler(commands=['exam'])
async def exam_initiate(message: types.Message):
    """
    Функция ловит сообщение с текстом '/exam'.
    Отправляет запрос о выборе группы и вызывает функцию get_exam_timetable().
    """
    await bot.send_message(
        message.chat.id,
        'Ещё не время... Но ты не забывай...'
    )
    await bot.send_sticker(
        message.chat.id,
        'CAACAgIAAxkBAAMEXj8IxnJkYATlpAOTkJyLiXH2u0UAAvYfAAKiipYBsZcZ_su45LkYBA'
    )


@dp.message_handler(commands=['custom'])
async def custom_initiate(message: types.Message):
    """
    Функция ловит сообщение с текстом '/custom'.
    Если пользователь есть в базе, то функция проверяет наличие кастомного расписания.
    В случае отсутствия такового в базе данных отправляет пользователю вопрос, хочет ли он
    завести такое расписание. Если кастомное расписание для этого пользователя есть в базе,
    фукция посылает запрос о выборе дня недели, расписание на который нужно выдать или как-то поменять.
    """
    await bot.send_message(
        message.chat.id,
        'Хочешь посмотреть кастомное расписание '
        'или что-то отредактировать в нем? '
        'В этом я всегда рад тебе помочь 😉'
    )
    table = psg.send_timetable(custom=True, my_group=False, chat_id=message.chat.id)
    if table:  # если пользователь есть в базе
        if table[0]:  # если у него уже есть кастомное расписание
            await Custom.existing.set()  # изменяем состояние на Custom.existing
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Посмотреть', 'Изменить', 'Выход']])
            await bot.send_message(  # вопрос, что пользователь хочет сделать с расписанием
                message.chat.id,
                'Выбери, пожалуйста, что ты хочешь '
                'сделать с кастомным расписанием)',
                reply_markup=keyboard
            )
        else:  # если у пользователя еще нет кастомного расписания
            await Custom.new.set()  # изменяем состояние на Custom.new
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Давай', 'Как-нибудь потом', 'Выход']])
            await bot.send_message(
                message.chat.id,
                'У тебя пока еще нет кастомного расписания 😢\n'
                'Давай заведем его тебе?',
                reply_markup=keyboard
            )
    else:  # если в базе данных нет этого пользователя (или произошла ошибка)
        await bot.send_message(
            message.chat.id,
            'Что-то пошло не так, попробуй еще раз позже, пожалуйста)\n'
            'Если мы с тобой еще не знакомы, то скорей пиши /start!',
            reply_markup=today_tomorrow_keyboard()
        )


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT
                    or message.text not in ['Давай', 'Как-нибудь потом', 'Выход'],
                    state=Custom.new,
                    content_types=types.message.ContentType.ANY)
async def custom_add_new_invalid(message: types.Message):
    """
    Функция просит пользователя выбрать вариант из списка ['Давай', 'Как-нибудь потом', 'Выход'],
    если сообщение не содержит никакую из этих строк.
    """
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


@dp.message_handler(Text(equals=['Давай', 'Как-нибудь потом']), state=Custom.new)
async def custom_add_new(message: types.Message, state: FSMContext):
    """
    Функция принимает ответ пользователя, нужно ли ему кастомное расписание,
    в случае положительного ответа заводит ему такое расписание.
    """
    if message.text == 'Давай':  # положительный ответ
        group = psg.check_user_group(message.chat.id)  # группа пользователя из базы данных
        if group and psg.update_user(message.chat.id, group[0], update_custom=True):
            await bot.send_message(  # все нормально обновилось
                message.chat.id,
                'Отлично, все получилось 🙃\n'
                'Теперь ты можешь использовать кастомное расписание! '
                'Чтобы вызвать его, напиши /custom.',
                reply_markup=today_tomorrow_keyboard()
            )
        else:  # произошла какая-то ошибка
            await bot.send_message(
                message.chat.id,
                'Что-то пошло не так, попробуй еще раз позже, пожалуйста)',
                reply_markup=today_tomorrow_keyboard()
            )
    else:  # отрицательный ответ
        await bot.send_message(
            message.chat.id,
            'Хорошо, но не забывай, что ты всегда можешь вернуться, '
            'если захочешь опробовать его в деле 😉',
            reply_markup=today_tomorrow_keyboard()
        )
    await state.finish()  # тупиковая ветка, останавливаем машину состояний


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT
                    or message.text not in ['Посмотреть', 'Изменить', 'Выход'],
                    state=Custom.existing,
                    content_types=types.message.ContentType.ANY)
async def custom_choose_existing_invalid(message: types.Message):
    """
    Функция просит пользователя выбрать вариант из списка ['Посмотреть', 'Изменить', 'Выход'],
    если сообщение не содержит никакую из этих строк.
    """
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


@dp.message_handler(Text(equals=['Посмотреть', 'Изменить']), state=Custom.existing)
async def custom_choose_existing(message: types.Message, state: FSMContext):
    """
    Функция ловит запрос пользователя о просмотре или изменении кастомного расписания,
    отправляет запрос о нужном дне недели.
    """
    await Custom.weekday.set()  # изменяем состояние на Custom.weekday
    async with state.proxy() as data:
        data['choice'] = message.text  # сохраняем ответ, понадобится дальше
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # дни недели для тыков и кнопка для выхода (строки выбраны по размеру слов)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Понедельник', 'Вторник']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Среда', 'Четверг']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Пятница', 'Суббота']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Воскресенье', 'Выход']])
    text = ('расписание на который ты хочешь посмотреть)'
            if message.text == 'Посмотреть' else
            'в расписание на который ты хочешь внести изменения)'
            )  # в зависимости от ответа выбираем строчку, которую будем отправлять
    await bot.send_message(
        message.chat.id,
        'Выбери, пожалуйста, день недели, ' + text,
        reply_markup=keyboard
    )


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT
                    or message.text not in ['Понедельник', 'Вторник', 'Среда', 'Четверг',
                                            'Пятница', 'Суббота', 'Воскресенье', 'Выход'],
                    state=Custom.weekday,
                    content_types=types.message.ContentType.ANY)
async def custom_proceed_weekday_invalid(message: types.Message):
    """
    Функция просит пользователя выбрать вариант из списка ['Понедельник', 'Вторник', 'Среда', 'Четверг',
                                                           'Пятница', 'Суббота', 'Воскресенье', 'Выход'],
    если сообщение не содержит никакую из этих строк.
    """
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


@dp.message_handler(Text(equals=['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']),
                    state=Custom.weekday)
async def custom_proceed_weekday(message: types.Message, state: FSMContext):
    """
    Функция ловит сообщение с днем недели и, в зависимости от того, что нужно пользователю,
    либо выдает ему расписание, либо посылает запрос о времени пары, расписание на которую нужно поменять.
    """
    table = psg.send_timetable(custom=True, my_group=False, chat_id=message.chat.id)
    if table:  # не произошло никакой ошибки (кастомное расписание точно есть, проверено ранее)
        schedule = pickle.loads(table[0])  # расписание на неделю
        await bot.send_message(  # присылаем текущее состояние расписания
            message.chat.id,
            schedule_string(schedule[message.text].to_frame()),
            parse_mode='HTML'
        )  # parse_mode - чтобы читал измененный шрифт
        async with state.proxy() as data:
            choice = data['choice']
            data.clear()
        if choice == 'Посмотреть':  # смотрим на ответ, сохраненный ранее
            await bot.send_message(  # если пользователю нужно было посмотреть расписание,
                message.chat.id,  # то это уже сделано
                'Чем ещё я могу помочь?',
                reply_markup=today_tomorrow_keyboard()
            )
            await state.finish()  # в этом случае выключаем машину состояний
        else:  # если польователю нужно было изменить расписание, то спрашиваем, какую пару он хочет поменять
            await Custom.time.set()  # изменяем состояние на Custom.time
            async with state.proxy() as data:
                data['schedule'] = schedule  # сохраняем расписание и день
                data['day'] = message.text
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['09:00 – 10:25', '10:45 – 12:10']])
            keyboard.add(*[types.KeyboardButton(name) for name in ['12:20 – 13:45', '13:55 – 15:20']])
            keyboard.add(*[types.KeyboardButton(name) for name in ['15:30 – 16:55', '17:05 – 18:30']])
            keyboard.add(*[types.KeyboardButton(name) for name in ['18:35 – 20:00', 'Выход']])
            await bot.send_message(
                message.chat.id,
                'Выбери, пожалуйста, время, расписание '
                'на которое ты хочешь поменять)',
                reply_markup=keyboard
            )
    else:  # если произошла какая-то ошибка
        await bot.send_message(
            message.chat.id,
            'Что-то пошло не так, попробуй еще раз позже, пожалуйста)',
            reply_markup=today_tomorrow_keyboard()
        )
        await state.finish()  # останавливаем машину состояний


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT
                    or message.text not in ['09:00 – 10:25', '10:45 – 12:10', '12:20 – 13:45', '13:55 – 15:20',
                                            '15:30 – 16:55', '17:05 – 18:30', '18:35 – 20:00', 'Выход'],
                    state=Custom.time,
                    content_types=types.message.ContentType.ANY)
async def custom_proceed_time_invalid(message: types.Message):
    """
    Функция просит пользователя выбрать вариант из списка ['09:00 – 10:25', '10:45 – 12:10', '12:20 – 13:45',
                                                           '13:55 – 15:20', '15:30 – 16:55', '17:05 – 18:30',
                                                           '18:35 – 20:00', 'Выход'],
    если сообщение не содержит никакую из этих строк.
    """
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


@dp.message_handler(Text(equals=['09:00 – 10:25', '10:45 – 12:10', '12:20 – 13:45', '13:55 – 15:20',
                                 '15:30 – 16:55', '17:05 – 18:30', '18:35 – 20:00']), state=Custom.time)
async def custom_proceed_time(message: types.Message, state: FSMContext):
    """
    Функция ловит сообщение со временем пары, расписание на которую нужно изменить,
    спрашивает у пользователя, на что нужно заменить текущее значение.
    """
    await Custom.edit.set()  # изменяем состояние на Custom.edit
    async with state.proxy() as data:
        data['time'] = message.text  # сохраняем время пары
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])  # кнопка для выхода из функции
    await bot.send_message(
        message.chat.id,  # просим пользователя ввести номер группы
        'Введи, пожалуйста, на что ты хочешь заменить '
        'это значение) (Можешь присылать мне и смайлики)',
        reply_markup=keyboard
    )


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT,
                    state=Custom.edit,
                    content_types=types.message.ContentType.ANY)
async def custom_proceed_edit_invalid_type(message: types.Message):
    """
    Функция просит ввести номер группы заново, если формат ввода неправильный.
    """
    await message.reply("Пришли значение в верном формате, пожалуйста)")


@dp.message_handler(state=Custom.edit)
async def custom_proceed_edit(message: types.Message, state: FSMContext):
    """
    Функция принимает строку, на которую нужно поменять текущее значение пары,
    и сохраняет новое расписание в базе данных.
    Спрашивает пользователя, хочет ли он изменить что-то еще в расписании на этот день.
    """
    async with state.proxy() as data:
        schedule = data['schedule']  # достаем расписание и день
        day = data['day']
        schedule[day].loc[data['time']] = message.text  # заменяем нужную пару
        data.clear()
    # сохраняем новое расписание
    if psg.update_custom_timetable(message.chat.id, pickle.dumps(schedule, protocol=pickle.HIGHEST_PROTOCOL)):
        await Custom.again.set()  # изменяем состояние на Custom.again
        async with state.proxy() as data:
            data['schedule'] = schedule  # перезаписываем расписание и день (особенности state.proxy())
            data['day'] = day
        await bot.send_message(
            message.chat.id,
            'Отлично, все получилось 🙃\n'
            'Хочешь изменить еще какое-то значение '
            'в расписании на этот день?'
        )
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Хочу', 'Не хочу', 'Выход']])
        await bot.send_message(  # посылаем запрос, хочет ли пользователь изменить
            message.chat.id,  # в расписании на этот день что-то еще
            schedule_string(schedule[day].to_frame()),
            parse_mode='HTML',
            reply_markup=keyboard
        )
    else:  # если произошла какая-то ошибка
        await bot.send_message(
            message.chat.id,
            'Что-то пошло не так, попробуй еще раз позже, пожалуйста)',
            reply_markup=today_tomorrow_keyboard()
        )
        await state.finish()


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT
                    or message.text not in ['Хочу', 'Не хочу', 'Выход'],
                    content_types=types.message.ContentType.ANY, state=Custom.again)
async def custom_proceed_again_invalid(message: types.Message):
    """
    Функция просит выбрать из вариант из предложенных, если формат ввода неправильный.
    """
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


@dp.message_handler(Text(equals=['Хочу', 'Не хочу']), state=Custom.again)
async def custom_proceed_again(message: types.Message, state: FSMContext):
    """
    Функция ловит ответ от пользователя, хочет ли он продолжить редактирование.
    Если хочет, то функция задает вопрос про время пары.
    """
    if message.text == 'Не хочу':  #  отрицательный ответ
        await bot.send_message(
            message.chat.id,
            'Хорошо, но не забывай, что ты всегда можешь вернуться, '
            'если захочешь что-то изменить в нем 😉',
            reply_markup=today_tomorrow_keyboard()
        )
        await state.finish()  # останавливаем машину состояний
    else:  # положительный ответ
        await Custom.time.set()  # изменяем состояние на Custom.time
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['09:00 – 10:25', '10:45 – 12:10']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['12:20 – 13:45', '13:55 – 15:20']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['15:30 – 16:55', '17:05 – 18:30']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['18:35 – 20:00', 'Выход']])
        await bot.send_message(
            message.chat.id,
            'Выбери, пожалуйста, время, расписание '
            'на которое ты хочешь поменять)',
            reply_markup=keyboard
        )


@dp.message_handler(commands='plot')
async def plot(message: types.Message):
    """
    Функция ловит сообщение с текстом '/plot'.
    """
    await bot.send_message(message.chat.id, 'Снова лабки делаешь?) Ох уж эти графики!...'
                                            ' Сейчас быстренько всё построю, только тебе придётся'
                                            ' ответить на пару вопросов'
                                            '😉. И не засиживайся, ложись спать)')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Без названия', 'Выход']])
    await bot.send_message(message.chat.id, 'Как мы назовём график?'
                                            ' Если не хочешь давать ему название,'
                                            ' то нажми кнопку ниже 😉', reply_markup=keyboard)
    await Plots.title_state.set()


@dp.message_handler(lambda message: message.content_type == types.message.ContentType.TEXT, state=Plots.title_state)
async def title(message: types.Message):
    if message.text == 'Без названия':
        Plots.title = ''
    else:
        Plots.title = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['✅', '❌', 'Выход']])
    await bot.send_message(message.chat.id, 'Прямую по МНК строим?', reply_markup=keyboard)
    await Plots.mnk_state.set()


# In case some bad input
@dp.message_handler(state=Plots.title_state, content_types=types.message.ContentType.ANY)
async def title_bad_input(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Без названия']])
    await bot.send_message(message.chat.id, 'Я тебя не понял... Напиши ещё раз название графика.'
                                            ' Если не хочешь давать ему название,'
                                            ' то нажми кнопку ниже 😉', reply_markup=keyboard)


@dp.message_handler(Text(equals=['✅', '❌']), state=Plots.mnk_state)
async def mnk(message: types.Message):
    if message.text == '✅':
        Plots.mnk = True
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['0.0/0.0']])
        await bot.send_message(message.chat.id, 'Пришли данные для крестов погрешностей по осям х и y в'
                                                ' формате "123.213/123.231", если кресты не нужны, то'
                                                ' нажми на кнопку ниже', reply_markup=keyboard)
        await Plots.error_bars_state.set()
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])
        with open('files/Example.xlsx', 'rb') as example:
            await bot.send_document(message.chat.id, example)
        await bot.send_message(message.chat.id,
                               'Пришли .xlsx файл с данными как в example.xlsx, и всё будет готово',
                               reply_markup=keyboard)
        await Plots.plot_state.set()


# In case of bad input
@dp.message_handler(state=Plots.mnk_state, content_types=types.message.ContentType.ANY)
async def mnk_bad_input(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['✅', '❌', 'Выход']])
    await bot.send_message(message.chat.id, 'Извини, повтори ещё раз... Прямую по МНК строим?',
                           reply_markup=keyboard)


@dp.message_handler(lambda message: message.content_type == types.message.ContentType.TEXT,
                    state=Plots.error_bars_state)
async def error_bars(message: types.Message):
    try:
        Plots.errors = list(map(float, message.text.split('/')))
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])
        with open('files/Example.xlsx', 'rb') as expl:
            await bot.send_document(message.chat.id, expl)
        await bot.send_message(message.chat.id,
                               'Пришли .xlsx файл с данными как в example.xlsx и всё будет готово',
                               reply_markup=keyboard)
        await Plots.plot_state.set()
    except Exception as e:
        print(e)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['0.0/0.0']])
        await bot.send_message(message.chat.id,
                               'Не могу распознать формат данных( Давай ещё раз. '
                               'Пришли данные для крестов погрешностей по осям х и y в '
                               'формате "123.213/123.231", если кресты не нужны, то'
                               ' нажми на кнопку ниже', reply_markup=keyboard)


# In case of bad input
@dp.message_handler(state=Plots.error_bars_state, content_types=types.message.ContentType.ANY)
async def eror_bars_bad_input(message: types.Message):
    Plots.mnk = True
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['0.0/0.0']])
    await bot.send_message(message.chat.id, 'Ты прислал что-то не то( Давай ещё раз. '
                                            'Пришли данные для крестов погрешностей по осям х и y в '
                                            'формате "123.213/123.231", если кресты не нужны, то'
                                            ' нажми на кнопку ниже', reply_markup=keyboard)


@dp.message_handler(content_types=types.message.ContentTypes.DOCUMENT, state=Plots.plot_state)
async def plot(message: types.Message, state: FSMContext):
    try:
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        await bot.download_file(file.file_path, 'file.xlsx')
        a, b, d_a, d_b = math_part.mnk_calc('file.xlsx')
        math_part.plots_drawer('file.xlsx', Plots.title, Plots.errors[0], Plots.errors[1], Plots.mnk)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
        await bot.send_message(message.chat.id, 'Принимай работу!)', reply_markup=keyboard)
        with open('plot.png', 'rb') as photo:
            await bot.send_document(message.chat.id, photo)
        if Plots.mnk:
            for i in range(0, len(a)):
                await bot.send_message(message.chat.id, f"Коэффициенты {i + 1}-ой прямой:\n"
                                                        f" a = {a[i]} +- {d_a[i]}\n"
                                                        f" b = {b[i]} +- {d_b[i]}")
        with open('plot.pdf', 'rb') as photo:
            await bot.send_document(message.chat.id, photo)
        os.remove('plot.pdf')
        os.remove('plot.png')
        math_part.BOT_PLOT = False
        os.remove('file.xlsx')
        Plots.title = ''
        Plots.errors = [0, 0]
        Plots.mnk = False
        await state.finish()
    except Exception as e:
        os.remove('file.xlsx')
        print(e.with_traceback())
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])
        await bot.send_message(message.chat.id,
                               'Ты точно прислал .xlsx файл как в примере? Давай ещё раз!', reply_markup=keyboard)


# In case of bad input
@dp.message_handler(content_types=types.message.ContentType.ANY, state=Plots.plot_state)
async def plot_bad_input(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])
    await bot.send_message(message.chat.id,
                           'Ты точно прислал .xlsx файл? Давай ещё раз! '
                           'Пришли .xlsx файл с данными, и всё будет готово', reply_markup=keyboard)


executor.start_polling(dp, skip_updates=True)
