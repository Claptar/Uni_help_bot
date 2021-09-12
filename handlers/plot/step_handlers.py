from create_env import bot
from database_queries import insert_action
from handlers_utils.math_module import math_part
from ..states import Plots

import os

from aiogram import types
from aiogram.dispatcher import FSMContext


async def initiate(message: types.Message):
    """
    Функция ловит сообщение с текстом '/plot' и отправляет сообщение пользователю с просьбой
    указать название графика.
    """
    await insert_action("plot", message.chat.id)
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    await bot.send_message(
        message.chat.id,
        "Снова лабки делаешь?) Ох уж эти графики!..."
        " Сейчас быстренько всё построю, только тебе придётся"
        " ответить на пару вопросов"
        "😉 И не засиживайся, ложись спать)",
    )
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ["Без названия", "Выход"]])
    await bot.send_message(
        message.chat.id,
        "Как мы назовём график?\n"
        "Если не хочешь давать ему название, "
        "то нажми на кнопку ниже 😉",
        reply_markup=keyboard,
    )
    await Plots.title_state.set()


async def title_proceed(message: types.Message, state: FSMContext):
    """
    Функция записывает название графика присланное пользователем в data storage и отправляет
    сообщение пользователю с просьбой указать нужно ли строить прямую по мнк.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    async with state.proxy() as data:
        if message.text == "Без названия":
            data["title"] = ""
        else:
            data["title"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ["✅", "❌", "Выход"]])
    await bot.send_message(
        message.chat.id, "Прямую по МНК строим?", reply_markup=keyboard
    )
    await Plots.mnk_state.set()


async def mnk_proceed(message: types.Message, state: FSMContext):
    """
    Функция ловит сообщение с одним из символов ['✅', '❌'] и в зависимости от ответа
    выставляет error_bars_state или plot_state.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    if message.text == "✅":
        async with state.proxy() as data:
            data["mnk"] = True
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["0.0/0.0"]])
        await bot.send_message(
            message.chat.id,
            "Укажи погрешности по осям х и y в "
            'формате "2.51/2.51", '
            "если кресты не нужны, то нажми на кнопку ниже.",
            reply_markup=keyboard,
        )
        await Plots.error_bars_state.set()
    else:
        async with state.proxy() as data:
            data["mnk"] = False
            data["errors"] = [0.0, 0.0]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
        with open("files/Example.xlsx", "rb") as example:
            await bot.send_document(message.chat.id, example)
        await bot.send_message(
            message.chat.id,
            "Пришли .xlsx файл с данными как в example.xlsx, и всё будет готово.",
            reply_markup=keyboard,
        )
        await Plots.plot_state.set()


async def error_bars_proceed(message: types.Message, state: FSMContext):
    """
    Функция ловит сообщение с размерами крестов погрешностей и просит прислать excel файл, по которому будет
    строиться график.
    """
    try:
        await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
        async with state.proxy() as data:
            data["errors"] = list(map(float, message.text.split("/")))
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
        with open("files/Example.xlsx", "rb") as expl:
            await bot.send_document(message.chat.id, expl)
        await bot.send_message(
            message.chat.id,
            "Пришли .xlsx файл с данными как в example.xlsx и всё будет готово.",
            reply_markup=keyboard,
        )
        await Plots.plot_state.set()
    except Exception as e:
        print(e)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["0.0/0.0"]])
        await bot.send_message(
            message.chat.id,
            "Не могу распознать формат данных( Давай ещё раз. "
            "Пришли данные для крестов погрешностей по осям х и y в "
            'формате "2.51/2.51", если кресты не нужны, то'
            " нажми на кнопку ниже.",
            reply_markup=keyboard,
        )


async def plot_finish(message: types.Message, state: FSMContext):
    """
    Функция ловит сообщение с Excel-файлом, строит график по данным внутри него и присылает сообщение пользователю с
    коэффициентами прямых (если надо) и pdf и png файлы с изображением графика.
    """
    try:
        await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
        file_id = message.document.file_id
        file = await bot.get_file(file_id)
        await bot.download_file(file.file_path, "file.xlsx")
        async with state.proxy() as data:
            title = data["title"]
            errors = data["errors"]
            mnk = data["mnk"]
            data.clear()
        coef = math_part.plots_drawer("file.xlsx", title, errors[0], errors[1], mnk)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            *[types.KeyboardButton(name) for name in ["На сегодня", "На завтра"]]
        )
        await bot.send_message(
            message.chat.id, "Принимай работу!)", reply_markup=keyboard
        )
        with open("plot.png", "rb") as photo:
            await bot.send_chat_action(
                message.chat.id, "upload_document"
            )  # Отображение "upload document"
            await bot.send_document(message.chat.id, photo)
        if mnk:
            for i in range(len(coef)):
                a, b, d_a, d_b = coef[i]
                await bot.send_chat_action(
                    message.chat.id, "typing"
                )  # Отображение "typing"
                await bot.send_message(
                    message.chat.id,
                    f"Коэффициенты {i + 1}-ой прямой:\n"
                    f" a = {a} +- {d_a}\n"
                    f" b = {b} +- {d_b}",
                )
        with open("plot.pdf", "rb") as photo:
            await bot.send_chat_action(
                message.chat.id, "upload_document"
            )  # Отображение "upload document"
            await bot.send_document(message.chat.id, photo)
        os.remove("plot.pdf")
        os.remove("plot.png")
        math_part.BOT_PLOT = False
        os.remove("file.xlsx")
        await state.finish()
    except Exception as e:
        os.remove("file.xlsx")
        print(e)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
        await bot.send_message(
            message.chat.id,
            "Ты точно прислал .xlsx файл как в примере? Давай ещё раз!",
            reply_markup=keyboard,
        )
