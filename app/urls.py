from app.api import api
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api/v1/", api.urls),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]
