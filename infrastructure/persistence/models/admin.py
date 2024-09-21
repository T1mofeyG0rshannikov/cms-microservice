from django.db import models


class AdminLoginCode(models.Model):
    code = models.PositiveIntegerField()
    email = models.CharField(max_length=100)

    class Meta:
        app_label = "custom_admin"
