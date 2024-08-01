from notifications.models import Notification, UserNotification
from notifications.serializers import UserNotificationSerializer
from user.user_interface import UserInterface


def create_user_notification(user: UserInterface, trigger_name: str):
    alert = Notification.objects.get(trigger__name=trigger_name)
    user_alert = UserNotification(user=user, notification=alert)
    user_alert.save()

    user_alert = UserNotificationSerializer(user_alert, context={"user": user}).data

    return user_alert
