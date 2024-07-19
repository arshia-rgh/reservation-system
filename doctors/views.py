from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from doctors.models import Doctor, Schedule

from .forms import ScheduleForm


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = "doctors/detail.html"


class DoctorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Doctor
    template_name = "doctors/create.html"
    permission_required = "is_staff"
    fields = '__all__'

    def get_success_url(self):
        return reverse("doctors:schedule-create", kwargs={'pk' : self.object.pk})


class DoctorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Doctor
    template_name = "doctors/update.html"
    permission_required = "is_staff"
    fields = '__all__'
    
    def get_success_url(self):
        return reverse("doctors:schedule-update", kwargs={'pk' : self.object.pk})


class DoctorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Doctor
    template_name = "doctors/delete.html"
    permission_required = "is_staff"
    success_url = reverse_lazy("home:index")


class ScheduleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Schedule
    template_name = "doctors/schedule.html"
    permission_required = "is_staff"
    form_class = ScheduleForm
    
    def form_valid(self, form):
        doctor = Doctor.objects.get(pk=self.kwargs["pk"])
        form.instance.doctor = doctor
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("doctors:detail", kwargs={'pk' : self.object.doctor.pk})
    
class ScheduleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Schedule
    template_name = "doctors/schedule.html"
    permission_required = "is_staff"
    form_class= ScheduleForm

    def form_valid(self, form):
        doctor = Doctor.objects.get(pk=self.kwargs["pk"])
        form.instance.doctor = doctor
        return super().form_valid(form)
    
    def post(self,request):
        form = ScheduleForm(
            request.POST,
            instance = self.kwargs["pk"])

    def get_success_url(self):
        return reverse("doctors:detail", kwargs={'pk' : self.object.doctor.pk})