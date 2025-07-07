import zlib

from .base import ArchiveHandler, DataHandler, StorageTypeError


class ChunkedStorageHandler():
    def __init__(
            self,
            data_handler: DataHandler,
            archive_handler: ArchiveHandler
    ):
        self.data_handler = data_handler
        self.archive_handler = archive_handler
        self.parts = 16

    def _save(self, name: str, content: list[bytes]) -> str:
        uid = self.data_handler.save_meta(name, self.parts)
        self.data_handler.save_many(uid, content)
        return uid

    def split(self, content: bytes, parts: int = None) -> list[bytes]:
        if parts is None:
            parts = self.parts
        if not isinstance(content, bytes):
            raise StorageTypeError
        n = len(content)
        remainder = n % parts
        part = n // parts
        data = []
        for i in range(parts):
            data.append(content[i*part:(i+1)*part])
        if remainder > 0:
            data[-1] += content[-remainder:]
        return data

    def archive(self, content: bytes) -> bytes:
        return self.archive_handler.compress(content)

    def decompress(self, content: bytes) -> bytes:
        return self.archive_handler.extract(content)

    def save(self, name: str, content: bytes) -> str:
        zip_parts = [
            self.archive(item)
            for item in self.split(content, self.parts)
        ]
        return self._save(name, zip_parts)

    def get_chunks(self, name: str) -> list[bytes]:
        return self.data_handler.get(name)

    def merge(self, chunks: list[bytes]) -> bytes:
        return b''.join(chunks)

    def get(self, name: str) -> tuple[str, bytes]:
        meta = self.get_meta(name)
        unzip_chunks = [
            self.decompress(item)
            for item in self.get_chunks(name)
        ]
        return meta.get("file_name"), self.merge(unzip_chunks)

    def get_meta(self, name: str) -> dict:
        return self.data_handler.get_meta(name)

    def exists(self, name: str) -> bool:
        return self.data_handler.exists(name)


class ZipArchiveHandler(ArchiveHandler):
    def compress(self, content: bytes) -> bytes:
        return zlib.compress(content)

    def extract(self, content: bytes) -> bytes:
        return zlib.decompress(content)
