from django.db import models
from django.db.models.signals import post_save

from common.models import OneInstanceModel


class Roles(OneInstanceModel):
    class Meta:
        verbose_name = "Роли"
        verbose_name_plural = "Роли"


class BaseUserRole(models.Model):
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class SuperUserRole(BaseUserRole):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        self.user.is_superuser = False
        self.user.staff = False
        return super().delete(*args, **kwargs)

    def __str__(self):
        return ""


def superuser_role_created_handler(sender, instance, created, *args, **kwargs):
    if created:
        instance.user.is_puperuser = True
        instance.user.staff = True


post_save.connect(superuser_role_created_handler, sender=SuperUserRole)
