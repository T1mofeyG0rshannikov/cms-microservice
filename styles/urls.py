from django.urls import path
from .views import GetColorStyles, GetHeaderStyles, GetMainTextStyles, GetExplanationTextStyles, GetSubheaerStyles, GetMarginBlock, GetIconSize


urlpatterns = [
    path("colors", GetColorStyles.as_view()),
    path("header", GetHeaderStyles.as_view()),
    path("main-text", GetMainTextStyles.as_view()),
    path("explanation-text", GetExplanationTextStyles.as_view()),
    path("subheader", GetSubheaerStyles.as_view()),
    path("margin-block", GetMarginBlock.as_view()),
    path("icon-size", GetIconSize.as_view()),
]