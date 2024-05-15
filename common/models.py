from django.db import models


class OneInstanceModel(models.Model):
    def __str__(self):
        return self._meta.verbose_name
    
    class Meta:
        abstract = True