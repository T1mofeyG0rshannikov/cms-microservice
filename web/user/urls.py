from django.urls import path

from web.settings.views.views import ActivateSite, StopSite
from web.user.views.auth import LoginView, Logout, RefreshTokensView, RegisterUser, SetToken
from web.user.views.email import ConfirmEmail, ConfirmNewEmail
from web.user.views.ideas import (
    AddIdeaView,
    DeleteIdeaView,
    GetIdeasView,
    LikeView,
    UpdateIdeaView,
)
from web.user.views.password import (
    ResetPasswordView,
    SendMailToResetPassword,
    SetPassword,
)
from web.user.views.views import (
    DeleteUserProductView,
    IsUserAuth,
    SendConfirmPhoneView,
    SubmitPhoneView,
)

urlpatterns = [
    path("register", RegisterUser.as_view()),
    path("password", SetPassword.as_view()),
    path("password/<str:token>", ResetPasswordView.as_view()),
    path("login", LoginView.as_view()),
    path("get-user-info", IsUserAuth.as_view()),
    path("confirm-email/<str:token>", ConfirmEmail.as_view()),
    path("confirm-new-email/<str:token>", ConfirmNewEmail.as_view()),
    path("reset-password", SendMailToResetPassword.as_view()),
    path("set-token/<str:access_token>/<str:refresh_token>", SetToken.as_view()),
    path("delete-user-product", DeleteUserProductView.as_view()),
    path("logout", Logout.as_view()),
    path("idea", AddIdeaView.as_view()),
    path("update-idea", UpdateIdeaView.as_view()),
    path("delete-idea", DeleteIdeaView.as_view()),
    path("ideas", GetIdeasView.as_view()),
    path("like", LikeView.as_view()),
    path("send-confirm-phone", SendConfirmPhoneView.as_view()),
    path("confirm-phone", SubmitPhoneView.as_view()),
    path("stop-site", StopSite.as_view()),
    path("activate-site", ActivateSite.as_view()),
    path("refresh-tokens/<str:refresh_token>", RefreshTokensView.as_view())
]
