from django.contrib import admin

from web.site_tests.models import Error, TestUserSet
from web.user.models.user import User


class TestUserInline(admin.StackedInline):
    model = User
    extra = 0
    fields = ["username", "second_name"]


class AdminTestUserSet(admin.ModelAdmin):
    inlines = [TestUserInline]


class AdminError(admin.ModelAdmin):
    exclude = ["status"]
    readonly_fields = ["client_ip", "user", "time", "status", "message", "path"]


admin.site.register(TestUserSet, AdminTestUserSet)
admin.site.register(Error, AdminError)
