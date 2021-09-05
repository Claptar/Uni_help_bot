from create_env import bot

from aiogram import types


async def new_invalid(message: types.Message):
    """
    Функция просит пользователя выбрать вариант из списка ['Давай', 'Как-нибудь потом', 'Выход'],
    если сообщение не содержит никакую из этих строк.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


async def existing_invalid(message: types.Message):
    """
    Функция просит пользователя выбрать вариант из списка ['Посмотреть', 'Изменить', 'Выход'],
    если сообщение не содержит никакую из этих строк.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


async def weekday_invalid(message: types.Message):
    """
    Функция просит пользователя выбрать вариант из списка ['Понедельник', 'Вторник', 'Среда', 'Четверг',
                                                           'Пятница', 'Суббота', 'Воскресенье', 'Выход'],
    если сообщение не содержит никакую из этих строк.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


async def time_invalid(message: types.Message):
    """
    Функция просит пользователя выбрать вариант из списка ['09:00 – 10:25', '10:45 – 12:10', '12:20 – 13:45',
                                                           '13:55 – 15:20', '15:30 – 16:55', '17:05 – 18:30',
                                                           '18:35 – 20:00', 'Выход'],
    если сообщение не содержит никакую из этих строк.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


async def edit_invalid_type(message: types.Message):
    """
    Функция просит ввести номер группы заново, если формат ввода неправильный.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await message.reply("Пришли значение в верном формате, пожалуйста)")


async def again_invalid(message: types.Message):
    """
    Функция просит выбрать из вариант из предложенных, если формат ввода неправильный.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await message.reply("Выбери вариант из предложенных, пожалуйста)")
