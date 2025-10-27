import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print(">>> ChatConsumer.connect called", self.channel_name)
        self.room_group_name = 'order'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.send(text_data=json.dumps(
            {'status': 'connected from django channels'}))

    def receive(self, text_data):
        print("Raw received:", text_data)

        data = json.loads(text_data)

        username = data.get('username')
        room = data.get('room', self.room_group_name)  # default to 'order'
        message = data.get('message')

        print(
            f">>> Parsed: username={username}, room={room}, message={message}")

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'username': username,
                'room': room,
                'message': message,
            }
        )

    def chat_message(self, event):

        username = event.get('username')
        room = event.get('room')
        message = event.get('message')

        self.send(text_data=json.dumps({
            'type': 'chat',
            'username': username,
            'room': room,
            'message': message
        }))

    def disconnect(self, close_code):
        print(">>> ChatConsumer.disconnect", close_code)
