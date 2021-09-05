from .error_handlers import choose_invalid, custom_invalid, group_invalid_type
from .step_handlers import choose_proceed, custom_proceed, group_proceed, initiate

from create_env import dp
from ..states import Profile

from aiogram import types
from aiogram.dispatcher.filters import Text

initiate = dp.message_handler(commands="profile")(initiate)

choose_proceed = dp.message_handler(Text(equals=["Да", "Нет"]), state=Profile.choose)(
    choose_proceed
)
choose_invalid = dp.message_handler(
    lambda message: message.content_type != types.message.ContentType.TEXT
    or message.text not in ["Да", "Нет", "Выход"],
    content_types=types.message.ContentType.ANY,
    state=Profile.choose,
)(choose_invalid)

group_proceed = dp.message_handler(state=Profile.group)(group_proceed)
group_invalid_type = dp.message_handler(
    lambda message: message.content_type != types.message.ContentType.TEXT,
    content_types=types.message.ContentType.ANY,
    state=Profile.group,
)(group_invalid_type)

custom_proceed = dp.message_handler(
    Text(equals=["Хочу", "Не хочу"]), state=Profile.custom
)(custom_proceed)
custom_invalid = dp.message_handler(
    lambda message: message.content_type != types.message.ContentType.TEXT
    or message.text not in ["Хочу", "Не хочу"],
    content_types=types.message.ContentType.ANY,
    state=Profile.custom,
)(custom_invalid)
