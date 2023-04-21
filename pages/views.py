from django.shortcuts import render

# Create your views here.


def home(resp):
    if resp.user.is_verified:
        orders = resp.user.orders.all()
        relay = {
            "orders": orders,
        }
        return render(resp, "pages/index.html", relay)
    else:
        return render(resp, "pages/index.html")
