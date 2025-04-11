from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Merchant
from django.contrib.auth.models import Group


class MerchantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', write_only=True)
    password = serializers.CharField(
        source='user.password', write_only=True, style={'input_type': 'password'})
    email_address = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Merchant
        fields = [
            'username', 'password', 'email_address',
            'company_name', 'first_name', 'last_name', 'phone_number'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['username'],
            password=user_data['password'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
        )
        group = Group.objects.get(name='Merchant')
        user.groups.add(group)

        merchant = Merchant.objects.create(user=user, **validated_data)
        return merchant
