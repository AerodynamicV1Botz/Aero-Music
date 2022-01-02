from . import InitDB
from configs import config
from typing import Dict, List


class ChatDB(InitDB):
    @staticmethod
    def _get(chats: List) -> Dict[str, str]:
        result = {}
        for chat in chats:
            (
                owner_id,
                chat_id,
                lang,
                quality,
                admin_only,
                gcast_type,
                del_cmd,
                player_mode,
                duration_limit,
                selecting_photo,
                queued_photo,
                now_streaming_photo,
                settings_photo
            ) = chat
            admin_mode = bool(admin_only)
            del_cmd_mode = bool(del_cmd)
            player_mode = bool(player_mode)
            result.update(
                {
                    "owner_id": owner_id,
                    "chat_id": chat_id,
                    "lang": lang,
                    "quality": quality,
                    "admin_only": admin_mode,
                    "gcast_type": gcast_type,
                    "del_cmd_mode": del_cmd_mode,
                    "player_mode": player_mode,
                    "duration_limit": duration_limit,
                    "selecting_photo": selecting_photo,
                    "queued_photo": queued_photo,
                    "now_streaming_photo": now_streaming_photo,
                    "settings_photo": settings_photo
                }
            )
        return result

    @staticmethod
    def _get_chats(chats: List) -> List[Dict[str, str]]:
        result = []
        for chat in chats:
            (
                owner_id,
                chat_id,
                lang,
                quality,
                admin_only,
                gcast_type,
                del_cmd,
                player_mode,
                duration_limit,
                selecting_photo,
                queued_photo,
                now_streaming_photo,
                settings_photo
            ) = chat
            admin_mode, del_cmd, player_mode = bool(admin_only), bool(del_cmd), bool(player_mode)
            x = {
                "owner_id": owner_id,
                "chat_id": chat_id,
                "lang": lang,
                "quality": quality,
                "admin_only": admin_mode,
                "gcast_type": gcast_type,
                "del_cmd_mode": del_cmd,
                "player_mode": player_mode,
                "duration_limit": duration_limit,
                "selecting_photo": selecting_photo,
                "queued_photo": queued_photo,
                "now_streaming_photo": now_streaming_photo,
                "settings_photo": settings_photo
            }
            result.append(x.copy())
        return result

    async def get_chat_id(self) -> List[int]:
        results = await self.db.fetch_all("select chat_id from chat_db")
        chat_list = []
        for result in results:
            chat_list.append(result[0])
        return chat_list

    async def get_chat(self, chat_id: int) -> Dict[str, str]:
        results = list(
            await self.db.fetch_all(
                "select * from chat_db where chat_id = :chat_id", {"chat_id": chat_id}
            )
        )
        return self._get(results) if results else {}

    async def add_chat(self, chat_id: int, lang: str = "en"):
        cur = self.db
        x = await self.get_chat(chat_id)
        if not x:
            await cur.execute(
                """
                insert into chat_db values (
                    :owner_id,
                    :chat_id, 
                    :lang, 
                    :quality, 
                    :admin_only, 
                    :gcast_type, 
                    :del_cmd, 
                    :player_mode, 
                    :duration_limit,
                    :selecting_photo,
                    :queued_photo,
                    :now_streaming_photo,
                    :setting_photo
                )
                """,
                {
                    "owner_id": config.OWNER_ID,
                    "chat_id": chat_id,
                    "lang": lang,
                    "quality": "medium",
                    "admin_only": False,
                    "gcast_type": "bot",
                    "del_cmd": True,
                    "player_mode": True,
                    "duration_limit": 0,
                    "selecting_photo": "https://telegra.ph/file/cc8d02e67023005905405.png",
                    "queued_photo": "https://telegra.ph/file/73fbe8adadbd9d061d3e1.png",
                    "now_streaming_photo": "https://telegra.ph/file/3a4d2300271b92787f79f.png",
                    "setting_photo": "https://telegra.ph/file/53b33624eafa208525a27.png"
                },
            )
            return "add_chat_success"
        return "chat_already_added"

    async def del_chat(self, chat_id: int):
        cur = self.db
        x = await self.get_chat(chat_id)
        if x:
            await cur.execute("delete from chat_db where chat_id = ?", (chat_id,))
            return "delete_chat_success"
        return "chat_already_deleted"

    async def set_lang(self, chat_id: int, lang: str):
        chat = await self.get_chat(chat_id)
        if lang == chat["lang"]:
            return "lang_already_used"
        await self.db.execute(
            "update chat_db set lang = :lang where chat_id = :chat_id",
            {"lang": lang, "chat_id": chat_id},
        )
        return "lang_changed"

    async def set_quality(self, chat_id: int, quality: str):
        chat = await self.get_chat(chat_id)
        if quality == chat["quality"]:
            return "quality_already_used"
        await self.db.execute(
            "update chat_db set quality = :quality where chat_id = :chat_id",
            {"quality": quality, "chat_id": chat_id},
        )
        return "quality_changed"
    
    async def set_admin_mode(self, chat_id: int, admin_mode: bool):
        chat = await self.get_chat(chat_id)
        if admin_mode == chat["admin_only"]:
            return "admin_mode_already_used"
        await self.db.execute(
            "update chat_db set admin_only = :admin_only where chat_id = :chat_id",
            {"admin_only": admin_mode, "chat_id": chat_id},
        )
        return "admin_mode_changed"
    
    async def set_gcast_type(self, chat_id: int, gcast_type: str):
        chat = await self.get_chat(chat_id)
        if gcast_type == chat["gcast_type"]:
            return "gcast_type_already_used"
        await self.db.execute(
            "update chat_db set gcast_type = :gcast_type where chat_id = :chat_id",
            {"gcast_type": gcast_type, "chat_id": chat_id},
        )
        return "gcast_type_changed"
    
    async def set_del_cmd_mode(self, chat_id: int, del_cmd_mode: bool):
        chat = await self.get_chat(chat_id)
        if del_cmd_mode == chat["del_cmd_mode"]:
            return "del_cmd_mode_already_used"
        await self.db.execute(
            "update chat_db set del_cmd_mode = :del_cmd where chat_id = :chat_id",
            {"del_cmd": del_cmd_mode, "chat_id": chat_id},
        )
        return "del_cmd_mode_changed"
    
    async def set_player_mode(self, chat_id: int, player_mode: bool):
        chat = await self.get_chat(chat_id)
        if player_mode == chat["player_mode"]:
            return "player_mode_already_used"
        await self.db.execute(
            "update chat_db set player_mode = :player_mode where chat_id = :chat_id",
            {"player_mode": player_mode, "chat_id": chat_id},
        )
        return "player_mode_changed"
    
    async def set_duration_limit(self, chat_id: int, duration_limit: int):
        chat = await self.get_chat(chat_id)
        if duration_limit == chat["duration_limit"]:
            return "duration_limit_already_used"
        await self.db.execute(
            "update chat_db set duration_limit = :duration_limit where chat_id = :chat_id",
            {"duration_limit": duration_limit, "chat_id": chat_id},
        )
        return "duration_limit_changed"

    async def get_stats(self):
        chats = list(await self.db.fetch_all("select * from chat_db"))
        group = pm = 0
        results = self._get_chats(chats)
        for chat in results:
            chat_id = str(chat["chat_id"])
            if chat_id.startswith("-"):
                group += 1
            else:
                pm += 1
        return pm, group


chat_db = ChatDB()
