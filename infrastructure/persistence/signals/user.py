from django.db.models.signals import post_save, pre_save

from domain.email.exceptions import CantSendMailError
from domain.user.exceptions import (
    SingleSuperSponsorExistError,
    UserWithEmailAlreadyExists,
    UserWithPhoneAlreadyExists,
)
from infrastructure.email_services.email_service.email_service import get_email_service
from infrastructure.email_services.email_service.email_service_interface import (
    EmailServiceInterface,
)
from infrastructure.persistence.models.user.user import User
from web.notifications.create_user_notification import create_user_notification
from web.notifications.error import CantSendNotification
from web.notifications.send_message import send_message_to_user


def user_created_handler(
    sender, instance, created, *args, email_service: EmailServiceInterface = get_email_service(), **kwargs
):
    if created and not instance.test:
        try:
            email_service.send_mail_to_confirm_email(instance)
        except CantSendMailError:
            pass

        user_alert = create_user_notification(instance, "SIGNEDUP")

        try:
            send_message_to_user(instance.id, user_alert)
        except CantSendNotification:
            pass


def user_verified_email_handler(sender, instance, *args, **kwargs):
    if instance.id is None:
        pass
    else:
        previous = User.objects.get_user_by_id(id=instance.id)
        if not previous.email_is_confirmed and instance.email_is_confirmed:
            user_alert = create_user_notification(instance, "EMAILVERIFIED")
            try:
                send_message_to_user(instance.id, user_alert)
            except CantSendNotification:
                pass


def user_change_email_handler(
    sender, instance, *args, email_service: EmailServiceInterface = get_email_service(), **kwargs
):
    if instance.id is None:
        pass
    else:
        previous = User.objects.get_user_by_id(id=instance.id)

        if (not previous.new_email and instance.new_email) or (previous.email != instance.email):
            try:
                email_service.send_mail_to_confirm_new_email(instance)
            except CantSendMailError:
                pass


def check_existing_user(sender, instance, *args, **kwargs):
    user_by_email = User.objects.get_user_by_email(instance.email)
    if user_by_email:
        if instance.pk != user_by_email.pk:
            raise UserWithEmailAlreadyExists(f"user with email '{instance.email}' already exists")

    user_by_phone = User.objects.get_user_by_phone(instance.phone)
    if user_by_phone:
        if instance.pk != user_by_phone.pk:
            raise UserWithPhoneAlreadyExists(f"user with phone '{instance.phone}' already exists")


def check_supersponsor(sender, instance, *args, **kwargs):
    supersponsor = User.objects.filter(supersponsor=True).first()
    if supersponsor:
        if supersponsor.pk == instance.pk:
            raise SingleSuperSponsorExistError("there can only be a single super sponsor on the site")


post_save.connect(user_created_handler, sender=User)
pre_save.connect(user_verified_email_handler, sender=User)
pre_save.connect(user_change_email_handler, sender=User)
pre_save.connect(check_existing_user, sender=User)
