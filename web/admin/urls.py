from django.urls import path

from web.admin.views import JoomlaAdminPage

urlpatterns = [
    path("", JoomlaAdminPage.as_view()),
]
