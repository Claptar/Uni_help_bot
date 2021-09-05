from create_env import bot

from aiogram import types


async def group_invalid_format(message: types.Message):
    """
    Функция просит ввести номер группы заново, если формат ввода номера группы неправильный.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await message.reply("Пришли номер группы в верном формате, пожалуйста)")


async def custom_invalid_variant(message: types.Message):
    """
    Функция просит выбрать вариант из предложенных, если формат ввода неправильный.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await message.reply("Выбери вариант из предложенных, пожалуйста)")
