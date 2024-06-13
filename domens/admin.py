from django.contrib import admin
from django.contrib.admin.decorators import register

from domens.models import Site


@register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass
