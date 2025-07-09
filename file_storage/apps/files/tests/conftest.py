import logging
import uuid
from collections import defaultdict

import pytest

from apps.files.services.file_service import FileService
from apps.files.storage.base import ArchiveHandler, BaseStorage, DataHandler
from apps.files.storage.storage import ChunkedStorageHandler

logger = logging.getLogger("files")


# ---------------------------------------------------------------------
# In-memory stubs
# ---------------------------------------------------------------------
class InMemoryDataHandler(DataHandler):
    def __init__(self):
        self._blobs = defaultdict(list)
        self._meta = {}

    def save_many(self, uid: str, data: list[bytes]) -> None:  # noqa: D401
        self._blobs[str(uid)] = data

    def save_meta(self, name: str, parts: int) -> str:  # noqa: D401
        uid = str(uuid.uuid4())
        self._meta[uid] = {"parts": parts, "file_name": name}
        return uid

    def get(self, name: str) -> list[bytes]:  # noqa: D401
        return self._blobs[str(name)]

    def get_meta(self, name: str) -> dict:  # noqa: D401
        return self._meta[str(name)]


class NoopArchive(ArchiveHandler):
    """Skip compression/decompression for speed."""

    def compress(self, content: bytes) -> bytes:
        return content

    def extract(self, content: bytes) -> bytes:
        return content


# ---------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------
@pytest.fixture(scope="session")
def file_service() -> FileService:
    """Session-wide FileService wired to the in-memory handlers."""
    handler = ChunkedStorageHandler(InMemoryDataHandler(), NoopArchive())
    storage = BaseStorage(handler)
    return FileService(storage, logger)


@pytest.fixture()
def api_client(client, file_service, monkeypatch):
    """
    Django test client with the in-memory FileService patched
    into the singleton at ``apps.files.infra.file_service``.
    """
    from apps.files import infra

    monkeypatch.setattr(infra, "file_service", file_service, raising=False)
    return client
