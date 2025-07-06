import io
import uuid
import pytest
from unittest.mock import patch

from django.urls import reverse

upload_url = reverse("file_upload")
download_url = lambda uid: reverse("file_upload")[:-6] + f"download/{uid}"


@pytest.mark.django_db
def test_file_upload_view_success(api_client):
    content = b"test content" * 1000  # <16MB
    file = io.BytesIO(content)
    file.name = "test.txt"

    with patch(
        "apps.files.infra.file_service.save", return_value="fake-uuid"
    ) as mocked_save:
        response = api_client.post(
            upload_url, {"file": file}, format="multipart"
        )

    assert response.status_code == 201
    assert "uid" in response.data
    mocked_save.assert_called_once()


@pytest.mark.django_db
def test_file_download_view_success(api_client):
    uid = str(uuid.uuid4())
    file_content = b"restored file"
    file_name = "test.txt"

    with patch(
        "apps.files.infra.file_service.get",
        return_value=(file_name, file_content)
    ):
        response = api_client.get(download_url(uid))

    assert response.status_code == 200
    assert response.getvalue() == file_content
