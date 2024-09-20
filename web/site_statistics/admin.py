from django.contrib import admin

from web.site_statistics.models import TryLoginToAdminPanel, TryLoginToFakeAdminPanel

admin.site.register(TryLoginToAdminPanel)
admin.site.register(TryLoginToFakeAdminPanel)
