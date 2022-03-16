# Routing for Django Channels Websocket connections - Desk Reservations

from django.urls import re_path

from mainsite.consumers import DeskReservationConsumer

websocket_urlpatterns = [
    re_path(r'ws/desk-reservation/(?P<building>\w+)/(?P<floor>\w+)/$', DeskReservationConsumer.as_asgi()),
]