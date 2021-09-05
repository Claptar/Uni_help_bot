from datetime import datetime
import pickle
from pytz import timezone

from create_env import bot
from data_constructor import psg
from ...helpers import schedule_string, today_tomorrow_keyboard


async def send_today_tomorrow_schedule(message):
    """
    Функция ловит сообщение с текстом 'На сегодня/завтра'.
    Возвращает расписание на этот день, вызывает функцию timetable.timetable_by_group().
    По умолчанию, если у этого пользователя есть личное расписание, выдает его,
    иначе - расписание группы пользователя.
    Схема:
                             CUSTOM
                            /     \
                        True    False (ERR or EMPTY_RES)
                       /   \         \
                  (SMTH,) (None,) — MY_GROUP — True — SEND()
                    /                   /
                  SEND()             False — EMPTY_RES — Знакомы ли мы?
                                       |
                              CONN_ERR or OTHER_ERR — Попробуй позже, пожалуйста
    """
    await psg.insert_action("to/yes", message.chat.id)
    # список дней для удобной конвертации номеров дней недели (0, 1, ..., 6) в их названия
    week = tuple(
        [
            "Понедельник",
            "Вторник",
            "Среда",
            "Четверг",
            "Пятница",
            "Суббота",
            "Воскресенье",
        ]
    )
    # today - какой сегодня день недели (от 0 до 6)
    today = datetime.now(tz=timezone("Europe/Moscow")).weekday()
    tomorrow = (
        today + 1 if today in range(6) else 0
    )  # номер дня для завтра, если это воскресенье (6), то 0
    day = (
        today if message.text == "На сегодня" else tomorrow
    )  # выбор дня в зависимости от запроса
    custom_timetable = await psg.send_timetable(custom=True, chat_id=message.chat.id)
    # проверка, есть ли у этого пользователя личное расписание в базе данных (+ не произошло ли ошибок)
    if custom_timetable[0] and custom_timetable[1][0] is not None:
        schedule = pickle.loads(custom_timetable[1][0])[week[day]].to_frame()
        await bot.send_message(  # отправляем расписание
            message.chat.id, schedule_string(schedule), parse_mode="HTML"
        )
    # если у этого пользователя нет личного расписания в базе данных или произошла ошибка при запросе
    # личного расписания, то пробуем отправить расписание группы
    else:
        group_timetable = await psg.send_timetable(
            my_group=True, chat_id=message.chat.id
        )
        if group_timetable[0]:  # если пользователь есть в базе
            if bytes(group_timetable[1][0]) == b"DEFAULT":
                await bot.send_message(  # отправляем расписание
                    message.chat.id,
                    "В этом семестре нет официального расписания для твоей группы( "
                    "Пожалуйста, измени номер своей группы в /profile "
                    "или создай личное расписание в /custom 😉",
                    reply_markup=today_tomorrow_keyboard(),
                )
            else:
                schedule = pickle.loads(group_timetable[1][0])[week[day]].to_frame()
                await bot.send_message(  # отправляем расписание
                    message.chat.id, schedule_string(schedule), parse_mode="HTML"
                )
                await bot.send_message(
                    message.chat.id,
                    "Чем ещё я могу помочь?",
                    reply_markup=today_tomorrow_keyboard(),
                )
        # если в базе данных нет этого пользователя
        elif not group_timetable[0] and group_timetable[1] == "empty_result":
            await bot.send_message(
                message.chat.id,
                "Кажется, мы с тобой еще не знакомы... 😢\nСкорей пиши мне /start!",
                reply_markup=today_tomorrow_keyboard(),
            )
        # если произошла ошибка
        else:
            await bot.send_message(
                message.chat.id,
                "Что-то пошло не так, попробуй еще раз позже, пожалуйста)",
                reply_markup=today_tomorrow_keyboard(),
            )
