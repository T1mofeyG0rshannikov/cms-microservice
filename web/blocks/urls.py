from django.urls import path

from .views import CloneBlock, ClonePageView, PageView

urlpatterns = [
    path("api/page", PageView.as_view()),
    path("api/page/clone", ClonePageView.as_view()),
    path("api/block/clone", CloneBlock.as_view()),
]
