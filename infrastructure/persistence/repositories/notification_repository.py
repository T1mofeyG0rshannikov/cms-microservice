from domain.user.notifications.repository import NotificationRepositoryInterface
from domain.user.user import UserInterface
from infrastructure.persistence.models.notifications import (
    Notification,
    NotificationFormatPattern,
    UserNotification,
)


class NotificationRepository(NotificationRepositoryInterface):
    def get_notification(self, notification_id: int):
        return Notification.objects.get(id=notification_id)

    def get_notification_patterns(self, notification_id: int):
        return NotificationFormatPattern.objects.filter(notification_id=notification_id)

    def get_user_notifications(self, user_id: int):
        return UserNotification.objects.filter(user_id=user_id)

    def create_user_notification(self, user: UserInterface, alert_id: int):
        return UserNotification.objects.create(user=user, notification_id=alert_id)

    def delete_user_notification(self, notification_id: int) -> None:
        UserNotification.objects.filter(id=notification_id).delete()


def get_notification_repository() -> NotificationRepositoryInterface:
    return NotificationRepository()
