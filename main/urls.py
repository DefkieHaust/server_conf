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
from authenticators import views as user_views
from market import views as market_views


urlpatterns = [
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('jet/', include('jet.urls', 'jet')),
    path("admin/", admin.site.urls),
    path("db/", include("data_browser.urls")),
    path("", page_views.home, name="home"),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path("register/", user_views.register, name="register"),
    path("logout/", user_views.logout_view, name="logout"),
    path("market/", market_views.market, name="market"),
    path("market/<int:id>", market_views.product, name="product"),
    path("cart/", market_views.cart, name="cart"),
    path("address/", user_views.address, name="address"),
    path("edit_profile/", user_views.edit_profile, name="edit_profile"),
    path("change_password/", user_views.change_password, name="change_password"),
    path('totp/setup/', user_views.totp_setup, name='totp_setup'),
    path('totp/verify/', user_views.totp_verify, name='totp_verify'),
    path('password-recovery/', user_views.password_recovery, name='password_recovery'),
    path('password-reset/confirm/<uidb64>/<token>/', user_views.custom_password_reset,
         name='password_reset_confirm'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
