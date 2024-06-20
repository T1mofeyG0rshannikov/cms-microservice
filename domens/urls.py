from django.urls import path

from domens.views import CreateSite

urlpatterns = [
    path("create-site", CreateSite.as_view()),
]
