from typing import Iterable, Protocol

from domain.account.notifications import NotificationInterface, NotificationPatternInterface


class NotificationRepositoryInterface(Protocol):
    def get_notification(self, id: int) -> NotificationInterface:
        raise NotImplementedError
    
    def get_notification_patterns(self, notification_id: int) -> Iterable[NotificationPatternInterface]:
        raise NotImplementedError
    
    def get_user_notifications(self, user_id: int) -> Iterable[NotificationInterface]:
        raise NotImplementedError
    
    def delete_user_notification(self, id: int) -> None:
        raise NotImplementedError
