import logging

from .base import BaseService

from apps.files.storage.base import BaseStorage


class FileService(BaseService):

    def __init__(self, storage: BaseStorage, logger: logging.Logger):
        self.logger = logger
        self.storage = storage

    def save(self, file_name: str, file: bytes) -> str:
        return self.storage.save(file_name, file)

    def get(self, uid: str) -> tuple[str, bytes]:
        file_name = self.storage.get_meta(uid)
        return (file_name, self.storage.get(uid))
