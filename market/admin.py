from django.contrib import admin
from .models import *
from accounts.models import *
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from jet.filters import DateRangeFilter


# Register your models here.


def check_shipped(modeladmin, request, queryset):
    queryset.update(shipped=True)

def check_payment_received(modeladmin, request, queryset):
    queryset.update(payment_received=True)


class AddressInline(admin.TabularInline):
    model = Address


class CartItemInline(admin.TabularInline):
    model = CartItem


class UserAdmin(admin.ModelAdmin):
    list_filter = (
        "is_staff",
        "insta",
        "is_verified",
        "allow_crypto",
        "allow_bank",
        "allow_cash",
        "local",
    )
    inlines = [
        AddressInline,
        CartItemInline,
    ]


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class InstaListFilter(admin.SimpleListFilter):
    title = _('Insta')
    parameter_name = 'insta'

    def lookups(self, request, model_admin):
        insta_set = set()
        for user in User.objects.all():
            insta_set.add((user.insta, user.insta))
        return sorted(insta_set)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user__insta=self.value())
        return queryset


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "orders",
        "payment_received",
        "shipped",
    ]
    list_filter = (
        "user",
        InstaListFilter,
        "order_id",
        "payment_method",
        "shipment_method",
        "address",
        "payment_received",
        "shipped",
        ("order_date", DateRangeFilter)
    )
    inlines = [
        OrderItemInline,
    ]
    actions = [
        check_payment_received,
        check_shipped,
    ]

    def orders(self, obj):
        try:
            data = [
                f"<strong>Insta:</strong> {obj.user.insta}",
                f"<strong>Name:</strong> {obj.address.name}",
                f"<strong>Address:</strong> {obj.address.street}",
                f"<strong>City:</strong> {obj.address.city}",
                f"<strong>Postcode:</strong> {obj.address.postcode}",
                f"<strong>Email:</strong> {obj.user.email}",
                f"<strong>Payment Method:</strong> {obj.payment_method}",
            ]
            return mark_safe("<br>".join(data))
        except Exception:
            return "null"


class VariationInline(admin.TabularInline):
    model = Variation


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        VariationInline,
    ]


class AddressAdmin(admin.ModelAdmin):
    list_filter = (
        "user",
        InstaListFilter,
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(PaymentMethod)
admin.site.register(ShipmentMethod)
admin.site.register(Address, AddressAdmin)
