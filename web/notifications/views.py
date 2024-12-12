from django.http import HttpRequest, HttpResponse
from django.views.generic import View
from rest_framework import generics

from domain.user.notifications.repository import NotificationRepositoryInterface
from infrastructure.persistence.repositories.notification_repository import (
    get_notification_repository,
)
from web.notifications.serializers import UserNotificationSerializer


class DeleteUserNotificationView(View):
    def get(
        self,
        request: HttpRequest,
        id: int,
        *args,
        notification_repository: NotificationRepositoryInterface = get_notification_repository(),
        **kwargs
    ) -> HttpResponse:
        notification_repository.delete_user_notification(id)

        return HttpResponse(status=200)


class GetAllUserNotifications(generics.ListAPIView):
    serializer_class = UserNotificationSerializer

    def get_queryset(self, notification_repository: NotificationRepositoryInterface = get_notification_repository()):
        user_id = self.request.query_params.get("user_id")

        return notification_repository.get_notifications(user_id=user_id)
