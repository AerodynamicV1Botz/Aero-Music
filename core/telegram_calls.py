import asyncio
import datetime

from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from database.lang_utils import gm
from functions.image_editor import generate_queued_image
from .calls import Call


class TelegramPlayer(Call):
    async def insert_to_telegram_playlist(
        self,
        replied,
        chat_id: int,
        user_id: int,
        title: str,
        duration: str,
        source_file: str,
        link: str,
        process_text,
    ):
        data = {
            "user_id": user_id,
            "title": title,
            "duration": duration,
            "source_file": source_file,
            "link": link,
            "stream_type": "local_music",
        }
        self.playlist.insert_one(chat_id, data)
        await process_text.delete()
        queued_image = await generate_queued_image(chat_id)
        mess = await replied.reply_photo(queued_image)
        await asyncio.sleep(5)
        return await mess.delete()

    async def _local_stream(
        self,
        mess: Message,
        user_id: int,
        chat_id: int,
        title: str,
        duration: str,
        source_file: str,
        link: str,
        stream_type: str,
    ):
        call = self.call
        mention = await self.bot.get_user_mention(user_id)
        self.insert_telegram_playlist(
            chat_id, user_id, title, duration, source_file, link, stream_type
        )
        audio_parameters, video_parameters = self.get_quality(chat_id)
        stream = (
            AudioPiped(source_file, audio_parameters)
            if stream_type == "local_music"
            else AudioVideoPiped(source_file, audio_parameters, video_parameters)
        )
        media_stream_type = (
            await gm(chat_id, "stream_type_local_music")
            if stream_type == "local_music"
            else await gm(chat_id, "stream_type_local_video")
        )
        try:
            await call.join_group_call(
                chat_id,
                stream,
                stream_type=StreamType().local_stream,
            )
            return f"""
{await gm(chat_id, 'now_streaming')}
📎 {await gm(chat_id, 'yt_title')}: [{title}]({link})
⏱️ {await gm(chat_id, 'duration')}: {duration}
✨ {await gm(chat_id, 'req_by')}: {mention}
🎥 {await gm(chat_id, 'stream_type_text')}: {media_stream_type}
"""
        except NoActiveGroupCall:
            await self.start_call(chat_id)
            return await self._local_stream(
                mess, user_id, chat_id, title, duration, source_file, link, stream_type
            )
        except FloodWait as e:
            await mess.edit(await gm(chat_id, "flood_wait_error", [str(e.x)]))
            await asyncio.sleep(e.x)
            return await self._local_stream(
                mess, user_id, chat_id, title, duration, source_file, link, stream_type
            )
        except UserNotParticipant:
            await self.join_chat(chat_id)
            return await self._local_stream(
                mess, user_id, chat_id, title, duration, source_file, link, stream_type
            )

    async def stream_from_telegram(self, user_id: int, replied: Message):
        chat_id = replied.chat.id
        playlist = self.playlist.playlists
        process_text = await replied.reply(await gm(chat_id, "process"))
        duration_limit = int((await self.db.get_chat(chat_id))["duration_limit"])
        link = replied.link
        if replied.audio or replied.voice:
            stream_type = "local_music"
            if replied.audio and replied.audio.title:
                title = replied.audio.title[:36]
                duration = replied.audio.duration
                if duration >= duration_limit:
                    return await process_text.edit(
                        await gm(chat_id, "duration_reach_limit", [str(duration)])
                    )
                download = replied.download()
            elif replied.audio and replied.audio.file_name:
                duration = replied.audio.duration
                title = replied.audio.file_name[:36]
                if duration >= duration_limit:
                    return await process_text.edit(
                        await gm(chat_id, "duration_reach_limit", [str(duration)])
                    )
                download = await replied.download()
            elif replied.audio and not (
                replied.audio.file_name and replied.audio.title
            ):
                title = await gm(chat_id, "stream_type_local_music")
                duration = replied.audio.duration
                if duration >= duration_limit:
                    return await process_text.edit(
                        await gm(chat_id, "duration_reach_limit", [str(duration)])
                    )
                download = await replied.download()
            else:
                title = "Voice Note"
                duration = replied.voice.duration
                if duration >= duration_limit:
                    return await process_text.edit(
                        await gm(chat_id, "duration_reach_limit", [str(duration)])
                    )
                download = await replied.download()
            duration = str(datetime.timedelta(seconds=duration))
            if chat_id in playlist and len(playlist[chat_id]) >= 1:
                return await self.insert_to_telegram_playlist(
                    replied,
                    chat_id,
                    user_id,
                    title,
                    duration,
                    download,
                    link,
                    process_text,
                )
            return await self._local_stream(
                process_text,
                user_id,
                chat_id,
                title,
                duration,
                download,
                link,
                stream_type,
            )
        if replied.video or replied.document:
            stream_type = "local_video"
            if replied.video:
                title = replied.video.file_name[:36]
                duration = replied.video.duration
                if duration >= duration_limit:
                    return await process_text.edit(
                        await gm(chat_id, "duration_reach_limit", [str(duration)])
                    )
                source_file = await replied.download()
            else:
                source_file = await replied.download()
                title = replied.document.file_name[:36]
                duration = None
            duration = (
                str(datetime.timedelta(seconds=duration)) if duration else "Not Found"
            )
            if chat_id in playlist and len(playlist[chat_id]) >= 1:
                return await self.insert_to_telegram_playlist(
                    replied,
                    chat_id,
                    user_id,
                    title,
                    duration,
                    source_file,
                    link,
                    process_text,
                )
            return await self._local_stream(
                replied,
                user_id,
                chat_id,
                title,
                duration,
                source_file,
                link,
                stream_type,
            )
