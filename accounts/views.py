import secrets

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone as tz
from django.views.generic import CreateView, View
from dotenv import load_dotenv

from accounts.forms import LoginEmailForm, LoginUsernameForm, OtpForm, RegisterForm, TransactionForm, UpdatePatientForm
from .models import OtpToken, Patient

load_dotenv()


class RegisterView(CreateView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:login")


class LoginUsernameView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginUsernameForm


def login_by_email(request):
    if request.method == "GET":
        form = LoginEmailForm()
        return render(request, "accounts/login_by_email.html", context={"form": form})

    if request.method == "POST":
        form = LoginEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                return render(
                    request, "accounts/login_by_email.html", {"form": form, "error": "Invalid email or password."}
                )
        else:
            return render(request, "accounts/login_by_email.html", {"form": form})


def send_otp(user, otp_code):
    subject = "Email Verification"
    message = f"""
    Hi {user.username}, here is your OTP {otp_code} 
                                
    it expires in 5 minute.

    """
    sender = settings.EMAIL_HOST_USER
    receiver = [
        user.email,
    ]

    send_mail(
        subject,
        message,
        sender,
        receiver,
        fail_silently=False,
    )


def login_by_otp(request):
    if request.method == "GET":
        form = OtpForm()
        return render(request, "accounts/login_by_otp.html", {"form": form})
    elif request.method == "POST":
        form = OtpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            otp_code = form.cleaned_data.get("otp_code")
            user = User.objects.filter(email=email).first()
            if user:
                if otp_code:
                    otp_token = OtpToken.objects.filter(
                        user=user, otp_code=otp_code, otp_expires_at__gte=timezone.now()
                    ).first()
                    if otp_token:
                        login(request, user)
                        return redirect("/")
                    else:
                        return render(
                            request, "accounts/login_by_otp.html", {"form": form, "error": "Invalid or expired OTP."}
                        )
                else:
                    otp_code = secrets.token_hex(3)
                    otp_expires_at = timezone.now() + timezone.timedelta(minutes=5)
                    OtpToken.objects.create(user=user, otp_code=otp_code, otp_expires_at=otp_expires_at)
                    send_otp(user, otp_code)
                    return render(
                        request, "accounts/login_by_otp.html", {"form": form, "message": "OTP sent to your email."}
                    )
            else:
                return render(request, "accounts/login_by_otp.html", {"form": form, "error": "Email not found."})
        else:
            return render(request, "accounts/login_by_otp.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/")


class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Dashboard View provides a page for the patient to have access to :
        -profile details
        -wallet details
        -appointment details
    """

    login_url = "login/"
    permission_required=["accounts.view_patient"]
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        pass

    def get(self, request):

        try:
            patient = get_object_or_404(Patient, user=request.user)
        except Http404:
            return render(request, "404.html", status=404)

        context = {
            "now": tz.now(),
            "patient": patient,
            "appointments": {
                "attended": patient.appointments.filter(attended=True),
                "not_attended": patient.appointments.filter(attended=False),
            },
        }

        return render(request,
                        "accounts/dashboard.html",
                        context=context)


class AdminDashboardView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = "accounts/admin_dashboard.html"
    login_url = "login/"
    permission_required=["is_staff"]
    
    def get(self,request):
        return render(request ,
                      "accounts/admin_dashboard.html"
                    )


class ProfileView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    A View linked to the patient's profile
    """

    login_url = "login/"
    permission_required = "accounts.view_patient"
    template_name = "accounts/profile.html"

    def get(self, request):
        patient = get_object_or_404(Patient, user=request.user)
        patient_form = UpdatePatientForm(
            request.POST,
            instance=patient,
        )
        return render(
            request, "accounts/profile.html", context={"patient_data": patient.__dict__, "patient_form": patient_form}
        )

    def post(self, request):
        patient = get_object_or_404(Patient, user=request.user)
        patient_form = UpdatePatientForm(request.POST, instance=patient)
        if patient_form.is_valid():
            patient_form.save()
            messages.success(request, "Successfully updated patient")
            return render(
                request,
                "accounts/profile.html",
                context={"patient_data": patient.__dict__, "patient_form": patient_form},
                status=200,
            )
        else:
            messages.error(request, "not valid, please try again.")
            return redirect(to="accounts:profile")


class WalletView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    A view for transaction. Works with Patient.wallet. Uses a Transaction Form
    Currently, does not provide actual money transfering ability.
    """

    login_url = "login/"
    permission_required = ("accounts.change_patient", "accounts.view_patient")

    def get(self, request):
        patient = get_object_or_404(Patient, user=request.user)
        transaction_form = TransactionForm()
        return render(
            request,
            "accounts/transact.html",
            context={
                "wallet_balance": patient.wallet,
                "transaction_form": transaction_form,
            },
        )

    def post(self, request):
        patient = get_object_or_404(Patient, user=request.user)
        transaction_form = TransactionForm(request.POST, instance=patient)
        if transaction_form.is_valid():
            message = transaction_form.save()
            messages.success(request, message)
        return redirect(to="accounts:wallet")
