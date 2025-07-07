from django.apps import AppConfig
from .factory import build_file_service


class FilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.files'

    def ready(self):  # called once Django registry is ready
        from apps.files import infra  # local import to avoid early evaluation

        # Build the concrete service *now* – settings are frozen; tests may
        # have patched them.
        infra.file_service = build_file_service()
