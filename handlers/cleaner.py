import os
from pyrogram import Client, filters
from pyrogram.types import Message
from helpers.filters import command, other_filters
from helpers.decorators import sudo_users_only, errors

downloads = os.path.realpath("downloads")
raw_files = os.path.realpath("raw_files")

@Client.on_message(command(["erase", "rmd"]) & ~filters.edited)
@errors
@sudo_users_only
async def clear_downloads(_, message: Message):
    ls_dir = os.listdir(downloads)
    if ls_dir:
        for file in os.listdir(downloads):
            os.remove(os.path.join(downloads, file))
        await message.reply_text("**ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ꜰɪʟᴇs ꜰʀᴏᴍ ᴅᴀᴛᴀʙᴀsᴇ ʙᴀʙʏ​**")
    else:
        await message.reply_text("**ɴᴏ ꜰɪʟᴇs ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ᴏɴ ᴅᴀᴛᴀʙᴀsᴇ ʙᴀʙʏ​**")

        
@Client.on_message(command(["rmw", "erase"]) & ~filters.edited)
@errors
@sudo_users_only
async def clear_raw(_, message: Message):
    ls_dir = os.listdir(raw_files)
    if ls_dir:
        for file in os.listdir(raw_files):
            os.remove(os.path.join(raw_files, file))
        await message.reply_text("**ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ʀᴀᴡ ꜰɪʟᴇs**")
    else:
        await message.reply_text("**ɴᴏ ʀᴀᴡ ꜰɪʟᴇs ꜰᴏᴜɴᴅ​**")


@Client.on_message(command(["cleanup"]) & ~filters.edited)
@errors
@sudo_users_only
async def cleanup(_, message: Message):
    pth = os.path.realpath(".")
    ls_dir = os.listdir(pth)
    if ls_dir:
        for dta in os.listdir(pth):
            os.system("rm -rf *.webm *.jpg")
        await message.reply_text("**ᴄʟᴇᴀɴᴇᴅ​**")
    else:
        await message.reply_text("**ᴄʟᴇᴀɴᴇᴅ​**")
