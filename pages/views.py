from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(resp):
    return render(resp, "pages/index.html")


@login_required(login_url='/login/')
def profile(resp):
    if resp.user.is_verified:
        return render(resp, "pages/base.html")
    else:
        return redirect("/")
