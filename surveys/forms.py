from django import forms

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


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("title", "content")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }