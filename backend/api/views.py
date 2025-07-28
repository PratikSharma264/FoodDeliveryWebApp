from django.contrib.auth import login
from django.shortcuts import render

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer

from rest_framework_simplejwt.tokens import RefreshToken

from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from .serializers import AppUserSerializer, RegisterSerializer, EmailAuthTokenSerializer


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
            'refresh': str(refresh),
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
