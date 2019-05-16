import os
import random
import telebot
from telebot.types import Message
from telebot import types
import pandas as pd
import numpy as np
import math_part
import timetable


base_url = 'https://api.telegram.org/bot838117295:AAGUldfunZu6Cyx-kJkCucQuH3pCLBD4Jcg/'
TOKEN = '838117295:AAGUldfunZu6Cyx-kJkCucQuH3pCLBD4Jcg'
PATH = os.path.abspath('')
bot = telebot.TeleBot(TOKEN)
MESSAGE_NUM = 0
MESSAGE_COM = ''
Q_NUM = 0
GROUP_NUM = ''

comms = ['help', 'start', 'flash_cards', 'figure_mnk', 'figure', 'mnk_constants', 'timetable', 'exam']

crazy_tokens = 0
emoji = ['😀', '😬', '😁', '😂', '😃', '👿', '😈','😴','🤧', '🤢', '🤮', '🤒','🤕','😷','🤐',
         '🤯','😲','😵','🤩','😭','😓','🤤','😪','😥','😢','😧','😦','😄','🤣','😅',
         '😆','😇','😉','😊','🙂','🙃','☺','😋','😌','😍','😘','😗','😙','😚','🤪',
         '😜','😝','😛','🤑','😎','🤓','🧐','🤠','🤗','🤡','😏','😶','😐','😑','😒',
         '🙄','🤨','🤔','🤫','🤭','🤥','😳','😞','😟','😠','😡','🤬','😔','😕','🙁',
         '☹','😣','😖','😫','😩','😤','😮','😱','😨','😰','😯','😦','😧','😢','😥',
         '😪','🤤','😓','😭','🤩']

quotes = ['Трудности похожи на собак: они кусают лишь тех, кто к ним не привык... - Антисфен.',
          'Когда долго начинаешь всматриваться в пропасть – пропасть начинает всматриваться в тебя. - Ницше.',
          'Найти любовь проще, чем стать тем человеком, которого ищут.',
          'Желание - это тысяча способов, нежелание - это тысяча препятствий.',
          'Обиженные люди обижают людей. И все равно любите их. Хотя никто не запрещает вам любить их на расстоянии.',
          'Не злись на идиотов. Они так и останутся идиотами, а ты потеряешь самообладание. - Мэри Хиггинс Кларк.',
          'Очень опасно встретить женщину, которая полностью тебя понимает. Это обычно кончается женитьбой. - Оскар Уайльд.',
          'Чтобы дойти до цели, надо прежде всего идти. - Оноре де Бальзак.',
          'Если вы идете через ад, идите не останавливаясь. - Уинстон Черчилль.',
          'Лишь очень немногие живут сегодняшним днем. Большинство готовится жить позднее. - Джонатан Свифт.',
          'Если Бог откладывает, то это еще не значит, что он отказывает.',
          'В любой непонятной ситуации — ложись спать. - Еврейская мудрость.',
          'Не переживай о многом, и ты переживёшь многих.',
          'В жизни все временно. Так что, если все идет хорошо, наслаждайся–вечно не продлится. А если все идет плохо – не переживай, это не продлится вечно.',
          'История учит нас по меньшей мере тому, что хуже может быть всегда.',
          'Самое ужасное, это ожидание того, чего не будет.',
          'Люди думают, что будут счастливы, если переедут в другое место, а потом оказывается: куда бы ты ни переехал, ты берешь с собой себя.',
          'Умный человек иногда торопится, но никогда не делает ничего второпях.',
          'Ненависть — месть труса за испытанный им страх. - Бернард Шоу.',
          'Те люди, которые чаще всего прощали и дольше всего терпели, обычно уходят неожиданно и навсегда...',
          'Постарайтесь получить то, что любите, иначе придется полюбить то, что получили. - Бернард Шоу.',
          'Никогда не делай выводов о человеке, пока не узнаешь причины его поступков.']


@bot.message_handler(commands=['help'])
def help_def(message):
    bot.send_message(message.chat.id, 'Сейчас я расскажу, чем я могу тебе помочь ☺️\n'
                                      '/figure - Хочешь построить график по точкам ? Не вопрос !\n'
                                      '/figure_mnk - Хочешь построить график линеаризованный по МНК? Запросто !\n'
                                      '/mnk_constants - Нужно посчитать константы прямой по МНК? Я помогу !\n'
                                      '/timetable - Забыл расписание?) Бывает, пиши, я помогу 😉📱📱📱'
                                      '\n/exam - Подскажу расписание экзаменов, но ты сам захотел...'
                                      ' Я не люблю напоминать'
                                      'о плохом...\n'
                                      '/flash_cards - Давай сыграем в игру... Я тебе определение/формулировку, а ты мне'
                                      '"знаю/не знаю.')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет-привет 🙃 Я очень люблю помогать людям,'
                                      ' напиши /help чтобы узнать, что я умею. ')


@bot.message_handler(commands=['flash_cards'])
def start(message):
    bot.send_message(message.chat.id, 'Хочешь вспомнить парочку определений ?)📚📚')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Матан']])
    msg = bot.send_message(message.chat.id, 'Сначала выбери предмет', reply_markup=keyboard)
    bot.register_next_step_handler(msg, subject)


def subject(message):
    global Q_NUM, PATH
    if (message.text == 'Матан') or (message.text == 'Ещё'):
        Q_NUM = random.randint(0, 13)
        questions = pd.read_excel(f'{PATH}/flash_cards/math/flash_data.xlsx', header=None)
        d = np.array(questions)
        question = d[Q_NUM, 0]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Покажи']])
        msg = bot.send_message(message.chat.id, question, reply_markup=keyboard)
        bot.register_next_step_handler(msg, answer)
    elif message.text == 'Всё, хватит' or message.text == 'В другой раз...':
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Возвращайся ещё !', reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Матан', 'В другой раз...']])
        msg = bot.send_message(message.chat.id, 'Извини, я тебя не понял, можешь повторить ?', reply_markup=keyboard)
        bot.register_next_step_handler(msg, subject)


def answer(message):
    global Q_NUM
    if message.text == 'Покажи' or message.text == 'Покажи правильный ответ':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Ещё', 'Всё, хватит']])
        bot.send_message(message.chat.id, 'Правильный ответ:')
        with open(f'{PATH}/flash_cards/math/{Q_NUM + 1}.png', 'rb') as photo:
            msg = bot.send_photo(message.chat.id, photo, reply_markup=keyboard)
        bot.register_next_step_handler(msg, subject)
    elif message.text == 'Я не хочу смотреть ответ':
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ты не расстраивайся ! Все мы делаем ошибки...', reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Покажи правильный ответ', 'Я не хочу смотреть ответ']])
        msg = bot.send_message(message.chat.id,
                               'Извини, что-то не могу уловить твои мозговые волны... Попробуй ещё раз',
                               reply_markup=keyboard)
        bot.register_next_step_handler(msg, answer)


@bot.message_handler(commands=['figure_mnk'])
def figure_mnk(message):
    global MESSAGE_COM
    bot.send_message(message.chat.id, 'Снова лабки делаешь ?) Ох уж эти линеаризованные графики !...'
                                      ' Сейчас быстренько всё построю, только тебе придётся ответить на пару вопросов'
                                      '😉. И не засиживайся, ложись спать))')
    msg = bot.send_message(message.chat.id, 'Скажи, как мне подписать ось х ?')
    MESSAGE_COM = 'figure_mnk'
    bot.register_next_step_handler(msg, ax_x)


@bot.message_handler(commands=['mnk_constants'])
def mnk_constants(message):
    global MESSAGE_COM
    msg = bot.send_message(message.chat.id, 'Хочешь узнать константы прямых по МНК ?)'
                                            ' Даа, непростая задача, так и быть, помогу тебе ! ')
    MESSAGE_COM = 'mnk_constants'
    bot.register_next_step_handler(msg, tit)


@bot.message_handler(commands=['figure'])
def figure(message):
    global MESSAGE_COM
    MESSAGE_COM = 'figure'
    bot.send_message(message.chat.id, 'Ой, а что это у тебя за зависимость такая?) Мне даже самому интересно стало.'
                                      ' Сейчас быстренько всё построю, только тебе придётся ответить на пару вопросов'
                                      '😉))')
    msg = bot.send_message(message.chat.id, 'Скажи, как мне подписать ось х ?')
    bot.register_next_step_handler(msg, ax_x)


def ax_x(message):
    math_part.LABEL_X = message.text
    msg = bot.send_message(message.chat.id, 'А, как мне подписать ось у ?')
    bot.register_next_step_handler(msg, ax_y)


def ax_y(message):
    math_part.LABEL_Y = message.text
    msg = bot.send_message(message.chat.id, 'Самое главное: как мне назвать график ?')
    bot.register_next_step_handler(msg, tit)


def tit(message):
    if message.text == 'Видимо не в этот раз ...':
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ну ладно... 😥', reply_markup=keyboard)
    else:
        if message.text == 'Попробую ещё раз':
            keyboard = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Давай попробуем ещё раз😔', reply_markup=keyboard)
        math_part.TITLE = message.text
        bot.send_message(message.chat.id, 'Пришли мне файл с данными вот в таком формате и всё будет готово😊')
        with open('example.jpg', 'rb') as photo:
            msg = bot.send_photo(message.chat.id, photo)
        bot.register_next_step_handler(msg, date_mnk)


def date_mnk(message):
    try:
        global MESSAGE_COM
        file_id = message.json.get('document').get('file_id')
        file_path = bot.get_file(file_id).file_path
        downloaded_file = bot.download_file(file_path)
        src = message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        a, b, d_a, d_b = math_part.mnk_calc(src)

        if MESSAGE_COM == 'figure_mnk':

            math_part.plots_drawer(src, math_part.LABEL_X, math_part.LABEL_Y, math_part.TITLE)

            with open('plot.png', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)

            for i in range(0, len(a)):
                bot.send_message(message.chat.id, f'Коэффициенты {i + 1}-ой прямой:\n'
                f' a = {round(a[i], 3)} +- {round(d_a[i], 3)}\n'
                f' b = {round(b[i], 3)} +- {round(d_b[i], 3)}')
            os.remove('plot.png')

        elif MESSAGE_COM == 'figure':

            math_part.plot_drawer(src, math_part.LABEL_X, math_part.LABEL_Y, math_part.TITLE)

            with open('plot.png', 'rb') as photo:

                bot.send_photo(message.chat.id, photo)

            os.remove('plot.png')

        elif MESSAGE_COM == 'mnk_constants':

            for i in range(0, len(a)):
                bot.send_message(message.chat.id, f'Коэффициенты {i + 1}-ой прямой:\n'
                f' a = {round(a[i], 3)} +- {round(d_a[i], 3)}\n'
                f' b = {round(b[i], 3)} +- {round(d_b[i], 3)}')
        os.remove(src)
        math_part.TITLE = ''
        math_part.LABEL_Y = ''
        math_part.LABEL_X = ''
    except Exception as e:
        print(e)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ['Попробую ещё раз', 'Видимо не в этот раз ...']])
        msg = bot.send_message(message.chat.id,
                               'Что-то не получилось... Проверь файл который ты прислал😨 ', reply_markup=keyboard)
        bot.register_next_step_handler(msg, tit)


@bot.message_handler(commands=['timetable'])
def get_group(message)
    bot.send_message(message.chat.id, 'Снова не можешь вспомнить какая пара следующая?)'
                                      'Ничего, я уже тут!')
    bot.send_message(message.chat.id, 'Не подскажешь номер своей группы? (В формате Б00-000)')
    bot.register_next_step_handler(message, get_weekday)


def get_weekday(message):
    global GROUP_NUM
    GROUP_NUM = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']])
    msg = bot.send_message(message.chat.id, 'Расписание на какой день ты хочешь узнать?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, get_schedule)


def get_schedule(message):
    timetable.get_timetable(GROUP_NUM, message.text)
    f = open('class.txt')
    for line in f:
        bot.send_message(message.chat.id, line)
    open('class.txt', 'w').close()
    keyboard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Чем я ещё могу помочь?', reply_markup=keyboard)


@bot.message_handler(commands=['exam'])
def ask_group(message):
    bot.send_message(message.chat.id, 'Не подскажешь номер своей группы? (В формате Б00-000)')
    bot.register_next_step_handler(message, get_exam_timetable)


def get_exam_timetable(message):
    timetable.get_exam_timetable(message.text)
    f = open('exam.txt')
    for line in f:
        bot.send_message(message.chat.id, line)
    open('exam.txt', 'w').close()


# Если отправить боту просто текст или незнакомую команду, то он ответит так:
@bot.message_handler(content_types=['text'])
def chatting(message):
    global crazy_tokens
    crazy_tokens += 1
    if crazy_tokens <= 2:
        bot.send_message(message.chat.id, 'Боюсь, я не совсем понимаю, о чём ты. \n' 
                                          'Напиши /help, чтобы узнать, что я умею.\n')
    elif crazy_tokens <= 4:
        bot.send_message(message.chat.id, random.choice(emoji))
    elif crazy_tokens <= 7:
        bot.send_message(message.chat.id, random.choice(quotes))
    elif crazy_tokens == 8:
        bot.send_message(message.chat.id, 7*random.choice(emoji))
        crazy_tokens = 0


bot.polling()
