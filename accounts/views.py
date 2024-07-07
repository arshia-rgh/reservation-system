from django.views.generic import CreateView
from django.urls import reverse_lazy

from accounts.forms import RegisterForm


class Register(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')
