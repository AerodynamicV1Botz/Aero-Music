import asyncio
from time import time
from helpers.filters import command
from config import BOT_USERNAME, SUPPORT_GROUP
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(command(["ping", "repo", "anon", "alive"]) & filters.group & ~filters.edited & ~filters.private)

async def help(client: Client, message: Message):
    start = time()
    delta_ping = time() - start
    await message.reply_sticker("CAACAgUAAxkBAAEENxZiNtPdibVkMsjLZrUG9NK4hotHQgAC2wEAAoM12VSdN9ujxVtnUyME")
    await message.reply_photo(
        photo="https://telegra.ph/file/89cbc8b8760b6abff430f.jpg",
        caption=f"""<b>🏓 ᴩᴏɴɢ ʙᴀʙʏ !</b>\n`{delta_ping * 1000:.3f} ᴍs`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💖 sᴜᴘᴘᴏʀᴛ 💖", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                    InlineKeyboardButton(
                        "🙄 sᴏᴜʀᴄᴇ 🙄", url="https://github.com/AnonymousBoy1025/FallenMusic"
                    )
                ],[ 
                    InlineKeyboardButton(
                        "🥺 ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ​​ 🥺", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                    )]
            ]
        ),
    )
