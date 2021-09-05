from create_env import bot
from ..states import Koryavov

from aiogram import types


async def semester_number_invalid(message: types.Message):
    """
    В случае некоректного ответа на запрос номера семестра отправляется сообщение с просьбой
    указать правильный номер семестра
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        *[types.KeyboardButton(name) for name in [1, 2, 3, 4, 5, "Выход"]]
    )  # кнопки c номерами семестров
    await bot.send_message(
        message.chat.id, "Что-то не так, давай ещё раз. Выбери номер семестра:"
    )


async def task_number_invalid(message: types.Message):
    """
    В случае некорректоного ввода номера задачи, функция отправляет сообщение с просьбой повторить ввод
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
    await bot.send_message(
        message.chat.id,
        "Что-то не так, введи номер задачи ещё раз)",
        reply_markup=keyboard,
    )


async def finish_invalid(message: types.Message):
    """
    В случае некорректного сообщения, функция отправляет сообщение с просьбой попробовать ещё раз.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        *[types.KeyboardButton(name) for name in ["Ещё одну", "Всё, хватит", "Выход"]]
    )
    await bot.send_message(
        message.chat.id,
        "Что-то пошло не так. Ты хочешь узнать номер страницы для ещё одной задачи ?",
        reply_markup=keyboard,
    )
