from .models import Thread,ChatMessage
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
import json
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        user = self.scope['user']
        user2 = self.scope['url_route']['kwargs']['username']
        self.thread_obj = await self.get_thread(user,user2)
        self.chat_room = f"thread_{self.thread_obj.id}"
        print(self.chat_room)
        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )
        await self.send({
            "type":"websocket.accept"
        })

    async def websocket_receive(self,event):
        msg = event.get('text',None)
        if msg is not None:
            msg = json.loads(msg)
            data = msg.get('message')
            # obj  = await ChatMessage.objects.create(user = self.scope['user'],thread=self.thread_obj,message=data)
            # print(obj)
            user = self.scope['user']
            res = {
                    "message":data,
                    "user":user.username
                }
            if user.is_authenticated:
                await self.save_chat(user,data)
                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                    "type":"message_send",
                    "text":json.dumps(res)
                    }
                )

    async def message_send(self,event):
        print(event["text"])
        await self.send({
            "type": "websocket.send",
            "text":event['text'],
        })

    async def websocket_disconnect(self,event):
        await self.channel_layer.group_discard(self.chat_room, self.channel_name)

    @database_sync_to_async
    def save_chat(self,user,message):
        return ChatMessage.objects.create(user = user,message=message,thread=self.thread_obj)

    @database_sync_to_async
    def get_thread(self,user,user2):
        return Thread.objects.get_or_new(user,user2)[0]