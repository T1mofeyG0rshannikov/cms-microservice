from django.contrib import admin

from infrastructure.persistence.models.messanger import Chat, ChatUser, Message

admin.site.register(Chat)
admin.site.register(ChatUser)
admin.site.register(Message)
