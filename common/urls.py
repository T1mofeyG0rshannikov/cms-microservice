from django.urls import path

from .views import RedirectToLink

urlpatterns = [
    path("product", RedirectToLink.as_view()),
]
