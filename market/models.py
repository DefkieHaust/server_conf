from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from accounts.models import User

# Create your models here.


class Product(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.CharField(blank=True, max_length=1000)
    price = models.FloatField()
    image = models.ImageField(blank=True)
    listed = models.BooleanField()

    def __str__(self):
        return self.name


class Variation(models.Model):
    name = models.CharField(max_length=50)
    stock = models.IntegerField()
    product = models.ForeignKey(
            Product,
            on_delete=models.CASCADE,
            related_name='variations',
            )

    def __str__(self):
        return f"{self.product} > {self.name}"


class Cart(models.Model):
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            related_name="cart",
            )

    def __str__(self):
        return f"{self.user} > Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(
                Cart,
                on_delete=models.CASCADE,
                related_name='items',
            )
    item = models.ForeignKey(
                Variation,
                on_delete=models.CASCADE,
            )
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.cart.user} > {self.item}"


class PaymentMethod(models.Model):
    name = models.CharField(unique=True, max_length=20)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name="orders",
            )
    cart = models.ForeignKey(
                Cart,
                on_delete=models.CASCADE,
            )
    paymentmethod = models.ForeignKey(
                PaymentMethod,
                on_delete=models.CASCADE,
            )
    address = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField()

    def __str__(self):
        if self.completed:
            status = "Completed"
        else:
            status = "Pending"
        return f"Order by {self.user}/{self.paymentmethod}: {status}"


@receiver(pre_save, sender=Product)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        existing_image = Product.objects.get(pk=instance.pk)
        if existing_image.image != instance.image:
            existing_image.image.delete(False)


def update_cart(request, delete=False):
    variation = request.POST.get("variation")
    amount = request.POST.get("amount")
    variation_object = Variation.objects.filter(name=variation)[0]

    if (cart := Cart.objects.filter(user=request.user)):
        # cart exists
        if (cartitem := cart[0].items.filter(item=variation_object)):
            # cart item exists
            if delete:
                cartitem[0].delete()
            else:
                cartitem[0].amount = amount
                cartitem[0].save()
        else:
            # cart item doesn't exist
            new_cartitem = CartItem()
            new_cartitem.cart = cart[0]
            new_cartitem.item = variation_object
            new_cartitem.amount = amount
            new_cartitem.save()
    else:
        # cart doesn't exist
        Cart(user=request.user).save()
        update_cart(request)
