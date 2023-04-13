from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from market.models import PaymentMethod, ShipmentMethod, create_order
from itertools import chain

# Create your views here.


def home(resp):
    return render(resp, "pages/index.html")


@login_required(login_url='/login/')
def cart(resp):
    if resp.user.is_verified:
        cartitems = resp.user.cart.all()
        total = 0
        for item in cartitems:
            total += item.amount * item.item.product.price
        orders = resp.user.orders.all()
        addresses = resp.user.addresses.all()
        pay_ms = PaymentMethod.objects
        ship_ms = ShipmentMethod.objects
        not_received = resp.user.orders.filter(payment_received=False)
        pay_mc = pay_mb = pay_mm = ""
        if resp.user.allow_crypto:
            pay_mc = pay_ms.filter(type="crypto")
        if resp.user.allow_bank:
            pay_mb = pay_ms.filter(type="bank")
        if resp.user.allow_cash:
            pay_mm = pay_ms.filter(type="cash")
        pay_mt = list(chain(pay_mc, pay_mb, pay_mm))
        if resp.method == "POST":
            print(resp.POST)
            if resp.POST.get("rm_s"):
                for i in resp.POST:
                    if i and i.isdigit():
                        try: resp.user.cart.get(pk=int(i)).delete()
                        except: pass
                return redirect("/cart/")
            elif resp.POST.get("placeorder"):
                pm_name = resp.POST.get("payment_method")
                sm_name = resp.POST.get("shipment_method")
                addrs = resp.POST.get("address")
                addrs_obj = resp.user.addresses.filter(pk=int(addrs))[0]
                pm_object = pay_ms.filter(name=pm_name)[0]
                sm_object = ship_ms.filter(name=sm_name)[0]
                p_total = (total * pm_object.multiplier) + sm_object.fee
                if p_total > 0 and not not_received:
                    payment = f"{pm_object.name}: {pm_object.description}"
                    create_order(
                            resp,
                            round(p_total, 2),
                            payment,
                            addrs_obj,
                            sm_object,
                        )
                return redirect("/cart/")
        relay = {
            "cartitems": cartitems,
            "total": round(total, 2),
            "orders": orders,
            "pay_ms": pay_mt,
            "ship_ms": ship_ms.all(),
            "addresses": addresses,
            "not_received" : not_received,
        }
        return render(resp, "pages/cart.html", relay)
    else:
        return redirect("/")
