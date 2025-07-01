import logging

from file_storage.apps.files.services.file_service import FileService
from file_storage.apps.files.storage.base import (
    BaseStorage, ChunkedStorageHandler
)
from file_storage.apps.files.storage.mongo import MongoDataHandler


# ─── raw driver → repository --------------------------------------------

mongo_handler = MongoDataHandler()
chunked_handler = ChunkedStorageHandler(mongo_handler)
storage = BaseStorage(chunked_handler)

# ─── service ------------------------------------------------------------

logger = logging.getLogger("files")        # configure in LOGGING
file_service = FileService(storage, logger)

__all__ = ["file_service"]       # public surface
