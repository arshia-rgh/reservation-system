from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .models import Patient
from django.contrib.auth.models import Permission

class LoginUsernameForm(AuthenticationForm):
    pass


class LoginEmailForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"placeholder": "Enter email-address"}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


class OtpForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"placeholder": "Enter email-address"}))
    otp_code = forms.CharField(max_length=6, required=False, widget=forms.TextInput(attrs={"placeholder": "Enter OTP"}))


class RegisterForm(UserCreationForm):
    birth_date = forms.DateField(help_text="Required. Format= YYYY-MM-DD")
    phone_number = forms.CharField(
        max_length=13,
        help_text="Required",
        validators=[RegexValidator(r"^(09|\+989)\d{9}$", "Invalid Iranian phone number.")],
    )
    address = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "birth_date",
            "address",
        )
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.user_permissions.add(Permission.objects.get(codename='view_patient')) 
            user.user_permissions.add(Permission.objects.get(codename='change_patient'))  
            patient = Patient(
                user=user,
                phone_number=self.cleaned_data["phone_number"],
                birth_date=self.cleaned_data["birth_date"],
                address=self.cleaned_data["address"],
            )
            patient.save()

        return user


class UpdatePatientForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=13,
        required=False,
        widget=forms.widgets.TextInput
        )
    address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.widgets.Textarea,
    )
    birth_date = forms.DateField(
        required=False,
        widget=forms.widgets.SelectDateWidget( years = [n for n in range(1960,2024)]),
        )
    
    class Meta:
        model = Patient
        fields = [
            "phone_number",
            "address",
            "birth_date",
        ]

class TransactionForm(forms.ModelForm):
    """
    A form for patient to have a transaction
    """
    CHOICES_TRANSACTION = [
        ("W","WITHRAW"),
        ("D","DIPOSIT"),
    ]

    transaction_type = forms.ChoiceField(
        choices=CHOICES_TRANSACTION,
        required=True,
        )
    
    amount = forms.IntegerField(
        required=True,
        help_text= "how much (IRR) ?",
        min_value=0,
        )
    
    class Meta:
        model = Patient
        fields=["wallet"]
        exclude = ["wallet"]
        
    def save(self, commit=True):
        match (self.cleaned_data["transaction_type"]):
            case "W":
                if self.cleaned_data["amount"] <= self.instance.wallet:
                    self.instance.wallet -= self.cleaned_data["amount"]
                    if commit:
                        self.instance.save()
                    return "Withraw Is Done!"
                else:
                    return "Unable to do Transaction, Please try again."
                
            case "D":
                    self.instance.wallet += self.cleaned_data["amount"]
                    if commit:
                        self.instance.save()
                    return "Deposit Successfull !"
                    