from create_env import bot
from database_queries import (
    insert_action,
    send_timetable,
    create_custom_timetable,
    update_custom_timetable,
)
from ...helpers import schedule_string, today_tomorrow_keyboard
from ...states import Custom

from aiogram import types
from aiogram.dispatcher import FSMContext


async def initiate(message: types.Message):
    """
    Функция ловит сообщение с текстом '/custom'.
    Если пользователь есть в базе, то функция проверяет наличие личного расписания.
    В случае отсутствия такового в базе данных отправляет пользователю вопрос, хочет ли он
    завести такое расписание. Если личное расписание для этого пользователя есть в базе,
    фукция посылает запрос о выборе дня недели, расписание на который нужно выдать или как-то поменять.
    """
    await insert_action("custom", message.chat.id)
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await bot.send_message(
        message.chat.id,
        "Хочешь посмотреть личное расписание "
        "или что-то отредактировать в нем? "
        "В этом я всегда рад тебе помочь 😉",
    )
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    timetable = await send_timetable(custom=True, chat_id=message.chat.id)
    if timetable[0] and timetable[1][0] is not None:  # если пользователь есть в базе
        await Custom.existing.set()  # изменяем состояние на Custom.existing
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[
                types.KeyboardButton(name)
                for name in ["Посмотреть", "Изменить", "Выход"]
            ]
        )
        await bot.send_message(  # вопрос, что пользователь хочет сделать с расписанием
            message.chat.id,
            "Выбери, пожалуйста, что ты хочешь сделать с личным расписанием)",
            reply_markup=keyboard,
        )
    elif (
        timetable[0] and timetable[1][0] is None
    ):  # если у пользователя еще нет личного расписания
        await Custom.new.set()  # изменяем состояние на Custom.new
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[
                types.KeyboardButton(name)
                for name in ["Давай", "Как-нибудь потом", "Выход"]
            ]
        )
        await bot.send_message(
            message.chat.id,
            "У тебя пока еще нет личного расписания 😢\nДавай заведем его тебе?",
            reply_markup=keyboard,
        )
    elif not timetable[0] and timetable[1] == "empty_result":
        await bot.send_message(
            message.chat.id,
            "Кажется, мы с тобой еще не знакомы... 😢\nCкорей пиши мне /start!",
            reply_markup=today_tomorrow_keyboard(),
        )
    # произошла ошибка
    else:
        await bot.send_message(
            message.chat.id,
            "Что-то пошло не так, попробуй еще раз позже, пожалуйста)",
            reply_markup=today_tomorrow_keyboard(),
        )


async def new_proceed(message: types.Message, state: FSMContext):
    """
    Функция принимает ответ пользователя, нужно ли ему личное расписание,
    в случае положительного ответа заводит ему такое расписание.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    if message.text == "Давай":  # положительный ответ
        update = await create_custom_timetable(message.chat.id)
        if update[0]:
            await bot.send_message(  # все нормально обновилось
                message.chat.id,
                "Отлично, все получилось 🙃\n"
                "Теперь ты можешь использовать личное расписание! "
                "Чтобы вызвать его, напиши /custom.",
                reply_markup=today_tomorrow_keyboard(),
            )
        else:  # произошла какая-то ошибка
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так, попробуй еще раз позже, пожалуйста)",
                reply_markup=today_tomorrow_keyboard(),
            )
    else:  # отрицательный ответ
        await bot.send_message(
            message.chat.id,
            "Хорошо, но не забывай, что ты всегда можешь вернуться, "
            "если захочешь опробовать его в деле 😉",
            reply_markup=today_tomorrow_keyboard(),
        )
    await state.finish()  # тупиковая ветка, останавливаем машину состояний


async def existing_proceed(message: types.Message, state: FSMContext):
    """
    Функция ловит запрос пользователя о просмотре или изменении личного расписания,
    отправляет запрос о нужном дне недели.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await Custom.weekday.set()  # изменяем состояние на Custom.weekday
    async with state.proxy() as data:
        data["choice"] = message.text  # сохраняем ответ, понадобится дальше
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # дни недели для тыков и кнопка для выхода (строки выбраны по размеру слов)
    keyboard.add(*[types.KeyboardButton(name) for name in ["Понедельник", "Вторник"]])
    keyboard.add(*[types.KeyboardButton(name) for name in ["Среда", "Четверг"]])
    keyboard.add(*[types.KeyboardButton(name) for name in ["Пятница", "Суббота"]])
    keyboard.add(*[types.KeyboardButton(name) for name in ["Воскресенье", "Выход"]])
    text = (
        "расписание на который ты хочешь посмотреть)"
        if message.text == "Посмотреть"
        else "в расписание на который ты хочешь внести изменения)"
    )  # в зависимости от ответа выбираем строчку, которую будем отправлять
    await bot.send_message(
        message.chat.id,
        "Выбери, пожалуйста, день недели, " + text,
        reply_markup=keyboard,
    )


async def weekday_proceed(message: types.Message, state: FSMContext):
    """
    Функция ловит сообщение с днем недели и, в зависимости от того, что нужно пользователю,
    либо выдает ему расписание, либо посылает запрос о времени пары, расписание на которую нужно поменять.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    timetable = await send_timetable(custom=True, chat_id=message.chat.id)
    if timetable[
        0
    ]:  # не произошло никакой ошибки (личное расписание точно есть, проверено ранее)
        schedule = timetable[1][0]  # расписание на неделю
        await bot.send_message(  # присылаем текущее состояние расписания
            message.chat.id,
            schedule_string(schedule[message.text]),
            parse_mode="HTML",
        )  # parse_mode - чтобы читал измененный шрифт
        async with state.proxy() as data:
            choice = data["choice"]
            data.clear()
        if choice == "Посмотреть":  # смотрим на ответ, сохраненный ранее
            await bot.send_message(  # если пользователю нужно было посмотреть расписание,
                message.chat.id,  # то это уже сделано
                "Чем ещё я могу помочь?",
                reply_markup=today_tomorrow_keyboard(),
            )
            await state.finish()  # в этом случае выключаем машину состояний
        else:  # если польователю нужно было изменить расписание, то спрашиваем, какую пару он хочет поменять
            await Custom.time.set()  # изменяем состояние на Custom.time
            async with state.proxy() as data:
                data["schedule"] = schedule  # сохраняем расписание и день
                data["day"] = message.text
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(
                *[
                    types.KeyboardButton(name)
                    for name in ["09:00 – 10:25", "10:45 – 12:10"]
                ]
            )
            keyboard.add(
                *[
                    types.KeyboardButton(name)
                    for name in ["12:20 – 13:45", "13:55 – 15:20"]
                ]
            )
            keyboard.add(
                *[
                    types.KeyboardButton(name)
                    for name in ["15:30 – 16:55", "17:05 – 18:30"]
                ]
            )
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["18:35 – 20:00", "Выход"]]
            )
            await bot.send_message(
                message.chat.id,
                "Выбери, пожалуйста, время, расписание "
                "на которое ты хочешь поменять)",
                reply_markup=keyboard,
            )
    else:  # если произошла какая-то ошибка
        await bot.send_message(
            message.chat.id,
            "Что-то пошло не так, попробуй еще раз позже, пожалуйста)",
            reply_markup=today_tomorrow_keyboard(),
        )
        await state.finish()  # останавливаем машину состояний


async def time_proceed(message: types.Message, state: FSMContext):
    """
    Функция ловит сообщение со временем пары, расписание на которую нужно изменить,
    спрашивает у пользователя, на что нужно заменить текущее значение.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await Custom.edit.set()  # изменяем состояние на Custom.edit
    async with state.proxy() as data:
        data["time"] = message.text  # сохраняем время пары
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        *[types.KeyboardButton(name) for name in ["Выход"]]
    )  # кнопка для выхода из функции
    await bot.send_message(
        message.chat.id,  # просим пользователя ввести номер группы
        "Введи, пожалуйста, на что ты хочешь заменить "
        "это значение) (Можешь присылать мне и смайлики)",
        reply_markup=keyboard,
    )


async def edit_proceed(message: types.Message, state: FSMContext):
    """
    Функция принимает строку, на которую нужно поменять текущее значение пары,
    и сохраняет новое расписание в базе данных.
    Спрашивает пользователя, хочет ли он изменить что-то еще в расписании на этот день.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    async with state.proxy() as data:
        schedule = data["schedule"]  # достаем расписание и день
        day = data["day"]
        schedule[day][data["time"]] = message.text  # заменяем нужную пару
        data.clear()
    # сохраняем новое расписание
    update = await update_custom_timetable(message.chat.id, schedule)
    if update[0]:
        await Custom.again.set()  # изменяем состояние на Custom.again
        async with state.proxy() as data:
            data[
                "schedule"
            ] = schedule  # перезаписываем расписание и день (особенности state.proxy())
            data["day"] = day
        await bot.send_message(
            message.chat.id,
            "Отлично, все получилось 🙃\n"
            "Хочешь изменить еще какое-то значение "
            "в расписании на этот день?",
        )
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[types.KeyboardButton(name) for name in ["Хочу", "Не хочу", "Выход"]]
        )
        await bot.send_message(  # посылаем запрос, хочет ли пользователь изменить
            message.chat.id,  # в расписании на этот день что-то еще
            schedule_string(schedule[day]),
            parse_mode="HTML",
            reply_markup=keyboard,
        )
    else:  # если произошла какая-то ошибка
        await bot.send_message(
            message.chat.id,
            "Что-то пошло не так, попробуй еще раз позже, пожалуйста)",
            reply_markup=today_tomorrow_keyboard(),
        )
        await state.finish()


async def again_proceed(message: types.Message, state: FSMContext):
    """
    Функция ловит ответ от пользователя, хочет ли он продолжить редактирование.
    Если хочет, то функция задает вопрос про время пары.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    if message.text == "Не хочу":  # отрицательный ответ
        await bot.send_message(
            message.chat.id,
            "Хорошо, но не забывай, что ты всегда можешь вернуться, "
            "если захочешь что-то изменить в нем 😉",
            reply_markup=today_tomorrow_keyboard(),
        )
        await state.finish()  # останавливаем машину состояний
    else:  # положительный ответ
        await Custom.time.set()  # изменяем состояние на Custom.time
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[types.KeyboardButton(name) for name in ["09:00 – 10:25", "10:45 – 12:10"]]
        )
        keyboard.add(
            *[types.KeyboardButton(name) for name in ["12:20 – 13:45", "13:55 – 15:20"]]
        )
        keyboard.add(
            *[types.KeyboardButton(name) for name in ["15:30 – 16:55", "17:05 – 18:30"]]
        )
        keyboard.add(
            *[types.KeyboardButton(name) for name in ["18:35 – 20:00", "Выход"]]
        )
        await bot.send_message(
            message.chat.id,
            "Выбери, пожалуйста, время, расписание на которое ты хочешь поменять)",
            reply_markup=keyboard,
        )
