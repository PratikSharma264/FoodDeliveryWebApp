from django.contrib.auth import login
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions, status, response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer

from rest_framework_simplejwt.tokens import RefreshToken

from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from .serializers import AppUserSerializer, RegisterSerializer, EmailAuthTokenSerializer, FooditemSerial, Orderserializer,RestaurantSerial
from merchant.models import FoodItem, Restaurant, Order
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator

import math

def api_overview(request):
    api_urls = {
        'API': {
            'API overview': "/api/",
            'API token': "/api/token/",
            'API token refresh': "/api/token/refresh",
        },
        'App User': {
            'Register App User': "/api/register-user/",
            'Login App User': "/api/login-user/",
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
            secure=True,
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
        queryset = queryset.filter(restaurant__restaurant_type__iexact=res_type)

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


from django.db.models import F
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
    if total_price < 300:
        return Response({"message": "Minimum order amount is 300."}, status=status.HTTP_400_BAD_REQUEST)

    order_data = {
        "user": user.id,
        "food": food.id,
        "restaurant": restaurant.id,
        "quantity": quantity,
        "total_price": total_price
    }

    serializer = Orderserializer(data=order_data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'Order placed successfully.', 'order': serializer.data},
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
    cart_items = Order.objects.filter(user=user, is_transited=False)
    serializer = Orderserializer(cart_items, many=True)

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
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart(request):
    user = request.user
    order_id = request.data.get('order_id')
    try:
        order = Order.objects.get(id=order_id, user=user,is_transited=False)
    except Order.DoesNotExist:
        return Response({'message': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

    order.delete()
    return Response({'message': 'Order deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart(request):
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

    # Delete the previous order if it exists
    Order.objects.filter(user=user, food_item=food, restaurant=restaurant).delete()

    #Recalculate total price
    total_price = food.price * quantity
    if total_price < 300:
        return Response({"message": "Minimum order amount is 300."}, status=status.HTTP_400_BAD_REQUEST)

    order_data = {
        "user": user.id,
        "food_item": food.id,
        "restaurant": restaurant.id,
        "quantity": quantity,
        "total_price": total_price
    }

    serializer = Orderserializer(data=order_data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'Order updated successfully.', 'order': serializer.data},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {'message': 'Error, invalid data.', 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


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
            status=status.HTTP_404_NOT_FOUND
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

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

@api_view(['GET'])
def get_nearby_restaurants(request):
    try:
        user_lat = float(request.GET.get('latitude'))
        user_lon = float(request.GET.get('longitude'))
    except (TypeError, ValueError):
        return Response({"error": "Please provide valid 'latitude' and 'longitude' as query params."}, status=400)

    restaurants = Restaurant.objects.all()

    distances = []
    for restaurant in restaurants:
        distance = haversine_distance(user_lat, user_lon, restaurant.latitude, restaurant.longitude)
        distances.append((distance, restaurant))

    # Sort and select top 4 nearby
    distances.sort(key=lambda x: x[0])
    nearest_restaurants = [r for _, r in distances[:4]]

    serializer = RestaurantSerial(nearest_restaurants, many=True)
    return Response(serializer.data)
