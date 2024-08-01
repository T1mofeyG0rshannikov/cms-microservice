from django.urls import path

from .views import RedirectToLink, GetChangeUserFormTemplate, GetChangeSiteFormTemplate

urlpatterns = [
    path("product", RedirectToLink.as_view()),
    path("get-change-user-form", GetChangeUserFormTemplate.as_view()),
    path("get-change-site-form", GetChangeSiteFormTemplate.as_view()),
]
