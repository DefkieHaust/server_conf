from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Product, Variation, update_cart

# Create your views here.


@login_required(login_url='/login/')
def market(resp):
    if resp.user.is_verified:
        if resp.method == "POST":
            print(resp.POST)
            id = int(list(resp.POST)[1])
            product_obj = Product.objects.get(pk=id)
            variation = Variation.objects.filter(product=product_obj)[0]
            update_cart(resp, variation, 1)
            return redirect("/profile/")
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
        if resp.method == "POST":
            variation = resp.POST.get("variation")
            amount = resp.POST.get("amount")
            variation_object = Variation.objects.filter(name=variation)[0]
            update_cart(resp, variation_object, amount)
            if resp.POST.get("purchase"):
                return redirect("/profile/")
            else:
                return redirect("/market/")
        elif (item := Product.objects.filter(pk=id)[0]):
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
