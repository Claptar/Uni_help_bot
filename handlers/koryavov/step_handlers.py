from create_env import bot
from database_queries import insert_action
from handlers_utils.koryavov import kor_page
from ..helpers import today_tomorrow_keyboard
from ..states import Koryavov

from aiogram import types
from aiogram.dispatcher.storage import FSMContext


async def initiate(message: types.Message):
    """
    Функция ловит сообщение с текстом /koryavov.
    Отправляет пользователю сообщение с просьбой выбрать интересующий его номер семестра курса общей физики
    """
    await insert_action("koryavov", message.chat.id)
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        *[types.KeyboardButton(name) for name in [1, 2, 3, 4, 5, "Выход"]]
    )  # кнопки c номерами семестров
    await bot.send_message(
        message.chat.id,
        "Выбери номер семестра общей физики: \n"
        "1) Механика \n"
        "2) Термодинамика \n"
        "3) Электричество \n"
        "4) Оптика\n"
        "5) Атомная и ядерная физика",
        reply_markup=keyboard,
    )
    await Koryavov.sem_num_state.set()


async def semester_number_proceed(message: types.Message, state: FSMContext):
    """
    Функция принимает сообщение от пользователя с номером семестра и записывает его в data storage.
    Так же отправляется сообщение с просьбой указать номер задачи, интересующей пользователя.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    async with state.proxy() as data:
        data["sem_num"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
    await bot.send_message(
        message.chat.id, "Отлично, напиши теперь номер задачи", reply_markup=keyboard
    )
    await Koryavov.task_num_state.set()


async def task_number_proceed(message: types.Message, state: FSMContext):
    """
    Функция ловит сообщение с номером задачи и делает запрос на сайт mipt1.ru чтобы
    узнать номер страницы в корявове с этой задаче. После чего отправляет пользователю
    эту информацию. Так же присылается вопрос "нужна ли ещё одна задача ?".
    """
    task_num = message.text
    await bot.send_chat_action(message.chat.id, "typing")
    async with state.proxy() as data:
        sem_num = int(data["sem_num"])
    reply = "Информация взята с сайта mipt1.ru \n\n" + kor_page(sem_num, task_num)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ["Ещё одну", "Всё, хватит"]])
    await bot.send_message(message.chat.id, reply, reply_markup=keyboard)
    await Koryavov.finish_state.set()


async def finish_proceed(message: types.Message, state: FSMContext):
    """
    Функция принимает сообщение содержащее ['Ещё одну', 'Всё, хватит'] и Koryavov.finish_state(). И в зависимости
    от сообщения завершает функцию /koryavov или отправляет на предыдущий шаг.
    """
    await bot.send_chat_action(message.chat.id, "typing")  # Отображение "typing"
    if message.text == "Ещё одну":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["Выход"]])
        await bot.send_message(
            message.chat.id, "Окей, напиши номер нужной задачи", reply_markup=keyboard
        )
        await Koryavov.task_num_state.set()
    else:
        async with state.proxy() as data:
            data.clear()
        await bot.send_message(
            message.chat.id,
            "Рад был помочь😉 Удачи !",
            reply_markup=today_tomorrow_keyboard(),
        )
        await state.finish()
