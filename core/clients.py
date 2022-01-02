from pytgcalls import PyTgCalls

from configs import config
from pyrogram import Client


user = Client(
    config.SESSION,
    config.API_ID,
    config.API_HASH
)

pyro_bot = Client(
    ":memory:",
    config.API_ID,
    config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins={"root": "plugins"}
)

call_py = PyTgCalls(user)
