from django.contrib import admin

from infrastructure.persistence.models.site_tests import (
    EnableErrorLogging,
    Error,
    TestUserSet,
)
from infrastructure.persistence.models.user.user import User


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
admin.site.register(EnableErrorLogging)
