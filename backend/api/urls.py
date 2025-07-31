from django.urls import path
from knox import views as knox_views
from api import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('', views.api_overview, name="api_overview"),
    path("token/", TokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh", TokenRefreshView.as_view(), name="refresh"),
    path('register-user/', views.register_user.as_view(),
         name="register_user"),
    path('login-user/', views.login_user.as_view(),
         name="login_user"),
    path('logout-user/', knox_views.LogoutView.as_view(), name='logout_user'),
    path('logout-all/', knox_views.LogoutAllView.as_view(), name='logout_all'),
    path('showuserorders/', views.show_user_order_history),
    path('viewcart/', views.view_cart),
    path('purchasecart/', views.purchase_cart),
    path('addtocart/', views.addtocart),
]
