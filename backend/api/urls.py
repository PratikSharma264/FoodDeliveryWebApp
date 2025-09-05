from django.urls import path
from knox import views as knox_views
from api import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import get_restaurant_by_id
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.api_overview, name="api_overview"),
    path("token/", TokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh", csrf_exempt(TokenRefreshView.as_view()), name="refresh"),
    path('register-user/', views.register_user.as_view(), name="register_user"),
    path('login-user/', views.login_user.as_view(), name="login_user"),
    path('logout-user/', knox_views.LogoutView.as_view(), name='logout_user'),
    path('logout-all/', knox_views.LogoutAllView.as_view(), name='logout_all'),

    path('showuserorders/', views.show_user_order_history),
    path('viewcart/', views.view_cart, name='view-cart'),
    path('purchasecart/', views.purchase_cart, name='purchase-cart'),
    path('addtocart/', views.addtocart, name='add-to-cart'),
    path('deletecartitem/', views.delete_cart, name='delete-cart'),
    path('updatecart/', views.update_cart, name='update-cart'),

    path('products/', views.product_list_view),
    path('products/<int:pk>', views.get_product_by_id),

    path('restaurants/<int:id>/', get_restaurant_by_id),
    path('nearby-restaurants/', views.get_nearby_restaurants,
         name='nearby-restaurants'),
    path('restaurant-locations/', views.restaurant_locations,
         name='restaurant-locations'),
    path('place-order', views.place_order_api, name='place-order'),
    path('resraurant-list/', views.get_restaurant_list),
]
