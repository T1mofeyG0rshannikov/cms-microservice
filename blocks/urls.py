from django.urls import path

from .views import ClonePage, ShowPage, ShowTemplates

urlpatterns = [
    path("<page_url>", ShowPage.as_view()),
    path("templates/get", ShowTemplates.as_view()),
    path("page/clone", ClonePage.as_view()),
]
