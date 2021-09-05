from .error_handlers import choose_invalid, another_group_invalid_type
from .step_handlers import (
    initiate,
    choose_my_group_and_send_schedule,
    choose_another_group_proceed,
    another_group_send_schedule,
)

from create_env import dp
from ...states import Exam

from aiogram import types
from aiogram.dispatcher.filters import Text

initiate = dp.message_handler(commands=["exam"])(initiate)

choose_my_group_and_send_schedule = dp.message_handler(
    Text(equals=["Моя группа"]), state=Exam.choose
)(choose_my_group_and_send_schedule)
choose_another_group_proceed = dp.message_handler(
    Text(equals=["Другая группа"]), state=Exam.choose
)(choose_another_group_proceed)
choose_invalid = dp.message_handler(
    lambda message: message.content_type != types.message.ContentType.TEXT
    or message.text not in ["Моя группа", "Другая группа", "Выход"],
    state=Exam.choose,
    content_types=types.message.ContentType.ANY,
)(choose_invalid)

another_group_send_schedule = dp.message_handler(state=Exam.another_group)(
    another_group_send_schedule
)
another_group_invalid_type = dp.message_handler(
    lambda message: message.content_type != types.message.ContentType.TEXT,
    state=Exam.another_group,
    content_types=types.message.ContentType.ANY,
)(another_group_invalid_type)
