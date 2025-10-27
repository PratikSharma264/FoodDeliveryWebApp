import json
from decimal import Decimal, InvalidOperation
from django.db import transaction
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'order'
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()
        self.send(text_data=json.dumps({'status': 'connected from django channels'}))

    def receive(self, text_data):
        from django.contrib.auth import get_user_model
        from .models import Order, FoodItem, Restaurant

        User = get_user_model()
        try:
            data = json.loads(text_data)
        except:
            data = {}

        username = data.get('username')
        room = data.get('room', self.room_group_name)
        order_data = data.get('order') or {}

        def parse_decimal(value):
            try:
                return Decimal(str(value))
            except:
                return None

        def find_user(payload):
            uid = payload.get('user_id') or payload.get('uid')
            if uid: return User.objects.filter(pk=uid).first()
            uname = payload.get('username') or payload.get('user') or payload.get('user_name')
            if uname: return User.objects.filter(username=uname).first()
            cd = payload.get('customer_details') or {}
            email = payload.get('email') or cd.get('email')
            if email: return User.objects.filter(email=email).first()
            return None

        def find_restaurant(payload):
            rid = payload.get('restaurant_id') or payload.get('restaurant')
            if rid: return Restaurant.objects.filter(pk=rid).first()
            rname = payload.get('restaurant_name')
            if rname: return Restaurant.objects.filter(name__iexact=rname).first()
            return None

        def find_food_item(item_payload, restaurant=None):
            fid = item_payload.get('food_item_id') or item_payload.get('id')
            if fid: f = FoodItem.objects.filter(pk=fid).first(); 
            else: 
                fname = item_payload.get('name') or item_payload.get('food_item_name')
                if fname:
                    qs = FoodItem.objects.filter(name__iexact=fname)
                    if restaurant: qs = qs.filter(restaurant=restaurant)
                    f = qs.first()
                else: f = None
            return f

        saved_orders_info = []
        try:
            if order_data:
                with transaction.atomic():
                    user = find_user(order_data)
                    restaurant = find_restaurant(order_data)
                    items_payload = order_data.get('order_items') or []

                    if user and restaurant and items_payload:
                        total_price = sum(parse_decimal(it.get('price')) or 0 for it in items_payload)
                        total_qty = sum(int(it.get('qty', 1)) for it in items_payload)

                        order_obj = Order.objects.create(
                            user=user,
                            restaurant=restaurant,
                            quantity=total_qty,
                            total_price=total_price,
                            status=order_data.get('status', 'Pending')
                        )

                        for it in items_payload:
                            fi = find_food_item(it, restaurant=restaurant)
                            if fi:
                                order_obj.food_items.add(fi)

                        saved_orders_info.append({
                            'order_pk': order_obj.pk,
                            'items_count': len(items_payload),
                            'total_price': str(order_obj.total_price)
                        })
        except Exception as e:
            print("Error saving order:", str(e))

        async_to_sync(self.channel_layer.group_send)(
            room,
            {
                'type': 'chat_message',
                'username': username,
                'room': room,
                'order': order_data,
                'db_saved': saved_orders_info
            }
        )

    def chat_message(self, event):
        payload = {'type': 'chat', 'username': event.get('username'), 'room': event.get('room'), 'order': event.get('order')}
        if event.get('db_saved'): payload['db_saved'] = event.get('db_saved')
        self.send(text_data=json.dumps(payload))

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        except:
            pass
