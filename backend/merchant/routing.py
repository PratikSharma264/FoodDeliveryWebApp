from django.urls import re_path
from django.utils.module_loading import import_string

def get_chat_consumer():
    return import_string("merchant.consumers.ChatConsumer")

websocket_urlpatterns = [
    re_path(r"ws/socket-server/$", get_chat_consumer().as_asgi()),
]
