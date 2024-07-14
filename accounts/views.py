import secrets

from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView
from dotenv import load_dotenv

from accounts.forms import RegisterForm, LoginUsernameForm, LoginEmailForm, OtpForm
from .models import OtpToken

load_dotenv()


class RegisterView(CreateView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:login")


class LoginUsernameView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginUsernameForm


def login_by_email(request):
    if request.method == 'GET':
        form = LoginEmailForm()
        return render(request, 'accounts/login_by_email.html', context={"form": form})

    if request.method == "POST":
        form = LoginEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'accounts/login_by_email.html',
                              {'form': form, 'error': 'Invalid email or password.'})
        else:
            return render(request, 'accounts/login_by_email.html', {'form': form})


def send_otp(user, otp_code):
    subject = "Email Verification"
    message = f"""
                                   Hi {user.username}, here is your OTP {otp_code} 
                                   load_dotenv(os.path.join(BASE_DIR, ".env"))

                                   it expires in 5 minute.

                                   """
    sender = settings.EMAIL_HOST_USER
    receiver = [user.email, ]

    send_mail(
        subject,
        message,
        sender,
        receiver,
        fail_silently=False,
    )


def login_by_otp(request):
    if request.method == 'GET':
        form = OtpForm()
        return render(request, 'accounts/login_by_otp.html', {'form': form})
    elif request.method == 'POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            otp_code = form.cleaned_data.get('otp_code')
            user = User.objects.filter(email=email).first()
            if user:
                if otp_code:
                    otp_token = OtpToken.objects.filter(user=user, otp_code=otp_code,
                                                        otp_expires_at__gte=timezone.now()).first()
                    if otp_token:
                        login(request, user)
                        return redirect('/')
                    else:
                        return render(request, 'accounts/login_by_otp.html',
                                      {'form': form, 'error': 'Invalid or expired OTP.'})
                else:
                    otp_code = secrets.token_hex(3)
                    otp_expires_at = timezone.now() + timezone.timedelta(minutes=5)
                    OtpToken.objects.create(user=user, otp_code=otp_code, otp_expires_at=otp_expires_at)
                    send_otp(user, otp_code)
                    return render(request, 'accounts/login_by_otp.html',
                                  {'form': form, 'message': 'OTP sent to your email.'})
            else:
                return render(request, 'accounts/login_by_otp.html', {'form': form, 'error': 'Email not found.'})
        else:
            return render(request, 'accounts/login_by_otp.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect("/")
