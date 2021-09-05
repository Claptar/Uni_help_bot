from .error_handlers import (
    choose_type_invalid,
    another_type_group_number_proceed_invalid,
    weekday_proceed_invalid,
)
from .step_handlers import (
    initiate,
    choose_another_type_proceed,
    choose_my_group_custom_type_proceed,
    another_type_group_number_proceed,
    weekday_proceed_and_schedule_send,
)

from create_env import dp
from ...states import Timetable

from aiogram import types
from aiogram.dispatcher.filters import Text

initiate = dp.message_handler(commands="timetable")(initiate)

choose_another_type_proceed = dp.message_handler(
    Text(equals=["Другая группа"]), state=Timetable.choose
)(choose_another_type_proceed)
choose_my_group_custom_type_proceed = dp.message_handler(
    Text(equals=["Личное", "Моя группа"]), state=Timetable.choose
)(choose_my_group_custom_type_proceed)
choose_type_invalid = dp.message_handler(
    lambda message: message.content_type != types.message.ContentType.TEXT
    or message.text not in ["Личное", "Моя группа", "Другая группа", "Выход"],
    state=Timetable.choose,
    content_types=types.message.ContentType.ANY,
)(choose_type_invalid)

another_type_group_number_proceed = dp.message_handler(state=Timetable.another_group)(
    another_type_group_number_proceed
)
another_type_group_number_proceed_invalid = dp.message_handler(
    lambda message: message.content_type != types.message.ContentType.TEXT,
    state=Timetable.another_group,
    content_types=types.message.ContentType.ANY,
)(another_type_group_number_proceed_invalid)

weekdays = (
    "На неделю",
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
)
weekday_proceed_and_schedule_send = dp.message_handler(
    Text(equals=weekdays),
    state=Timetable.weekday,
)(weekday_proceed_and_schedule_send)
weekday_proceed_invalid = dp.message_handler(
    lambda message: message.content_type != types.message.ContentType.TEXT
    or message.text not in weekdays,
    state=Timetable.weekday,
    content_types=types.message.ContentType.ANY,
)(weekday_proceed_invalid)
