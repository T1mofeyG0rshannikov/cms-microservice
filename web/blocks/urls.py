from django.urls import path

from .views import CatalogView, CloneBlock, ClonePageView, PageView

urlpatterns = [
    path("api/page", PageView.as_view()),
    path("api/catalog/<str:slug>", CatalogView.as_view()),
    path("page/clone", ClonePageView.as_view()),
    path("block/clone", CloneBlock.as_view()),
]
