from django.urls import path, re_path

from .views.api import GetReferals, GetReferral
from .views.templates import (
    ChangePasswordView,
    GetReferralPopupTemplate,
    PageNotFound,
    Profile,
    ProfileTemplate,
    RefsView,
    SiteView,
)
from .views.views import ChangeSiteView, ChangeSocialsView, ChangeUserView

urlpatterns = [
    re_path(r"my/?$", Profile.as_view()),
    re_path(r"my/site/?$", SiteView.as_view()),
    re_path(r"my/refs/?$", RefsView.as_view()),
    path("my/change-site", ChangeSiteView.as_view()),
    path("my/change-socials", ChangeSocialsView.as_view()),
    path("my/change-user", ChangeUserView.as_view()),
    path("my/change-password", ChangePasswordView.as_view()),
    path("my/template/<str:template_name>", ProfileTemplate.as_view()),
    path("my/get-referrals", GetReferals.as_view()),
    path("my/get-referral/<int:user_id>", GetReferral.as_view()),
    path("get-referral-popup", GetReferralPopupTemplate.as_view()),
    re_path(r"^my/.*", PageNotFound.as_view()),
]
