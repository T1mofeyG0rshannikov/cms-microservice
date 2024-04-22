from django.urls import path

from .views import GetIconSize, GetMarginBlock

urlpatterns = [
    path("icon-size", GetIconSize.as_view()),
    path("margin-block", GetMarginBlock.as_view())
]
