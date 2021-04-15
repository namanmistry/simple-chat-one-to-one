from channels.generic.websocket import AsyncWebsocketConsumer
import json
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(self.room_name,self.channel_name)
        await self.accept()
        

    async def receive(self,text_data):
        data=json.loads(text_data)
        username=data["username"]
        message=data["message"]
        await self.channel_layer.group_send(self.room_name,
        {
            'type':'chat_message',
            'username':username,
            'message':message
        }
        )
    async def chat_message(self,event):
        username=event["username"]
        message=event["message"]
        await self.send(json.dumps({
            'username':username,
            'message':message
        }))
    
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(self.room_name,self.channel_name)