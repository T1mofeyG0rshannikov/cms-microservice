from django.db.models.signals import post_save, pre_save

from application.email_services.user_email_service.email_service_interface import (
    EmailServiceInterface,
)
from application.usecases.notifications.create_notification import (
    CreateUserNotification,
)
from domain.email.exceptions import CantSendMailError
from domain.user.exceptions import (
    SingleSuperSponsorExistError,
    UserWithEmailAlreadyExists,
    UserWithPhoneAlreadyExists,
)
from domain.user.notifications.error import CantSendNotification
from domain.user.notifications.trigger_enum import TriggerNames
from domain.user.user import UserInterface
from infrastructure.email_services.email_service.email_service import get_email_service
from infrastructure.persistence.models.user.user import User
from infrastructure.persistence.repositories.notification_repository import (
    get_notification_repository,
)
from infrastructure.persistence.repositories.user_repository import get_user_repository
from web.notifications.send_message import send_message_to_user
from web.notifications.serializers import UserNotificationSerializer


def user_created_handler(
    sender,
    instance: UserInterface,
    created,
    *args,
    email_service: EmailServiceInterface = get_email_service(),
    create_user_notification=CreateUserNotification(get_notification_repository()),
    **kwargs,
) -> None:
    if created and not instance.test:
        try:
            email_service.send_mail_to_confirm_email(instance)
        except CantSendMailError:
            pass

        user_alert = create_user_notification(instance.id, TriggerNames.signedup)

        user_alert = UserNotificationSerializer(user_alert).data

        try:
            send_message_to_user(instance.id, user_alert)
        except CantSendNotification:
            pass


def user_verified_email_handler(
    sender,
    instance: UserInterface,
    *args,
    create_user_notification=CreateUserNotification(get_notification_repository()),
    **kwargs,
) -> None:
    if instance.id is None:
        pass
    else:
        previous = User.objects.get(id=instance.id)
        if not previous.email_is_confirmed and instance.email_is_confirmed:
            user_alert = create_user_notification(instance.id, TriggerNames.emailverified)
            try:
                send_message_to_user(instance.id, user_alert)
            except CantSendNotification:
                pass


def user_change_email_handler(
    sender, instance: UserInterface, *args, email_service: EmailServiceInterface = get_email_service(), **kwargs
) -> None:
    if instance.id is None:
        pass
    else:
        previous = User.objects.get(id=instance.id)

        if (not previous.new_email and instance.new_email) or (previous.email != instance.email):
            try:
                email_service.send_mail_to_confirm_new_email(instance)
            except CantSendMailError:
                pass


def check_existing_user(
    sender, instance: UserInterface, *args, user_repository=get_user_repository(), **kwargs
) -> None:
    user_by_email = user_repository.get(email=instance.email)
    if user_by_email:
        if instance.pk != user_by_email.pk:
            raise UserWithEmailAlreadyExists(f"user with email '{instance.email}' already exists")

    user_by_phone = user_repository.get(phone=instance.phone)
    if user_by_phone:
        if instance.pk != user_by_phone.pk:
            raise UserWithPhoneAlreadyExists(f"user with phone '{instance.phone}' already exists")


def check_supersponsor(sender, instance: UserInterface, *args, **kwargs) -> None:
    supersponsor = User.objects.filter(supersponsor=True).first()
    if supersponsor:
        if supersponsor.pk == instance.pk:
            raise SingleSuperSponsorExistError("there can only be a single super sponsor on the site")


post_save.connect(user_created_handler, sender=User)
pre_save.connect(user_verified_email_handler, sender=User)
pre_save.connect(user_change_email_handler, sender=User)
pre_save.connect(check_existing_user, sender=User)
