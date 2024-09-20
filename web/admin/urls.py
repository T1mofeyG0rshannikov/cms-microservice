from django.contrib import admin
from django.urls import path

from web.admin.views import JoomlaAdminPage

urlpatterns = [
    path("admin/", JoomlaAdminPage.as_view()),
    path("komutan/", admin.site.urls),
    path("komutan", admin.site.urls),
]
