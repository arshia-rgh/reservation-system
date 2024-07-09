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
        widgets["score"].input_type = "range"


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
