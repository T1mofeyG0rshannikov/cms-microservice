from collections.abc import Iterable

from domain.user.notifications.notifications import (
    NotificationInterface,
    NotificationPatternInterface,
)
from domain.user.notifications.repository import NotificationRepositoryInterface
from infrastructure.persistence.models.notifications import (
    Notification,
    NotificationFormatPattern,
    UserNotification,
)


class NotificationRepository(NotificationRepositoryInterface):
    def get_notification(self, notification_id: int) -> NotificationInterface:
        return Notification.objects.get(id=notification_id)

    def get_notification_patterns(self, notification_id: int) -> Iterable[NotificationPatternInterface]:
        return NotificationFormatPattern.objects.filter(notification_id=notification_id)

    def get_user_notifications(self, user_id: int) -> Iterable[NotificationInterface]:
        return UserNotification.objects.filter(user_id=user_id)

    def create_user_notification(self, user_id: int, alert_id: int) -> NotificationInterface:
        return UserNotification.objects.create(user_id=user_id, notification_id=alert_id)

    def delete_user_notification(self, notification_id: int) -> None:
        UserNotification.objects.filter(id=notification_id).delete()

    def get_notifiation_by_trigger(self, triger_name: str) -> NotificationInterface:
        return Notification.objects.get(trigger__name=triger_name)


def get_notification_repository() -> NotificationRepositoryInterface:
    return NotificationRepository()
