from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("connected",event)
        pass

    async def websocket_disconnect(self,event):
        print("disconnected",event)
        pass
    
    async def websocket_recieve(self,event):
        print("recieve",event)
        pass

