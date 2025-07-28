from rest_framework import permissions
from knox.auth import TokenAuthentication
from rest_framework import generics, permissions
from knox.models import AuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import AppUserSerializer ,FooditemSerial,Orderserializer # your serializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from .serializers import AppUserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import IsAuthenticated

from knox.views import LoginView as KnoxLoginView
from .serializers import AppUserSerializer, RegisterSerializer, EmailAuthTokenSerializer
from rest_framework.response import Response
from django.contrib.auth import login
from knox.models import AuthToken
from rest_framework import generics
from knox.auth import TokenAuthentication
from rest_framework import permissions
from merchant.models import FoodItem, Restaurant,Order

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
            'token': AuthToken.objects.create(user)[1]
        })



class login_user(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        serializer = EmailAuthTokenSerializer(
            data=request.data)  # 👈 using custom login serializer
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        response = super(login_user, self).post(request, format=None)
        token_data = response.data

        token_data['email'] = user.email
        token_data['full_name'] = user.first_name  # stored as first_name

        return Response(token_data)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addtocart(request, food_id, restaurant_id):
    user = request.user  # authenticated user from token

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
    user = request.user  # Get the currently authenticated user

    # Fetch all orders that are still in cart (not transited)
    cart_items = Order.objects.filter(user=user, is_transited=False)

    # Serialize the cart items
    serializer = Orderserializer(cart_items, many=True)

    return Response({
        "cart": serializer.data
    }, status=status.HTTP_200_OK)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase_cart(request):
    user = request.user

    # Get all cart items that haven't been purchased yet
    cart_items = Order.objects.filter(user=user, is_transited=False)

    if not cart_items.exists():
        return Response({"message": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

    # Update all items to mark them as purchased
    cart_items.update(is_transited=True)

    # Optionally return the updated orders
    serializer = Orderserializer(cart_items, many=True)
    return Response({
        "message": "Purchase successful.",
        "purchased_items": serializer.data
    }, status=status.HTTP_200_OK)