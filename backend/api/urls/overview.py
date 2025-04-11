from django.urls import path
from api import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('', views.api_overview, name="api_overview"),
    path("token/", TokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh", TokenRefreshView.as_view(), name="refresh"),
]
