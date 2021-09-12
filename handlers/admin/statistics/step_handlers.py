from handlers_utils.activity import unique_users, frequency_of_use
from create_env import bot
from ...helpers import today_tomorrow_keyboard
from ...states import Stat

from aiogram import types
from aiogram.dispatcher import FSMContext


async def initiate(message: types.Message):
    """
    Функция присылает сообщение с просьбой выбрать нужную функцию
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ["Frequency", "Unique"]])
    await bot.send_message(
        message.chat.id, "Выбери нужную функцию", reply_markup=keyboard
    )
    await Stat.choice.set()


async def period_proceed(message: types.Message):
    """
    Функция присылает сообщение с вопросом о том за какой период вермени нужна статистика
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        *[
            types.KeyboardButton(name)
            for name in ["За сегодня", "За вчера", "За неделю"]
        ]
    )
    await bot.send_message(
        message.chat.id,
        "За какой день показать количество уникальных пользователей",
        reply_markup=keyboard,
    )
    await Stat.unique.set()


async def number_of_unique_users(message: types.Message, state: FSMContext):
    """
    Функция присылает сообщением с числом уникальных пользователей за нужный период времени
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    number = unique_users(message.text)
    keyboard = today_tomorrow_keyboard()
    await bot.send_message(
        message.chat.id,
        f"В этот день было {number} уникальных пользователей",
        reply_markup=keyboard,
    )
    await state.finish()


async def function_usage_frequencies(message: types.Message, state: FSMContext):
    """
    Функция присылает сообщением с частотами использования функций за последнюю неделю
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await bot.send_message(
        message.chat.id, "Частота использования функций за последнюю неделю:"
    )
    freq = frequency_of_use()
    text = "\n".join(freq)
    keyboard = today_tomorrow_keyboard()
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await bot.send_message(message.chat.id, text, reply_markup=keyboard)
    await state.finish()
