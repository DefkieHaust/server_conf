from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from accounts.models import Address
from .forms import AddressForm

# Create your views here.


@login_required(login_url='/login/')
def address(resp):
    if resp.method == "POST":
        if resp.POST.get("address"):
            addr_obj = Address(user=resp.user)
            address_form = AddressForm(resp.POST, instance=addr_obj)
            if address_form.is_valid():
                address_form.save()
        else:
            for i in resp.POST:
                if i.isdigit():
                    resp.user.addresses.filter(pk=int(i))[0].delete()
        return redirect("/address/")
    addresses = resp.user.addresses.all()
    form_relay = {
        "user": resp.user,
    }
    relay = {
        "addressform": AddressForm(initial=form_relay),
        "addresses": addresses,
    }
    return render(resp, "pages/address.html", relay)
