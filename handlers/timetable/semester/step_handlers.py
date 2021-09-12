from create_env import bot
from database_queries import insert_action, send_timetable
from ...helpers import schedule_string, today_tomorrow_keyboard
from ...states import Timetable

from aiogram import types
from aiogram.dispatcher import FSMContext


async def initiate(message: types.Message):
    """
    Функция ловит сообщение с текстом "/timetable".
    Отправляет пользователю вопрос, расписание своей или другой группы ему нужно.
    """
    await insert_action("timetable", message.chat.id)
    await Timetable.choose.set()  # ставим состояние Timetable.choose
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await bot.send_message(
        message.chat.id,
        "Снова не можешь вспомнить, какая пара следующая?\nНичего, я уже тут! 😉",
    )
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ["Личное", "Моя группа"]])
    keyboard.add(*[types.KeyboardButton(name) for name in ["Другая группа", "Выход"]])
    await bot.send_message(
        message.chat.id,
        "Выбери, пожалуйста, какое расписание тебе нужно)",
        reply_markup=keyboard,
    )


async def choose_another_type_proceed(message: types.Message):
    """
    Функция ловит сообщение с текстом 'Другая группа' и отправляет пользователю вопрос о номере группы.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await Timetable.another_group.set()  # изменяем состояние на Timetable.another_group
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        *[types.KeyboardButton(name) for name in ["Выход"]]
    )  # кнопка для выхода из функции
    await bot.send_message(
        message.chat.id,  # просим пользователя ввести номер группы
        "Не подскажешь номер группы?\n(В формате Б00–228 или 777, как в расписании)",
        reply_markup=keyboard,
    )


async def choose_my_group_custom_type_proceed(
    message: types.Message, state: FSMContext
):
    """
    Функция принимает сообщение от пользователя с запросом нужного ему варианта расписания.
    Отправляет пользователю вопрос о нужном дне недели. В случае ошибки отправляет пользователю
    сообщение о необходимости редактирования номера группы или личного расписания.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    timetable = (
        await send_timetable(custom=True, chat_id=message.chat.id)
        if message.text == "Личное"
        else await send_timetable(my_group=True, chat_id=message.chat.id)
    )
    if timetable[0]:  # если расписание было найдено
        if timetable[1][0] is not None and timetable[1][0] != "DEFAULT":
            await Timetable.weekday.set()  # изменяем состояние на Timetable.weekday
            async with state.proxy() as data:
                data["schedule"] = timetable[1][0]  # записываем расписание
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # дни недели для тыков и кнопка для выхода (строки выбраны по размеру слов)
            keyboard.add(*[types.KeyboardButton(name) for name in ["На неделю"]])
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["Понедельник", "Вторник"]]
            )
            keyboard.add(*[types.KeyboardButton(name) for name in ["Среда", "Четверг"]])
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["Пятница", "Суббота"]]
            )
            keyboard.add(
                *[types.KeyboardButton(name) for name in ["Воскресенье", "Выход"]]
            )
            await bot.send_message(
                message.chat.id,
                "Расписание на какой день недели ты хочешь узнать?",
                reply_markup=keyboard,
            )
        elif timetable[1][0] is not None and timetable[1][0] == "DEFAULT":
            await bot.send_message(  # отправляем расписание
                message.chat.id,
                "В этом семестре нет официального расписания для твоей группы( "
                "Пожалуйста, измени номер своей группы в /profile 😉",
                reply_markup=today_tomorrow_keyboard(),
            )
            await state.finish()
        else:
            if message.text == "Личное":
                await bot.send_message(
                    message.chat.id,
                    "Не могу найти твое личное расписание 😞\n"
                    "Нажми /custom чтобы проверить корректность данных.",
                    reply_markup=today_tomorrow_keyboard(),
                )
            else:
                await bot.send_message(
                    message.chat.id,
                    "Не могу найти расписание твоей группы 😞\n"
                    "Нажми /profile чтобы проверить корректность данных.",
                    reply_markup=today_tomorrow_keyboard(),
                )
            await state.finish()
    # если в базе данных нет этого пользователя
    elif not timetable[0] and timetable[1] == "empty_result":
        await bot.send_message(
            message.chat.id,
            "Кажется, мы с тобой еще не знакомы... 😢\nCкорей пиши мне /start!",
            reply_markup=today_tomorrow_keyboard(),
        )
        await state.finish()  # в случае ошибки выключаем машину состояний
    # произошла ошибка
    else:
        await bot.send_message(
            message.chat.id,
            "Что-то пошло не так, попробуй еще раз позже, пожалуйста)",
            reply_markup=today_tomorrow_keyboard(),
        )
        await state.finish()


async def another_type_group_number_proceed(message: types.Message, state: FSMContext):
    """
    Функция принимает сообщение с номером группы и проверяет его. Если все хорошо, то отправляет
    пользователю запрос о дне недели. Если произошла какая-то ошибка, то функция просит пользователя
    ввести номер группы еще раз.
    """
    timetable = await send_timetable(another_group=message.text)
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    if timetable[0]:
        await Timetable.weekday.set()  # изменяем состояние на Timetable.weekday
        async with state.proxy() as data:
            data["schedule"] = timetable[1][0]  # записываем расписание
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # дни недели для тыков и кнопка для выхода (строки выбраны по размеру слов)
        keyboard.add(*[types.KeyboardButton(name) for name in ["На неделю"]])
        keyboard.add(
            *[types.KeyboardButton(name) for name in ["Понедельник", "Вторник"]]
        )
        keyboard.add(*[types.KeyboardButton(name) for name in ["Среда", "Четверг"]])
        keyboard.add(*[types.KeyboardButton(name) for name in ["Пятница", "Суббота"]])
        keyboard.add(*[types.KeyboardButton(name) for name in ["Воскресенье", "Выход"]])
        await bot.send_message(
            message.chat.id,
            "Расписание на какой день недели ты хочешь узнать?",
            reply_markup=keyboard,
        )
    # номера группы нет в базе / произошла какая-то ошибка, связанная с соединением
    elif not timetable[0] and timetable[1] == "connection_error":
        await bot.send_message(
            message.chat.id,
            "Что-то не так с соединением, попробуй еще раз позже, пожалуйста)",
            reply_markup=today_tomorrow_keyboard(),
        )
        await state.finish()
    # произошла какая-то ошибка другого рода
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
        await bot.send_message(  # просим пользователя ввести номер группы еще раз
            message.chat.id,
            "К сожалению я не знаю такой группы(\nВведи номер ещё раз, пожалуйста)",
            reply_markup=keyboard,
        )


async def weekday_proceed_and_schedule_send(message: types.Message, state: FSMContext):
    """
    Функция отправляет расписание на выбранный день недели.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    async with state.proxy() as data:
        schedule = data["schedule"]  # берем расписание из памяти
        data.clear()
    if message.text != "На неделю":  # расписание на 1 день
        await bot.send_message(  # отправляем расписание
            message.chat.id,
            schedule_string(schedule[message.text]),
            parse_mode="HTML",
        )
    else:  # расписание на неделю (на каждый из 7 дней)
        for day in [
            "Понедельник",
            "Вторник",
            "Среда",
            "Четверг",
            "Пятница",
            "Суббота",
            "Воскресенье",
        ]:
            await bot.send_message(  # отправляем расписание
                message.chat.id,
                "<b>" + day.upper() + "</b>" + "\n\n" + schedule_string(schedule[day]),
                parse_mode="HTML",
            )
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await bot.send_message(
        message.chat.id,
        "Чем ещё я могу помочь?",
        reply_markup=today_tomorrow_keyboard(),
    )
    await state.finish()  # выключаем машину состояний
