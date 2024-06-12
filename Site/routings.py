from django.urls import re_path
from ws_rotate import consumers

websocket_urlpatterns = [
    re_path(r'ws_rotate/',consumers.ChatConsumer.as_asgi())
]
