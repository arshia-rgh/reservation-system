from django.urls import path

from .views import RegisterView, LoginUsernameView, logout_view, LoginEmailView

app_name = "accounts"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginUsernameView.as_view(), name="login"),
    path("login/login-by-email/", LoginEmailView.as_view(), name="login_by_email"),
    path("logout/", logout_view, name="logout"),
]
