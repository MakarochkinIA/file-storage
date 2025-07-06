import logging

from apps.files.services.file_service import FileService
from apps.files.storage.base import BaseStorage
from apps.files.storage.mongo import MongoDataHandler
from apps.files.storage.storage import ChunkedStorageHandler, ZipArchiveHandler

# ─── raw driver → repository --------------------------------------------

mongo_handler = MongoDataHandler()
zip_archive = ZipArchiveHandler()
chunked_handler = ChunkedStorageHandler(mongo_handler, zip_archive)
storage = BaseStorage(chunked_handler)

# ─── service ------------------------------------------------------------

logger = logging.getLogger("files")        # configure in LOGGING
file_service = FileService(storage, logger)

__all__ = ["file_service"]       # public surface
