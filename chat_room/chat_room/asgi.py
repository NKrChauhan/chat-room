"""
ASGI config for chat_room project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from django.urls.conf import path
from chatApp.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_room.settings')

# Blunder file spend 12 hrs for the error.

Routers = [
     path("thread/<username>/",ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        # Aloowed host in settings validator
        AuthMiddlewareStack(
            # middleware for auth user to access websockets
            URLRouter(Routers)
        )
    ),
})