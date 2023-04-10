from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Product)
admin.site.register(Variation)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(PaymentMethod)
admin.site.register(ShipmentMethod)
admin.site.register(Address)
