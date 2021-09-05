from .error_handlers import (
    new_invalid,
    existing_invalid,
    weekday_invalid,
    time_invalid,
    edit_invalid_type,
    again_invalid,
)
from .step_handlers import (
    initiate,
    new_proceed,
    existing_proceed,
    weekday_proceed,
    time_proceed,
    edit_proceed,
    again_proceed,
)

from create_env import dp
from ...states import Custom

from aiogram import types
from aiogram.dispatcher.filters import Text

initiate = dp.message_handler(commands=["custom"])(initiate)

new_proceed = dp.message_handler(
    Text(equals=["Давай", "Как-нибудь потом"]), state=Custom.new
)(new_proceed)
new_invalid = dp.message_handler(
    lambda message: message.content_type != types.message.ContentType.TEXT
    or message.text not in ["Давай", "Как-нибудь потом", "Выход"],
    state=Custom.new,
    content_types=types.message.ContentType.ANY,
)(new_invalid)

existing_proceed = dp.message_handler(
    Text(equals=["Посмотреть", "Изменить"]), state=Custom.existing
)(existing_proceed)
existing_invalid = dp.message_handler(
    lambda message: message.content_type != types.message.ContentType.TEXT
    or message.text not in ["Посмотреть", "Изменить", "Выход"],
    state=Custom.existing,
    content_types=types.message.ContentType.ANY,
)(existing_invalid)

weekdays = (
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
)
weekday_proceed = dp.message_handler(
    Text(
        equals=weekdays,
    ),
    state=Custom.weekday,
)(weekday_proceed)
weekday_invalid = dp.message_handler(
    lambda message: message.content_type != types.message.ContentType.TEXT
    or message.text not in weekdays,
    state=Custom.weekday,
    content_types=types.message.ContentType.ANY,
)(weekday_invalid)

times = (
    "09:00 – 10:25",
    "10:45 – 12:10",
    "12:20 – 13:45",
    "13:55 – 15:20",
    "15:30 – 16:55",
    "17:05 – 18:30",
    "18:35 – 20:00",
)
time_proceed = dp.message_handler(
    Text(equals=times),
    state=Custom.time,
)(time_proceed)
time_invalid = dp.message_handler(
    lambda message: message.content_type != types.message.ContentType.TEXT
    or message.text not in times,
    state=Custom.time,
    content_types=types.message.ContentType.ANY,
)(time_invalid)

edit_proceed = dp.message_handler(state=Custom.edit)(edit_proceed)
edit_invalid_type = dp.message_handler(
    lambda message: message.content_type != types.message.ContentType.TEXT,
    state=Custom.edit,
    content_types=types.message.ContentType.ANY,
)(edit_invalid_type)

again_proceed = dp.message_handler(
    Text(equals=["Хочу", "Не хочу"]), state=Custom.again
)(again_proceed)
again_invalid = dp.message_handler(
    lambda message: message.content_type != types.message.ContentType.TEXT
    or message.text not in ["Хочу", "Не хочу", "Выход"],
    content_types=types.message.ContentType.ANY,
    state=Custom.again,
)(again_invalid)
