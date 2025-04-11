from django.urls import path
from api.merchant import views

urlpatterns = [
    path('register/', views.RegisterMerchantView.as_view(),
         name="register_merchant"),

]
