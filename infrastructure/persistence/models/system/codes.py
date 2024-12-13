from django.db import models

from infrastructure.persistence.models.user.user import User


class ConfirmPhoneCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True)
    code = models.CharField(max_length=6)

    class Meta:
        app_label = "system"
