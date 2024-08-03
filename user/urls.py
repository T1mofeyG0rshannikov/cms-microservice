from django.urls import path

from user.views.views import (
    ConfirmEmail,
    GetUserInfo,
    Login,
    Logout,
    RegisterUser,
    ResetPassword,
    SendMailToResetPassword,
    SetPassword,
    SetToken,
)

urlpatterns = [
    path("register", RegisterUser.as_view()),
    path("password", SetPassword.as_view()),
    path("password/<str:token>", ResetPassword.as_view()),
    path("login", Login.as_view()),
    path("get-user-info", GetUserInfo.as_view()),
    path("confirm-email/<str:token>", ConfirmEmail.as_view()),
    path("reset-password", SendMailToResetPassword.as_view()),
    path("set-token/<str:token>", SetToken.as_view()),
    path("logout", Logout.as_view()),
]
