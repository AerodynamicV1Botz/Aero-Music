import asyncio
from functions.image_editor import (
    generate_now_streaming_image,
    generate_queued_image
)

from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, CallbackQuery
from pytgcalls import StreamType
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped

from database.lang_utils import gm
from functions.youtube_utils import get_audio_direct_link, get_video_direct_link
from .calls import Call


class YoutubePlayer(Call):
    async def _youtube_player(
        self,
        mess: Message,
        chat_id: int,
        user_id: int,
        media_url: str,
        title: str,
        duration: str,
        yt_url: str,
        yt_id: str,
        stream_type: str,
    ):
        chat_title = mess.chat.title
        bot_username = (await self.bot.get_me()).username
        mention = await self.bot.get_user_mention(user_id)
        call = self.call
        playlist = self.playlist.playlists
        if not playlist or (playlist and chat_id not in playlist):
            self.insert_youtube_playlist(
                chat_id, user_id, title, duration, yt_url, yt_id, stream_type
            )
        audio_parameters, video_parameters = await self.get_quality(chat_id)
        stream = (
            AudioPiped(media_url, audio_parameters)
            if stream_type == "music"
            else AudioVideoPiped(media_url, audio_parameters, video_parameters)
        )
        media_stream_type = (
            await gm(chat_id, "stream_type_music")
            if stream_type == "music"
            else await gm(chat_id, "stream_type_video")
        )
        try:
            await call.join_group_call(
                chat_id,
                stream,
                stream_type=StreamType().local_stream,
            )
            await mess.delete()
            now_streaming_photo = await generate_now_streaming_image(
                chat_id, duration, media_url, title, chat_title
            )
            caption = f"""
{await gm(chat_id, 'now_streaming')}
📌 {await gm(chat_id, 'yt_title')}: [{title}](https://t.me/{bot_username}?start=ytinfo_{yt_id})
⏱️ {await gm(chat_id, 'duration')}: {duration} 
✨ {await gm(chat_id, 'req_by')}: {mention}
🎥 {await gm(chat_id, 'stream_type_title')}: {media_stream_type}
"""
            await mess.reply_photo(
                now_streaming_photo,
                caption=caption,
            )
        except NoActiveGroupCall:
            await self.start_call(chat_id)
            return await self._youtube_player(
                mess,
                chat_id,
                user_id,
                media_url,
                title,
                duration,
                yt_url,
                yt_id,
                stream_type,
            )
        except FloodWait as e:
            await mess.edit(await gm(chat_id, "flood_wait_error", [str(e.x)]))
            await asyncio.sleep(e.x)
            return await self._youtube_player(
                mess,
                chat_id,
                user_id,
                media_url,
                title,
                duration,
                yt_url,
                yt_id,
                stream_type,
            )
        except UserNotParticipant:
            await self.join_chat(chat_id)
            return await self._youtube_player(
                mess,
                chat_id,
                user_id,
                media_url,
                title,
                duration,
                yt_url,
                yt_id,
                stream_type,
            )

    async def start_yt_stream(
        self,
        cb: CallbackQuery,
        user_id: int,
        title: str,
        duration: str,
        yt_url: str,
        yt_id: str,
        stream_type: str,
    ):
        playlist = self.playlist.playlists
        chat_id = cb.message.chat.id
        await self.bot.get_user_mention(user_id)
        if playlist and chat_id in playlist and len(playlist[chat_id]) >= 1:
            self.insert_youtube_playlist(
                chat_id, user_id, title, duration, yt_url, yt_id, stream_type
            )
            await cb.message.delete()
            queued_image = await generate_queued_image(chat_id)
            mess = await cb.message.reply_photo(
                queued_image,
            )
            await asyncio.sleep(5)
            return await mess.delete()
        media_url = (
            get_audio_direct_link(yt_url)
            if stream_type == "music"
            else get_video_direct_link(yt_url)
        )
        mess = await cb.message.edit(await gm(chat_id, "process"))
        return await self._youtube_player(
            mess,
            chat_id,
            user_id,
            media_url,
            title,
            duration,
            yt_url,
            yt_id,
            stream_type,
        )
