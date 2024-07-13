# Create your views here.
from django.views.generic import DetailView

from .models import Appointment


class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = "appointments/detail.html"