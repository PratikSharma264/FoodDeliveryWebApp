from django.contrib import admin
from .models import Merchant, Restaurant, FoodItem, Order
# Register your models here.

admin.site.register(Merchant)
admin.site.register(Restaurant)
admin.site.register(FoodItem)
admin.site.register(Order)
# admin.site.register(OrderItem)
# admin.site.register(Delivery)
# admin.site.register(Deliveryman)
# admin.site.register(Cuisine)
