from django.urls import path
from django.views.decorators.cache import cache_page

from web.styles.views import (
    GetColorStyles,
    GetExplanationTextStyles,
    GetFonts,
    GetHeaderStyles,
    GetIconSize,
    GetMainTextStyles,
    GetMarginBlock,
    GetStyles,
    GetSubheaerStyles,
)

urlpatterns = [
    path("colors", cache_page(60 * 15)(GetColorStyles.as_view())),
    path("header", cache_page(60 * 15)(GetHeaderStyles.as_view())),
    path("main-text", cache_page(60 * 15)(GetMainTextStyles.as_view())),
    path("explanation-text", cache_page(60 * 15)(GetExplanationTextStyles.as_view())),
    path("subheader", cache_page(60 * 15)(GetSubheaerStyles.as_view())),
    path("margin-block", cache_page(60 * 15)(GetMarginBlock.as_view())),
    path("icon-size", cache_page(60 * 15)(GetIconSize.as_view())),
    path("fonts", cache_page(60 * 15)(GetFonts.as_view())),
    path("", GetStyles.as_view()),
]
