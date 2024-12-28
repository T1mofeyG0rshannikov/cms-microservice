from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from redis.exceptions import ConnectionError  # type: ignore

from domain.user.notifications.error import CantSendNotification


def send_message_to_user(user_id: int, message: str, channel_layer=get_channel_layer()) -> None:
    group_name = f"user_{user_id}"

    try:
        async_to_sync(channel_layer.group_send)(group_name, {"type": "chat.message", "message": message})
    except ConnectionError:
        raise CantSendNotification("cant send notification to user")
