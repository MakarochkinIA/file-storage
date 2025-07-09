import json
from datetime import datetime, timezone

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Json logger to format time and use utf-8.
    """
    def __init__(self, *args, **kwargs):
        self.constant_fields = kwargs.pop("constant_fields", {})
        super().__init__(*args, **kwargs)

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record.update(self.constant_fields)

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=timezone.utc)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()

    def jsonify_log_record(self, log_record):
        """
        Ensures UTF-8 encoding for logs instead of escaped Unicode sequences.
        """
        return json.dumps(log_record, ensure_ascii=False, default=str)
