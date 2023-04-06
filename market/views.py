from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Product

# Create your views here.


@login_required(login_url='/login/')
def market(resp):
    if resp.user.is_verified:
        relay = {
            "media_url": settings.MEDIA_URL,
            "products": Product.objects.filter(listed=True),
        }
        return render(resp, "pages/market.html", relay)
    else:
        return redirect("/")


@login_required(login_url='/login/')
def product(resp, id):
    if resp.user.is_verified:
        if (item := Product.objects.filter(pk=id)[0]):
            relay = {
                "media_url": settings.MEDIA_URL,
                "product": item,
                "variations": item.variations.all(),
            }
            return render(resp, "pages/product.html", relay)
        else:
            return redirect("/market/")
    else:
        return redirect("/")
