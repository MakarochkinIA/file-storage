import pytest
from file_storage.apps.files.services.file_service import FileService


class FakeStorage:
    def __init__(self):
        self.saved = {}
        self.meta = {}

    def save(self, name, content):
        self.saved[name] = content
        self.meta["uid"] = name
        return "fake-uid"

    def get(self, uid):
        return self.saved.get(uid, b"")

    def get_meta(self, uid):
        return self.meta


def test_file_service_save_and_get():
    service = FileService(storage=FakeStorage(), logger=None)

    file_name = "example.txt"
    content = b"example content"

    uid = service.save(file_name, content)
    assert uid == "fake-uid"

    name, data = service.get("fake-uid")
    assert data == content
