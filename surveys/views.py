from enum import Enum

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView

from doctors.models import Doctor
from .forms import CommentCreationForm, RateCreationForm


class RateCommentCreateView(FormView):
    template_name = "surveys/rate_comment_create.html"

    class FormType(Enum):
        Rate = "rate"
        Comment = "comment"

    def get_doctor(self):
        return get_object_or_404(Doctor, pk=self.kwargs["doctor_pk"])

    def get_form_type(self):
        return self.FormType.Rate if "rate" in self.request.path else self.FormType.Comment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_form_type() == self.FormType.Rate:
            context["title"] = f"Rate for {self.get_doctor()}"
        else:
            context["title"] = f"Comment for {self.get_doctor()}"
        return context

    def form_valid(self, form):
        form.instance.doctor = self.get_doctor()
        form.instance.patient = self.request.user.patient
        form.save()
        if self.get_form_type() == self.FormType.Rate:
            messages.success(self.request, "Rating submitted successfully!")
        else:
            messages.success(self.request, "Comment submitted successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("doctors:detail", args=[self.kwargs["doctor_pk"]])

    def get_form_class(self):
        if self.get_form_type() == self.FormType.Rate:
            return RateCreationForm
        return CommentCreationForm
