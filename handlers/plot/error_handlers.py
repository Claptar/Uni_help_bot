from create_env import bot

from aiogram import types


async def title_invalid(message: types.Message):
    """
    В случае неккоректного названия графика, функция просит пользователя повторить ввод.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ["Без названия"]])
    await bot.send_message(
        message.chat.id,
        "Я тебя не понял... Напиши ещё раз название графика.\n"
        "Если не хочешь давать ему название, "
        "то нажми кнопку ниже 😉",
        reply_markup=keyboard,
    )


async def mnk_invalid(message: types.Message):
    """
    В случае если сообщение не содержит ['✅', '❌'], функция просит пользователя повторить ввод.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ["✅", "❌", "Выход"]])
    await bot.send_message(
        message.chat.id,
        "Извини, повтори ещё раз... Прямую по МНК строим?",
        reply_markup=keyboard,
    )


async def error_bars_invalid(message: types.Message):
    """
    В случае если сообщение не содержит погрешности в формате "2.51/2.51",
    функция просит пользователя повторить ввод.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ["0.0/0.0"]])
    await bot.send_message(
        message.chat.id,
        "Ты прислал что-то не то( Давай ещё раз. "
        "Пришли данные для крестов погрешностей по осям х и y в "
        'формате "2.51/2.51", если кресты не нужны, то'
        " нажми на кнопку ниже.",
        reply_markup=keyboard,
    )


async def plot_invalid(message: types.Message):
    """
    В случае некорректного сообщения функция просит пользователя прислать excel-файл ещё раз.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
    await bot.send_message(
        message.chat.id,
        "Ты точно прислал .xlsx файл? Давай ещё раз! "
        "Пришли .xlsx файл с данными, и всё будет готово",
        reply_markup=keyboard,
    )
