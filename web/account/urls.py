from django.urls import path, re_path

from .views.api import GetReferals
from .views.forms import (
    AddUserProductView,
    ChangeSiteView,
    ChangeSocialsView,
    ChangeUserView,
)
from .views.templates import (
    ChangePasswordView,
    DocumentPage,
    IdeasView,
    ManualsView,
    MessangerView,
    PageNotFound,
    Profile,
    RefsView,
    SiteView,
    UserProductsView,
)

urlpatterns = [
    re_path(r"my/?$", Profile.as_view()),
    re_path(r"my/site/?$", SiteView.as_view()),
    re_path(r"my/refs/?$", RefsView.as_view()),
    re_path(r"my/manuals/?$", ManualsView.as_view()),
    re_path(r"my/products/?$", UserProductsView.as_view()),
    re_path(r"my/ideas/?$", IdeasView.as_view()),
    re_path(r"my/messanger/?$", MessangerView.as_view()),
    path("my/manual/<str:slug>", DocumentPage.as_view()),
    path("my/change-site", ChangeSiteView.as_view()),
    path("my/change-socials", ChangeSocialsView.as_view()),
    path("my/change-user", ChangeUserView.as_view()),
    path("my/change-password", ChangePasswordView.as_view()),
    path("my/get-referrals", GetReferals.as_view()),
    path("my/add-user-product", AddUserProductView.as_view()),
    re_path(r"^my/.*", PageNotFound.as_view()),
]
