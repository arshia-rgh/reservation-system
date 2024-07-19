from django.urls import path

from .views import (
    DashboardView,
    LoginUsernameView,
    ProfileView,
    RegisterView,
    WalletView,
    login_by_email,
    login_by_otp,
    logout_view,
)

app_name = "accounts"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginUsernameView.as_view(), name="login"),
    path("login/login-by-email/", login_by_email, name="login_by_email"),
    path("login/login-by-otp/", login_by_otp, name="login_by_otp"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("wallet/", WalletView.as_view(), name="wallet"),
]
