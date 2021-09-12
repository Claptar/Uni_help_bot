from create_env import bot
from ...states import DeleteMsg

import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from pyrogram import Client, filters

app = Client(
    "kek",
    bot_token=os.environ["TOKEN"],
    api_id=12345,
    api_hash="0123456789abcdef0123456789abcdef",
)


async def initiate(message):
    admins = [int(os.environ["ADMIN_1"]), int(os.environ["ADMIN_2"])]
    await bot.send_chat_action(message.chat.id, "typing")
    if message.chat.id in admins:
        await bot.send_message(
            message.chat.id, "Пришли мне текст сообщения бота для удаления"
        )
    await DeleteMsg.proceed.set()


@app.on_message(filters.text & filters.private)
async def message_delete(message: types.Message, state: FSMContext):
    async for msg in app.search_messages(message.chat.id, query=message.text):
        await bot.send_message(message.chat.id, msg)
    # result2 = await bot.delete_message(message.chat.id, message.forward_from.id)
    # await bot.send_message(
    #     message.chat.id, "Сообщение удалено2" if result2 else "Сообщение не удалено2"
    # )
    await state.finish()


app.run()
