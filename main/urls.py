"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from pages import views as page_views
from authenticators import views as account_views
from market import views as market_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("db/", include("data_browser.urls")),
    path("", page_views.home, name="home"),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path("register/", account_views.register, name="register"),
    path("logout/", account_views.logout_view, name="logout"),
    path("market/", market_views.market, name="market"),
    path("market/<int:id>", market_views.product, name="product"),
    path("profile/", page_views.profile, name="profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
