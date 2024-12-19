from chat.consumers import GroupConsumer, JoinAndLeave
from django.urls import path

websocket_urlpatterns = [
    path("", JoinAndLeave.as_asgi()),
    path("chat/groups/<uuid:uuid>/", GroupConsumer.as_asgi()),
]
