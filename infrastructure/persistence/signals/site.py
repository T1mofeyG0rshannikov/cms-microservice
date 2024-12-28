from django.db.models.signals import post_save

from application.usecases.notifications.create_notification import (
    CreateUserNotification,
)
from domain.user.notifications.error import CantSendNotification
from domain.user.notifications.trigger_enum import TriggerNames
from infrastructure.persistence.models.user.site import Site
from infrastructure.persistence.repositories.notification_repository import (
    get_notification_repository,
)
from web.notifications.send_message import send_message_to_user
from web.notifications.serializers import UserNotificationSerializer


def site_created_handler(
    sender,
    instance: Site,
    created,
    *args,
    create_user_notification=CreateUserNotification(get_notification_repository()),
    **kwargs
) -> None:
    if created:
        if instance.user:
            if not instance.user.test:
                user_alert = create_user_notification(instance.user, TriggerNames.sitecreated)
                user_alert = UserNotificationSerializer(user_alert).data
                try:
                    send_message_to_user(instance.user.id, user_alert)
                except CantSendNotification:
                    pass


post_save.connect(site_created_handler, sender=Site)
