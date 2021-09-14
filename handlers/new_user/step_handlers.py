from create_env import bot
from database_queries import (
    insert_action,
    check_user_group,
    insert_user,
    create_custom_timetable,
)
from ..helpers import today_tomorrow_keyboard
from ..states import Start

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


async def initiate(message: types.Message):
    """
    Функция ловит сообщение с командой '/start' и приветствует пользователя.
    """
    group = await check_user_group(message.chat.id)
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    if group[0]:  # если пользователь уже есть в базе данных
        await bot.send_message(
            message.chat.id,
            "Привет-привет! 🙃\nМы уже с тобой знакомы 😉 "
            "Напиши /help, чтобы я напомнил тебе, что я умею)",
            reply_markup=today_tomorrow_keyboard(),
        )
    elif not group[0] and group[1] == "empty_result":  # пользователя нет в базе данных
        await Start.group.set()  # изменяем состояние на Start.group
        await bot.send_message(
            message.chat.id,
            "Привет-привет! 🙃\nДавай знакомиться! Меня зовут Помогатор. "
            "Можешь рассказать мне немного о себе, "
            "чтобы я знал, чем могу тебе помочь?",
        )
        await insert_action(
            "start", message.chat.id
        )  # Запись события о новом пользователе
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[types.KeyboardButton(name) for name in ["Уже не учусь", "Выход"]]
        )
        await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
        await bot.send_message(  # 'Уже не учусь' - вариант для выпускников
            message.chat.id,
            " Не подскажешь номер своей группы?\n"
            "(В формате Б00-228 или 777, как в расписании)",
            reply_markup=keyboard,
        )
    # произошла какая-то ошибка (с соединением или другая)
    else:
        await bot.send_message(
            message.chat.id, "Что-то пошло не так, попробуй еще раз позже, пожалуйста)"
        )


async def group_proceed(message: types.Message, state: FSMContext):
    """
    Функция принимает значение номера группы и проверяет, есть ли такая группа в базе.
    Если группы нет в базе данных (или произошла какая-то ошибка), то функция просит ввести номер группы заново.
    Если группа есть в базе данных, информация о пользователе заносится в таблицу User, а пользователю
    отправляется запрос, нужно ли ему личное расписание.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    (group, text) = (
        ("ALUMNI", "Привет достопочтенному выпускнику! 👋")
        if message.text == "Уже не учусь"
        else (  # разные варианты для выпускника и студента
            message.text,
            "Отлично, вот мы и познакомились 🙃",
        )
    )
    insert = await insert_user(message.chat.id, group)
    if insert[0]:  # группа есть в базе, добавление пользователя прошло успешн
        await Start.custom.set()  # меняем состояние на Start.custom
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["Хочу", "Не хочу"]])
        await bot.send_message(  # запрос о личном расписании
            message.chat.id,
            text + "\nЕсли хочешь получить возможность использовать "
            "личное расписание, нажми на нужную кнопку внизу.",
            reply_markup=keyboard,
        )
    # группы нет в базе / что-то другое, не связанное с подключением, просим повторить ввод
    elif not insert[0] and insert[1] == "other_error":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[types.KeyboardButton(name) for name in ["Уже не учусь", "Выход"]]
        )
        await bot.send_message(
            message.chat.id,
            "Что-то пошло не так, введи номер своей группы ещё раз, пожалуйста)",
            reply_markup=keyboard,
        )
    # произошла какая-то ошибка с соединением
    else:
        await bot.send_message(
            message.chat.id,
            "Что-то не так с соединением, попробуй ещё раз позже, пожалуйста)",
        )
        await state.finish()


async def custom_proceed(message: types.Message, state: FSMContext):
    """
    Функция принимает ответ пользователя, нужно ли ему личное расписание, заносит заготовку
    в базу данных, если ответ положительный.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    if message.text == "Не хочу":  # ответ пользователя отрицательный
        await bot.send_message(
            message.chat.id,
            "Хорошо, но не забывай, что ты всегда можешь вернуться, "
            "если захочешь опробовать его в деле 😉\n"
            "Чтобы вызвать личное расписание, напиши /custom.",
        )
        await bot.send_message(  # в любом случае пишем про /help
            message.chat.id,
            "А теперь скорее пиши /help, чтобы узнать, чем еще я могу помочь тебе!",
            reply_markup=today_tomorrow_keyboard(),
        )
    elif message.text == "Хочу":  # ответ пользователя положительный
        # async with state.proxy() as data:
        #     group = data['group']
        # если номер группы верный (по идее должно быть выполнено)
        # и добавление заготовки расписания прошло успешно
        update = await create_custom_timetable(message.chat.id)
        if update[0]:
            await bot.send_message(
                message.chat.id,
                "Отлично, все получилось 🙃\n"
                "Теперь ты можешь использовать личное расписание! "
                "Чтобы вызвать его, напиши /custom.",
            )
            await bot.send_message(
                message.chat.id,
                "А теперь скорее пиши /help, чтобы узнать, "
                "чем еще я могу помочь тебе!",
                reply_markup=today_tomorrow_keyboard(),
            )
        else:
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так, попробуй еще раз позже, пожалуйста)\n"
                "Чтобы настроить личное расписание, напиши /custom.",
            )
            await bot.send_message(
                message.chat.id,
                "Не расстраивайся! Напиши /help, чтобы узнать, "
                "чем еще я могу помочь тебе!",
                reply_markup=today_tomorrow_keyboard(),
            )
    await state.finish()  # в любом случае останавливаем машину состояний
