from django.urls import path

from user.views.views import (
    ConfirmEmail,
    GetUserInfo,
    Login,
    Profile,
    RegisterUser,
    SendMailToResetPassword,
    SetPassword,
)

urlpatterns = [
    path("register", RegisterUser.as_view()),
    path("password/<str:token>", SetPassword.as_view()),
    path("login", Login.as_view()),
    path("profile", Profile.as_view()),
    path("get-user-info", GetUserInfo.as_view()),
    path("confirm-email/<str:token>", ConfirmEmail.as_view()),
    path("reset-password", SendMailToResetPassword.as_view()),
]
