from django.contrib import admin

from site_tests.models import TestUserSet
from user.models import User


class TestUserInline(admin.StackedInline):
    model = User
    extra = 0
    fields = ["username", "second_name"]


class AdminTestUserSet(admin.ModelAdmin):
    inlines = [TestUserInline]


admin.site.register(TestUserSet, AdminTestUserSet)
