import sys
from os import mkdir
from os.path import exists
from shutil import rmtree

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import idle
from pytz import utc

from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import CallbackQuery, Message

from .telegram_calls import TelegramPlayer
from .youtube_call import YoutubePlayer
from . import bot_username

from configs import config

scheduler = AsyncIOScheduler()


class MediaPlayer(TelegramPlayer, YoutubePlayer):
    async def start_stream(
        self,
        user_id: int,
        title: str,
        duration: str,
        replied: Message = None,
        yt_url: str = None,
        yt_id: str = None,
        cb: CallbackQuery = None,
        stream_type: str = None
    ):
        if stream_type == "music" and cb:
            return await self.start_yt_stream(
                cb, user_id, title, duration, yt_url, yt_id, stream_type
            )
        if stream_type == "video" and cb:
            return await self.start_yt_stream(
                cb, user_id, title, duration, yt_url, yt_id, stream_type
            )
        if stream_type in ["local_music", "local_video"] and replied:
            return await self.stream_from_telegram(
                user_id, replied
            )

    async def run(self):
        if not exists("search"):
            mkdir("search")
        await self.db.connect()
        await self.db.init()
        print("[ INFO ] STARTING BOT CLIENT")
        await self.bot.start()
        print("[ INFO ] GETTING BOT USERNAME")
        await self.get_bot_username()
        print(f"[ INFO ] GOT BOT USERNAME: {bot_username}")
        print("[ INFO ] STARTING PyTgCalls CLIENT")
        await self.call.start()
        await self.join_channel()
        if config.AUTO_LEAVE:
            print("[ INFO ] STARTING SCHEDULER")
            scheduler.configure(timezone=utc)
            scheduler.add_job(
                self.leave_from_inactive_call, "interval", minutes=config.AUTO_LEAVE
            )
            pass
        print("[ INFO ] CLIENT RUNNING")
        await idle()
        print("[ INFO ] STOPPING BOT")
        await self.db.disconnect()
        if exists("search"):
            rmtree("search")
        if exists("downloads"):
            rmtree("downloads")
        await self.bot.stop()
        sys.exit()

    async def get_bot_username(self):
        global bot_username
        username = (await self.bot.get_me()).username
        bot_username += username

    async def join_channel(self):
        try:
            await self.userbot.join_chat("solidprojects")
        except UserAlreadyParticipant:
            pass


player = MediaPlayer()
