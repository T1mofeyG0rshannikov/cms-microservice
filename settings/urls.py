from django.urls import path

from .views import GetSettings

urlpatterns = [
    path("", GetSettings.as_view())
]
