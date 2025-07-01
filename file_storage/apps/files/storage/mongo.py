import uuid
import datetime

from pymongo import MongoClient, InsertOne

from django.conf import settings

from base import DataHandler, StorageFileNotFound
from const import (
    MONGO_DB_NAME,
    MONGO_CHUNKS_NAME,
    MONGO_FILES_NAME
)


class MongoDataHandler(DataHandler):

    def __init__(self):
        self.host = settings.MONGO_DB_HOST
        self.client = MongoClient(self.host)
        self.db = self.client[MONGO_DB_NAME]
        self.files = self.db[MONGO_FILES_NAME]
        self.chunks = self.db[MONGO_CHUNKS_NAME]

    def save_many(self, uid: str, content: list[bytes]) -> None:
        ops = [
            InsertOne(
                {
                    "file_id": uid,
                    "data": data,
                    "idx":  index,
                }
            ) for index, data in enumerate(content)
        ]
        self.chunks.bulk_write(ops, ordered=False)

    def save_meta(self, name: str, parts: int) -> str:
        time = datetime.datetime.now(datetime.timezone.utc)
        uid = str(uuid.uuid4())
        self.files.insert_one({
            "_id": uid,
            "time": time,
            "file_name": name,
            "parts": parts,
        })
        return uid

    def get(self, uid: str) -> list[bytes]:
        meta = self.files.find_one({"_id": uid})
        if not meta:
            raise StorageFileNotFound(f"{uid} not found")
        cur = (
            self.chunks.find({"file_id": uid})
            .sort("idx", 1)
        )
        return [doc["data"] for doc in cur]
