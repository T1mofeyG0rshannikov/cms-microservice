from django.db import models

from infrastructure.persistence.models.common import OneInstanceModel
from infrastructure.persistence.models.settings import GlobalStyles


class BaseStyles(OneInstanceModel):
    global_styles = models.OneToOneField(GlobalStyles, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True
