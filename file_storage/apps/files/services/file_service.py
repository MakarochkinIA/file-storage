import logging

from apps.files.storage.base import BaseStorage

from .base import BaseService


class FileService(BaseService):
    """
    Service layer. Handles file upload and download.
    """
    def __init__(self, storage: BaseStorage, logger: logging.Logger):
        self.logger = logger
        self.storage = storage

    def save(self, file_name: str, file: bytes) -> str:
        return self.storage.save(file_name, file)

    def get(self, uid: str) -> tuple[str, bytes]:
        return self.storage.get(uid)
