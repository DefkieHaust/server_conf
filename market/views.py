from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Product, Variation, PaymentMethod, ShipmentMethod, create_order, update_cart
from itertools import chain


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
            return redirect("/cart/")
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
                return redirect("/cart/")
            else:
                return redirect("/market/")
        elif (item := Product.objects.filter(pk=id, listed=True)[0]):
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


@login_required(login_url='/login/')
def cart(resp):
    if resp.user.is_verified:
        cartitems = resp.user.cart.all()
        total = 0
        for item in cartitems:
            total += item.amount * item.item.product.price
        addresses = resp.user.addresses.all()
        pay_ms = PaymentMethod.objects
        ship_ms = ShipmentMethod.objects
        not_received = resp.user.orders.filter(payment_received=False)
        pay_mc = pay_mb = pay_mm = ""
        if resp.user.allow_bank:
            pay_mb = pay_ms.filter(type="bank")
        if resp.user.allow_cash:
            pay_mm = pay_ms.filter(type="cash")
        if resp.user.allow_crypto:
            pay_mc = pay_ms.filter(type="crypto")
        pay_mt = list(chain(pay_mc, pay_mb, pay_mm))
        if resp.method == "POST":
            if resp.POST.get("rm_s"):
                for i in resp.POST:
                    if i and i.isdigit():
                        try: resp.user.cart.get(pk=int(i)).delete()
                        except: pass
                return redirect("/cart/")
            elif resp.POST.get("placeorder"):
                pm_name = resp.POST.get("payment_method").split("/")[0]
                sm_name = resp.POST.get("shipment_method").split("/")[0]
                addrs = resp.POST.get("address")
                addrs_obj = resp.user.addresses.filter(pk=int(addrs))[0]
                pm_object = pay_ms.filter(name=pm_name)[0]
                sm_object = ship_ms.filter(name=sm_name)[0]
                p_total = (total * pm_object.multiplier) + sm_object.fee
                detail = resp.POST.get("detail") or None
                if p_total > 0 and not not_received:
                    payment = f"{pm_object.name}: {pm_object.description}"
                    create_order(
                            resp,
                            round(p_total, 2),
                            payment,
                            addrs_obj,
                            sm_object,
                            detail,
                        )
                    return redirect("/")
            return redirect("/cart/")
        if resp.user.local:
            relay_ship_ms = ship_ms.all()
        else:
            relay_ship_ms = ship_ms.exclude(name="local")
        bank_pm = PaymentMethod.objects.filter(type="bank")
        try:
            btc = pay_ms.get(id=1).description
        except Exception:
            btc = "BTC"
        relay = {
            "cartitems": cartitems,
            "total": round(total, 2),
            "pay_ms": pay_mt,
            "ship_ms": relay_ship_ms,
            "addresses": addresses,
            "not_received": not_received,
            "banks": bank_pm,
            "btc": btc,
        }
        return render(resp, "pages/cart.html", relay)
    else:
        return redirect("/")
