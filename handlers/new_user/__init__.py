from .step_handlers import custom_proceed, group_proceed, initiate
from .error_handlers import custom_invalid_variant, group_invalid_format

from create_env import dp
from ..states import Start

from aiogram import types
from aiogram.dispatcher.filters import Text

initiate = dp.message_handler(commands="start")(initiate)

group_proceed = dp.message_handler(state=Start.group)(group_proceed)
group_invalid_format = dp.message_handler(
    lambda message: message.content_type != types.message.ContentType.TEXT,
    content_types=types.message.ContentType.ANY,
    state=Start.group,
)(group_invalid_format)

custom_proceed = dp.message_handler(
    Text(equals=["Хочу", "Не хочу"]), state=Start.custom
)(custom_proceed)
custom_invalid_variant = dp.message_handler(
    lambda message: message.content_type != types.message.ContentType.TEXT
    or message.text not in ["Хочу", "Не хочу"],
    content_types=types.message.ContentType.ANY,
    state=Start.custom,
)(custom_invalid_variant)
