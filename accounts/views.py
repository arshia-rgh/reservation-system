from django.views.generic import CreateView

from accounts.forms import RegisterForm


class Register(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
