import asyncio
from time import time
from datetime import datetime
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(command("start", "fuck") & filters.private & ~filters.group & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_sticker("CAACAgQAAxkBAAEDsTZh4xBVu96tWo0G0CIbn_meSGs6LwACWxcAAqbxcR4yeTJRtPe4UCME")
    await message.reply_photo(
        photo=f"https://telegra.ph/file/053f99956ccee8416b8f7.jpg",
        caption=f"""**━━━━━━━━━━━━━━━━━━
🖤 ʜᴇʏ {},
      ɪ ᴀᴍ sᴜᴘᴇʀ ғᴀsᴛ ᴠᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘs...
ᴀʟʟ ᴏꜰ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /
┏━━━━━━━━━━━━━━┓
┣★ᴄʀᴇᴀᴛᴏʀ: [𝝙𝗡𝗢𝗡𝗬𝗠𝗢𝗨𝗦](t.me/anonymous_was_bot)
┗━━━━━━━━━━━━━━┛

💞 ɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ǫᴜᴇsᴛɪᴏɴs ᴛʜᴇɴ ᴅᴍ ᴛᴏ ᴍʏ [ᴏᴡɴᴇʀ](t.me/anonymous_was_bot) ʙᴀʙʏ...
━━━━━━━━━━━━━━━━━━**""".format(
      message.from_user.mention ),
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✗ ᴀᴅᴅ ᴍᴇ ᴇʟsᴇ ʏᴏᴜ ɢᴇʏ​ ✗", url="https://t.me/fallen_music_bot?startgroup=true")
                  ],[
                    InlineKeyboardButton(
                        "✗ ᴄʀᴇᴀᴛᴏʀ ✗", url="https://t.me/anonymous_was_bot"
                    ),
                    InlineKeyboardButton(
                        "✗ sᴜᴘᴘᴏʀᴛ ✗", url="https://t.me/DevilsHeavenMF"
                    )
                ],[ 
                    InlineKeyboardButton(
                        "✗ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ​ ✗", url="https://t.me/DevilsHeavenMF"
                    )]
            ]
       ),
    )

@Client.on_message(command(["ping"]) & filters.group & ~filters.edited & ~filters.private)

async def help(client: Client, message: Message):
    await message.reply_sticker("CAACAgQAAxkBAAEDsTZh4xBVu96tWo0G0CIbn_meSGs6LwACWxcAAqbxcR4yeTJRtPe4UCME")
    await message.reply_text(
        text=f"""ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ !🖤""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✗ 𝝙𝗡𝗢𝗡𝗬𝗠𝗢𝗨𝗦 ✗", url=f"https://t.me/anonymous_was_bot")
                ]
            ]
        ),
    )
