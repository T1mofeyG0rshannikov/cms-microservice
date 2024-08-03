from django.urls import path, re_path

from .views import (
    ChangePasswordView,
    ChangeSiteView,
    ChangeUserView,
    PageNotFound,
    Profile,
    ProfileTemplate,
    SiteView,
)

urlpatterns = [
    path("my/", Profile.as_view()),
    path("my/site/", SiteView.as_view()),
    path("my/change-site", ChangeSiteView.as_view()),
    path("my/change-user", ChangeUserView.as_view()),
    path("my/change-password", ChangePasswordView.as_view()),
    path("my/template/<str:template_name>", ProfileTemplate.as_view()),
    re_path(r"^.*", PageNotFound.as_view()),
]
