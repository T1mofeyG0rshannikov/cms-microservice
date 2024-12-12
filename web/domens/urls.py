from django.urls import path

from web.settings.views.views import ActivateSite, StopSite

urlpatterns = [
    path("stop", StopSite.as_view()),
    path("activate", ActivateSite.as_view()),
]
