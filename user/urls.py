from django.urls import path

from user.views import RegisterUser

urlpatterns = [
    path("register", RegisterUser.as_view()),
]
