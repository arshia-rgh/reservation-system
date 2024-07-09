from django.contrib import messages
from django.views.generic import DetailView

from accounts.models import Patient
from doctors.forms import DoctorRateForm, DoctorCommentForm
from doctors.models import Doctor


class DoctorDetailView(DetailView):
    model = Doctor
    context_object_name = "doctor"
    template_name = "doctors/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctor_rate_form"] = DoctorRateForm()
        context["doctor_comment_form"] = DoctorCommentForm()
        return context

    def post(self, request, *args, **kwargs):
        doctor = self.get_object()
        rate_form = DoctorRateForm(request.POST)
        comment_form = DoctorCommentForm(request.POST)

        if rate_form.is_valid():
            patient = Patient.objects.get(user=request.user)
            rate_form.cleaned_data["patient"] = patient
            rate_form.cleaned_data["doctor"] = doctor
            rate_form.save()
            messages.success(request, "Your rating has been submitted successfully.")
            return self.get(request, *args, **kwargs)
        elif comment_form.is_valid():
            patient = Patient.objects.get(user=request.user)
            comment_form.cleaned_data["patient"] = patient
            comment_form.cleaned_data["doctor"] = doctor
            comment_form.save()
            messages.success(request, "Your comment has been submitted successfully.")
            return self.get(request, *args, **kwargs)
        else:
            messages.warning(request, "Failed to submit your rating or comment.")
        return self.get(request, *args, **kwargs)
