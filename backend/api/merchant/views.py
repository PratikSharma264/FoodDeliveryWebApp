from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import MerchantSerializer
from .models import Merchant
from rest_framework.views import APIView


class RegisterMerchantView(generics.CreateAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [AllowAny]
