from django.urls import path

from .views import ChangePasswordView, ChangeSiteView, ChangeUserView, SiteView

urlpatterns = [
    path("site", SiteView.as_view()),
    path("change-site", ChangeSiteView.as_view()),
    path("change-user", ChangeUserView.as_view()),
    path("change-password", ChangePasswordView.as_view()),
]
