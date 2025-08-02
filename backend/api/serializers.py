from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from merchant.models import FoodItem, Restaurant, Order,FoodOrderCount, Cart


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name')  # use first_name for full_name


class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'password')

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        email = validated_data['email']
        password = validated_data['password']

        # Generate a dummy username from email
        username = email.split('@')[0]

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.first_name = full_name  # store full name in first_name
        user.save()
        return user


class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        attrs['user'] = user
        return attrs


class FooditemSerial(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'


class RestaurantSerial(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class Orderserializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = Order
        fields = ['cart_id','user', 'restaurant', 'food_item',
                  'quantity', 'is_transited', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField(read_only=True)  # uses AutoField from model

    class Meta:
        model = Cart
        fields = [
            'cart_id',
            'user',
            'restaurant',
            'food_item',
            'quantity',
            'total_price',
        ]
class FoodOrderCountSerializer(serializers.ModelSerializer):
    food_item = FooditemSerial(read_only=True)
    class Meta:
       model = FoodOrderCount
       fields = ['food_item' ]
