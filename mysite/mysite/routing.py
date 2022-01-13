from channels.routing import ProtocolTypeRouter,URLRouter
import os
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
import tutorial.routing
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # (your routes here)
    'http' : django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                tutorial.routing.websocket_urlpatterns
            )
        )
    )
})