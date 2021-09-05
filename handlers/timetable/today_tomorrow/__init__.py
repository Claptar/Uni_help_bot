from .fast_timetable import send_today_tomorrow_schedule
from create_env import dp

from aiogram.dispatcher.filters import Text

send_today_tomorrow_schedule = dp.message_handler(
    Text(equals=["На сегодня", "На завтра"])
)(send_today_tomorrow_schedule)
