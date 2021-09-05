from .common import exit_user, help_user

from create_env import dp

from aiogram.dispatcher.filters import Text

exit_user = dp.message_handler(Text(equals="Выход"), state="*")(exit_user)
help_user = dp.message_handler(commands=["help"])(help_user)
