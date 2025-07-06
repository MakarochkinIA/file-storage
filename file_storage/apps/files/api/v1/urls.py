from django.urls import path, include

from .views.file_views import FileDownloadView, FileUploadView

file_urls = [
    path(
        "upload/",
        FileUploadView.as_view(),
        name="file_upload",
    ),
    path(
        "download/<uuid:uid>",
        FileDownloadView.as_view(),
        name="file_upload",
    )
]

urlpatterns = [
    path("files/", include((file_urls, "files"))),
]
