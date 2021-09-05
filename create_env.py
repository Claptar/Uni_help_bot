import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = os.environ["TOKEN"]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
