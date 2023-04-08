from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from market.models import PaymentMethod, create_order

# Create your views here.


def home(resp):
    return render(resp, "pages/index.html")


@login_required(login_url='/login/')
def profile(resp):
    if resp.user.is_verified:
        cartitems = resp.user.cart.all()
        total = 0
        for item in cartitems:
            total += item.amount * item.item.product.price
        orders = resp.user.orders.all()
        pay_ms = PaymentMethod.objects
        if resp.method == "POST":
            print(resp.POST)
            if resp.POST.get("rm_s"):
                for i in resp.POST:
                    if i and i.isdigit():
                        try: resp.user.cart.get(pk=int(i)).delete()
                        except: pass
                return redirect("/profile/")
            elif resp.POST.get("placeorder"):
                pm_name = resp.POST.get("payment_method")
                pm_object = pay_ms.filter(name=pm_name)[0]
                p_total = total * pm_object.multiplier
                if p_total > 0:
                    payment = f"{pm_object.name}: {pm_object.description}"
                    address = resp.POST.get("address")
                    create_order(resp, round(p_total, 2), payment, address)
                    return redirect("/profile/")
        relay = {
            "cartitems": cartitems,
            "total": round(total, 2),
            "orders": orders,
            "pay_ms": pay_ms.all(),
        }
        return render(resp, "pages/profile.html", relay)
    else:
        return redirect("/")
