import logging
from datetime import datetime, timezone

from rest_framework.views import APIView


class BaseView(APIView):
    """
    Base view. Implements logging.
    """
    logger: logging.Logger
    action: str

    def log_action(self):
        """
        Logs action, user, time.
        """
        if not self.action:
            raise NotImplementedError("You should provide action name")

        self.logger = getattr(self, "logger", logging.getLogger("files"))

        # user logic is not implemented yet
        user = getattr(self.request, "user", None)
        user_repr = (
            user.username if getattr(user, "is_authenticated", False)
            else "anon"
        )
        self.logger.info(
            f"action={self.action}",
            extra={
                "action": self.action,
                "user": user_repr,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
