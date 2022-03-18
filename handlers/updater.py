import sys
import os
import heroku3
import traceback

from pyrogram import Client, filters
from pyrogram.types import Message, Dialog, Chat

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from config import UPSTREAM_REPO, REPO_BRANCH
REPO_ = UPSTREAM_REPO
BRANCH_ = U_BRANCH

@Client.on_message(command("update") & filters.user)
@sudo_users_only
async def updatebot(_, message: Message):
    msg = await message.reply_text("`Updating Module is Starting! Please Wait...`")
    try:
        repo = Repo()
    except GitCommandError:
        return await msg.edit(
            "`Invalid Git Command!`"
        )
    except InvalidGitRepositoryError:
        repo = Repo.init()
        if "upstream" in repo.remotes:
            origin = repo.remote("upstream")
        else:
            origin = repo.create_remote("upstream", REPO_)
        origin.fetch()
        repo.create_head(U_BRANCH, origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    if repo.active_branch.name != U_BRANCH:
        return await msg.edit(
            f"ʜᴍᴍ... sᴇᴇᴍs ʟɪᴋᴇ ʏᴏᴜ ᴀʀᴇ ᴜsɪɴɢ ᴄᴜsᴛᴏᴍ ʙʀᴀɴᴄʜ ɴᴀᴍᴇᴅ `{repo.active_branch.name}`! ᴄʀᴇᴀᴛᴇ `{U_BRANCH}` ᴛᴏ ᴍᴀᴋᴇ ᴛʜɪs ᴡᴏʀᴋ !"
        )
    try:
        repo.create_remote("upstream", REPO_)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(U_BRANCH)
    if not HEROKU_URL:
        try:
            ups_rem.pull(U_BRANCH)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await run_cmd("pip3 install --no-cache-dir -r requirements.txt")
        await msg.edit("**Successfully Updated! Restarting Now!**")
        args = [sys.executable, "main.py"]
        execle(sys.executable, *args, environ)
        exit()
        return
    else:
        await msg.edit("`Heroku Detected!`")
        await msg.edit("`Updating and Restarting has Started! Please wait for 5-10 Minutes!`")
        ups_rem.fetch(U_BRANCH)
        repo.git.reset("--hard", "FETCH_HEAD")
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(HEROKU_URL)
        else:
            remote = repo.create_remote("heroku", HEROKU_URL)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except BaseException as error:
            await msg.edit(f"**Updater Error** \nTraceBack : `{error}`")
            return repo.__del__()

