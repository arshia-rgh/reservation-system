from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Patient


class RegisterForm(UserCreationForm):
    date_of_birth = forms.DateField(help_text='Required. Format= YYYY-MM-DD')
    phone_number = forms.CharField(max_length=13, help_text='Required')
    address = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'address')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            patient = Patient(user=user, phone_number=self.cleaned_data['phone_number'],
                              birth_date=self.cleaned_data['date_of_birth'], address=self.cleaned_data['address'])

            patient.save()

        return user
