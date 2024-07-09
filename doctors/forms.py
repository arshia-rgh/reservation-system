from django import forms

from surveys.models import Rate, Comment


class DoctorRateForm(forms.ModelForm):
    """
    Form for rating a doctor.

    This form includes fields for rating (score).
    """

    class Meta:
        model = Rate
        fields = ["score"]
        labels = {
            "score": "Rate (1-5)",
        }
        widgets = {
            "score": forms.NumberInput(attrs={"min": 1, "max": 5}),
        }

    def save(self, commit=True):
        rate = super().save(commit=False)
        rate.patient = self.cleaned_data["patient"]
        rate.doctor = self.cleaned_data["doctor"]
        rate.save()
        return rate


class DoctorCommentForm(forms.ModelForm):
    """
    Form for commenting on a doctor.

    This form includes fields for comment.
    """

    class Meta:
        model = Comment
        fields = ["title", "content"]
        labels = {
            "title": "Title",
            "content": "Content",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Enter your title here", "class": "form-control"},
            ),
            "content": forms.Textarea(
                attrs={"placeholder": "Enter your comment here", "class": "form-control", "rows": 5},
            ),
        }

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.patient = self.cleaned_data["patient"]
        comment.doctor = self.cleaned_data["doctor"]
        comment.save()
        return comment
