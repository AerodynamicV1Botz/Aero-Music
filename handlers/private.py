import asyncio
from time import time
from datetime import datetime
from helpers.filters import command
from config import BOT_NAME as bn, BOT_USERNAME, SUPPORT_GROUP, OWNER_USERNAME
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(command("start") & filters.private & ~filters.group & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_sticker("CAACAgUAAx0CZIiVngACSppiDZZGd6IPFA0TnEuOM3EqFbRxVQACCQMAArU72FSskU3O5FiqcyME")
    await message.reply_photo(
        photo=f"https://telegra.ph/file/053f99956ccee8416b8f7.jpg",
        caption=f"""**━━━━━━━━━━━━━━━━━━
🖤 ʜᴇʏ {message.from_user.mention()} !
       ɪ ᴀᴍ [{bn}](t.me/{BOT_USERNAME}) sᴜᴘᴇʀ ғᴀsᴛ ᴠᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘs...
ᴀʟʟ ᴏꜰ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /
┏━━━━━━━━━━━━━━┓
┣★
┣★ ᴄʀᴇᴀᴛᴏʀ: [𝝙𝗡𝗢𝗡𝗬𝗠𝗢𝗨𝗦](tg://user?id=1356469075)
┣★
┗━━━━━━━━━━━━━━┛

💞 ɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ǫᴜᴇsᴛɪᴏɴs ᴛʜᴇɴ ᴅᴍ ᴛᴏ ᴍʏ [ᴏᴡɴᴇʀ](tg://user?id=1356469075) ʙᴀʙʏ...
━━━━━━━━━━━━━━━━━━**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✗ ᴀᴅᴅ ᴍᴇ ᴇʟsᴇ ʏᴏᴜ ɢᴇʏ​ ✗", url="https://t.me/{BOT_USERNAME}?startgroup=true")
                  ],[
                    InlineKeyboardButton(
                        "✗ ᴅᴇᴠᴇʟᴏᴘᴇʀ ✗", url="https://t.me/{OWNER_USERNAME}"
                    ),
                    InlineKeyboardButton(
                        "✗ sᴜᴘᴘᴏʀᴛ ✗", url="https://t.me/{SUPPORT_GROUP}"
                    )
                ],[ 
                    InlineKeyboardButton(
                        "✗ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ​ ✗", url="https://t.me/DevilsHeavenMF"
                    )]
            ]
       ),
    )

@Client.on_message(command(["ping", "repo", "anon", "alive"]) & filters.group & ~filters.edited & ~filters.private)

async def help(client: Client, message: Message):
    await message.reply_sticker("CAACAgUAAx0CZIiVngACSppiDZZGd6IPFA0TnEuOM3EqFbRxVQACCQMAArU72FSskU3O5FiqcyME")
    await message.reply_text(
        text=f"""» ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ !""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✗ ᴅᴇᴠᴇʟᴏᴘᴇʀ ✗", url="https://t.me/{OWNER_USERNAME}")
                  ],[
                    InlineKeyboardButton(
                        "✗ sᴜᴘᴘᴏʀᴛ ✗", url="https://t.me/{SUPPORT_GROUP}"
                    ),
                    InlineKeyboardButton(
                        "✗ sᴏᴜʀᴄᴇ ✗", url="https://t.me/DevilsHeavenMF"
                    )
                ],[ 
                    InlineKeyboardButton(
                        "✗ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ​​ ✗", url="https://t.me/{BOT_USERNAME}?startgroup=true"
                    )]
            ]
        ),
    )
