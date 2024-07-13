from django.urls import path,include

from .views import (CustomLoginView, DashboardView, ProfileView, RegisterView,
                    WalletView, logout_view)

app_name = "accounts"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("wallet/", WalletView.as_view(), name="wallet" ),
]
