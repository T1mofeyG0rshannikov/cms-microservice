from django.urls import path

from .views import CloneBlock, ClonePage, IndexPage, ShowTemplates, slug_router

urlpatterns = [
    path("", IndexPage.as_view()),
    path("<slug>", slug_router),
    path("templates/get", ShowTemplates.as_view()),
    path("page/clone", ClonePage.as_view()),
    path("block/clone", CloneBlock.as_view()),
]
