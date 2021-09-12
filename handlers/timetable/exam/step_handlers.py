from create_env import bot
from database_queries import insert_action, send_exam_timetable
from ...helpers import schedule_string, today_tomorrow_keyboard
from ...states import Exam

from aiogram import types
from aiogram.dispatcher import FSMContext


async def initiate(message: types.Message):
    """
    Функция ловит сообщение с текстом '/exam'.
    Заглушка на время семестра (нет расписания сессии).
    """
    await insert_action("exam", message.chat.id)
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await bot.send_message(message.chat.id, "Ещё не время... Но ты не забывай...")
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await bot.send_sticker(
        message.chat.id,
        "CAACAgIAAxkBAAMEXj8IxnJkYATlpAOTkJyLiXH2u0UAAvYfAAKiipYBsZcZ_su45LkYBA",
    )


# async def initiate(message: types.Message):
#     """
#     Функция ловит сообщение с текстом '/exam'.
#     Отправляет запрос о выборе группы.
#     """
#     await insert_action("exam", message.chat.id)
#     await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(
#         *[
#             types.KeyboardButton(name)
#             for name in ["Моя группа", "Другая группа", "Выход"]
#         ]
#     )
#     await bot.send_message(
#         message.chat.id,
#         "Это время настало... Выбери, расписание экзаменов"
#         " какой группы ты хочешь посмотреть)",
#         reply_markup=keyboard,
#     )
#     await Exam.choose.set()


async def choose_my_group_and_send_schedule(message: types.Message, state: FSMContext):
    timetable = await send_exam_timetable(my_group=True, chat_id=message.chat.id)
    if timetable[0]:  # если расписание было найдено
        if timetable[1][0] is not None:
            await bot.send_message(  # отправляем расписание
                message.chat.id,
                schedule_string(timetable[1][0]),
                parse_mode="HTML",
            )
            await bot.send_chat_action(
                message.chat.id, "typing"
            )  # Отображение "typing"
            await bot.send_message(
                message.chat.id,
                "Чем ещё я могу помочь?",
                reply_markup=today_tomorrow_keyboard(),
            )
            await state.finish()  # выключаем машину состояний
        else:  # если расписания этой группы не нашлось
            await bot.send_message(
                message.chat.id,
                "Извини, расписания сессии для твоей группы мы не нашли,"
                " попробуй еще раз позже, пожалуйста)",
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


async def choose_another_group_proceed(message: types.Message):
    """
    Функция ловит сообщение с текстом 'Другая группа' и отправляет пользователю вопрос о номере группы.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await Exam.another_group.set()  # изменяем состояние на Timetable.another_group
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        *[types.KeyboardButton(name) for name in ["Выход"]]
    )  # кнопка для выхода из функции
    await bot.send_message(
        message.chat.id,  # просим пользователя ввести номер группы
        "Не подскажешь номер группы?\n(В формате Б00–228 или 777, как в расписании)",
        reply_markup=keyboard,
    )


async def another_group_send_schedule(message: types.Message, state: FSMContext):
    """
    Функция принимает сообщение с номером группы и проверяет его. Если все хорошо, то отправляет
    пользователю расписание. Если произошла какая-то ошибка, то функция просит пользователя
    ввести номер группы еще раз.
    """
    timetable = await send_exam_timetable(another_group=message.text)
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    if timetable[0]:
        if timetable[1][0] is not None:
            await bot.send_message(  # отправляем расписание
                message.chat.id,
                schedule_string(timetable[1][0]),
                parse_mode="HTML",
            )
            await bot.send_chat_action(
                message.chat.id, "typing"
            )  # Отображение "typing"
            await bot.send_message(
                message.chat.id,
                "Чем ещё я могу помочь?",
                reply_markup=today_tomorrow_keyboard(),
            )
            await state.finish()  # выключаем машину состояний
        else:  # если расписания этой группы не нашлось
            await bot.send_message(
                message.chat.id,
                "Извини, расписания сессии для твоей группы мы не нашли,"
                " попробуй еще раз позже, пожалуйста)",
                reply_markup=today_tomorrow_keyboard(),
            )
            await state.finish()
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
