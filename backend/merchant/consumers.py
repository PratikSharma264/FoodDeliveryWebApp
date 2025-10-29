import json
import traceback
from decimal import Decimal
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import F
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

        order_payload = payload.get("order") or {}
        uid = order_payload.get("userId") or order_payload.get("user_id")
        rid = order_payload.get(
            "restaurantId") or order_payload.get("restaurant_id")
        food_ids_raw = order_payload.get(
            "foodIds") or order_payload.get("food_ids") or []

        try:
            User = apps.get_model("auth", "User")
            Order = apps.get_model("merchant", "Order")
            OrderItem = apps.get_model("merchant", "OrderItem")
            FoodItem = apps.get_model("merchant", "FoodItem")
            Restaurant = apps.get_model("merchant", "Restaurant")
            FoodOrderCount = apps.get_model("merchant", "FoodOrderCount")
        except Exception as e:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat_message", "order": order_payload,
                    "db_saved": [], "errors": [f"model_import_error: {str(e)}"]},
            )
            return

        def to_int(v):
            try:
                return int(v)
            except Exception:
                return None

        counts = {}
        for raw in food_ids_raw:
            fid = to_int(raw)
            if fid is None:
                continue
            counts[fid] = counts.get(fid, 0) + 1

        errors = []
        if not uid:
            errors.append("user_id_missing")
        if not rid:
            errors.append("restaurant_id_missing")
        if not counts:
            errors.append("no_valid_food_ids")

        if errors:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat_message", "order": order_payload,
                    "db_saved": [], "errors": errors},
            )
            return

        user = User.objects.filter(pk=uid).first()
        restaurant = Restaurant.objects.filter(pk=rid).first()
        if not user:
            errors.append("user_not_found")
        if not restaurant:
            errors.append("restaurant_not_found")
        if errors:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat_message", "order": order_payload,
                    "db_saved": [], "errors": errors},
            )
            return

        found_qs = FoodItem.objects.filter(
            pk__in=counts.keys(), restaurant=restaurant)
        found_items = {fi.pk: fi for fi in found_qs}
        requested_ids = set(counts.keys())
        found_ids = set(found_items.keys())
        missing_ids = sorted(list(requested_ids - found_ids))

        if not found_items:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat_message", "order": order_payload, "db_saved": [],
                    "errors": ["no_matching_food_items_for_restaurant"]},
            )
            return

        saved = []
        failed = []
        try:
            order_obj = Order.objects.create(
                user=user, restaurant=restaurant, status=order_payload.get("status", "PENDING"))
            running_total = Decimal("0.00")
            distinct_created = 0

            for fid, qty in counts.items():
                fi = found_items.get(fid)
                if not fi:
                    failed.append(fid)
                    continue
                try:
                    OrderItem.objects.create(
                        order=order_obj, food_item=fi, quantity=qty, price_at_order=fi.price)
                except Exception as e:
                    failed.append(fid)
                    traceback.print_exc()
                    continue

                updated = FoodOrderCount.objects.filter(food_item=fi).update(
                    no_of_orders=F("no_of_orders") + qty)
                if updated == 0:
                    try:
                        FoodOrderCount.objects.create(
                            food_item=fi, no_of_orders=qty)
                    except Exception:
                        # if concurrent create fails, attempt a second update
                        try:
                            FoodOrderCount.objects.filter(food_item=fi).update(
                                no_of_orders=F("no_of_orders") + qty)
                        except Exception:
                            traceback.print_exc()

                running_total += (fi.price or Decimal("0.00")) * Decimal(qty)
                distinct_created += 1

            order_obj.total_price = running_total
            order_obj.save(update_fields=["total_price"])

            saved.append({"order_pk": order_obj.pk, "distinct_items_created": distinct_created,
                         "missing_item_ids": missing_ids, "failed_item_ids": failed, "total_price": str(order_obj.total_price)})

        except Exception as e:
            traceback.print_exc()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat_message", "order": order_payload,
                    "db_saved": [], "errors": [f"db_error: {str(e)}"]},
            )
            return

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "chat_message", "order": order_payload,
                "db_saved": saved, "errors": []},
        )

    def chat_message(self, event):
        payload = {"type": "chat", "order": event.get("order")}
        if event.get("db_saved"):
            payload["db_saved"] = event.get("db_saved")
        if event.get("errors"):
            payload["errors"] = event.get("errors")
        self.send(text_data=json.dumps(payload))

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name, self.channel_name)
        except Exception:
            pass
