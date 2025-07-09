from django.urls import include, path
from rest_framework.authtoken import views

from .views.file_views import FileDownloadView, FileUploadView

file_urls = [
    path(
        "upload/",
        FileUploadView.as_view(),
        name="file_upload",
    ),
    path(
        "download/<uuid:uid>/",
        FileDownloadView.as_view(),
        name="file_upload",
    )
]

urlpatterns = [
    path("files/", include((file_urls, "files"))),

    # user register is not implemented
    path("login/",  views.obtain_auth_token)
]
