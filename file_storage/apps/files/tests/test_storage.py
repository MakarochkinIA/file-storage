import pytest
from file_storage.apps.files.storage.storage import ChunkedStorageHandler


class FakeMongo:
    def __init__(self):
        self.meta = {}
        self.data = []

    def save_meta(self, name, parts):
        self.meta[name] = parts
        return "mock-id"

    def save_many(self, uid, chunks):
        self.data = chunks

    def get(self, uid):
        return self.data

    def get_meta(self, uid):
        return {"file_name": "abc", "parts": len(self.data)}


class FakeArchive:
    def compress(self, content):
        return content[::-1]

    def extract(self, content):
        return content[::-1]


def test_storage_chunk_archive_logic():
    storage = ChunkedStorageHandler(data_handler=FakeMongo(), archive_handler=FakeArchive())
    content = b"abcdefgh12345678"
    uid = storage.save("test.txt", content)

    assert uid == "mock-id"
    retrieved = storage.get(uid)
    assert retrieved == content
