from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth.models import User
from .models import Thread
from asgiref.sync import sync_to_async
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        
        me=self.scope['url_route']['kwargs']['username']
        other_user=self.scope['url_route']['kwargs']['other_user']
        me_obj=await sync_to_async(User.objects.get)(username=me)
        other_user_obj=await sync_to_async(User.objects.get)(username=other_user)
        thread_obj= await sync_to_async(Thread.objects.get_or_create_personal_thread)(me_obj,other_user_obj)
        self.room_name= f'thread_obj_{thread_obj.id}'
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