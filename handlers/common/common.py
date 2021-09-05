from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from data_constructor import psg
from create_env import bot
from ..helpers import today_tomorrow_keyboard


async def exit_user(message: types.Message, state: FSMContext):
    """
    Функция, выполняющая выход по желанию пользователя (на любой стадии).
    """
    await psg.insert_action("exit", message.chat.id)
    current_state = (
        await state.get_state()
    )  # проверка, что запущено хотя бы какое-то из состояний
    if current_state is None:
        return
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await bot.send_message(
        message.chat.id,
        "Без проблем! Но ты это, заходи, если что 😉",
        reply_markup=today_tomorrow_keyboard(),
    )
    # стикос "Ты заходи есчо"
    await bot.send_sticker(
        message.chat.id,
        "CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ",
    )
    # При выходе выключаем машину состояний
    await state.finish()


async def help_user(message: types.Message):
    """
    Функция ловит сообщение с командой '/help' и присылает описание комманд бота.
    """
    await psg.insert_action("help", message.chat.id)
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    with open("files/help.txt", encoding="utf-8", mode="r") as f:
        text = f.read()
    await bot.send_message(message.chat.id, text)
