from rest_framework import permissions
from knox.auth import TokenAuthentication
from rest_framework import generics, permissions
from knox.models import AuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import AppUserSerializer  # your serializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from .serializers import AppUserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


from knox.views import LoginView as KnoxLoginView
from .serializers import AppUserSerializer, RegisterSerializer, EmailAuthTokenSerializer
from rest_framework.response import Response
from django.contrib.auth import login
from knox.models import AuthToken
from rest_framework import generics
from knox.auth import TokenAuthentication
from rest_framework import permissions


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
