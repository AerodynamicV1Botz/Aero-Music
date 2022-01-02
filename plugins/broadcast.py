import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
from configs import config
from core.bot import bot
from core.clients import user
from database.lang_utils import gm
from database.db import dbs


@Client.on_message(filters.command("gcast"))
async def gcast_(client: Client, m: Message):
    if m.reply_to_message:
        text = m.reply_to_message.text
    else:
        text = m.text[7:]
    chat_id = m.chat.id
    from_user_id = m.from_user.id
    if from_user_id != config.OWNER_ID:
        return await bot.send_message(chat_id, "you_not_owner")
    msg = await m.reply(await gm(chat_id, "process_gcast"))
    error = success = 0
    gcast_type = (await dbs.get_chat(chat_id))["gcast_type"]
    sender = user if gcast_type == "user" else client
    chat_lists = await dbs.get_chat_id()
    for chat in chat_lists:
        chat_ids = str(chat)
        if chat_ids.startswith("-"):
            try:
                success += 1
                await asyncio.sleep(2.5)
                await sender.send_message(int(chat_ids), text)
            except Exception as e:  # noqa
                print(e)
                error += 1
    return await msg.edit(
        await gm(chat_id, "success_gcast", [str(success), str(error)])
    )


@Client.on_message(filters.command("setgcast"))
async def set_gcast_(_, message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id != config.OWNER_ID:
        return await bot.send_message(chat_id, "you_not_owner")
    try:
        gcast_type = message.command[1]
    except IndexError:
        return await message.reply("Give me an input")
    if gcast_type not in ["bot", "user"]:
        return await message.reply(await gm(chat_id, "invalid_gcast_type"))
    key = await dbs.set_gcast_type(chat_id, gcast_type)
    return await bot.send_message(chat_id, key, [gcast_type])


__cmds__ = ["gcast", "setgcast"]
__help__ = {
    "gcast": "help_gcast",
    "setgcast": "help_setgcast"
}
