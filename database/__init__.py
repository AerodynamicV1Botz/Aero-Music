from databases import Database


class InitDB:
    def __init__(self):
        self.db = Database("sqlite:///solid.db")

    async def connect(self):
        return await self.db.connect()

    async def init(self):
        await self.db.execute(
            """
            create table if not exists chat_db
            (
                owner_id integer,
                chat_id integer,
                lang text,
                quality text,
                admin_only boolean,
                gcast_type text,
                del_cmd_mode boolean,
                player_mode boolean,
                duration_limit integer,
                selecting_photo text,
                queued_photo text,
                now_streaming_photo text,
                setting_photo text
            );
            """
        )
        await self.db.execute(
            """
            create table if not exists sudo_db
            (chat_id integer, user_id integer);
            """
        )

    async def disconnect(self):
        return await self.db.disconnect()


init_db = InitDB()
