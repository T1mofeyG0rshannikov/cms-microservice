import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import web.notifications.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(web.notifications.routing.websocket_urlpatterns)),
    }
)
