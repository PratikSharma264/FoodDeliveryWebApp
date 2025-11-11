import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Prefetch
from django.apps import apps


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
        Order = apps.get_model("merchant", "Order")
        OrderItem = apps.get_model("merchant", "OrderItem")
        return Order, OrderItem

    def _build_order_detail(self, order_obj):
        user = getattr(order_obj, "user", None)
        deliveryman = getattr(order_obj, "deliveryman", None)  # Added

        username = getattr(user, "username", "—") if user else "—"
        total = getattr(order_obj, "total_price", 0)
        total_display = f"NPR {total:.2f}" if total else f"NPR 0.00"

        delivery_charge = getattr(order_obj, "delivery_charge", 0)
        delivery_charge_display = f"NPR {delivery_charge:.2f}" if delivery_charge else f"NPR 0.00"

        items = []
        try:
            order_items_qs = order_obj.order_items.select_related(
                "food_item").all()
        except Exception:
            order_items_qs = []

        for oi in order_items_qs:
            fi = getattr(oi, "food_item", None)
            price = getattr(oi, "price_at_order", getattr(fi, "price", 0))
            qty = getattr(oi, "quantity", 0)
            line_total = (price or 0) * qty
            items.append({
                "food_item_name": getattr(fi, "name", "") if fi else "",
                "quantity": qty,
                "price_at_order": str(price),
                "line_total": str(line_total),
            })

        # Deliveryman info dict
        deliveryman_data = None
        if deliveryman:
            deliveryman_data = {
                "id": getattr(deliveryman, "id", None),
                "name": getattr(deliveryman, "name", ""),
                "email": getattr(deliveryman, "email", ""),
                "phone": getattr(deliveryman, "phone", ""),
            }

        return {
            "id": order_obj.pk,
            "user": {"username": username},
            "customer_name": username,
            "deliveryman": deliveryman_data,  # Added
            "total_price": str(total),
            "total_display": total_display,
            "delivery_charge": str(delivery_charge),
            "delivery_charge_display": delivery_charge_display,
            "status": getattr(order_obj, "status", "PENDING"),
            "restaurant": getattr(getattr(order_obj, "restaurant", None), "name",
                                  str(getattr(getattr(order_obj, "restaurant", None), "pk", ""))),
            "payment_method": getattr(order_obj, "payment_method", "—"),
            "latitude": str(getattr(order_obj, "latitude", None)),
            "longitude": str(getattr(order_obj, "longitude", None)),
            "order_items": items,
        }

    def _normalize_serialized_order(self, s):
        user_info = {}
        if isinstance(s.get("user"), dict):
            user_info["username"] = s["user"].get(
                "username") or s["user"].get("name") or "—"
        else:
            user_info["username"] = s.get(
                "customer_name") or s.get("username") or "—"
        return {
            "id": s.get("id") or s.get("pk") or s.get("order_pk"),
            "user": user_info,
            "customer_name": user_info.get("username"),
            "total_price": s.get("total_price"),
            "total_display": s.get("total_display") or (f"NPR {s.get('total_price')}" if s.get("total_price") else None),
            "delivery_charge": s.get("delivery_charge"),
            "delivery_charge_display": s.get("delivery_charge_display") or (f"NPR {s.get('delivery_charge')}" if s.get("delivery_charge") else None),
            "status": s.get("status"),
            "restaurant": s.get("restaurant_name") or s.get("restaurant"),
            "payment_method": s.get("payment_method"),
            "latitude": s.get("latitude"),
            "longitude": s.get("longitude"),
            "order_items": s.get("order_items") or [],
        }

    def chat_message(self, event):
        try:
            payload_order = event.get("order")
            payload_db_saved = event.get("db_saved", [])
            errors = event.get("errors", [])
            out_payload = {"type": "chat", "errors": errors}
            pks = []
            if payload_db_saved:
                for s in payload_db_saved:
                    if isinstance(s, dict) and s.get("order_pk"):
                        try:
                            pks.append(int(s.get("order_pk")))
                        except Exception:
                            pass
            if not pks and payload_order:
                if isinstance(payload_order, list):
                    for s in payload_order:
                        if isinstance(s, dict) and (s.get("id") or s.get("pk") or s.get("order_pk")):
                            try:
                                pks.append(int(s.get("id") or s.get(
                                    "pk") or s.get("order_pk")))
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
            elif payload_order:
                if isinstance(payload_order, dict):
                    payload_list = [payload_order]
                else:
                    payload_list = payload_order if isinstance(
                        payload_order, list) else []
                normalized = [self._normalize_serialized_order(
                    s) for s in payload_list]
                out_payload["orders"] = normalized
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
