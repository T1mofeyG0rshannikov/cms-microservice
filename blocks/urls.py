from django.urls import path

from .views import CloneBlock, ClonePage, IndexPage, slug_router

urlpatterns = [
    path("", IndexPage.as_view()),
    path("<slug>", slug_router),
    path("page/clone", ClonePage.as_view()),
    path("block/clone", CloneBlock.as_view()),
]
