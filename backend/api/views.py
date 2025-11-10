from django.utils import timezone
from django.db import transaction
from django.db.models import F
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework import generics, permissions, status, response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from decimal import Decimal, InvalidOperation
from math import radians, sin, cos, sqrt, atan2
import math
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .serializers import (
    AppUserSerializer,
    RegisterSerializer,
    EmailAuthTokenSerializer,
    FooditemSerial,
    Orderserializer,
    RestaurantSerial,
    CartSerializer,
    PlaceOrderSerializer,
    Restaurantlistserial,
    CartReadSerializer
)
from merchant.models import FoodItem, Restaurant, Order, Cart, OrderItem
from django.core.exceptions import ObjectDoesNotExist
from typing import List, Optional


def api_overview(request):
    api_urls = {
        'API': {
            'API overview': "/api/",
            'API token': "/api/token/",
            'API token refresh': "/api/token/refresh",
        },
        'User Authentication': {
            'Register App User': "/api/register-user/",
            'Login App User': "/api/login-user/",
            'Logout App User': "/api/logout-user/",
            'Logout All Sessions': "/api/logout-all/",
        },
        'Cart Management': {
            'View Cart': "/api/viewcart/",
            'Add to Cart': "/api/addtocart/",
            'Delete Cart Item': "/api/deletecartitem/",
            'Update Cart': "/api/updatecart/",
            'Purchase Cart': "/api/purchasecart/",
        },
        'Orders': {
            'Show User Orders': "/api/showuserorders/",
            'Place Order': "/api/place-order",
        },
        'Products': {
            'List Products': "/api/products/",
            'Get Product by ID': "/api/products/<int:pk>",
        },
        'Restaurants': {
            'Get Restaurant by ID': "/api/restaurants/<int:id>/",
            'Nearby Restaurants': "/api/nearby-restaurants/",
            'Restaurant Locations': "/api/restaurant-locations/",
        }
    }
    return render(request, 'api/api_overview.html', {'api_urls': api_urls})


class register_user(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': AppUserSerializer(user, context=self.get_serializer_context()).data,
        })


class login_user(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = EmailAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        refresh = RefreshToken.for_user(user)

        response = Response({
            'access': str(refresh.access_token),
            'email': user.email,
            'full_name': user.first_name
        })

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite='Lax'
        )

        return response


# -----------------------------
# ✅ NEW APPENDED VIEWS BELOW
# -----------------------------

class login_user_knox(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        serializer = EmailAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        response = super(login_user_knox, self).post(request, format=None)
        token_data = response.data

        token_data['email'] = user.email
        token_data['full_name'] = user.first_name

        return Response(token_data)


class ShopPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'per_page'


@api_view(['GET'])
@permission_classes([AllowAny])
def get_restaurant_list(request):
    query = Restaurant.objects.filter(approved=True)

    page_number = request.query_params.get('page', 1)
    per_page = request.query_params.get('per_page', 18)

    try:
        page_number = int(page_number)
        per_page = int(per_page)
    except ValueError:
        return Response({'error': 'Invalid pagination parameters'}, status=400)

    pag = Paginator(query, per_page)
    pagobj = pag.get_page(page_number)

    serializer = Restaurantlistserial(pagobj, many=True)
    response = Response(serializer.data)
    response['X-Total-Count'] = pag.count
    return response


class ShopPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'per_page'


@api_view(['GET'])
@permission_classes([AllowAny])
def product_list_view(request):
    queryset = FoodItem.objects.all()

    # Get query parameters
    category = request.query_params.get('category')
    res_type = request.query_params.get('res_category')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')

    if category and category.lower() != "all":
        queryset = queryset.filter(veg_nonveg__iexact=category)

    if res_type and res_type.lower() != "all":
        queryset = queryset.filter(
            restaurant__restaurant_type__iexact=res_type)

    if min_price:
        try:
            queryset = queryset.filter(price__gte=float(min_price))
        except ValueError:
            return Response({'error': 'min_price must be a number'}, status=status.HTTP_400_BAD_REQUEST)

    if max_price:
        try:
            queryset = queryset.filter(price__lte=float(max_price))
        except ValueError:
            return Response({'error': 'max_price must be a number'}, status=status.HTTP_400_BAD_REQUEST)

    page_number = request.query_params.get('_page', 1)
    per_page = request.query_params.get('_per_page', 6)
    try:
        page_number = int(page_number)
        per_page = int(per_page)
    except ValueError:
        return Response({'error': 'Pagination parameters must be integers'}, status=status.HTTP_400_BAD_REQUEST)
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page_number)
    serializer = FooditemSerial(page_obj, many=True)
    response = Response(serializer.data)
    response['X-Total-Count'] = paginator.count
    return response


class ShopPagination(PageNumberPagination):
    page_size = 5  # Changed from 6 to 5
    page_size_query_param = 'per_page'


class ShopPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'per_page'


@api_view(['GET'])
def get_most_ordered_food(request):
    # Get only food items that have been ordered, annotate them with order count
    most_ordered_foods = FoodItem.objects.filter(
        order_countno_of_ordersgt=0
    ).annotate(
        no_of_orders=F('order_count__no_of_orders')
    ).order_by('-no_of_orders')

    # Apply pagination (optional: comment out if not needed)
    paginator = ShopPagination()
    paginated_data = paginator.paginate_queryset(most_ordered_foods, request)

    # Serialize and return only the results array
    serializer = FooditemSerial(paginated_data, many=True)
    return Response(serializer.data, status=200)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def addtocart(request):
#     user = request.user
#     food_id = request.data.get('food_id')
#     restaurant_id = request.data.get('restaurant_id')
#     quantity = request.data.get('quantity')

#     if not all([food_id, restaurant_id, quantity]):
#         return Response(
#             {"message": "food_id, restaurant_id, and quantity are required."},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     try:
#         quantity = int(quantity)
#     except ValueError:
#         return Response({"message": "Quantity must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         food = FoodItem.objects.get(id=food_id)
#         restaurant = Restaurant.objects.get(id=restaurant_id)
#     except (FoodItem.DoesNotExist, Restaurant.DoesNotExist):
#         return Response({"message": "Invalid food or restaurant ID."}, status=status.HTTP_404_NOT_FOUND)

#     total_price = food.price * quantity
#     if total_price < 300:
#         return Response({"message": "Minimum order amount is 300."}, status=status.HTTP_400_BAD_REQUEST)

#     order_data = {
#         "user": user.id,
#         "food_item": food.id,
#         "restaurant": restaurant.id,
#         "quantity": quantity,
#         "total_price": total_price
#     }

#     serializer = Orderserializer(data=order_data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(
#             {'message': 'Order placed successfully.', 'order': serializer.data},
#             status=status.HTTP_201_CREATED
#         )
#     else:
#         return Response(
#             {'message': 'Error, invalid data.', 'errors': serializer.errors},
#             status=status.HTTP_400_BAD_REQUEST
#         )
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addtocart(request):
    user = request.user
    food_id = request.data.get('food_id')
    restaurant_id = request.data.get('restaurant_id')
    quantity = request.data.get('quantity')

    if not all([food_id, restaurant_id, quantity]):
        return Response(
            {"message": "food_id, restaurant_id, and quantity are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        quantity = int(quantity)
    except ValueError:
        return Response({"message": "Quantity must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        food = FoodItem.objects.get(id=food_id)
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except (FoodItem.DoesNotExist, Restaurant.DoesNotExist):
        return Response({"message": "Invalid food or restaurant ID."}, status=status.HTTP_404_NOT_FOUND)

    total_price = food.price * quantity

    cart_data = {
        "user": user.id,
        "food_item": food.id,
        "restaurant": restaurant.id,
        "quantity": quantity,
        "total_price": total_price
    }

    serializer = CartSerializer(data=cart_data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'Item added to cart successfully.', 'cart': serializer.data},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {'message': 'Error, invalid data.', 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    serializer = CartReadSerializer(cart_items, many=True)

    return Response({
        "cart": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase_cart(request):
    user = request.user
    cart_items = Order.objects.filter(user=user, is_transited=False)

    if not cart_items.exists():
        return Response({"message": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

    cart_items.update(is_transited=True)

    serializer = Orderserializer(cart_items, many=True)
    return Response({
        "message": "Purchase successful.",
        "purchased_items": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_user_order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user, is_transited=True)

    if not orders.exists():
        return Response({'message': 'No orders found for this user.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = Orderserializer(orders, many=True)

    return Response({
        "order_history": serializer.data,
    }, status=status.HTTP_200_OK)


# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_cart(request):
#     user = request.user
#     order_id = request.data.get('order_id')
#     try:
#         order = Order.objects.get(id=order_id, user=user, is_transited=False)
#     except Order.DoesNotExist:
#         return Response({'message': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

#     order.delete()
#     return Response({'message': 'Order deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart(request):
    """Delete a cart item using cart_id from request body"""
    user = request.user
    cart_id = request.data.get('cart_id')

    if not cart_id:
        return Response(
            {'message': 'cart_id is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        cart_item = Cart.objects.get(cart_id=cart_id, user=user)
    except Cart.DoesNotExist:
        return Response(
            {'message': 'Cart item not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    cart_item.delete()
    return Response(
        {'message': 'Cart item deleted successfully.'},
        status=status.HTTP_204_NO_CONTENT
    )


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_cart(request):
#     user = request.user
#     food_id = request.data.get('food_id')
#     restaurant_id = request.data.get('restaurant_id')
#     quantity = request.data.get('quantity')

#     if not all([food_id, restaurant_id, quantity]):
#         return Response(
#             {"message": "food_id, restaurant_id, and quantity are required."},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     try:
#         quantity = int(quantity)
#     except ValueError:
#         return Response({"message": "Quantity must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         food = FoodItem.objects.get(id=food_id)
#         restaurant = Restaurant.objects.get(id=restaurant_id)
#     except (FoodItem.DoesNotExist, Restaurant.DoesNotExist):
#         return Response({"message": "Invalid food or restaurant ID."}, status=status.HTTP_404_NOT_FOUND)

#     # Delete the previous order if it exists
#     Order.objects.filter(user=user, food_item=food,
#                          restaurant=restaurant).delete()

#     # Recalculate total price
#     total_price = food.price * quantity
#     if total_price < 300:
#         return Response({"message": "Minimum order amount is 300."}, status=status.HTTP_400_BAD_REQUEST)

#     order_data = {
#         "user": user.id,
#         "food_item": food.id,
#         "restaurant": restaurant.id,
#         "quantity": quantity,
#         "total_price": total_price
#     }

#     serializer = Orderserializer(data=order_data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(
#             {'message': 'Order updated successfully.', 'order': serializer.data},
#             status=status.HTTP_200_OK
#         )
#     else:
#         return Response(
#             {'message': 'Error, invalid data.', 'errors': serializer.errors},
#             status=status.HTTP_400_BAD_REQUEST
#         )

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_cart(request):
#     user = request.user
#     order_id = request.data.get('order_id')
#     quantity = request.data.get('quantity')

#     if not all([order_id, quantity]):
#         return Response(
#             {"message": "order_id and quantity are required."},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     try:
#         quantity = int(quantity)
#         if quantity < 1:
#             raise ValueError
#     except ValueError:
#         return Response({"message": "Quantity must be a positive integer."},
#                         status=status.HTTP_400_BAD_REQUEST)

#     try:
#         order = Order.objects.get(id=order_id, user=user, is_transited=False)
#     except Order.DoesNotExist:
#         return Response({"message": "Cart item not found."},
#                         status=status.HTTP_404_NOT_FOUND)

#     order.quantity = quantity
#     order.total_price = order.food_item.price * quantity

#     if order.total_price < 300:
#         return Response({"message": "Minimum order amount is 300."},
#                         status=status.HTTP_400_BAD_REQUEST)

#     order.save()
#     serializer = Orderserializer(order)
#     return Response({'message': 'Cart updated successfully.', 'order': serializer.data},
#                     status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart(request):
    user = request.user
    cart_id = request.data.get('cart_id')  # renamed for clarity
    quantity = request.data.get('quantity')

    if not all([cart_id, quantity]):
        return Response(
            {"message": "cart_id and quantity are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError
    except ValueError:
        return Response({"message": "Quantity must be a positive integer."},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        cart_item = Cart.objects.get(cart_id=cart_id, user=user)
    except Cart.DoesNotExist:
        return Response({"message": "Cart item not found."},
                        status=status.HTTP_404_NOT_FOUND)

    cart_item.quantity = quantity
    cart_item.save()
    serializer = CartSerializer(cart_item)
    return Response({'message': 'Cart updated successfully.', 'cart': serializer.data},
                    status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order_status(request):
    user = request.user
    cart_id = request.data.get('cart_id')     # example: 10
    checked = request.data.get('checked')     # example: true / false

    # Validate inputs
    if cart_id is None or checked is None:
        return Response(
            {"message": "cart_id and checked are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Ensure 'checked' is boolean
    if isinstance(checked, str):
        if checked.lower() == 'true':
            checked = True
        elif checked.lower() == 'false':
            checked = False
        else:
            return Response(
                {"message": "checked must be true or false."},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Get the cart item for this user
    try:
        cart_item = Cart.objects.get(cart_id=cart_id, user=user)
    except Cart.DoesNotExist:
        return Response(
            {"message": "Cart not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    # ✅ Set checked field exactly as frontend sends
    cart_item.checked = checked
    cart_item.save()

    serializer = CartSerializer(cart_item)

    return Response(
        {
            'message': f'Cart status updated to {checked}.',
            'order': serializer.data
        },
        status=status.HTTP_200_OK
    )
    # user = request.user
    # cart_id = request.data.get('cart_id')
    # checked = request.data.get('checked')  # expecting True/False from frontend

    # if not all([cart_id, checked is not None]):
    #     return Response(
    #         {"message": "cart_id and status are required."},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )

    # # Validate status value (must be boolean-like)
    # if str(checked).lower() not in ['true', 'false']:
    #     return Response(
    #         {"message": "Status must be true or false."},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )

    # try:
    #     cart_item = Cart.objects.get(cart_id=cart_id, user=user)
    # except Cart.DoesNotExist:
    #     return Response({"message": "cart not found."},
    #                     status=status.HTTP_404_NOT_FOUND)

    # cart_item.checked = checked
    # cart_item.save()

    # serializer = CartSerializer(cart_item)

    # return Response(
    #     {'message': 'Cart status updated successfully.', 'order': serializer.data},
    #     status=status.HTTP_200_OK
    # )

    # user = request.user
    # cart_id = request.data.get('cart_id')  # expect a list like [1, 2, 3]
    # checked = request.data.get('checked')    # true/false from frontend
    # print(cart_id, checked)
    # if not cart_id or checked is None:
    #     return Response(
    #         {"message": "cart_id (list) and checked are required."},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )

    # # Validate input
    # if not isinstance(cart_id, list):
    #     return Response(
    #         {"message": "cart_ids must be a list."},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )

    # if str(checked).lower() not in ['true', 'false']:
    #     return Response(
    #         {"message": "checked must be true or false."},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )

    # # Get all matching cart items
    # cart_items = Cart.objects.filter(cart_id__in=cart_id, user=user)
    # if not cart_items.exists():
    #     return Response(
    #         {"message": "No matching cart items found."},
    #         status=status.HTTP_404_NOT_FOUND
    #     )

    # # Update all statuses
    # new_status = str(checked).lower() == 'true'
    # cart_items.update(checked=new_status)

    # serializer = CartSerializer(cart_items, many=True)

    # return Response(
    #     {
    #         'message': f'Status updated for {cart_items.count()} cart item(s).',
    #         'cart': serializer.data
    #     },
    #     status=status.HTTP_200_OK
    # )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_all_status(request):
    user = request.user
    cart_ids = request.data.get('cart_ids')  # list of IDs
    checked = request.data.get('checked')    # true/false

    if not cart_ids or checked is None:
        return Response({"message": "cart_ids and checked are required."}, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(checked, str):
        checked = checked.lower() == 'true'

    cart_items = Cart.objects.filter(cart_id__in=cart_ids, user=user)
    if not cart_items.exists():
        return Response({"message": "No cart items found."}, status=status.HTTP_404_NOT_FOUND)

    cart_items.update(checked=checked)
    serializer = CartSerializer(cart_items, many=True)

    return Response({
        "message": f"Checked status updated for {cart_items.count()} items.",
        "cart": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_restaurant_by_id(request, id):
    try:
        restaurant = Restaurant.objects.get(id=id)
        serializer = RestaurantSerial(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": "Restaurant not found"},
            status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order_api(request):
    try:
        user = request.user
    except User.DoesNotExist:
        return Response(
            {"detail": "Test user 'admin' not found."},
            status=status.HTTP_400_BAD_REQUEST
        )

    cart_ids = request.data.get('cart_ids')
    payment_method = request.data.get('payment_method')
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')

    if not cart_ids or not isinstance(cart_ids, list):
        return Response(
            {"detail": "cart_ids must be provided as a list."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if payment_method is None or latitude is None or longitude is None:
        return Response(
            {"detail": "payment_method, latitude and longitude are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        lat_dec = Decimal(str(latitude))
        lon_dec = Decimal(str(longitude))
    except (InvalidOperation, TypeError, ValueError):
        return Response(
            {"detail": "latitude and longitude must be numeric."},
            status=status.HTTP_400_BAD_REQUEST
        )

    cart_items = Cart.objects.filter(
        cart_id__in=cart_ids,
        user=user
    ).select_related('food_item', 'restaurant')

    if not cart_items.exists():
        return Response(
            {"detail": "No valid cart items found."},
            status=status.HTTP_400_BAD_REQUEST
        )

    created_orders = []
    restaurant_orders = {}
    errors = []

    for cart in cart_items:
        try:
            restaurant = cart.restaurant
            if restaurant.id not in restaurant_orders:
                order = Order.objects.create(
                    user=user,
                    restaurant=restaurant,
                    order_date=timezone.now(),
                    payment_method=payment_method,
                    latitude=lat_dec,
                    longitude=lon_dec,
                )
                restaurant_orders[restaurant.id] = order
                created_orders.append(order)
            else:
                order = restaurant_orders[restaurant.id]

            OrderItem.objects.create(
                order=order,
                food_item=cart.food_item,
                quantity=cart.quantity,
                price_at_order=cart.food_item.price or Decimal('0.00')
            )
            order.update_total_price()

        except Exception as exc:
            errors.append({
                "cart_id": cart.cart_id,
                "error": str(exc)
            })

    # Delete processed cart items (ignore failures)
    cart_items.delete()

    if not created_orders:
        return Response(
            {"detail": "No orders could be placed.", "errors": errors},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    serializer = PlaceOrderSerializer(
        created_orders, many=True, context={'request': request})
    serialized = serializer.data

    db_saved = [
        {
            "order_pk": order.pk,
            "restaurant": getattr(order.restaurant, "id", None),
            "total_price": str(order.total_price if order.total_price is not None else "0.00"),
            "status": order.status,
            "payment_method": getattr(order, "payment_method", None),
            "latitude": str(getattr(order, "latitude", None)),
            "longitude": str(getattr(order, "longitude", None)),
        }
        for order in created_orders
    ]

    try:
        channel_layer = get_channel_layer()
        payload = {
            "type": "chat_message",
            "order": serialized,
            "db_saved": db_saved,
            "errors": errors
        }
        async_to_sync(channel_layer.group_send)("order", payload)
    except Exception as exc:
        # Log the error or continue, since orders are already created
        errors.append({"channel_error": str(exc)})

    return Response(
        {
            "message": "Order(s) placed successfully." if created_orders else "Order placement failed.",
            "orders": serialized,
            "errors": errors
        },
        status=status.HTTP_201_CREATED if created_orders else status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_by_id(request, pk):
    try:
        product = FoodItem.objects.get(pk=pk)
        serializer = FooditemSerial(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except FoodItem.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * \
        math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


@api_view(['GET'])
@permission_classes([AllowAny])
def get_nearby_restaurants(request):
    try:
        user_lat = float(request.GET.get('latitude'))
        user_lon = float(request.GET.get('longitude'))
    except (TypeError, ValueError):
        return Response({"error": "Please provide valid 'latitude' and 'longitude' as query params."}, status=400)

    restaurants = Restaurant.objects.all()

    distances = []
    for restaurant in restaurants:
        distance = haversine_distance(
            user_lat, user_lon, restaurant.latitude, restaurant.longitude)
        distances.append((distance, restaurant))

    # Sort and select top 4 nearby
    distances.sort(key=lambda x: x[0])
    nearest_restaurants = [r for _, r in distances[:4]]

    serializer = RestaurantSerial(nearest_restaurants, many=True)
    return Response(serializer.data)


def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of Earth in kilometers (use 3956 for miles)
    R = 6371.0

    # Convert degrees to radians
    lat1_rad, lon1_rad = radians(lat1), radians(lon1)
    lat2_rad, lon2_rad = radians(lat2), radians(lon2)

    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c  # in kilometers
    return distance


@api_view(['GET'])
@permission_classes([AllowAny])
def restaurant_locations(request):
    restaurant_id = request.query_params.get('id')
    user_longitude = request.query_params.get('user_longitude')
    user_latitude = request.query_params.get('user_latitude')

    if not restaurant_id:
        return Response({'error': 'restaurant ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    if not user_latitude or not user_longitude:
        return Response({'error': 'User latitude and longitude are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Parse user lat/lon safely
        user_lat = float(user_latitude)
        user_lon = float(user_longitude)

        restaurant = Restaurant.objects.get(id=restaurant_id)
        distance = calculate_distance(
            user_lat, user_lon, restaurant.latitude, restaurant.longitude)

        return Response({
            'id': restaurant.id,
            'restaurant_name': restaurant.restaurant_name,
            'latitude': restaurant.latitude,
            'longitude': restaurant.longitude,
            'user_latitude': user_lat,
            'user_longitude': user_lon,
            'distance': round(distance, 2),
        }, status=status.HTTP_200_OK)

    except ValueError:
        return Response({'error': 'Latitude and longitude must be valid numbers'}, status=status.HTTP_400_BAD_REQUEST)

    except Restaurant.DoesNotExist:
        return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
