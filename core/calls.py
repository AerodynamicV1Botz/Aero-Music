import asyncio
import random

from pyrogram.errors import (
    UserNotParticipant,
    PeerIdInvalid,
    ChannelPrivate,
    ChatForbidden,
    ChatAdminRequired,
    UserAlreadyParticipant,
)
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.exceptions import GroupCallNotFound
from pytgcalls.types.input_stream import (
    AudioPiped,
    AudioVideoPiped,
)
from pytgcalls.types.input_stream.quality import (
    LowQualityVideo,
    LowQualityAudio,
    MediumQualityVideo,
    MediumQualityAudio,
    HighQualityVideo,
    HighQualityAudio,
)
from pytgcalls.types import (
    Update,
)
from pytgcalls.types.stream import (
    StreamAudioEnded,
)

from functions.youtube_utils import get_audio_direct_link, get_video_direct_link
from .bot import Bot
from .clients import user, call_py
from database.chat_database import ChatDB
from database.sudo_database import SudoDB
from .queue import Playlist


class Methods(ChatDB, SudoDB):
    pass


class Call:
    def __init__(self):
        self.call = call_py
        self.playlist = Playlist()
        self.bot = Bot()
        self.userbot = user
        self.db = Methods()

        @self.call.on_stream_end()
        async def _(_, update: Update):
            if isinstance(update, StreamAudioEnded):
                chat_id = update.chat_id
                await self.is_chat_have_playlist(chat_id)

        @self.call.on_left()
        @self.call.on_kicked()
        @self.call.on_closed_voice_chat()
        async def __(_, chat_id: int):
            return self.playlist.delete_chat(chat_id)

    async def get_quality(self, chat_id: int):
        quality: str = (await self.db.get_chat(chat_id))["quality"]
        if quality == "low":
            audio_quality, video_quality = LowQualityAudio(), LowQualityVideo()
        elif quality == "medium":
            audio_quality, video_quality = MediumQualityAudio(), MediumQualityVideo()
        else:
            audio_quality, video_quality = HighQualityAudio(), HighQualityVideo()
        return audio_quality, video_quality

    def insert_youtube_playlist(
        self,
        chat_id: int,
        user_id: int,
        title: str,
        duration: str,
        yt_url: str,
        yt_id: str,
        stream_type: str,
    ):
        data = {
            "user_id": user_id,
            "title": title,
            "duration": duration,
            "yt_url": yt_url,
            "yt_id": yt_id,
            "stream_type": stream_type,
        }
        return self.playlist.insert_one(chat_id, data)

    def insert_telegram_playlist(
        self,
        chat_id: int,
        user_id: int,
        title: str,
        duration: str,
        source_file: str,
        link: str,
        stream_type: str,
    ):
        data = {
            "user_id": user_id,
            "title": title,
            "duration": duration,
            "source_file": source_file,
            "link": link,
            "stream_type": stream_type,
        }
        return self.playlist.insert_one(chat_id, data)

    @staticmethod
    def is_call_active(chat_id: int):
        try:
            if call_py.get_call(chat_id):
                return True
        except GroupCallNotFound:
            return False

    async def start_call(self, chat_id: int):
        try:
            active = self.is_call_active(chat_id)
            if not active:
                await self.userbot.send(
                    CreateGroupCall(
                        peer=await self.userbot.resolve_peer(chat_id),
                        random_id=random.randint(10000, 999999999),
                    )
                )
                await self.bot.send_message(chat_id, "call_started")
            else:
                pass
        except (ChannelPrivate, ChatForbidden):
            try:
                await self.bot.unban_assistant(chat_id)
                await self.start_call(chat_id)
            except PeerIdInvalid:
                await self.userbot.send_message((await self.bot.get_me()).id, "/start")
                await self.start_call(chat_id)
            except (ChannelPrivate, ChatForbidden):
                self.playlist.delete_chat(chat_id)
                return await self.bot.send_message(chat_id, "user_banned")
        except ChatAdminRequired:
            try:
                await self.bot.promote_assistant(chat_id)
                await self.start_call(chat_id)
            except PeerIdInvalid:
                await self.userbot.send_message((await self.bot.get_me()).id, "/start")
                await self.bot.promote_assistant(chat_id)
                await self.start_call(chat_id)

    async def end_call(self, chat_id: int):
        try:
            call = await self.call.get_call(chat_id)
            await self.userbot.send(DiscardGroupCall(call=call))
            await self.bot.send_message(chat_id, "call_closed")
        except GroupCallNotFound:
            await self.bot.send_message(chat_id, "no_active_group_call")

    async def change_vol(self, chat_id: int, volume: int):
        call = self.call
        active = self.is_call_active(chat_id)
        if active:
            await call.change_volume_call(chat_id, volume)
            return await self.bot.send_message(chat_id, "volume_changed", [str(volume)])
        return await self.bot.send_message(chat_id, "not_in_call")

    async def change_streaming_status(self, chat_id: int, status: str):
        active = self.is_call_active(chat_id)
        if active and status == "pause":
            await call_py.pause_stream(chat_id)
            return await self.bot.send_message(chat_id, "track_paused")
        if active and status == "resume":
            await call_py.resume_stream(chat_id)
            return await self.bot.send_message(chat_id, "track_resumed")
        if not active:
            return await self.bot.send_message(chat_id, "not_in_call")

    async def end_stream(self, chat_id: int, first_name: str):
        active = self.is_call_active(chat_id)
        if active:
            await call_py.leave_group_call(chat_id)
            self.playlist.delete_chat(chat_id)
            return await self.bot.send_message(chat_id, "stream_ended", [first_name])
        return await self.bot.send_message(chat_id, "not_in_call")

    async def _stream_change(
        self, chat_id: int, yt_url: str = None, stream_type: str = None
    ):
        if stream_type == "music":
            url = get_audio_direct_link(yt_url)
            audio_quality, _ = self.get_quality(chat_id)
            await call_py.change_stream(chat_id, AudioPiped(url, audio_quality))
        elif stream_type == "video":
            url = get_video_direct_link(yt_url)
            audio_parameters, video_parameters = self.get_quality(chat_id)
            await call_py.change_stream(
                chat_id, AudioVideoPiped(url, audio_parameters, video_parameters)
            )
        elif stream_type == "local_music":
            audio_quality, _ = self.get_quality(chat_id)
            source = self.playlist.get_queue(chat_id)["source_file"]
            await call_py.change_stream(chat_id, AudioPiped(source, audio_quality))
        elif stream_type == "local_video":
            audio_parameters, video_parameters = self.get_quality(chat_id)
            source = self.playlist.get_queue(chat_id)["source_file"]
            await call_py.change_stream(
                chat_id, AudioVideoPiped(source, audio_parameters, video_parameters)
            )

    async def _change_stream(self, chat_id: int):
        playlist = self.playlist
        playlist.delete_one(chat_id)
        title = playlist.get_queue(chat_id)["title"]
        stream_type = playlist.get_queue(chat_id)["stream_type"]
        if stream_type in ["video", "music"]:
            yt_url = playlist.get_queue(chat_id)["yt_url"]
            await self._stream_change(chat_id, yt_url, stream_type)
        elif stream_type in ["local_video", "local_music"]:
            await self._stream_change(chat_id, stream_type)
        return title

    async def is_chat_have_playlist(self, chat_id: int):
        playlist = self.playlist.playlists
        call = self.call
        if playlist and chat_id in playlist and len(playlist[chat_id]) > 1:
            title = await self._change_stream(chat_id)
            await self.bot.send_message(chat_id, "track_changed", [title])
        elif playlist and chat_id in playlist and len(playlist[chat_id]) == 1:
            self.playlist.delete_chat(chat_id)
            await call.leave_group_call(chat_id)
        else:
            await call.leave_group_call(chat_id)

    async def change_stream(self, chat_id: int):
        playlist = self.playlist.playlists
        if chat_id in playlist and len(playlist[chat_id]) > 1:
            title = await self._change_stream(chat_id)
            return await self.bot.send_message(chat_id, "track_skipped", [title])
        return await self.bot.send_message(
            chat_id,
            "no_playlists",
            markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("▶️ ʀᴇsᴜᴍᴇ", "continue"),
                        InlineKeyboardButton("❌ ᴇɴᴅ", "stopcall"),
                    ]
                ]
            ),
        )

    async def join_chat(self, chat_id: int):
        link = await self.bot.export_chat_invite_link(chat_id)
        try:
            await self.userbot.join_chat(link)
            await self.bot.promote_assistant(chat_id)
        except ChatAdminRequired:
            if chat_id in self.playlist.playlists:
                self.playlist.delete_chat(chat_id)
            return await self.bot.send_message(chat_id, "need_all_permissions")
        except UserAlreadyParticipant:
            pass
        await asyncio.sleep(3)
        await self.bot.revoke_chat_invite_link(chat_id, link)

    def send_playlist(self, chat_id: int):
        playlist = self.playlist.playlists
        if chat_id in playlist:
            current = playlist[chat_id][0]
            queued = playlist[chat_id][1:]
            return current, queued
        return None, None

    async def leave_from_inactive_call(self):
        all_chats_id = []
        async for dialog in self.userbot.iter_dialogs():
            chat_id = dialog.chat.id
            if dialog.chat.type == "supergroup":
                for call in self.call.calls:
                    if hasattr(call, "chat_id"):
                        call_chat_id = int(getattr(call, "chat_id"))
                        all_chats_id.append(
                            call_chat_id
                        ) if call_chat_id not in all_chats_id else None
                        call_status = ""
                        if hasattr(call, "status"):
                            call_status = getattr(call, "status")
                        try:
                            if call_chat_id == chat_id and call_status == "not_playing":
                                await self.userbot.leave_chat(chat_id)
                            elif chat_id not in all_chats_id:
                                await self.userbot.leave_chat(chat_id)
                        except (UserNotParticipant, PeerIdInvalid):
                            pass
                if chat_id not in all_chats_id:
                    try:
                        return await self.userbot.leave_chat(chat_id)
                    except (PeerIdInvalid, UserNotParticipant):
                        pass
