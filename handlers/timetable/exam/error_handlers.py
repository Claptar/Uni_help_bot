from create_env import bot

from aiogram import types


async def choose_invalid(message: types.Message):
    """
    Функция просит пользователя выбрать вариант из списка ['Личное', 'Моя группа', 'Другая группа', 'Выход'],
    если сообщение не содержит никакую из этих строк (+ проверка типа сообщения).
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


async def another_group_invalid_type(message: types.Message):
    """
    Функция просит ввести номер группы заново, если формат ввода неправильный.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await message.reply("Пришли номер группы в верном формате, пожалуйста)")
