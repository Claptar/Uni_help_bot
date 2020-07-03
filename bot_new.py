import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from data_constructor import psg
from math_module import math_part
from koryavov import kor

logging.basicConfig(level=logging.INFO)

API_TOKEN = '893576564:AAHxlCPFCfcewfz2_0rlygYfJzCbhz4HYJs'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


class Form(StatesGroup):
    course = State()  # Will be represented in storage as 'Form:course'
    group = State()  # Will be represented in storage as 'Form:group'


@dp.message_handler(commands=['help'])
async def help_def(message):
    """
    Функция ловит сообщение с командой '/help' и присылает описание комманд бота
    :param message: telebot.types.Message
    :return:
    """
    with open('txt_files/help.txt', encoding='utf-8', mode='r') as f:
        text = f.read()
    await bot.send_message(message.chat.id, text)


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.course.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(str(name)) for name in range(1, 6)])  # кнопки c номерами курсов
    await bot.send_message(message.chat.id, 'Привет-привет 🙃 Давай знакомиться! Меня зовут A2.'
                                            ' Можешь рассказать мне немного о себе,'
                                            ' чтобы я знал, как могу тебе помочь?'
                                            ' Для начала выбери номер своего курса.', reply_markup=keyboard)


# Check course number. Age gotta be digit from 1 to 4
@dp.message_handler(lambda message: not message.text.isdigit() or not 1 < int(message.text) < 5, state=Form.course)
async def process_age_invalid(message: types.Message):
    """
    Если номер курса введен некорректно
    """
    return await message.reply("Выбери номер курса из предложенных, пожалуйста)")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.course)
async def process_name(message: types.Message):
    """
    Запись номера курса
    """
    await psg.insert_data(message.chat.id, 'Б00-228', message.text)
    await Form.next()
    keyboard = types.ReplyKeyboardRemove()
    await bot.send_message(message.chat.id, 'Отлично, а теперь не подскажешь номер своей группы?\n'
                                            '(В формате Б00–228 или 777, как в расписании)', reply_markup=keyboard)


@dp.message_handler(state=Form.group)
async def process_age(message: types.Message):
    await psg.update_group_num(message.chat.id, message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # кнопки для получения расписания на сегодня или завтра
    keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
    await bot.send_message(message.chat.id, 'Отлично, вот мы и познакомились 🙃 Я очень люблю помогать людям, напиши '
                                            '/help чтобы узнать, что я умею. ', reply_markup=keyboard)

executor.start_polling(dp, skip_updates=True)
