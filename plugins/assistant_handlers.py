from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant

from core.clients import user
from core.bot import bot
from database.lang_utils import gm
from functions.decorators import authorized_only


@Client.on_message(filters.command("userbotjoin"))
@authorized_only
async def userbot_join_(_, m: Message):
    chat_id = m.chat.id
    invite_link = await m.chat.export_invite_link()
    try:
        await user.join_chat(invite_link)
    except UserAlreadyParticipant:
        admin = await m.chat.get_member((await user.get_me()).id)
        if not admin.can_manage_voice_chats:
            return
    await bot.promote_assistant(chat_id)
    return await user.send_message(chat_id, await gm(chat_id, "user_here"))


@Client.on_message(filters.command("userbotleave"))
@authorized_only
async def ubot_leave_(_, m: Message):
    chat_id = m.chat.id
    try:
        await user.leave_chat(chat_id)
        return await bot.send_message(
            chat_id,
            "user_leave_chat"
        )
    except UserNotParticipant:
        return await bot.send_message(
            chat_id,
            "user_already_leave_chat"
        )

__cmds__ = ["userbotjoin", "userbotleave"]
__help__ = {
    "userbotjoin": "help_userbotjoin",
    "userbotleave": "help_userbotleave"
}
