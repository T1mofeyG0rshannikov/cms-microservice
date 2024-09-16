from django.urls import path

from web.user.views.auth import LoginView, Logout, RegisterUser, SetToken
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
from web.user.views.views import DeleteUserProductView, GetUserInfo

urlpatterns = [
    path("register", RegisterUser.as_view()),
    path("password", SetPassword.as_view()),
    path("password/<str:token>", ResetPasswordView.as_view()),
    path("login", LoginView.as_view()),
    path("get-user-info", GetUserInfo.as_view()),
    path("confirm-email/<str:token>", ConfirmEmail.as_view()),
    path("confirm-new-email/<str:token>", ConfirmNewEmail.as_view()),
    path("reset-password", SendMailToResetPassword.as_view()),
    path("set-token/<str:token>", SetToken.as_view()),
    path("delete-user-product", DeleteUserProductView.as_view()),
    path("logout", Logout.as_view()),
    path("idea", AddIdeaView.as_view()),
    path("update-idea", UpdateIdeaView.as_view()),
    path("delete-idea", DeleteIdeaView.as_view()),
    path("ideas", GetIdeasView.as_view()),
    path("like", LikeView.as_view()),
]
