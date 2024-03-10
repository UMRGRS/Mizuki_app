from django.contrib import admin
from .models import Order, Product, Categories, OrderDetail


# Register your models here.

admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Categories)
admin.site.register(OrderDetail)