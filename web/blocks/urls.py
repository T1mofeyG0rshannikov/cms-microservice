from django.urls import path

from .views import CloneBlock, ClonePage, IndexPage

urlpatterns = [
    path("", IndexPage.as_view()),
    path("page/clone", ClonePage.as_view()),
    path("block/clone", CloneBlock.as_view()),
]
