from .step_handlers import (
    initiate,
    period_proceed,
    number_of_unique_users,
    function_usage_frequencies,
)

from create_env import dp
from ...states import Stat

from aiogram.dispatcher.filters import Text

initiate = dp.message_handler(commands=["stat"])(initiate)
period_proceed = dp.message_handler(Text(equals="Unique"), state=Stat.choice)(
    period_proceed
)
number_of_unique_users = dp.message_handler(state=Stat.unique)(number_of_unique_users)
function_usage_frequencies = dp.message_handler(
    Text(equals="Frequency"), state=Stat.choice
)(function_usage_frequencies)
