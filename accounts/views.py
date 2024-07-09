from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import RegisterForm, LoginForm


class RegisterView(CreateView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("login")


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm


def logout_view(request):
    logout(request)
    return redirect("/")
