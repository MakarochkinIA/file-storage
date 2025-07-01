import logging

from base import BaseService
from file_storage.apps.files.storage.base import (
    BaseStorage
)


class FileService(BaseService):

    def __init__(self, storage: BaseStorage, logger: logging.Logger):
        self.logger = logger
        self.storage = storage

    def save(self, file_name: str, file: bytes) -> str:
        return self.storage.save(file_name, file)

    def get(self, file_name: str) -> bytes:
        return self.storage.get(file_name)
