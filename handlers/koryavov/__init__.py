from .error_handlers import finish_invalid, semester_number_invalid, task_number_invalid
from .step_handlers import (
    initiate,
    semester_number_proceed,
    task_number_proceed,
    finish_proceed,
)

from create_env import dp
from ..states import Koryavov
from handlers_utils.math_module import math_part

from aiogram.dispatcher.filters import Text

initiate = dp.message_handler(commands="koryavov")(initiate)

semester_number_proceed = dp.message_handler(
    lambda message: message.text.isdigit(), state=Koryavov.sem_num_state
)(semester_number_proceed)
semester_number_invalid = dp.message_handler(state=Koryavov.sem_num_state)(
    semester_number_invalid
)

task_number_proceed = dp.message_handler(
    lambda message: math_part.is_digit(message.text) or message.text == "Ещё одну",
    state=Koryavov.task_num_state,
)(task_number_proceed)
task_number_invalid = dp.message_handler(state=Koryavov.task_num_state)(
    task_number_invalid
)

finish_proceed = dp.message_handler(
    Text(equals=["Ещё одну", "Всё, хватит"]),
    state=Koryavov.finish_state,
)(finish_proceed)
finish_invalid = dp.message_handler(state=Koryavov.finish_state)(finish_invalid)
