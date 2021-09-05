from create_env import bot

from aiogram import types


async def choose_type_invalid(message: types.Message):
    """
    Функция просит пользователя выбрать вариант из списка ['Личное', 'Моя группа', 'Другая группа', 'Выход'],
    если сообщение не содержит никакую из этих строк (+ проверка типа сообщения).
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


async def another_type_group_number_proceed_invalid(message: types.Message):
    """
    Функция просит ввести номер группы заново, если формат ввода неправильный.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await message.reply("Пришли номер группы в верном формате, пожалуйста)")


async def weekday_proceed_invalid(message: types.Message):
    """
    Функция просит пользователя выбрать вариант из списка ['На неделю', 'Понедельник', 'Вторник', 'Среда',
                                                           'Четверг', 'Пятница', 'Суббота', 'Воскресенье', 'Выход'],
    если сообщение не содержит никакую из этих строк.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await message.reply("Выбери вариант из предложенных, пожалуйста)")
