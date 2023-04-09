from uuid import uuid4
from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from accounts.models import User

# Create your models here.

payment_opts = [
        ("crypto", "crypto"),
        ("bank", "bank"),
        ("cash", "cash"),
    ]


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


class CartItem(models.Model):
    user = models.ForeignKey(
                User,
                on_delete=models.CASCADE,
                related_name='cart',
            )
    item = models.ForeignKey(
                Variation,
                on_delete=models.CASCADE,
            )
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.user} > {self.item}"


class PaymentMethod(models.Model):
    name = models.CharField(unique=True, max_length=20)
    description = models.CharField(max_length=200)
    multiplier = models.FloatField(default=1.0, blank=True)
    type = models.CharField(max_length=20, choices=payment_opts)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
                User,
                on_delete=models.CASCADE,
                related_name='orders',
            )
    order_id = models.CharField(max_length=36, blank=True)
    payment_method = models.CharField(max_length=1000)
    pay_amount = models.FloatField()
    address = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    payment_received = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} > {self.order_id}"

    def save(self, *args, **kwargs):
        if not self.pk:
            # Only run the function if the object is being created
            self.order_id = str(uuid4())
        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(
                Order,
                on_delete=models.CASCADE,
                related_name='items',
            )
    item = models.ForeignKey(
                Variation,
                on_delete=models.CASCADE,
            )
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.order} > {self.item}"


@receiver(post_save, sender=Order)
def on_complete(sender, instance, *args, **kwargs):
    if instance.delivered and not instance.delivery_date:
        instance.delivery_date = timezone.now()
        instance.save()

@receiver(pre_save, sender=Product)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        existing_image = Product.objects.get(pk=instance.pk)
        if existing_image.image != instance.image:
            existing_image.image.delete(False)


def update_cart(request, variation, amount):

    if (cartitem := request.user.cart.filter(item=variation)):
        # cart item exists
        cartitem[0].amount = amount
        cartitem[0].save()
    else:
        # cart item doesn't exist
        new_cartitem = CartItem()
        new_cartitem.user = request.user
        new_cartitem.item = variation
        new_cartitem.amount = amount
        new_cartitem.save()


def create_order(request, total,  payment, address):
    new_order = Order()
    new_order.user = request.user
    new_order.payment_method = payment
    new_order.pay_amount = total
    new_order.address = address
    new_order.save()
    for item in request.user.cart.all():
        order_item = OrderItem()
        order_item.order = new_order
        order_item.item = item.item
        order_item.amount = item.amount
        item.delete()
        order_item.save()
