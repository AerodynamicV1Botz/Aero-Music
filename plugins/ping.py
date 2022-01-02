from time import time

from pyrogram import Client, filters
from pyrogram.types import Message

from core.clients import call_py
from database.lang_utils import gm


@Client.on_message(filters.command("ping"))
async def check_ping_(_, message: Message):
    chat_id = message.chat.id
    start = time()
    msg = await message.reply(await gm(chat_id, "ping_text"))
    pytgcalls_latency = await call_py.ping
    pyrogram_latency = time() - start
    await msg.edit(
        await gm(
            chat_id,
            "pong_text",
            [str(round(pyrogram_latency * 1000, 3)), str(round(pytgcalls_latency, 2))]
        )
    )


__cmds__ = ["ping"]
__help__ = {
    "ping": "help_ping"
}
