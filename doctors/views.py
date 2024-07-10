from django.views.generic import DetailView

from doctors.models import Doctor


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = "doctors/detail.html"
