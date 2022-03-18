import aiohttp

from io import BytesIO
from traceback import format_exc

from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.types import Message
from Python_ARQ import ARQ

from helpers.merrors import capture_err
from config import ARQ_API_URL, ARQ_API_KEY

aiohttpsession = ClientSession()
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

async def quotify(messages: list):
    response = await arq.quotly(messages)
    if not response.ok:
        return [False, response.result]
    sticker = response.result
    sticker = BytesIO(sticker)
    sticker.name = "sticker.webp"
    return [True, sticker]


def getArg(message: Message) -> str:
    arg = message.text.strip().split(None, 1)[1].strip()
    return arg


def isArgInt(message: Message) -> bool:
    count = getArg(message)
    try:
        count = int(count)
        return [True, count]
    except ValueError:
        return [False, 0]


@Client.on_message(filters.command(["q", "quote"]))
@capture_err
async def quotly_func(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ sᴏ ᴛʜᴀᴛ ɪ ᴄᴀɴ ǫᴜᴏᴛᴇ ɪᴛ ! 😉")
    if not message.reply_to_message.text:
        return await message.reply_text(
            "ᴅɪᴅɴ'ᴛ ғᴏᴜɴᴅ ᴀɴʏ ᴛᴇxᴛ ɪɴ ᴛʜᴀᴛ ᴍᴇssᴀɢᴇ ! 🥺"
        )
    m = await message.reply_text("`ᴄʀᴇᴀᴛɪɴɢ ᴀ ǫᴜᴏᴛᴇ...`")
    if len(message.command) < 2:
        messages = [message.reply_to_message]

    elif len(message.command) == 2:
        arg = isArgInt(message)
        if arg[0]:
            if arg[1] < 2 or arg[1] > 10:
                return await m.edit("ɴᴜᴍʙᴇʀ ᴍᴜsᴛ ʙᴇ ʙᴇᴛᴡᴇᴇɴ 2-10.")
            count = arg[1]
            messages = await client.get_messages(
                message.chat.id,
                [
                    i
                    for i in range(
                        message.reply_to_message.message_id,
                        message.reply_to_message.message_id + count,
                    )
                ],
                replies=0,
            )
        else:
            if getArg(message) != "r":
                return await m.edit(
                    "Incorrect Argument, Pass **'r'** or **'INT'**, **Example:** `/q 2`"
                )
            reply_message = await client.get_messages(
                message.chat.id,
                message.reply_to_message.message_id,
                replies=1,
            )
            messages = [reply_message]
    else:
        await m.edit(
            "ɪɴᴄᴏʀʀᴇᴄᴛ ɴᴜᴍʙᴇʀ !"
        )
        return
    try:
        sticker = await quotify(messages)
        if not sticker[0]:
            await message.reply_text(sticker[1])
            return await m.delete()
        sticker = sticker[1]
        await message.reply_sticker(sticker)
        await m.delete()
        sticker.close()
    except Exception as e:
        await m.edit(
            "sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴩᴩᴇɴᴇᴅ ᴡʜɪʟᴇ ǫᴜᴏᴛɪɴɢ ᴍᴇssᴀɢᴇs,"
            + " ᴛʜɪs ᴇʀʀᴏʀ ᴜsᴜᴀʟʟʏ ʜᴀᴩᴩᴇɴs ᴡʜᴇɴ ᴛʜᴇʀᴇ's"
            + " ᴍᴇssᴀɢᴇ ᴄᴏɴᴛᴀɪɴɪɴɢ sᴏᴍᴇᴛʜɪɴɢ ᴏᴛʜᴇʀ ᴛʜᴀɴ ᴛᴇxᴛ."
        )
        e = format_exc()
        print(e)
