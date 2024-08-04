from django.urls import path

from .views.views import (
    GetChangeSiteFormTemplate,
    GetChangeUserFormTemplate,
    RedirectToLink,
    slug_router,
)

urlpatterns = [
    path("<slug>", slug_router),
    path("product", RedirectToLink.as_view()),
    path("get-change-user-form", GetChangeUserFormTemplate.as_view()),
    path("get-change-site-form", GetChangeSiteFormTemplate.as_view()),
]
