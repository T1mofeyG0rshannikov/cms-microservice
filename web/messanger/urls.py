from django.urls import path

from .views import GetChatsView, SendMessageView

urlpatterns = [path("get-chats", GetChatsView.as_view()), path("send-message", SendMessageView.as_view())]
