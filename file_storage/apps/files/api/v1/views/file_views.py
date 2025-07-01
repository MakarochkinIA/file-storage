from rest_framework.views import APIView
import logging

from file_storage.apps.files.infra import file_service


logger = logging.getLogger(__name__)


class FileView(APIView):
    service = file_service

    def post(self, request):
        pass
