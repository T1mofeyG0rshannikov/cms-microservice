from django.contrib import admin
from notifications.models import Notification, Trigger, UserNotification


class NotificationAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": ["name", "message", "status", "trigger"],
                "description": "Доступны подстановочные шаблоны:" + "<br><code>[user.site]</code> - сайт пользователя",
            },
        )
    ]


class UserNotificationAdmin(admin.ModelAdmin):
    pass


class TriggerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Notification, NotificationAdmin)
admin.site.register(UserNotification, UserNotificationAdmin)
admin.site.register(Trigger, TriggerAdmin)
