import re
import sys
import time
from config import (API_ID, API_HASH, BOT_TOKEN)

from pyrogram import Client

StartTime = time.time()

app = Client(
    "FallenMusic",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
)

