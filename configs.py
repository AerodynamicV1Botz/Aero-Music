from dotenv import load_dotenv
from os.path import exists
from os import getenv, mkdir


class Config:
    None if exists("search") else mkdir("search")
    load_dotenv("local.env") if exists("local.env") else load_dotenv()
    API_ID = int(getenv("API_ID", "0"))
    API_HASH = getenv("API_HASH", "abcd123")
    BOT_TOKEN = getenv("BOT_TOKEN", "1234:abcd")
    SESSION = getenv("SESSION", "session")
    OWNER_ID = int(getenv("OWNER_ID", "7777777"))
    CHANNEL_LINK = getenv("CHANNEL_LINK", "https://t.me/AnonymousSupport")
    GROUP_LINK = getenv("GROUP_LINK", "https://t.me/AnonymousRobotSupport")
    AUTO_LEAVE = int(getenv("AUTO_LEAVE", "15"))
    OWNER_USERNAME = getenv("OWNER_USERNAME", "anonymous_was_bot")


config = Config()
