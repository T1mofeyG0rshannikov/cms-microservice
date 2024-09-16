from django.urls import path

from web.materials.views import GetPopup

urlpatterns = [
    path("popup", GetPopup.as_view()),
]
