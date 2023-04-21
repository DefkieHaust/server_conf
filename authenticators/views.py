from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import RegisterForm, AddressForm, UpdateForm
from .models import Address


# Create your views here.


def register(resp):
    if resp.user.is_authenticated:
        return redirect("/")
    else:
        if resp.method == "POST":
            form = RegisterForm(resp.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(resp, user)
                return redirect("/")
        else:
            form = RegisterForm()
        relay = {"form": form}
        return render(resp, "pages/register.html", relay)


@login_required(login_url='/login/')
def logout_view(resp):
    logout(resp)
    return redirect("/login/")


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
    addresses = resp.user.addresses.all()
    form_relay = {
        "user": resp.user,
    }
    relay = {
        "addressform": AddressForm(initial=form_relay),
        "addresses": addresses,
    }
    return render(resp, "pages/address.html", relay)


@login_required(login_url='/login/')
def edit_profile(resp):
    if resp.method == "POST":
        update_form = UpdateForm(resp.POST, instance=resp.user)
        if update_form.is_valid():
            update_form.save()
    relay = {
        "updateform": UpdateForm(instance=resp.user),
    }
    return render(resp, "pages/edit_profile.html", relay)


@login_required(login_url='/login/')
def change_password(resp):
    if resp.method == 'POST':
        form = PasswordChangeForm(resp.user, resp.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(resp, user)
            return redirect("/")
    else:
        form = PasswordChangeForm(resp.user)
    relay = {
        'passwordform': form,
    }
    return render(resp, 'pages/change_password.html', relay)
