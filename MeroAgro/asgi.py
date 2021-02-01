import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import messagingsystem.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MeroAgro.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  #   we need user to authenticate ...
  "websocket": AuthMiddlewareStack(
        URLRouter(
            messagingsystem.routing.websocket_urlpatterns
        )
    ),
})