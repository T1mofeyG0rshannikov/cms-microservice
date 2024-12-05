from domain.user.notifications.repository import NotificationRepositoryInterface
from infrastructure.persistence.models.notifications import Notification


class CreateUserNotification:
    def __init__(self, repository: NotificationRepositoryInterface) -> None:
        self.repository = repository

    def __call__(self, user_id: int, trigger_name: str):
        alert = Notification.objects.get(trigger__name=trigger_name)
        return self.repository.create_user_notification(user_id=user_id, notification_id=alert.id)
