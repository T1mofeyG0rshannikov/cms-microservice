from collections.abc import Iterable
from typing import Protocol

from domain.user.notifications.notifications import (
    NotificationInterface,
    NotificationPatternInterface,
)


class NotificationRepositoryInterface(Protocol):
    def get_notification(self, id: int) -> NotificationInterface:
        raise NotImplementedError

    def get_notification_patterns(self, notification_id: int) -> Iterable[NotificationPatternInterface]:
        raise NotImplementedError

    def get_user_notifications(self, user_id: int) -> Iterable[NotificationInterface]:
        raise NotImplementedError

    def delete_user_notification(self, id: int) -> None:
        raise NotImplementedError

    def create_user_notification(self, user_id: int, notification_id: int) -> NotificationInterface:
        raise NotImplementedError

    def get_notifiation_by_trigger(self, triger_name: str) -> NotificationInterface:
        raise NotImplementedError
