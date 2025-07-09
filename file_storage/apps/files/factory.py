import logging

from django.conf import settings

from apps.files.services.file_service import FileService
from apps.files.storage.base import BaseStorage
from apps.files.storage.mongo import MongoDataHandler
from apps.files.storage.storage import ChunkedStorageHandler, ZipArchiveHandler

logger = logging.getLogger("files")


def build_file_service() -> FileService:
    """
    File service builder.
    """
    data_handler = MongoDataHandler(settings.MONGO_DB_HOST)
    archive_handler = ZipArchiveHandler()

    storage_handler = ChunkedStorageHandler(
        data_handler, archive_handler,
    )
    storage = BaseStorage(storage_handler)

    return FileService(storage, logger)
