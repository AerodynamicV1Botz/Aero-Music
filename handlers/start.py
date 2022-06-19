import asyncio

from helpers.filters import command
from config import BOT_NAME as bn, BOT_USERNAME as bu, SUPPORT_GROUP, OWNER_USERNAME as me, START_IMG
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(command("start") & filters.private & ~filters.group & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{START_IMG}",
        caption=f"""**━━━━━━━━━━━━━━━━━━
💔 Hey {message.from_user.mention()} !

This Is [{bn}](t.me/{bu}), A Super Fast VC Player Bot For Telegram Group VideoChats...

Press /help to see all the commands and how they work!
┏━━━━━━━━━━━━━━┓
┣★
┣★Made By: [AerodynamicV1~🇮🇳](t.me/AerodynamicV1_OFFICIAL)
┣★
┗━━━━━━━━━━━━━━┛

💞 If You Have Any Questions About Me Then DM To My[👑Owner👑](t.me/AerodynamicV1_OFFICIAL).....
━━━━━━━━━━━━━━━━━━**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕Add Me To Your Chat➕", url=f"https://t.me/{bu}?startgroup=true"
                       ),
                  ],[
                    InlineKeyboardButton(
                        "👑ᴏᴡɴᴇʀ👑", url=f"https://t.me/{me}"
                    ),
                    InlineKeyboardButton(
                        "[► ChitChat💬 ◄]", url=f"https://t.me/{SUPPORT_GROUP}"
                    )
                ],[
                    InlineKeyboardButton(
                        "[►Inline🔎◄]", switch_inline_query_current_chat=""
                    ),
                    InlineKeyboardButton(
                        ""[► Help ◄]​", url=f"t.me/Aero_MusicBot?help=help")"
                    )],[
                    InlineKeyboardButton(
                        "New Update Or More✅", url=f"https://t.me/AerodynamicV1_UPDATE"
                       ),
                  ]
            ]
       ),
    )

