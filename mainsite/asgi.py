"""
ASGI config for lcog project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import mainsite.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainsite.settings')

# Add channels
application = ProtocolTypeRouter({
    # For standard HTTP requests
    "http": get_asgi_application(),
    # For WebSocket requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            mainsite.routing.websocket_urlpatterns
        )
    ),
})
