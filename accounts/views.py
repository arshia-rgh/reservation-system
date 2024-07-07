from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import RegisterForm


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')
