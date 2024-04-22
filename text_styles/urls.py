from django.urls import path

from .views import GetHeaderStyles, GetMainTextStyles, GetExplanationTextStyles, GetSubheaerStyles

urlpatterns = [
    path("header", GetHeaderStyles.as_view()),
    path("main-text", GetMainTextStyles.as_view()),
    path("subheader", GetSubheaerStyles.as_view()),
    path("explanation-text", GetExplanationTextStyles.as_view()),
]
