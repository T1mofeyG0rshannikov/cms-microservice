from django.urls import path

from user.views import GetUserInfo, Login, Profile, RegisterUser, SetPassword

urlpatterns = [
    path("register", RegisterUser.as_view()),
    path("password/<str:token>", SetPassword.as_view()),
    path("login", Login.as_view()),
    path("profile", Profile.as_view()),
    path("get-user-info", GetUserInfo.as_view()),
]
