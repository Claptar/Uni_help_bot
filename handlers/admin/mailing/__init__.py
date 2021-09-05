from .step_handlers import initiate, message_send

from create_env import dp
from ...states import Mailing

initiate = dp.message_handler(commands=["mail"])(initiate)
message_send = dp.message_handler(state=Mailing.mailing)(message_send)
