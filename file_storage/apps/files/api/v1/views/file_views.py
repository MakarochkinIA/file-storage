import io
import logging

from django.http import FileResponse
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   OpenApiResponse, extend_schema)
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from apps.files.infra import file_service
from apps.files.storage.base import StorageError, StorageFileNotFound

from ..serializers.file_serializer import FileUploadSerializer
from .base import BaseView

logger = logging.getLogger("files")


class FileUploadView(BaseView):
    """
    POST /files/upload/
    """
    parser_classes = [MultiPartParser]
    serializer_class = FileUploadSerializer
    service = file_service
    action = "upload"
    logger = logger

    @extend_schema(
        summary="Upload a file",
        description=(
            "Upload a file up to 16MB. "
            "File will be split into 16 zipped parts and stored."
        ),
        request=FileUploadSerializer,
        responses={
            201: OpenApiResponse(
                description="File successfully uploaded", response=None
            ),
            400: OpenApiResponse(description="Validation or storage error"),
        },
        examples=[
            OpenApiExample(
                "Upload example",
                value={"file": "example.pdf"},
                request_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        """
        Logs action, saves file.
        """
        self.log_action()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded = serializer.validated_data["file"]
        try:
            uid = self.service.save(
                uploaded.name,
                uploaded.read()
            )
        except StorageError as e:
            self.logger.error("upload failed", str(e))
            return Response({
                "detail": "Failed to upload file",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                "uid": uid
            }, status=status.HTTP_201_CREATED
        )


class FileDownloadView(BaseView):
    """
    GET /files/<uid>/
    """
    service = file_service
    action = "download"
    logger = logger

    @extend_schema(
        summary="Download a file",
        description=(
            "Download a previously uploaded file by UID. "
            "File will be reconstructed and streamed back."
        ),
        parameters=[
            OpenApiParameter(
                name="uid", description="File UUID", required=True, type=str
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="File downloaded successfully", response=bytes
            ),
            404: OpenApiResponse(description="File not found"),
            400: OpenApiResponse(
                description="Invalid request or server error"
            ),
        },
    )
    def get(self, request, uid, *args, **kwargs):
        """
        Logs action, downloads file.
        """
        self.log_action()
        try:
            name, content = self.service.get(uid)
            return FileResponse(
                io.BytesIO(content),
                as_attachment=True,
                filename=name
            )
        except StorageFileNotFound as e:
            self.logger.warning("File not found", str(e))
            return Response({
                "detail": "File not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except StorageError as e:
            self.logger.error("Failed to get a file", str(e))
            return Response({
                "detail": "Failed to upload file",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
