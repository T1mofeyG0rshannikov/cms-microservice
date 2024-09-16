from django.urls import path

from web.common.views import RedirectToLink

urlpatterns = [
    path("product", RedirectToLink.as_view()),
]
