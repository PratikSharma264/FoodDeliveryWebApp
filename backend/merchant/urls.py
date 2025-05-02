from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.merchant_home_view, name='home'),

    path("signuplogin/", views.merchant_signuplogin_view, name='signup_login'),

    path("forgetpassword/", views.merchant_forgetpassword_view,
         name='forget_password'),

     path('merchant/reset-password/<uidb64>/<token>/', views.merchant_reset_password_view, 
     name='merchant_reset_password'),

    path("registerresturant/", views.merchant_res_reg_view,
         name='restaurant_register'),

    path("registerdeliveryman/", views.merchant_del_reg_view,
         name='deliveryman_register'),

    path("dashboard/", views.merchant_dashboard, name='merchant-dashboard'),
    path("formsignup/", views.merchant_form_signup, name='form_signup'),
    path("formlogin/", views.merchant_form_login, name='form_login'),
    path("formresreg/", views.merchant_form_res_reg, name='form_res_reg'),
    path("formdelreg/", views.merchant_form_del_reg, name='form_del_reg'),
    path("register-deliveryman/", views.deliveryman_register_view,
         name='deliveryman_register'),

    path("register-restaurant/", views.merchant_res_reg_view,
         name='restaurant_register'),
         
    path("login/", views.merchant_login_view, name='signup_login'),
    path("dashboard/", views.merchant_dashboard, name='merchant-dashboard'),
    path("logout/", views.merchant_logout_view, name='merchant-logout'),
]
