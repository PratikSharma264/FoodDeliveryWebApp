from django.urls import re_path
from django.utils.module_loading import import_string
from merchant.consumers import ChatConsumer, DeliverymanConsumer, ClientConsumer


# def get_chat_consumer():
#     return import_string("merchant.consumers.ChatConsumer")


# def get_deliveryman_consumer():
#     return import_string("merchant.consumers.DeliverymanConsumer")

# def get_client_consumer():
#     return import_string("merchant.consumers.ClientConsumer")


websocket_urlpatterns = [
    re_path(r"ws/socket-server/(?P<restaurant_id>\d+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/deliveryman/(?P<deliveryman_id>\d+)/$", DeliverymanConsumer.as_asgi()),
    re_path(r"ws/client/(?P<order_id>\d+)/$", ClientConsumer.as_asgi())
]
