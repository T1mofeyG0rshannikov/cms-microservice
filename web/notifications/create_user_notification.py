from domain.referrals.referral import UserInterface
from domain.user.notifications.repository import NotificationRepositoryInterface
from infrastructure.persistence.models.notifications import Notification
from infrastructure.persistence.repositories.notification_repository import (
    get_notification_repository,
)
from web.notifications.serializers import UserNotificationSerializer


def create_user_notification(
    user: UserInterface,
    trigger_name: str,
    notification_repository: NotificationRepositoryInterface = get_notification_repository(),
):
    alert = Notification.objects.get(trigger__name=trigger_name)
    user_alert = notification_repository.create_user_notification(user=user, notification_id=alert.id)

    return UserNotificationSerializer(user_alert, context={"user": user}).data
