from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm

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
