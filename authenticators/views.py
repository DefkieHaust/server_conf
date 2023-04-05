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
                return redirect("/")
        else:
            form = RegisterForm()
        relay = {"form": form}
        return render(resp, "pages/register.html", relay)