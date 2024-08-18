from django.urls import path

from .views.views import (
    GetChangeSiteFormTemplate,
    GetChangeSocialsFormTemplate,
    GetChangeUserFormTemplate,
    ManualsTemplate,
    ProfileTemplate,
    RefsTemplate,
    SiteTemplate,
    slug_router,
)

urlpatterns = [
    path("get-change-socials-form", GetChangeSocialsFormTemplate.as_view()),
    path("get-change-site-form", GetChangeSiteFormTemplate.as_view()),
    path("get-change-user-form", GetChangeUserFormTemplate.as_view()),
    path("get-template-profile", ProfileTemplate.as_view()),
    path("get-template-manuals", ManualsTemplate.as_view()),
    path("get-template-refs", RefsTemplate.as_view()),
    path("get-template-site", SiteTemplate.as_view()),
    path("<slug>", slug_router),
]
