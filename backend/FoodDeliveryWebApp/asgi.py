import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FoodDeliveryWebApp.settings")

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

import merchant.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                merchant.routing.websocket_urlpatterns
            )
        )
    ),
})
