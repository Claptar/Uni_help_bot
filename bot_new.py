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
from data_constructor import psg
import timetable.timetable
import datetime

logging.basicConfig(level=logging.INFO)

API_TOKEN = '893576564:AAHxlCPFCfcewfz2_0rlygYfJzCbhz4HYJs'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    choose_group = State()
    my_group = State()
    course = State()
    group = State()
    weekday = State()
    student = {'Group': 'None', 'Course': 'None'}


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
@dp.message_handler(lambda message: not message.text.isdigit() or not 1 <= int(message.text) < 5, state=Form.course)
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
    Form.student['Course'] = message.chat.id
    await Form.group.set()
    keyboard = types.ReplyKeyboardRemove()
    await bot.send_message(message.chat.id, 'Отлично, а теперь не подскажешь номер своей группы?\n'
                                            '(В формате Б00–228 или 777, как в расписании)', reply_markup=keyboard)


@dp.message_handler(state=Form.group)
async def process_age(message: types.Message, state: FSMContext):
    psg.insert_data(message.chat.id, message.text, int(Form.student['Course']))
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # кнопки для получения расписания на сегодня или завтра
    keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
    await bot.send_message(message.chat.id, 'Отлично, вот мы и познакомились 🙃 Я очень люблю помогать людям, напиши '
                                            '/help чтобы узнать, что я умею. ', reply_markup=keyboard)
    await state.finish()


@dp.message_handler(Text(equals='Выход'), state='*')
async def user_exit(message: types.Message, state: FSMContext):
    """
    Функция, выполняющая выход по желанию пользователя (на любой стадии).
    """
    current_state = await state.get_state()  # проверка, что запущено хотя бы какое-то из состояний
    if current_state is None:
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # кнопки для получения расписания на сегодня или завтра
    keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
    await bot.send_message(message.chat.id, 'Без проблем! Но ты это, заходи, если что 😉', reply_markup=keyboard)
    # стикос "Ты заходи есчо"
    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIsCV42vjU8mR9P-zoPiyBu_3_eG-wTAAIMDQACkjajC9UvBD6_RUE4GAQ')

    # При выходе выключаем машину состояний
    await state.finish()


@dp.message_handler(Text(equals=['На сегодня', 'На завтра']), state='*')
async def get_start_schedule(message):
    """
    Функция ловит сообщение с текстом "Расписание на сегодня/завтра".
    Узнает номер дня недели сегодня/завтра и по этому значению обращается в функцию timetable_by_group().
    :return:
    """
    student = psg.get_student(message.chat.id)
    # проверка существования сочетания курс-группа, которое записано в базе данных для этого пользователя
    if timetable.timetable.check_group(student[0], student[1]):
        # список дней для удобной конвертации номеров дней недели (0, 1, ..., 6) в их названия
        week = tuple(['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'])
        today = datetime.datetime.today().weekday()  # today - какой сегодня день недели (от 0 до 6)
        if message.text == 'На сегодня':  # расписание на сегодня
            schedule = timetable.timetable.timetable_by_group(student[1], student[0], week[today])
            STRING = ''  # "строка" с расписанием, которую отправляем сообщением
            for row in schedule.iterrows():  # проходимся по строкам расписания, приплюсовываем их в общую "строку"
                # время пары - жирный + наклонный шрифт, название пары на следующей строке
                string: str = '<b>' + '<i>' + row[0] + '</i>' + '</b>' + '\n' + row[1][0]
                STRING += string + '\n\n'  # между парами пропуск (1 enter)
            # parse_mode - чтобы читал измененный шрифт
            await bot.send_message(message.chat.id, STRING, parse_mode='HTML')
            # кнопки для получения расписания на сегодня или завтра
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
            await bot.send_message(message.chat.id, 'Чем ещё я могу помочь?', reply_markup=keyboard)
        elif message.text == 'На завтра':  # расписание на завтра
            tomorrow = 0  # номер дня для завтра, если это воскресенье (6), то уже стоит (0)
            if today in range(6):  # если не воскресенье, то значение равно today + 1
                tomorrow = today + 1
            schedule = timetable.timetable.timetable_by_group(student[1], student[0], week[tomorrow])
            STRING = ''  # "строка" с расписанием, которую отправляем сообщением
            for row in schedule.iterrows():  # проходимся по строкам расписания, приплюсовываем их в общую "строку"
                # время пары - жирный + наклонный шрифт, название пары на следующей строке
                string: str = '<b>' + '<i>' + row[0] + '</i>' + '</b>' + '\n' + row[1][0]
                STRING += string + '\n\n'  # между парами пропуск (1 enter)
            # parse_mode - чтобы читал измененный шрифт
            await bot.send_message(message.chat.id, STRING, parse_mode='HTML')
            # кнопки для получения расписания на сегодня или завтра
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
            await bot.send_message(message.chat.id, 'Чем ещё я могу помочь?', reply_markup=keyboard)
    else:  # если в базе данных для этого пользователя указано несуществующее сочетание курс-группа
        await bot.send_message(message.chat.id, 'Не могу найти расписание для указанных тобой номера курса и группы 😞 '
                                                'Нажми /profile чтобы проверить корректность данных.')


@dp.message_handler(commands='timetable')
async def initiate_timetable(message: types.Message):
    """
    Функция ловит сообщение с текстом "/timetable".
    Отправляет пользователю вопрос, расписание своей или другой группы ему нужно.
    """
    await Form.choose_group.set()  # ставим 1 состояние - choose_group

    await bot.send_message(message.chat.id, 'Снова не можешь вспомнить, какая пара следующая?\nНичего, я уже тут! 😉')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Моя группа', 'Другая группа', 'Выход']])
    await bot.send_message(message.chat.id, 'Тебе нужно расписание своей группы или '
                                            'какой-то другой?', reply_markup=keyboard)


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT
                    or message.text not in ['Моя группа', 'Другая группа', 'Выход'],
                    state=Form.choose_group, content_types=types.message.ContentType.ANY)
async def initiate_invalid(message: types.Message):
    """
    Функция просит пользователя выбрать вариант из списка ['Моя группа', 'Другая группа', 'Выход'],
    если сообщение не содержит никакую из этих строк (+ проверка типа сообщения).
    """
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


@dp.message_handler(Text(equals='Моя группа'), state=Form.choose_group)
async def process_my_group_weekday(message: types.Message, state: FSMContext):
    """
    Функция принимает сообщение, если нужно расписание своей группы.
    Отправляет пользователю вопрос о нужном дне недели.
    В случае ошибки отправляет пользователю сообщение о необходимости редактирования данных в разделе "/profile".
    """
    await Form.my_group.set()  # изменяем состояние на my_group

    student = psg.get_student(message.chat.id)
    # проверка существования сочетания курс-группа, которое записано в базе данных для этого пользователя
    if timetable.timetable.check_group(student[0], student[1]):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # дни недели для тыков и кнопка для выхода (строки выбраны по размеру слов)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Понедельник', 'Вторник']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Среда', 'Четверг']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Пятница', 'Суббота']])
        keyboard.add(*[types.KeyboardButton(name) for name in ['Воскресенье', 'Выход']])
        await bot.send_message(message.chat.id,
                               'Расписание на какой день недели ты хочешь узнать?',
                               reply_markup=keyboard)
    else:  # если в базе данных для этого пользователя указано несуществующее сочетание курс-группа
        keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=True)  # кнопки для получения расписания на сегодня или завтра
        keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
        await bot.send_message(message.chat.id,
                               'Не могу найти расписание для указанных тобой номеров курса и группы 😞\n'
                               'Нажми /profile чтобы проверить корректность данных.',
                               reply_markup=keyboard)
        await state.finish()  # в случае ошибки выключаем машину состояний


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT
                    or message.text not in ['Понедельник', 'Вторник', 'Среда', 'Четверг',
                                            'Пятница', 'Суббота', 'Воскресенье', 'Выход'],
                    state=Form.my_group,
                    content_types=types.message.ContentType.ANY)
async def process_my_group_weekday_invalid(message: types.Message):
    """
    Функция просит пользователя выбрать вариант из списка ['Понедельник', 'Вторник', 'Среда', 'Четверг',
                                                           'Пятница', 'Суббота', 'Воскресенье', 'Выход'],
    если сообщение не содержит никакую из этих строк.
    """
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


@dp.message_handler(Text(equals=['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']),
                    state=Form.my_group)
async def return_my_group_schedule(message: types.Message, state: FSMContext):
    student = psg.get_student(message.chat.id)
    # проверка на достоверность пары курс-группа для этого пользователя уже была сделана
    schedule = timetable.timetable.timetable_by_group(student[1], student[0], message.text)
    STRING = ''  # "строка" с расписанием, которую отправляем сообщением
    for row in schedule.iterrows():  # проходимся по строкам расписания, приплюсовываем их в общую "строку"
        # время пары - жирный + наклонный шрифт, название пары на следующей строке
        string: str = '<b>' + '<i>' + row[0] + '</i>' + '</b>' + '\n' + row[1][0]
        STRING += string + '\n\n'  # между парами пропуск (1 enter)
    await bot.send_message(message.chat.id, STRING, parse_mode='HTML')  # parse_mode - чтобы читал измененный шрифт
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # кнопки для получения расписания на сегодня или завтра
    keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
    await bot.send_message(message.chat.id, 'Чем ещё я могу помочь?', reply_markup=keyboard)

    await state.finish()  # выключаем машину состояний


@dp.message_handler(Text(equals='Другая группа'), state=Form.choose_group)
async def get_course(message: types.Message):
    await Form.course.set()  # изменяем состояние на course

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in map(str, range(1, 4))])  # кнопки c номерами курсов
    keyboard.add(*[types.KeyboardButton(name) for name in map(str, [4, 5, 'Выход'])])  # и выход
    await bot.send_message(message.chat.id, 'Не подскажешь номер курса?', reply_markup=keyboard)


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT
                    or (not message.text.isdigit() and message.text != 'Выход')
                    or not 1 <= int(message.text) <= 5,
                    state=Form.course,
                    content_types=types.message.ContentType.ANY)
async def process_course_invalid(message: types.Message):
    """
    Функция просит ввести номер курса заново, если он введен некорректно.
    """
    await message.reply("Выбери номер курса из предложенных, пожалуйста)")


@dp.message_handler(Text(equals=list(map(str, range(1, 6)))), state=Form.course)
async def process_course(message: types.Message, state: FSMContext):
    """
    Функция сохраняет номер курса и отправляет пользователю вопрос о номере группы.
    """
    async with state.proxy() as data:
        data['course'] = message.text  # сохраняем номер курса

    await Form.group.set()  # изменяем состояние на group
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])  # кнопка для выхода из функции
    await bot.send_message(message.chat.id,  # просим пользователя ввести номер группы
                           'Не подскажешь номер группы?\n'
                           '(В формате Б00–228 или 777, как в расписании)',
                           reply_markup=keyboard)


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT,
                    state=Form.group,
                    content_types=types.message.ContentType.ANY)
async def process_group_invalid_type(message: types.Message):
    """
    Функция просит ввести номер группы заново, если формат ввода неправильный.
    """
    await message.reply("Пришли номер группы в верном формате, пожалуйста)")


@dp.message_handler(state=Form.group)
async def process_group(message: types.Message, state: FSMContext):
    """
    Функция проверяет существования пары курс-группа в расписании. Если такая существует, то пользователю
    отправляется вопрос о нужном дне недели, иначе функция просит ввести номер группы заново.
    """
    async with state.proxy() as data:
        # проверяем существование такой пары курс-группа в расписании
        if timetable.timetable.check_group(message.text, data['course']):
            data['group'] = message.text  # если такая пара существует, то сохраняем номер группы
            await Form.weekday.set()  # и изменяем состояние на weekday
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # дни недели для тыков и кнопка для выхода (строки выбраны по размеру слов)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Понедельник', 'Вторник']])
            keyboard.add(*[types.KeyboardButton(name) for name in ['Среда', 'Четверг']])
            keyboard.add(*[types.KeyboardButton(name) for name in ['Пятница', 'Суббота']])
            keyboard.add(*[types.KeyboardButton(name) for name in ['Воскресенье', 'Выход']])
            await bot.send_message(message.chat.id,
                                   'Расписание на какой день недели ты хочешь узнать?',
                                   reply_markup=keyboard)
        else:  # в случае отсутствия такой пары курс-группа в расписании, просим пользователя заново ввести номер группы
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*[types.KeyboardButton(name) for name in ['Выход']])  # кнопка для выхода из функции
            await bot.send_message(message.chat.id,
                                   'Не могу найти расписание для указанного тобой номера группы 😞\n'
                                   'Пришли мне номер как в расписании, пожалуйста)',
                                   reply_markup=keyboard)


@dp.message_handler(lambda message: message.content_type != types.message.ContentType.TEXT
                    or message.text not in ['Понедельник', 'Вторник', 'Среда', 'Четверг',
                                            'Пятница', 'Суббота', 'Воскресенье', 'Выход'],
                    state=Form.weekday,
                    content_types=types.message.ContentType.ANY)
async def process_weekday_invalid(message: types.Message):
    """
    Функция просит пользователя выбрать вариант из списка ['Понедельник', 'Вторник', 'Среда', 'Четверг',
                                                           'Пятница', 'Суббота', 'Воскресенье', 'Выход'],
    если сообщение не содержит никакую из этих строк.
    """
    await message.reply("Выбери вариант из предложенных, пожалуйста)")


@dp.message_handler(state=Form.weekday)
async def return_schedule(message: types.Message, state: FSMContext):
    """
    Функция отправляет расписание на выбранный день недели.
    """
    async with state.proxy() as data:
        data['weekday'] = message.text  # все проверки уже были сделаны выше
        schedule = timetable.timetable.timetable_by_group(data['course'], data['group'], data['weekday'])
        STRING = ''  # "строка" с расписанием, которую отправляем сообщением
        for row in schedule.iterrows():  # проходимся по строкам расписания, приплюсовываем их в общую "строку"
            # время пары - жирный + наклонный шрифт, название пары на следующей строке
            string: str = '<b>' + '<i>' + row[0] + '</i>' + '</b>' + '\n' + row[1][0]
            STRING += string + '\n\n'  # между парами пропуск (1 enter)
        await bot.send_message(message.chat.id, STRING, parse_mode='HTML')  # parse_mode - чтобы читал измененный шрифт
        # кнопки для получения расписания на сегодня или завтра
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['На сегодня', 'На завтра']])
        await bot.send_message(message.chat.id, 'Чем ещё я могу помочь?', reply_markup=keyboard)

    await state.finish()  # выключаем машину состояний


@dp.message_handler(commands=['exam'])
async def initiate_exam_timetable(message):
    """
    Функция ловит сообщение с текстом '/exam'.
    Отправляет запрос о выборе группы и вызывает функцию get_exam_timetable().
    :param message: telebot.types.Message
    :return:
    """
    await bot.send_message(message.chat.id, 'Ещё не время... Но ты не забывай...')
    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAMEXj8IxnJkYATlpAOTkJyLiXH2u0UAAvYfAAKiipYBsZcZ_su45LkYBA')


# def get_exam_timetable(message):
#     """
#     Функция считывает номер группы, вызывает функцию get_exam_timetable из модуля timetable,
#     отправляет пользователю раписание экзаменов из файла.
#     :param message: telebot.types.Message
#     :return:
#     """
#     if message.text in texting.texting_symbols.groups:
#         path = os.path.abspath('')
#         timetable.timetable_old.get_exam_timetable(message.text)
#         f = open(f'{path}/timetable/exam.txt')
#         for line in f:
#             bot.send_message(message.chat.id, line)
#         open(f'{path}/timetable/exam.txt', 'w').close()
#     else:
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         keyboard.add(*[types.KeyboardButton(name) for name in ['Попробую ещё раз', 'Ладно, сам посмотрю']])
#         msg = bot.send_message(message.chat.id, 'Что-то не получилось... '
#                                                 'Ты мне точно прислал номер группы в правильном формате ?',
#                                reply_markup=keyboard)
#         bot.register_next_step_handler(msg, ask_group)


executor.start_polling(dp, skip_updates=True)
