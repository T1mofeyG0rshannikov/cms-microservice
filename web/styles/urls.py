from django.urls import path

from .views import (
    GetColorStyles,
    GetExplanationTextStyles,
    GetFonts,
    GetHeaderStyles,
    GetIconSize,
    GetMainTextStyles,
    GetMarginBlock,
    GetSubheaerStyles,
)

urlpatterns = [
    path("colors", GetColorStyles.as_view()),
    path("header", GetHeaderStyles.as_view()),
    path("main-text", GetMainTextStyles.as_view()),
    path("explanation-text", GetExplanationTextStyles.as_view()),
    path("subheader", GetSubheaerStyles.as_view()),
    path("margin-block", GetMarginBlock.as_view()),
    path("icon-size", GetIconSize.as_view()),
    path("fonts", GetFonts.as_view()),
]
