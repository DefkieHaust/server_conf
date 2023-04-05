from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(blank=True, max_length=1000)
    price = models.FloatField()
    image = models.ImageField(blank=True)
    listed = models.BooleanField()

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Product)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        existing_image = Product.objects.get(pk=instance.pk)
        if existing_image.image != instance.image:
            existing_image.image.delete(False)


class Variation(models.Model):
    name = models.CharField(max_length=50)
    stock = models.IntegerField()
    product = models.ForeignKey(
            Product,
            on_delete=models.CASCADE,
            related_name='variations',
            )

    def __str__(self):
        return f"{self.product}: {self.name}"


class Cart(models.Model):
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            )


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
    address = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField()

    def __str__(self):
        if self.completed:
            status = "Completed"
        else:
            status = "Pending"
        return f"Order by {self.user}: {status}"
