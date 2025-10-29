from django.contrib import admin
from .models import Merchant, Restaurant, FoodItem, Order, OrderItem, Delivery, Deliveryman, Cuisine, FoodOrderCount, GoToDashClickCheck
# Register your models here.

admin.site.register(Merchant)
admin.site.register(Restaurant)
admin.site.register(FoodItem)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(Deliveryman)
admin.site.register(Cuisine)
admin.site.register(FoodOrderCount)
admin.site.register(GoToDashClickCheck)
admin.site.register(OrderItem)
