from django import forms
from django.core.exceptions import ValidationError

from .models import Rate, Comment


class RateCreationForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ("score",)
        widgets = {
            "score": forms.NumberInput(attrs={"min": 1, "max": 5, "class": "form-control"}),
        }
        labels = {
            "score": "Rate (1-5)",
        }

    def save(self, commit=True):
        rate = super().save(commit=False)
        if self.cleaned_data["doctor"] and self.cleaned_data["patient"]:
            rate.doctor = self.cleaned_data["doctor"]
            rate.patient = self.cleaned_data["patient"]
        else:
            raise ValidationError("Doctor and patient must be provided.")
        if commit:
            rate.save()
        return rate


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("title", "content")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        comment = super().save(commit=False)
        if self.cleaned_data["doctor"] and self.cleaned_data["patient"]:
            comment.doctor = self.cleaned_data["doctor"]
            comment.patient = self.cleaned_data["patient"]
        else:
            raise ValidationError("Doctor and patient must be provided.")
        if commit:
            comment.save()
        return comment
