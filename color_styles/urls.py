from django.urls import path

from .views import GetBackgroundColor, GetMainColor, GetSecondaryColor

urlpatterns = [
    path("backgroundcolor", GetBackgroundColor.as_view()),
    path("maincolor", GetMainColor.as_view()),
    path("secondarycolor", GetSecondaryColor.as_view()),
]
