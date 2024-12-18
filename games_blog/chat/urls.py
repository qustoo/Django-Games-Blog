from chat.views import HomeChatListView, group_chat_view
from django.urls import path

app_name = "chat"

urlpatterns = [
    path("groups/<uuid:uuid>/", group_chat_view, name="group-detail"),
    path("", HomeChatListView.as_view(), name="home"),
]
