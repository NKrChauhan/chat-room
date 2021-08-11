from concurrent.futures import thread
from .models import Thread,ChatMessage
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
import json
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("connected",event)
        await self.send({
            "type":"websocket.accept"
        })
        user = self.scope['user']
        user2 = self.scope['url_route']['kwargs']['username']
        thread_obj = await self.get_thread(user,user2)

    async def websocket_receive(self,event):
        msg = event.get('text',None)
        msg = json.loads(msg)
        if msg is not None:
            data = msg.get('message')
            # ChatMessage.objects.create(user = self.scope['user'],thre)
            user = self.scope['user']
            await self.send({
                "type":"websocket.send",
                "text":json.dumps({"text":data,
                                    "user":user.username
                                    })
            })
    
    async def websocket_disconnect(self,event):
        print("disconnected",event)
    


    @database_sync_to_async
    def get_thread(self,user,user2):
        return Thread.objects.get_or_new(user,user2)[0]