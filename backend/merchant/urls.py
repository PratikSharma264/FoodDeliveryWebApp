from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.merchant_signup_view, name='merchant-sign-up'),
    path("login/", views.merchant_login_view, name='merchant-login'),
    path("dashboard/", views.merchant_dashboard, name='merchant-dashboard'),
    path("logout/", views.merchant_logout_view, name='merchant-logout')
]
