from django.apps import AppConfig

from .factory import build_file_service


class FilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.files'

    def ready(self):
        """
        Build File service for views to import and use.
        """
        from apps.files import infra

        infra.file_service = build_file_service()
