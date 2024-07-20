from django.urls import path

from .views import DeleteUserNotificationView, GetAllUserNotifications

urlpatterns = [
    path("delete/<int:id>", DeleteUserNotificationView.as_view()),
    path("get", GetAllUserNotifications.as_view()),
]
