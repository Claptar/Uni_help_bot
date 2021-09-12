from handlers_utils.activity import get_user_list
from create_env import bot
from ...states import Mailing

import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import TelegramAPIError, BotBlocked


async def initiate(message):
    pers_id = message.chat.id
    admins = [int(os.environ["ADMIN_1"]), int(os.environ["ADMIN_2"])]
    await bot.send_chat_action(message.chat.id, "typing")
    if pers_id in admins:
        await bot.send_message(message.chat.id, "Пришли мне сообщение текст сообщения")
    else:
        await bot.send_message(
            message.chat.id,
            "Боюсь, я не совсем понимаю, о чём ты. \n"
            "Напиши /help, чтобы узнать, что я умею.\n",
        )
    await Mailing.mailing.set()


async def message_send(message: types.Message, state: FSMContext):
    users = get_user_list()
    await state.finish()
    for user in users:
        try:
            await bot.send_message(user, message.text)
        except BotBlocked:
            print(f"Bot was blocked by user with chat_id = {user}")
        except TelegramAPIError:
            print(f"Smth went wrong with user chat_id = {user}")
