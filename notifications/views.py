from django.http import HttpResponse
from django.views.generic import View
from rest_framework import generics

from notifications.models import UserNotification
from notifications.serializers import UserNotificationSerializer


class DeleteUserNotificationView(View):
    def get(self, request, id, *args, **kwargs):
        UserNotification.objects.filter(id=id).delete()

        return HttpResponse(status=200)


class GetAllUserNotifications(generics.ListAPIView):
    serializer_class = UserNotificationSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")

        return UserNotification.objects.filter(user__id=user_id)
