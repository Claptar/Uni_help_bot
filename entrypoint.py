from create_env import dp
import handlers

import logging

from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)
executor.start_polling(dp, skip_updates=True)
