from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/socket-server/", consumers.ChatConsumer.as_asgi()),
    path("ws/send/<user_id>/<user_notification_id>", consumers.SendAlertConsumer.as_asgi()),
]
