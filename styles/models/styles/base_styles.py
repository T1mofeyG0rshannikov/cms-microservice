from django.db import models

from common.models import OneInstanceModel
from styles.models.styles.styles import GlobalStyles


class BaseStyles(OneInstanceModel):
    global_styles = models.OneToOneField(GlobalStyles, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True
