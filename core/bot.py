import asyncio

from pyrogram.errors import PeerIdInvalid
from pyrogram.types import InlineKeyboardMarkup

from database.lang_utils import gm
from .clients import pyro_bot, user
from typing import List


class Bot:
    def __init__(self):
        self._bot = pyro_bot
        self._user = user

    async def start(self):
        return await self._bot.start()

    async def stop(self):
        return await self._bot.stop()

    async def export_chat_invite_link(self, chat_id: int):
        return (await self._bot.export_chat_invite_link(chat_id)).invite_link

    async def promote_assistant(self, chat_id: int):
        user_id = (await self._user.get_me()).id
        return await self._bot.promote_chat_member(
            chat_id, user_id, can_manage_voice_chats=True
        )

    async def unban_assistant(self, chat_id: int):
        user_id = (await self._user.get_me()).id
        return await self._bot.unban_chat_member(chat_id, user_id)

    async def send_message(
        self,
        chat_id: int,
        key: str,
        format_key: List[str] = None,
        media_type: str = None,
        media_file: str = None,
        markup: InlineKeyboardMarkup = None,
        delete: int = 10,
    ):
        text = await gm(chat_id, key, format_key)
        if media_type == "photo" and media_file:
            msg = await self._bot.send_photo(
                chat_id, media_file, caption=text, reply_markup=markup
            )
        elif media_type == "video" and media_file:
            msg = await self._bot.send_video(
                chat_id, media_file, caption=text, reply_markup=markup
            )
        else:
            msg = await self._bot.send_message(
                chat_id, text, reply_markup=markup, disable_web_page_preview=True
            )
        if delete:
            await asyncio.sleep(delete)
            return await msg.delete()
        return msg

    async def get_me(self):
        return await self._bot.get_me()

    async def revoke_chat_invite_link(self, chat_id: int, link: str):
        return await self._bot.revoke_chat_invite_link(chat_id, link)

    async def get_user_mention(self, user_id: int):
        try:
            return (await self._bot.get_users(user_id)).mention
        except PeerIdInvalid:
            await self._user.send_message((await self.get_me()).id, "/start")
            return await self.get_user_mention(user_id)


bot = Bot()
