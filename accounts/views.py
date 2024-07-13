from django.utils import timezone as tz
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View

from accounts.forms import (LoginForm, RegisterForm, TransactionForm,
                            UpdatePatientForm)

from .models import Patient


class RegisterView(CreateView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:login")


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    authentication_form = LoginForm
    redirect_authenticated_user= True
    redirect_field_name="dashboard"
    

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
    permission_required="accounts.view_patient"
    template_name = "accounts/dashboard.html"

    
    def get_context_data(self, **kwargs):
        pass
    
    def get(self,request):
        patient = get_object_or_404(Patient, user= request.user)
        context ={"now": tz.now() }
        context["patient"] = patient
        context["appointments"] = {
            "attended": patient.appointments.filter(attended=True),
            "not_attended": patient.appointments.filter(attended=False),
        }

        return render(request, "accounts/dashboard.html", context)


class ProfileView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    A View linked to the patient's profile
    """
    login_url = "login/"
    permission_required = "accounts.view_patient"
    template_name = "accounts/profile.html"

    def get(self,request):
        patient = get_object_or_404(Patient, user= request.user)
        patient_form = UpdatePatientForm(
            request.POST,
            instance= patient,
        )
        return render(
            request,
            "accounts/profile.html",
            context={
                "patient_data":patient.__dict__,
                "patient_form":patient_form
                }
            )
    
    def post(self,request):
        patient = get_object_or_404(Patient, user= request.user)
        patient_form = UpdatePatientForm(
            request.POST,
            instance=patient)
        if patient_form.is_valid():
           patient_form.save()
           messages.success(request,"Successfully updated patient")
           return render(
            request,
            "accounts/profile.html",
            context={
                "patient_data":patient.__dict__,
                "patient_form":patient_form
                }
           )
        else:
            messages.error(request, "not valid, please try again.")
            return redirect(to="accounts:patient")
        

class WalletView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "login/"
    permission_required = ("accounts.change_patient","accounts.view_patient")
    
    def get(self,request):
        patient = get_object_or_404(Patient, user= request.user)
        transaction_form = TransactionForm()
        return render(
            request,
            "accounts/transact.html",
            context={
                "wallet_balance":patient.wallet,
                "transaction_form":transaction_form,
            }
        )
    def post(self,request):
        patient = get_object_or_404(Patient, user= request.user)
        transaction_form = TransactionForm(
            request.POST,
            instance=patient)
        if transaction_form.is_valid():
            message = transaction_form.save()
            messages.success(request,message)
        return redirect(to="accounts:wallet")
        