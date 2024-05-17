from django.urls import path

from user.views import Login, RegisterUser, SetPassword

urlpatterns = [
    path("register", RegisterUser.as_view()),
    path("password/<str:token>", SetPassword.as_view()),
    path("login", Login.as_view()),
]
