from django.urls import re_path
from django.utils.module_loading import import_string


def get_chat_consumer():
    return import_string("merchant.consumers.ChatConsumer")


def get_deliveryman_consumer():
    return import_string("merchant.consumers.DeliverymanConsumer")


def get_current_delivery_consumer():
    return import_string("merchant.consumers.CurrentDeliveryConsumer")


websocket_urlpatterns = [
    re_path(r"ws/socket-server/$", get_chat_consumer().as_asgi()),
    re_path(r"ws/deliveryman/$", get_deliveryman_consumer().as_asgi()),
    re_path(r"ws/current-delivery/$",
            get_current_delivery_consumer().as_asgi()),
]
