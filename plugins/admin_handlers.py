from sys import executable
from os import execle, environ

from pyrogram import Client, filters
from pyrogram.types import Message

from configs import config
from core.player import player

from database.lang_utils import gm
from functions.decorators import authorized_only


@Client.on_message(filters.command(["pause", "resume"]))
@authorized_only
async def pause(_, m: Message):
    chat_id = m.chat.id
    status = m.command[1]
    return await player.change_streaming_status(chat_id, status)


@Client.on_message(filters.command("skip"))
@authorized_only
async def skip_(_, m: Message):
    chat_id = m.chat.id
    return await player.change_stream(chat_id)


@Client.on_message(filters.command(["vol", "volume"]))
@authorized_only
async def change_vol_(_, m: Message):
    chat_id = m.chat.id
    volume = int(m.command[1])
    return await player.change_vol(chat_id, volume)


@Client.on_message(filters.command("end"))
@authorized_only
async def end_stream_(_, m: Message):
    chat_id = m.chat.id
    first_name = m.from_user.first_name
    return await player.end_stream(chat_id, first_name)


@Client.on_message(filters.command("restart") & filters.user(config.OWNER_ID))
async def restart_bot_(_, m: Message):
    chat_id = m.chat.id
    msg = await m.reply(await gm(chat_id, "restart_bot"))
    args = [executable, "main.py"]
    await msg.edit(await gm(chat_id, "restarted"))
    execle(executable, *args, environ)  # noqa
    return


__cmds__ = [
    "pause",
    "resume",
    "skip",
    "volume",
    "end",
    "restart"
]
__help__ = {
    "pause": "help_pause",
    "resume": "help_resume",
    "skip": "help_skip",
    "volume": "help_volume",
    "end": "help_end",
    "restart": "help_restart"
}
