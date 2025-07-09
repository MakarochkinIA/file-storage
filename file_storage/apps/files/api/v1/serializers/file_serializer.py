from django.conf import settings
from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    """
    File serializer. Validates file size.
    """
    file = serializers.FileField()

    def validate_file(self, uploaded):
        if uploaded.size > settings.MAX_FILE_SIZE:
            raise serializers.ValidationError(
                f"File too large. Max size: {settings.MAX_FILE_SIZE}"
            )
        return uploaded
