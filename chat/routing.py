from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns=[path('ws/chat/<str:username>/<str:other_user>/',ChatConsumer.as_asgi())]