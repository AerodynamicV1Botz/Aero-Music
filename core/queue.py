from typing import Dict, List


class Playlist:
    def __init__(self):
        self.__queue: Dict[int, List[Dict[str, str]]] = {}

    def insert_one(self, chat_id: int, data: Dict[str, str]):
        if chat_id not in self.__queue:
            self.__queue[chat_id] = [data]
        else:
            queue = self.__queue[chat_id]
            queue.extend([data])

    def delete_one(self, chat_id: int):
        return "not_in_queue" if chat_id not in self.__queue else self.__queue[chat_id].pop(0)

    def delete_chat(self, chat_id: int):
        if chat_id not in self.__queue:
            return "not_in_queue"
        del self.__queue[chat_id]

    def get_queue(self, chat_id: int):
        return self.__queue[chat_id][0]

    @property
    def playlists(self):
        return self.__queue


playlist = Playlist()
