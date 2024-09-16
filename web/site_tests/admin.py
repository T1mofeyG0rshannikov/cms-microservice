from django.contrib import admin

from web.site_tests.models import TestUserSet
from web.user.models.user import User


class TestUserInline(admin.StackedInline):
    model = User
    extra = 0
    fields = ["username", "second_name"]


class AdminTestUserSet(admin.ModelAdmin):
    inlines = [TestUserInline]


admin.site.register(TestUserSet, AdminTestUserSet)
