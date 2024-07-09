from django.contrib import messages
from django.views.generic import DetailView

from accounts.models import Patient
from doctors.forms import DoctorRateForm, DoctorCommentForm
from doctors.models import Doctor
from surveys.models import Rate, Comment


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
            score = rate_form.cleaned_data["score"]
            patient = Patient.objects.get(user=request.user)
            Rate.objects.create(doctor=doctor, patient=patient, score=score)
            messages.success(request, "Your rating has been submitted successfully.")

        if comment_form.is_valid():
            comment_title = comment_form.cleaned_data["title"]
            comment_content = comment_form.cleaned_data["content"]
            patient = Patient.objects.get(user=request.user)
            Comment.objects.create(
                doctor=doctor,
                patient=patient,
                title=comment_title,
                content=comment_content,
            )
            messages.success(request, "Your comment has been submitted successfully.")
        return self.get(request, *args, **kwargs)
