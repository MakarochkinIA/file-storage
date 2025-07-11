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


class DataHandler(ABC):
    """Raw read/write to one blob by name."""

    @abstractmethod
    def save_many(self, uid: str, data: list[bytes]) -> None:
        pass

    @abstractmethod
    def save_meta(self, uid: str, parts: int) -> str:
        pass

    @abstractmethod
    def get(self, name: str) -> list[bytes]:
        pass

    @abstractmethod
    def get_meta(self, name: str) -> dict:
        pass


class ArchiveHandler(ABC):
    """Compress/decompress content."""
    @abstractmethod
    def extract(self, content: bytes) -> bytes:
        pass

    @abstractmethod
    def compress(self, content: bytes) -> bytes:
        pass


class StorageHandler(ABC):
    """Save/download files."""

    @abstractmethod
    def save(self, name: str, content: bytes) -> str:
        pass

    @abstractmethod
    def get(self, name: str) -> bytes:
        pass


class BaseStorage(StorageBackend):
    """Save/download files."""

    def __init__(self, storage_handler: StorageHandler):
        self.storage = storage_handler

    def save(self, name: str, content: bytes) -> str:
        uid = self.storage.save(name, content)
        return uid

    def get(self, name: str) -> tuple[str, bytes]:
        file_name, file = self.storage.get(name)
        return file_name, file
