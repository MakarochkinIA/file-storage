import logging
from datetime import datetime, timezone

from rest_framework.views import APIView


class BaseView(APIView):
    logger: logging.Logger
    action: str

    def log_action(self):
        if not self.action:
            raise NotImplementedError("You should provide action name")

        self.logger = getattr(self, "logger", logging.getLogger("files"))

        self.logger.info(
            f"action={self.action}",
            extra={
                "action": self.action,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
