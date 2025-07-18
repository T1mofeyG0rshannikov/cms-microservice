from django.urls import path

from .views import CloneBlock, ClonePage, PageView

urlpatterns = [
    path("api/page", PageView.as_view()),
    path("page/clone", ClonePage.as_view()),
    path("block/clone", CloneBlock.as_view()),
]
