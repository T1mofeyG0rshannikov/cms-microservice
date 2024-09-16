from django.db import models

from web.common.models import OneInstanceModel
from web.settings.models import GlobalStyles


class BaseStyles(OneInstanceModel):
    global_styles = models.OneToOneField(GlobalStyles, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True
