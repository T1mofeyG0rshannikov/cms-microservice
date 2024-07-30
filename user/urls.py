from django.urls import path

from user.views.views import (
    ConfirmEmail,
    GetUserInfo,
    Login,
    Logout,
    RegisterUser,
    SendMailToResetPassword,
    SetPassword,
    SetToken,
    email_template,
)

urlpatterns = [
    path("register", RegisterUser.as_view()),
    path("password/<str:token>", SetPassword.as_view()),
    path("login", Login.as_view()),
    path("get-user-info", GetUserInfo.as_view()),
    path("confirm-email/<str:token>", ConfirmEmail.as_view()),
    path("reset-password", SendMailToResetPassword.as_view()),
    path("set-token/<str:token>", SetToken.as_view()),
    path("logout", Logout.as_view()),
    path("email-template", email_template),
]
