from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.db.models import Prefetch
from django.apps import apps
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone


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
        Restaurant = apps.get_model("merchant", "Restaurant")
        return Order, OrderItem, Restaurant

    def _safe_image_url(self, obj, attr_name):
        """
        Try to obtain a URL from an image/file field or an external URL attribute.
        Mirrors the safe_url usage from the API side in spirit (but simple here).
        """
        try:
            f = getattr(obj, attr_name, None)
            if f:
                try:
                    return f.url
                except Exception:
                    return str(f)
        except Exception:
            pass
        return None

    def _get_user_phone(self, user_obj):
        phone = None
        if not user_obj:
            return None
        for attr in ('phone', 'phone_number', 'mobile', 'contact', 'telephone'):
            phone = getattr(user_obj, attr, None)
            if phone:
                break

        if not phone and hasattr(user_obj, 'user_profile'):
            profile = user_obj.user_profile
            phone = getattr(profile, 'phone', None) or getattr(
                profile, 'phone_number', None)

        if not phone and hasattr(user_obj, 'merchant_profile'):
            merchant = user_obj.merchant_profile
            phone = getattr(merchant, 'phone_number', None)

        return phone or None

    def _build_order_detail(self, order_obj):
        """
        Build the order dict in the exact shape & chronology used by the API response.
        """
        # order items
        items = []
        computed_total = Decimal('0.00')
        try:
            order_items_qs = order_obj.order_items.select_related(
                "food_item").all()
        except Exception:
            order_items_qs = []

        for oi in order_items_qs:
            fi = getattr(oi, "food_item", None)
            price_each = oi.price_at_order or (
                getattr(fi, 'price', Decimal('0.00')) if fi else Decimal('0.00'))
            item_total = (price_each or Decimal('0.00')) * (oi.quantity or 0)
            computed_total += item_total

            image_url = None
            if fi:
                try:
                    image_url = fi.profile_picture.url if getattr(
                        fi, 'profile_picture', None) else getattr(fi, 'external_image_url', None)
                except Exception:
                    image_url = getattr(fi, 'external_image_url', None)

            items.append({
                "id": getattr(oi, "pk", None),
                "food_item": getattr(fi, "pk", None),
                "food_item_name": getattr(fi, "name", "") if fi else "",
                "restaurant_name": getattr(getattr(fi, 'restaurant', None), 'restaurant_name', getattr(getattr(order_obj, 'restaurant', None), 'restaurant_name', '')) if fi or getattr(order_obj, 'restaurant', None) else '',
                "food_item_image": image_url,
                "quantity": getattr(oi, "quantity", 0),
                "price_at_order": str(price_each),
                "total_price": float(item_total),
            })

        # total price fallback to computed_total if order.total_price is falsy
        total_value = getattr(order_obj, "total_price", None) or computed_total

        # user info
        user_obj = getattr(order_obj, 'user', None)
        customer_name = user_obj.get_full_name() if user_obj and hasattr(
            user_obj, 'get_full_name') else (getattr(user_obj, 'username', '') if user_obj else '')

        # phone lookup like API
        phone = self._get_user_phone(user_obj)

        # deliveryman info
        deliveryman_obj = getattr(order_obj, 'deliveryman', None)
        deliveryman_data = None
        if deliveryman_obj:
            deliveryman_data = {
                "id": getattr(deliveryman_obj, 'id', None),
                "name": "{} {}".format(getattr(deliveryman_obj, 'Firstname', ''), getattr(deliveryman_obj, 'Lastname', '')).strip(),
                "email": getattr(deliveryman_obj, 'email', None),
                "phone": getattr(deliveryman_obj, 'phone', None),
            }

        # restaurant owner user info
        restaurant_user = getattr(
            getattr(order_obj, 'restaurant', None), 'user', None)
        restaurant_user_data = None
        if restaurant_user:
            restaurant_user_data = {
                "id": getattr(restaurant_user, 'id', None),
                "username": getattr(restaurant_user, 'username', ''),
                "first_name": getattr(restaurant_user, 'first_name', ''),
                "last_name": getattr(restaurant_user, 'last_name', ''),
                "email": getattr(restaurant_user, 'email', ''),
            }

        # restaurant data (many fields copied from API)
        rest = getattr(order_obj, 'restaurant', None)
        restaurant_data = None
        if rest:
            restaurant_data = {
                "id": getattr(rest, 'pk', None),
                "user": restaurant_user_data,
                "restaurant_name": getattr(rest, 'restaurant_name', ''),
                "owner_name": getattr(rest, 'owner_name', ''),
                "owner_email": getattr(rest, 'owner_email', ''),
                "owner_contact": getattr(rest, 'owner_contact', ''),
                "restaurant_address": getattr(rest, 'restaurant_address', ''),
                "latitude": getattr(rest, 'latitude', None),
                "longitude": getattr(rest, 'longitude', None),
                "cuisine": getattr(rest, 'cuisine', None),
                "description": getattr(rest, 'description', None),
                "restaurant_type": getattr(rest, 'restaurant_type', None),
                "profile_picture": self._safe_image_url(rest, 'profile_picture'),
                "cover_photo": self._safe_image_url(rest, 'cover_photo'),
                "menu": self._safe_image_url(rest, 'menu'),
                "created_at": getattr(rest, 'created_at', None).isoformat() if getattr(rest, 'created_at', None) else None,
                "approved": getattr(rest, 'approved', None),
            }

        # assemble final dict in same key order & names as API
        return {
            "order_id": getattr(order_obj, "pk", None),
            "user": {
                "id": getattr(user_obj, 'id', None),
                "username": getattr(user_obj, 'username', '') if user_obj else '',
                "first_name": getattr(user_obj, 'first_name', '') if user_obj else '',
                "last_name": getattr(user_obj, 'last_name', '') if user_obj else '',
                "email": getattr(user_obj, 'email', '') if user_obj else '',
            },
            "deliveryman": deliveryman_data,
            "restaurant_id": getattr(getattr(order_obj, 'restaurant', None), 'pk', None),
            "restaurant": restaurant_data,
            "is_transited": getattr(order_obj, 'is_transited', False),
            "delivery_charge": f"{(getattr(order_obj, 'delivery_charge', None) or Decimal('0.00')):.2f}",
            "total_price": f"{(total_value or Decimal('0.00')):.2f}",
            "order_items": items,
            "order_date": getattr(order_obj, 'order_date', None).isoformat() if getattr(order_obj, 'order_date', None) else None,
            "status": getattr(order_obj, 'status', None),
            "payment_method": (getattr(order_obj, 'payment_method', '') or '').lower(),
            "latitude": str(getattr(order_obj, 'latitude', None)) if getattr(order_obj, 'latitude', None) is not None else None,
            "longitude": str(getattr(order_obj, 'longitude', None)) if getattr(order_obj, 'longitude', None) is not None else None,
            "customer_details": {
                "email": getattr(user_obj, 'email', '') if user_obj else '',
                "phone": phone,
            },
            "assigned": getattr(order_obj, 'assigned', False),
        }

    def _normalize_serialized_order(self, s):
        """
        When socket receives serialized payload (not saved in DB), map to API shape.
        Keep the same key order as the API.
        """
        # minimal normalization - try to map known fields
        user_obj = s.get("user") or {}
        user_dict = {
            "id": user_obj.get("id") if isinstance(user_obj, dict) else None,
            "username": (user_obj.get("username") if isinstance(user_obj, dict) else (s.get("username") or s.get("customer_name") or "")),
            "first_name": user_obj.get("first_name") if isinstance(user_obj, dict) else '',
            "last_name": user_obj.get("last_name") if isinstance(user_obj, dict) else '',
            "email": user_obj.get("email") if isinstance(user_obj, dict) else s.get("email") or '',
        }

        # order_items normalization
        raw_items = s.get("order_items") or []
        items = []
        for oi in raw_items:
            items.append({
                "id": oi.get("id") if isinstance(oi, dict) else None,
                "food_item": oi.get("food_item") if isinstance(oi, dict) else None,
                "food_item_name": oi.get("food_item_name") if isinstance(oi, dict) else '',
                "restaurant_name": oi.get("restaurant_name") if isinstance(oi, dict) else '',
                "food_item_image": oi.get("food_item_image") if isinstance(oi, dict) else None,
                "quantity": oi.get("quantity") if isinstance(oi, dict) else 0,
                "price_at_order": str(oi.get("price_at_order")) if isinstance(oi, dict) else str(oi.get("price", '0.00')),
                "total_price": float(oi.get("total_price")) if isinstance(oi, dict) and oi.get("total_price") is not None else 0.0,
            })

        # derive delivery_charge and total_price
        delivery_charge = s.get("delivery_charge")
        total_price = s.get("total_price")

        # deliveryman
        deliveryman = s.get("deliveryman")

        # restaurant info (try to map restaurant_name or restaurant)
        restaurant_obj = s.get("restaurant") or {}
        restaurant_id = s.get("restaurant_id") or (restaurant_obj.get(
            "id") if isinstance(restaurant_obj, dict) else None)

        return {
            "order_id": s.get("id") or s.get("pk") or s.get("order_pk"),
            "user": user_dict,
            "deliveryman": deliveryman,
            "restaurant_id": restaurant_id,
            "restaurant": restaurant_obj if isinstance(restaurant_obj, dict) else None,
            "is_transited": s.get("is_transited", False),
            "delivery_charge": f"{delivery_charge:.2f}" if isinstance(delivery_charge, (int, float, Decimal)) else (delivery_charge if delivery_charge is not None else f"{Decimal('0.00'):.2f}"),
            "total_price": f"{total_price:.2f}" if isinstance(total_price, (int, float, Decimal)) else (total_price if total_price is not None else f"{Decimal('0.00'):.2f}"),
            "order_items": items,
            "order_date": s.get("order_date"),
            "status": s.get("status"),
            "payment_method": (s.get("payment_method") or '').lower(),
            "latitude": s.get("latitude"),
            "longitude": s.get("longitude"),
            "customer_details": {
                "email": user_dict.get("email", ""),
                "phone": (s.get("customer_details") or {}).get("phone") if isinstance(s.get("customer_details"), dict) else None,
            },
            "assigned": s.get("assigned", False),

        }

    def chat_message(self, event):
        try:
            payload_order = event.get("order")
            payload_db_saved = event.get("db_saved", [])
            errors = event.get("errors", [])
            # match API outer structure + chronology: {"success": True, "data": [...]}
            out_payload = {"type": "chat", "errors": errors, "success": True}
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
                Order, OrderItem, Restaurant = self._get_models()
                qs = Order.objects.select_related("user", "restaurant", "deliveryman").prefetch_related(
                    Prefetch(
                        "order_items", queryset=OrderItem.objects.select_related("food_item"))
                ).filter(pk__in=pks)
                detailed = [self._build_order_detail(o) for o in qs]
                # API nested result is in key "data" and is a list
                out_payload["data"] = detailed
            elif payload_order:
                if isinstance(payload_order, dict):
                    payload_list = [payload_order]
                else:
                    payload_list = payload_order if isinstance(
                        payload_order, list) else []
                normalized = [self._normalize_serialized_order(
                    s) for s in payload_list]
                out_payload["data"] = normalized
            else:
                out_payload["data"] = []

            # ensure JSON encodable for Decimal/datetime etc.
            self.send(text_data=json.dumps(out_payload, cls=DjangoJSONEncoder))
        except Exception:
            try:
                self.send(text_data=json.dumps(
                    {"type": "chat", "errors": ["consumer_error"], "success": False, "data": []}))
            except Exception:
                pass

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name, self.channel_name)
        except Exception:
            pass


class DeliverymanConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            self.close()
            return

        Deliveryman = apps.get_model("merchant", "Deliveryman")
        DeliverymanStatus = apps.get_model("merchant", "DeliverymanStatus")

        try:
            deliveryman = getattr(
                user, 'deliveryman_profile', None) or Deliveryman.objects.filter(user=user).first()
        except Exception:
            deliveryman = None

        if not deliveryman:
            self.close()
            return

        status_obj, _ = DeliverymanStatus.objects.get_or_create(
            deliveryman=deliveryman)
        status_obj.online = True
        status_obj.save(update_fields=['online'])

        self.deliveryman_pk = deliveryman.pk
        self.group_name = f"deliveryman_{self.deliveryman_pk}"

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name)
        async_to_sync(self.channel_layer.group_add)(
            "deliverymen", self.channel_name)

        self.accept()
        self.send(text_data=json.dumps({
            "type": "status",
            "status": "connected",
            "deliveryman_id": self.deliveryman_pk
        }))

    def disconnect(self, close_code):
        try:
            DeliverymanStatus = apps.get_model("merchant", "DeliverymanStatus")
            status_obj = DeliverymanStatus.objects.filter(
                deliveryman_id=self.deliveryman_pk).first()
            if status_obj:
                status_obj.online = False
                status_obj.save(update_fields=['online'])

            async_to_sync(self.channel_layer.group_discard)(
                self.group_name, self.channel_name)
            async_to_sync(self.channel_layer.group_discard)(
                "deliverymen", self.channel_name)
        except Exception:
            pass

    def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data) if text_data else {}
        except Exception:
            data = {}
        self.send(text_data=json.dumps({"type": "ack", "received": data}))

    def _get_models(self):
        Order = apps.get_model("merchant", "Order")
        OrderItem = apps.get_model("merchant", "OrderItem")
        Restaurant = apps.get_model("merchant", "Restaurant")
        return Order, OrderItem, Restaurant

    def _safe_image_url(self, obj, attr_name):
        try:
            f = getattr(obj, attr_name, None)
            if f:
                try:
                    return f.url
                except Exception:
                    return str(f)
        except Exception:
            pass
        return None

    def _get_user_phone(self, user_obj):
        phone = None
        if not user_obj:
            return None
        for attr in ('phone', 'phone_number', 'mobile', 'contact', 'telephone'):
            phone = getattr(user_obj, attr, None)
            if phone:
                break

        if not phone and hasattr(user_obj, 'user_profile'):
            profile = user_obj.user_profile
            phone = getattr(profile, 'phone', None) or getattr(
                profile, 'phone_number', None)

        if not phone and hasattr(user_obj, 'merchant_profile'):
            merchant = user_obj.merchant_profile
            phone = getattr(merchant, 'phone_number', None)

        return phone or None

    def _build_order_detail(self, order_obj):
        OrderItem = apps.get_model("merchant", "OrderItem")
        items = []
        computed_total = Decimal('0.00')
        try:
            order_items_qs = order_obj.order_items.select_related(
                "food_item").all()
        except Exception:
            order_items_qs = []

        for oi in order_items_qs:
            fi = getattr(oi, "food_item", None)
            price_each = oi.price_at_order or (
                getattr(fi, 'price', Decimal('0.00')) if fi else Decimal('0.00'))
            item_total = (price_each or Decimal('0.00')) * (oi.quantity or 0)
            computed_total += item_total

            image_url = None
            if fi:
                try:
                    image_url = fi.profile_picture.url if getattr(
                        fi, 'profile_picture', None) else getattr(fi, 'external_image_url', None)
                except Exception:
                    image_url = getattr(fi, 'external_image_url', None)

            items.append({
                "id": getattr(oi, "pk", None),
                "food_item": getattr(fi, "pk", None),
                "food_item_name": getattr(fi, "name", "") if fi else "",
                "restaurant_name": getattr(getattr(fi, 'restaurant', None), 'restaurant_name', getattr(getattr(order_obj, 'restaurant', None), 'restaurant_name', '')) if fi or getattr(order_obj, 'restaurant', None) else '',
                "food_item_image": image_url,
                "quantity": getattr(oi, "quantity", 0),
                "price_at_order": str(price_each),
                "total_price": float(item_total),
            })

        total_value = getattr(order_obj, "total_price", None) or computed_total
        user_obj = getattr(order_obj, 'user', None)
        phone = self._get_user_phone(user_obj)

        deliveryman_obj = getattr(order_obj, 'deliveryman', None)
        deliveryman_data = None
        if deliveryman_obj:
            deliveryman_data = {
                "id": getattr(deliveryman_obj, 'id', None),
                "name": "{} {}".format(getattr(deliveryman_obj, 'Firstname', ''), getattr(deliveryman_obj, 'Lastname', '')).strip(),
                "email": getattr(deliveryman_obj, 'email', None),
                "phone": getattr(deliveryman_obj, 'phone', None),
            }

        rest = getattr(order_obj, 'restaurant', None)
        restaurant_user_data = None
        if rest and getattr(rest, 'user', None):
            ru = rest.user
            restaurant_user_data = {
                "id": getattr(ru, 'id', None),
                "username": getattr(ru, 'username', ''),
                "first_name": getattr(ru, 'first_name', ''),
                "last_name": getattr(ru, 'last_name', ''),
                "email": getattr(ru, 'email', ''),
            }

        restaurant_data = None
        if rest:
            restaurant_data = {
                "id": getattr(rest, 'pk', None),
                "user": restaurant_user_data,
                "restaurant_name": getattr(rest, 'restaurant_name', ''),
                "owner_name": getattr(rest, 'owner_name', ''),
                "owner_email": getattr(rest, 'owner_email', ''),
                "owner_contact": getattr(rest, 'owner_contact', ''),
                "restaurant_address": getattr(rest, 'restaurant_address', ''),
                "latitude": getattr(rest, 'latitude', None),
                "longitude": getattr(rest, 'longitude', None),
                "cuisine": getattr(rest, 'cuisine', None),
                "description": getattr(rest, 'description', None),
                "restaurant_type": getattr(rest, 'restaurant_type', None),
                "profile_picture": self._safe_image_url(rest, 'profile_picture'),
                "cover_photo": self._safe_image_url(rest, 'cover_photo'),
                "menu": self._safe_image_url(rest, 'menu'),
                "created_at": getattr(rest, 'created_at', None).isoformat() if getattr(rest, 'created_at', None) else None,
                "approved": getattr(rest, 'approved', None),
            }

        return {
            "order_id": getattr(order_obj, "pk", None),
            "user": {
                "id": getattr(user_obj, 'id', None),
                "username": getattr(user_obj, 'username', '') if user_obj else '',
                "first_name": getattr(user_obj, 'first_name', '') if user_obj else '',
                "last_name": getattr(user_obj, 'last_name', '') if user_obj else '',
                "email": getattr(user_obj, 'email', '') if user_obj else '',
            },
            "deliveryman": deliveryman_data,
            "restaurant_id": getattr(rest, 'pk', None) if rest else None,
            "restaurant": restaurant_data,
            "is_transited": getattr(order_obj, 'is_transited', False),
            "delivery_charge": f"{(getattr(order_obj, 'delivery_charge', None) or Decimal('0.00')):.2f}",
            "total_price": f"{(total_value or Decimal('0.00')):.2f}",
            "order_items": items,
            "order_date": getattr(order_obj, 'order_date', None).isoformat() if getattr(order_obj, 'order_date', None) else None,
            "status": getattr(order_obj, 'status', None),
            "payment_method": (getattr(order_obj, 'payment_method', '') or '').lower(),
            "latitude": str(getattr(order_obj, 'latitude', None)) if getattr(order_obj, 'latitude', None) is not None else None,
            "longitude": str(getattr(order_obj, 'longitude', None)) if getattr(order_obj, 'longitude', None) is not None else None,
            "customer_details": {
                "email": getattr(user_obj, 'email', '') if user_obj else '',
                "phone": phone,
            },
            "assigned": getattr(order_obj, 'assigned', False),
            "assigned_to_other_deliveryman": getattr(order_obj, 'assigned_to_other_deliveryman', False),
            # <--- APPENDED FIELD
            "customer_location": getattr(order_obj, 'customer_location', '')
        }

    def notify(self, event):
        payload = event.get('payload', {}) or {}
        errors = event.get('errors', []) or []
        out_payload = {"type": "chat", "errors": errors, "success": True}

        try:
            pks = []
            db_saved = payload.get('db_saved') or []
            if db_saved and isinstance(db_saved, list):
                for s in db_saved:
                    if isinstance(s, dict) and s.get('order_pk'):
                        try:
                            pks.append(int(s.get('order_pk')))
                        except Exception:
                            pass

            if not pks:
                payload_order = payload.get('order') or payload
                if isinstance(payload_order, list):
                    for s in payload_order:
                        if isinstance(s, dict) and (s.get('id') or s.get('pk') or s.get('order_pk') or s.get('order_id')):
                            try:
                                pks.append(int(s.get('id') or s.get('pk') or s.get(
                                    'order_pk') or s.get('order_id')))
                            except Exception:
                                pass
                elif isinstance(payload_order, dict):
                    possible_id = payload_order.get('id') or payload_order.get(
                        'pk') or payload_order.get('order_pk') or payload_order.get('order_id')
                    if possible_id:
                        try:
                            pks.append(int(possible_id))
                        except Exception:
                            pass

            if pks:
                Order, OrderItem, _ = self._get_models()
                qs = Order.objects.select_related("user", "restaurant", "deliveryman").prefetch_related(
                    Prefetch(
                        "order_items", queryset=OrderItem.objects.select_related("food_item"))
                ).filter(pk__in=pks)
                detailed = [self._build_order_detail(o) for o in qs]
                out_payload["data"] = detailed
            else:
                out_payload["data"] = []

            self.send(text_data=json.dumps(out_payload, cls=DjangoJSONEncoder))

        except Exception:
            try:
                self.send(text_data=json.dumps({"type": "chat", "errors": [
                          "delivery_consumer_error"], "success": False, "data": []}))
            except Exception:
                pass

    def check_picked(self, event):
        payload = event.get("payload", {}) or {}
        try:
            self.send(text_data=json.dumps({
                "type": "check_picked",
                "payload": payload
            }, cls=DjangoJSONEncoder))
        except Exception:
            pass


class CurrentDeliveryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Access deliveryman_profile in async-safe way
        self.deliveryman = await sync_to_async(getattr)(self.scope["user"], "deliveryman_profile", None)
        if not self.deliveryman:
            await self.close()
            return

        self.group_name = f"deliveryman_{self.deliveryman.pk}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_current_delivery()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get("action") == "refresh":
            await self.send_current_delivery()

    async def current_delivery_update(self, event):
        await self.send_current_delivery()

    async def send_current_delivery(self):
        DeliverymanStatus = apps.get_model("merchant", "DeliverymanStatus")
        Order = apps.get_model("merchant", "Order")
        OrderItem = apps.get_model("merchant", "OrderItem")
        deliveryman = self.deliveryman

        # get_or_create wrapped in sync_to_async
        status_obj, _ = await sync_to_async(DeliverymanStatus.objects.get_or_create)(deliveryman=deliveryman)
        status_data = {
            "deliveryman_id": deliveryman.pk,
            "online": bool(status_obj.online),
            "on_delivery": bool(status_obj.on_delivery),
            "latitude": float(status_obj.latitude) if status_obj.latitude else None,
            "longitude": float(status_obj.longitude) if status_obj.longitude else None,
            "last_updated": status_obj.last_updated.isoformat() if status_obj.last_updated else None
        }

        if status_obj.on_delivery:
            await self.send(text_data=json.dumps({
                "status": status_data,
                "has_current_assignments": False,
                "orders": [],
                "returned_at": timezone.now().isoformat()
            }))
            return

        # Helper functions (no change)
        def _safe_image_url(obj, attr_name):
            f = getattr(obj, attr_name, None)
            if f:
                try:
                    return f.url
                except:
                    return str(f)
            return None

        def _get_user_phone(user_obj):
            if not user_obj:
                return None
            for attr in ('phone', 'phone_number', 'mobile', 'contact', 'telephone'):
                phone = getattr(user_obj, attr, None)
                if phone:
                    return phone
            if hasattr(user_obj, 'user_profile'):
                p = user_obj.user_profile
                return getattr(p, 'phone', None) or getattr(p, 'phone_number', None)
            if hasattr(user_obj, 'merchant_profile'):
                m = user_obj.merchant_profile
                return getattr(m, 'phone_number', None)
            return None

        def _build_order_detail(order_obj):
            items = []
            computed_total = Decimal('0.00')
            try:
                order_items_qs = order_obj.order_items.select_related(
                    "food_item").all()
            except:
                order_items_qs = []
            for oi in order_items_qs:
                fi = getattr(oi, "food_item", None)
                price_each = oi.price_at_order or (
                    getattr(fi, 'price', Decimal('0.00')) if fi else Decimal('0.00'))
                qty = oi.quantity or 0
                item_total = (price_each or Decimal('0.00')) * qty
                computed_total += item_total
                try:
                    image_url = fi.profile_picture.url if getattr(
                        fi, 'profile_picture', None) else getattr(fi, 'external_image_url', None)
                except:
                    image_url = getattr(fi, 'external_image_url', None)
                items.append({
                    "id": getattr(oi, "pk", None),
                    "food_item": getattr(fi, "pk", None),
                    "food_item_name": getattr(fi, "name", "") if fi else "",
                    "restaurant_name": getattr(getattr(fi, 'restaurant', None), 'restaurant_name', getattr(getattr(order_obj, 'restaurant', None), 'restaurant_name', '')) if fi or getattr(order_obj, 'restaurant', None) else '',
                    "food_item_image": image_url,
                    "quantity": qty,
                    "price_at_order": str(price_each),
                    "total_price": float(item_total),
                })
            total_value = getattr(order_obj, "total_price",
                                  None) or computed_total
            user_obj = getattr(order_obj, 'user', None)
            phone = _get_user_phone(user_obj)
            rest = getattr(order_obj, 'restaurant', None)
            restaurant_user_data = None
            if rest and getattr(rest, 'user', None):
                ru = rest.user
                restaurant_user_data = {
                    "id": getattr(ru, 'id', None),
                    "username": getattr(ru, 'username', ''),
                    "first_name": getattr(ru, 'first_name', ''),
                    "last_name": getattr(ru, 'last_name', ''),
                    "email": getattr(ru, 'email', ''),
                }
            restaurant_data = None
            if rest:
                restaurant_data = {
                    "id": getattr(rest, 'pk', None),
                    "user": restaurant_user_data,
                    "restaurant_name": getattr(rest, 'restaurant_name', ''),
                    "owner_name": getattr(rest, 'owner_name', ''),
                    "owner_email": getattr(rest, 'owner_email', ''),
                    "owner_contact": getattr(rest, 'owner_contact', ''),
                    "restaurant_address": getattr(rest, 'restaurant_address', ''),
                    "latitude": getattr(rest, 'latitude', None),
                    "longitude": getattr(rest, 'longitude', None),
                    "cuisine": getattr(rest, 'cuisine', None),
                    "description": getattr(rest, 'description', None),
                    "restaurant_type": getattr(rest, 'restaurant_type', None),
                    "profile_picture": _safe_image_url(rest, 'profile_picture'),
                    "cover_photo": _safe_image_url(rest, 'cover_photo'),
                    "menu": _safe_image_url(rest, 'menu'),
                    "created_at": getattr(rest, 'created_at', None).isoformat() if getattr(rest, 'created_at', None) else None,
                    "approved": getattr(rest, 'approved', None),
                }
            return {
                "order_assigned": bool(order_obj.assigned),
                "order_id": getattr(order_obj, "pk", None),
                "user": {
                    "id": getattr(user_obj, 'id', None),
                    "username": getattr(user_obj, 'username', '') if user_obj else '',
                    "first_name": getattr(user_obj, 'first_name', '') if user_obj else '',
                    "last_name": getattr(user_obj, 'last_name', '') if user_obj else '',
                    "email": getattr(user_obj, 'email', '') if user_obj else '',
                },
                "restaurant_id": getattr(rest, 'pk', None) if rest else None,
                "restaurant": restaurant_data,
                "is_transited": getattr(order_obj, 'is_transited', False),
                "delivery_charge": f"{(getattr(order_obj, 'delivery_charge', None) or Decimal('0.00')):.2f}",
                "total_price": f"{(total_value or Decimal('0.00')):.2f}",
                "order_items": items,
                "order_date": getattr(order_obj, 'order_date', None).isoformat() if getattr(order_obj, 'order_date', None) else None,
                "status": getattr(order_obj, 'status', None),
                "payment_method": (getattr(order_obj, 'payment_method', '') or '').lower(),
                "latitude": str(getattr(order_obj, 'latitude', None)) if getattr(order_obj, 'latitude', None) is not None else None,
                "longitude": str(getattr(order_obj, 'longitude', None)) if getattr(order_obj, 'longitude', None) is not None else None,
                "customer_details": {
                    "email": getattr(user_obj, 'email', '') if user_obj else '',
                    "phone": phone,
                },
                # <--- APPENDED FIELD
                "customer_location": getattr(order_obj, 'customer_location', '')
            }

        # Fetch queryset asynchronously
        order_qs = await sync_to_async(lambda: list(
            Order.objects.select_related("user", "restaurant", "deliveryman")
            .prefetch_related('order_items')
            .filter(deliveryman=deliveryman, assigned=True, status="WAITING_FOR_DELIVERY")
            .order_by('order_date')
        ))()

        # Build order details in a thread-safe way
        detailed_orders = []
        for o in order_qs:
            detail = await sync_to_async(_build_order_detail)(o)
            detailed_orders.append(detail)

        await self.send(text_data=json.dumps({
            "status": status_data,
            "has_current_assignments": bool(order_qs),
            "orders": detailed_orders,
            "returned_at": timezone.now().isoformat()
        }))
