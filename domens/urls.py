from django.urls import path

from domens.views import ActivateSite, CreateSite, StopSite

urlpatterns = [
    path("create-site", CreateSite.as_view()),
    path("stop", StopSite.as_view()),
    path("activate", ActivateSite.as_view()),
]
