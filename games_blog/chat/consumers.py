import json

from channels.db import database_sync_to_async
from channels.generic.websocket import (AsyncWebsocketConsumer,
                                        WebsocketConsumer)
from django.contrib.auth.models import User
from .models import Group, Message


class JoinAndLeave(WebsocketConsumer):

    def connect(self):
        print('scope', self.scope)
        self.user = self.scope["user"]
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        type = text_data.get("type", None)
        if type:
            data = text_data.get("data", None)

        if type == "leave_group":
            self.leave_group(data)
        elif type == "join_group":
            self.join_group(data)

    def leave_group(self, group_uuid):
        group = Group.objects.get(uuid=group_uuid)
        group.remove_user_from_group(self.user)
        data = {"type": "leave_group", "data": group_uuid}
        self.send(json.dumps(data))

    def join_group(self, group_uuid):
        group = Group.objects.get(uuid=group_uuid)
        group.add_user_to_group(self.user)
        data = {"type": "join_group", "data": group_uuid}
        self.send(json.dumps(data))


class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_uuid = str(self.scope["url_route"]["kwargs"]["uuid"])
        self.group = await database_sync_to_async(Group.objects.get)(
            uuid=self.group_uuid
        )
        await self.channel_layer.group_add(self.group_uuid, self.channel_name)

        self.user = self.scope["user"]
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        type = text_data.get("type", None)
        message = text_data.get("message", None)
        author = text_data.get("author", None)
        if type == "text_message":
            pass
            user = await database_sync_to_async(User.objects.get)(
                username=author
            )
            message = await database_sync_to_async(Message.objects.create)(
                author=user, content=message, group=self.group
            )
        await self.channel_layer.group_send(
            self.group_uuid,
            {"type": "text_message", "message": str(message), "author": author},
        )

    async def text_message(self, event):
        message = event["message"]
        author = event.get("author")

        returned_data = {
            "type": "text_message",
            "message": message,
            "group_uuid": self.group_uuid,
        }
        await self.send(json.dumps(returned_data))

        async def event_message(self, event):
            message = event.get("message")
            user = event.get("user", None)

            await self.send(
                json.dumps(
                    {
                        "type": "event_message",
                        "message": message,
                        "status": event.get("status", None),
                        "user": user,
                        "author": author,
                    }
                )
            )
