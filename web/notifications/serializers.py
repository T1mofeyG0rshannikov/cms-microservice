from rest_framework import serializers

from application.usecases.formatters.format_notification import (
    FormatNotification,
    get_format_notification,
)
from infrastructure.persistence.models.notifications import (
    Notification,
    UserNotification,
)
from web.common.serializers import DateFieldDot


class NotificationSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ["message", "status"]

    def get_message(self, notification, notification_formatter: FormatNotification = get_format_notification()):
        user = self.context.get("user")

        notification_message = notification_formatter(notification.id)
        if user:
            if user.full_site_name:
                notification_message = notification_message.replace("[user.site]", user.full_site_name)
        return notification_message


class UserNotificationSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()
    date_created = DateFieldDot()

    class Meta:
        model = UserNotification
        fields = ["notification", "date_created", "id"]
