from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.merchant_home_view, name='home'),

    path("email-sent/", views.email_sent_view, name='email-sent'),
    path("forgetpassword/", views.merchant_forgetpassword_view,
         name='forget_password'),

    path('merchant/reset-password/<uidb64>/<token>/', views.merchant_reset_password_view,
         name='merchant_reset_password'),

    #     path('dummy/', views.restaurant_register_view, name='dummy'),
    path("restaurant-dashboard/", views.restaurant_dashboard, name='restaurant-dashboard'),
       path("deliveryman-dashboard/", views.deliveryman_dashboard, name='deliveryman-dashboard'),
    path("formsignup/", views.merchant_form_signup, name='form_signup'),
    path("formlogin/", views.merchant_form_login, name='form_login'),
    path("formresreg/", views.merchant_form_res_reg, name='form_res_reg'),
    path("formdelreg/", views.merchant_form_del_reg, name='form_del_reg'),
    path("register-merchant/", views.deliveryman_register_view,
         name='merchant_register'),

    path("register-restaurant/", views.merchant_res_reg_view,
         name='restaurant_register'),
    path("application-status/", views.application_status_view,
         name="application-status"),

    path("signup/", views.merchant_signup_view, name='merchant-signup'),
    path("merchant/login/", views.merchant_login_view, name="merchant-signin"),
    path("logout/", views.merchant_logout_view, name='merchant-logout'),
    path("lobby/", views.lobby_view, name='lobby'),


]
