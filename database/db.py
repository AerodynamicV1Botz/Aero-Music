from .chat_database import ChatDB
from .sudo_database import SudoDB


class Methods(ChatDB, SudoDB):
    pass


dbs = Methods()
