from django.urls import path

from .views import ShowPage

urlpatterns = [
    path("<page_url>", ShowPage.as_view()),
]
