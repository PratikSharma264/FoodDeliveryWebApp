import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Prefetch


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "order"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name)
        self.accept()
        self.send(text_data=json.dumps(
            {"type": "status", "status": "connected"}))

    def receive(self, text_data):
        try:
            payload = json.loads(text_data)
        except Exception:
            payload = {}
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "chat_message", "order": payload, "db_saved": [], "errors": []},
        )

    def _get_models(self):
        from django.apps import apps
        Order = apps.get_model("merchant", "Order")
        OrderItem = apps.get_model("merchant", "OrderItem")
        return Order, OrderItem

    def _build_order_detail(self, order_obj):
        user = getattr(order_obj, "user", None)

        customer_name = getattr(user, "username", "—")
        customer_email = getattr(user, "email", "—")
        customer_phone = getattr(user, "phone", "—")

        total = getattr(order_obj, "total_price", 0)
        total_display = f"NPR {total:.2f}"

        return {
            "id": order_obj.pk,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_phone": customer_phone,
            "total_price": str(total),
            "total_display": total_display,
            "status": getattr(order_obj, "status", "PENDING"),
            "restaurant": getattr(getattr(order_obj, "restaurant", None), "name", str(getattr(order_obj.restaurant, "pk", ""))),
        }

    def chat_message(self, event):
        try:
            payload_order = event.get("order")
            payload_db_saved = event.get("db_saved", [])
            errors = event.get("errors", [])
            out_payload = {"type": "chat", "errors": errors}

            if isinstance(payload_order, list) and payload_order:
                out_payload["orders"] = payload_order
            elif isinstance(payload_order, dict) and payload_order:
                out_payload["orders"] = [payload_order]
            elif payload_db_saved:
                pks = []
                for s in payload_db_saved:
                    if isinstance(s, dict) and s.get("order_pk"):
                        try:
                            pks.append(int(s.get("order_pk")))
                        except Exception:
                            pass
                if pks:
                    Order, OrderItem = self._get_models()
                    qs = Order.objects.select_related("user", "restaurant").prefetch_related(
                        Prefetch(
                            "order_items", queryset=OrderItem.objects.select_related("food_item"))
                    ).filter(pk__in=pks)
                    detailed = [self._build_order_detail(o) for o in qs]
                    out_payload["orders"] = detailed
                else:
                    out_payload["orders"] = payload_db_saved
            else:
                out_payload["orders"] = []

            self.send(text_data=json.dumps(out_payload))
        except Exception:
            try:
                self.send(text_data=json.dumps(
                    {"type": "chat", "errors": ["consumer_error"]}))
            except Exception:
                pass

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name, self.channel_name)
        except Exception:
            pass
