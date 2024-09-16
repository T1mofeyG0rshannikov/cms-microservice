from rest_framework import serializers

from web.common.serializers import DateFieldDot
from web.notifications.models import Notification, UserNotification


class NotificationSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ["message", "status"]

    def get_message(self, notification):
        user = self.context.get("user")
        if not user:
            return notification.message

        if not user.full_site_name:
            return notification.message

        return notification.message.replace("[user.site]", user.full_site_name)


class UserNotificationSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()
    date_created = DateFieldDot()

    class Meta:
        model = UserNotification
        fields = ["notification", "date_created", "id"]
