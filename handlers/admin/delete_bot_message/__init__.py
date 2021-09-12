from .step_handlers import initiate, message_delete

from create_env import dp
from ...states import DeleteMsg

initiate = dp.message_handler(commands=["delmsg"])(initiate)
message_delete = dp.message_handler(state=DeleteMsg.proceed)(message_delete)
