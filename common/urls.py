from django.urls import path

from .views.views import (
    GetChangeSiteFormTemplate,
    GetChangeSocialsFormTemplate,
    GetChangeUserFormTemplate,
    RedirectToLink,
    slug_router,
)

urlpatterns = [
    path("product", RedirectToLink.as_view()),
    path("get-change-user-form", GetChangeUserFormTemplate.as_view()),
    path("get-change-site-form", GetChangeSiteFormTemplate.as_view()),
    path("get-change-socials-form", GetChangeSocialsFormTemplate.as_view()),
    path("<slug>", slug_router),
]
