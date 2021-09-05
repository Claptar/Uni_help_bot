from create_env import bot
from data_constructor import psg
from ..helpers import today_tomorrow_keyboard
from ..states import Profile


from aiogram import types
from aiogram.dispatcher.storage import FSMContext


async def initiate(message: types.Message):
    """
    Функция ловит сообщение с командой '/profile' и спрашивает у пользователя,
    хочет ли он изменить группу, закрепленную за ним.
    """
    await psg.insert_action("profile", message.chat.id)
    cur_group = await psg.check_user_group(message.chat.id)
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    if cur_group[0]:
        await Profile.choose.set()  # изменяем состояние на Profile.choose
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["Да", "Нет", "Выход"]])
        if cur_group[1][0] == "ALUMNI":
            await bot.send_message(
                message.chat.id,
                f"Сейчас у тебя указано, что ты – выпускник. "
                "Ты хочешь изменить это значение на номер группы?",
                reply_markup=keyboard,
            )
        else:
            await bot.send_message(
                message.chat.id,
                f"Сейчас у тебя указано, что ты учишься в группе {cur_group[1][0]}. "
                "Ты хочешь изменить это значение?",
                reply_markup=keyboard,
            )
    # если в базе данных нет этого пользователя
    elif not cur_group[0] and cur_group[1] == "empty_result":
        await bot.send_message(
            message.chat.id,
            "Кажется, мы с тобой еще не знакомы... 😢\nСкорей пиши мне /start!",
            reply_markup=today_tomorrow_keyboard(),
        )
    # если произошла ошибка
    else:
        await bot.send_message(
            message.chat.id,
            "Что-то пошло не так, попробуй еще раз позже, пожалуйста)",
            reply_markup=today_tomorrow_keyboard(),
        )


async def choose_proceed(message: types.Message, state: FSMContext):
    """
    Функция принимает ответ пользователя, хочет ли он поменять значение группы
    и просит пользователя ввести желаемый номер группы.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    if message.text == "Да":  # положительный ответ, запрос о вводе номера группы
        await Profile.group.set()  # изменяем состояние на Profile.group
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[types.KeyboardButton(name) for name in ["Уже не учусь", "Выход"]]
        )
        await bot.send_message(
            message.chat.id, "Введи номер группы, пожалуйста)", reply_markup=keyboard
        )
    elif message.text == "Нет":  # отрицательный ответ
        await bot.send_message(
            message.chat.id,
            "Я рад, что тебя все устраивает 😉",
            reply_markup=today_tomorrow_keyboard(),
        )
        await state.finish()  # выключаем машину состояний


async def group_proceed(message: types.Message, state: FSMContext):
    """
    Функция ловит ответ пользователя с номером группы, если обновление удалось сделать,
    посылает пользователю запрос, хочет ли он изменить свое личное расписание.
    :param message:
    :param state:
    :return:
    """
    # получилось обновить номер группы, запрос о изменении личного расписания
    group = "ALUMNI" if message.text == "Уже не учусь" else message.text
    update = await psg.update_user(message.chat.id, group)
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    if update[0]:
        await Profile.custom.set()  # изменяем состояние на Profile.custom
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["Хочу", "Не хочу"]])
        await bot.send_message(
            message.chat.id,
            "Все готово) Ты хочешь поменять личное "
            "расписание на расписание новой группы?",
            reply_markup=keyboard,
        )
    # номера группы нет в базе (или произошла какая-то другая ошибка, не связанная с соединением)
    elif not update[0] and update[1] == "other_error":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[types.KeyboardButton(name) for name in ["Уже не учусь", "Выход"]]
        )
        await bot.send_message(  # просим пользователя ввести номер группы еще раз
            message.chat.id,
            "Что-то пошло не так, введи номер своей группы ещё раз, пожалуйста)",
            reply_markup=keyboard,
        )
    else:
        await bot.send_message(  # просим пользователя ввести номер группы еще раз
            message.chat.id,
            "Что-то не так с соединением, попробуй ещё раз позже, пожалуйста)",
            reply_markup=today_tomorrow_keyboard(),
        )
        await state.finish()


# TODO: to edit_existing
async def custom_proceed(message: types.Message, state: FSMContext):
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    if message.text == "Не хочу":  # если пришел отрицательный ответ
        await bot.send_message(
            message.chat.id,
            "Я рад, что тебя все устраивает 😉",
            reply_markup=today_tomorrow_keyboard(),
        )
    elif (
        message.text == "Хочу"
    ):  # если пришел положительный ответ, то изменяем личное расписание
        update = await psg.create_custom_timetable(message.chat.id)
        if update[0]:
            await bot.send_message(
                message.chat.id,
                "Отлично, все получилось 🙃\n"
                "Чтобы вызвать личное расписание, напиши /custom.",
                reply_markup=today_tomorrow_keyboard(),
            )
        else:  # если произошла ошибка при обновлении расписания
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так, попробуй еще раз позже, пожалуйста)\n"
                "Чтобы настроить личное расписание, напиши /custom.",
                reply_markup=today_tomorrow_keyboard(),
            )
    await state.finish()
