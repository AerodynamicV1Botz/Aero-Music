import os

import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageFont

from core.queue import playlist
from database.db import dbs
from database.lang_utils import gm


async def generate_now_streaming_image(
    chat_id: int,
    duration: str,
    youtube_image_url: str,
    youtube_title: str,
    chat_title: str,
):
    chat_title = chat_title[:21]
    now_streaming_image_url = (await dbs.get_chat(chat_id))["now_streaming_photo"]
    background_image_location = f"search/now_streaming_{chat_id}.png"
    yt_image_location = f"search/youtube_now_streaming_{chat_id}.png"
    temp_image_location = f"search/temp_streaming_{chat_id}.png"
    async with aiohttp.ClientSession() as session, session.get(
        now_streaming_image_url
    ) as res1, session.get(youtube_image_url) as res2:
        if res1.status == 200:
            f = await aiofiles.open(background_image_location, mode="wb")
            await f.write(await res1.read())
            await f.close()
        if res2.status == 200:
            f = await aiofiles.open(yt_image_location, mode="wb")
            await f.write(await res2.read())
            await f.close()
        await session.close()
    background_image = (
        (Image.open(background_image_location)).resize((1270, 720))
    ).convert("RGBA")
    youtube_image = ((Image.open(yt_image_location)).resize((1270, 720))).convert(
        "RGBA"
    )
    Image.alpha_composite(youtube_image, background_image).save(temp_image_location)
    temp_image = Image.open(temp_image_location)
    draw = ImageDraw.Draw(temp_image).text
    image_font = ImageFont.truetype("fonts/bg_font.ttf", 40)
    draw((10, 14), chat_title, (255, 255, 255), font=image_font)
    now_playing_text = await gm(chat_id, "now_streaming")
    duration_text = await gm(chat_id, "duration")
    draw((22, 500), now_playing_text, (255, 255, 255), font=image_font)
    draw((21, 550), youtube_title, (255, 255, 255), font=image_font)
    draw((21, 650), f"{duration_text}: {duration}", (255, 255, 255), font=image_font)
    temp_image.save(f"search/final_streaming_{chat_id}.png")
    os.remove(temp_image_location)
    os.remove(yt_image_location)
    os.remove(background_image_location)
    return f"search/final_streaming_{chat_title}.png"


async def generate_queued_image(
    chat_id: int,
):
    position = len(playlist.playlists[chat_id])
    queued_text = await gm(chat_id, "track_queued", [str(position)])
    queued_image_url = (await dbs.get_chat(chat_id))["queued_photo"]
    queued_image_location = f"search/queued_image_{chat_id}.png"
    async with aiohttp.ClientSession() as session, session.get(queued_image_url) as res:
        if res.status == 200:
            f = await aiofiles.open(queued_image_location, mode="wb")
            await f.write(await res.read())
            await f.close()
        await session.close()
    font = ImageFont.truetype("fonts/bg_font.ttf", 50)
    queued_image = ((Image.open(queued_image_location)).resize((1270, 720))).convert(
        "RGBA"
    )
    draw = ImageDraw.Draw(queued_image).text
    draw((350, 330), f"{queued_text}", (255, 255, 255), font=font)
    queued_image.save(queued_image_location)
    return queued_image_location
