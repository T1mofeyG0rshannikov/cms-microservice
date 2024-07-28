from rest_framework import serializers

from notifications.models import Notification, UserNotification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["message", "status"]


class UserNotificationSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()
    date_created = serializers.SerializerMethodField()

    class Meta:
        model = UserNotification
        fields = ["notification", "date_created", "id"]

    def get_date_created(self, obj):
        return obj.date_created.strftime("%d.%m.%Y")
