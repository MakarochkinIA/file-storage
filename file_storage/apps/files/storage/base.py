from abc import ABC, abstractmethod


class StorageError(Exception):
    pass


class StorageIOError(StorageError):
    pass


class StorageFileNotFound(StorageError):
    pass


class StorageTypeError(StorageError):
    pass


class StorageBackend(ABC):
    @abstractmethod
    def save(self, name: str, content: bytes) -> str:
        """Save content and return its uid."""
        pass

    @abstractmethod
    def get(self, name: str) -> bytes:
        """Get file by name."""
        pass

    @abstractmethod
    def delete(self, name: str):
        """Delete the file by name/path."""
        pass

    @abstractmethod
    def exists(self, name: str) -> bool:
        """Check if a file exists."""
        pass


class DataHandler(ABC):
    """Raw read/write to one blob by name."""

    @abstractmethod
    def save(self, name: str, data: bytes) -> None:
        pass

    @abstractmethod
    def get(self, name: str) -> bytes:
        pass

    @abstractmethod
    def delete(self, name: str) -> None:
        pass

    @abstractmethod
    def exists(self, name: str) -> bool:
        pass


class BaseStorage(StorageBackend):
    def __init__(self, storage_handler):
        self.storage = storage_handler

    def save(self, name: str, content: bytes) -> str:
        uid = self.storage.save(name, content)
        return uid

    def get(self, name: str) -> bytes:
        file = self.storage.get(name)
        return file

    def delete(self, name: str) -> bytes:
        file = self.storage.delete(name)
        return file


class ChunkedStorageHandler():
    def __init__(self, data_handler: DataHandler):
        self.data_handler = data_handler
        self.parts = 16

    def _save(self, name: str, content: list[bytes]) -> str:
        uid = self.data_handler.save_meta(name, self.parts)
        self.data_handler.save_many(uid, content)
        return uid

    def split(self, content: bytes, parts: int) -> list[bytes]:
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

    def save(self, name: str, content: bytes) -> str:
        parts = self.split(content)
        return self._save(name, parts)

    def get_chunks(self, name: str) -> list[bytes]:
        return self.data_handler.get(name)

    def merge(self, chunks: list[bytes]) -> bytes:
        return b''.join(chunks)

    def get(self, name: str) -> bytes:
        chunks = self.get_chunks(name)
        return self.merge(chunks)

    def exists(self, name: str) -> bool:
        return self.data_handler.exists(name)
