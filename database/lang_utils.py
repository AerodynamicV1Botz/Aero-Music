import json
import logging
from os import listdir
from os.path import join, dirname, realpath
from pyrogram import emoji
from .chat_database import chat_db

lang_folder = join(dirname(realpath(__file__)), "lang")
lang_code = ""
lang_lists = []
lang_dict = {}
lang_flags = {
    "en": f"{emoji.FLAG_UNITED_STATES} English",
    "id": f"{emoji.FLAG_INDONESIA} Indonesia",
    "pt": f"{emoji.FLAG_PORTUGAL} Portuguese",
    "hi": f"{emoji.FLAG_INDIA} Hindi"
}

for file in listdir(lang_folder):
    if file.endswith(".json"):
        lang_code = file[:-5]
        lang_lists.append(lang_code)
        lang_dict[lang_code] = json.load(open(join(lang_folder, file), encoding="UTF-8"))


async def gm(chat_id: int, key: str, format_key=None) -> str:
    if format_key is None:
        format_key = [""]
    chat_lang = (await chat_db.get_chat(chat_id))["lang"]
    try:
        return lang_dict[chat_lang][key].format(*format_key)
    except (IndexError, KeyError):
        try:
            logging.warning(" set your language by using /lang command!")
            return lang_dict["en"][key].format(*format_key)
        except KeyError:
            return f"`Error`:\n**can't get lang with key: {key}**"
