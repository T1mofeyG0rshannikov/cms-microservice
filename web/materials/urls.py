from django.urls import path
from materials.views import GetPopup

urlpatterns = [
    path("popup", GetPopup.as_view()),
]
