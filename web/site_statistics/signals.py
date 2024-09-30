from django.db.models.signals import post_save

from infrastructure.persistence.models.site_statistics import (
    SessionAction,
    SessionModel,
    UserActivity,
)


def hacking_session_handler(sender, instance, created, *args, **kwargs):
    if instance.hacking:
        SessionModel.objects.filter(unique_key=instance.unique_key).update(
            hacking=True, hacking_reason=instance.hacking_reason
        )

        instance.delete()
        """SessionModel.objects.filter(unique_key=instance.unique_key).update(
            hacking = True,
        )

        for action in instance.actions:
            SessionAction.objects.create(
                adress=action.adress,
                time=action.time,
                session=SessionModel.objects.get(unique_key=instance.unique_key)
            )"""


post_save.connect(hacking_session_handler, sender=UserActivity)
