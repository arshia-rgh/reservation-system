import datetime
import enum

from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, TemplateView

from accounts.mixins import LoginPatientRequiredMixin
from appointments.models import Appointment
from appointments.order import Order
from doctors.models import Doctor, Schedule
from utils.zarinpal import send_request, verify


class PaymentMethod(enum.Enum):
    WALLET = "wallet"
    GATEWAY = "gateway"


class ShowWeeklyDoctorAvailabilityView(LoginPatientRequiredMixin, TemplateView):
    template_name = "appointments/show_weekly_doctor_availability.html"

    @staticmethod
    def get_current_week():
        current_date = timezone.now()

        start_date = current_date
        end_date = start_date + timezone.timedelta(days=7)
        return start_date, end_date

    @staticmethod
    def get_available_slots(doctor, start_date, end_date):
        def get_daily_slots(date):
            day_of_week = date.weekday() + 1
            availabilities = Schedule.objects.filter(doctor=doctor, day_of_week=day_of_week)

            available_slots = []
            slot_duration = timezone.timedelta(minutes=20)

            for availability in availabilities:
                start_time = timezone.make_aware(timezone.datetime.combine(date, availability.start_time))
                end_time = timezone.make_aware(timezone.datetime.combine(date, availability.end_time))

                current_time = start_time
                while current_time + slot_duration <= end_time:
                    slot_end = current_time + slot_duration
                    if not Appointment.objects.filter(
                            Q(start_date__gte=current_time) & Q(start_date__lt=slot_end)
                    ).exists():
                        available_slots.append((current_time, True))
                    else:
                        available_slots.append((current_time, False))
                    current_time += slot_duration

            return available_slots

        if start_date >= end_date:
            return []

        # Generate all dates within the range
        delta = end_date - start_date
        all_available_slots = {}

        for i in range(delta.days):
            current_date = start_date + timezone.timedelta(days=i)
            daily_slots = get_daily_slots(current_date)
            all_available_slots[current_date.strftime("%A %d")] = daily_slots

        return all_available_slots

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = get_object_or_404(Doctor, pk=kwargs.get("doctor_pk"))
        start_date, end_date = self.get_current_week()
        available_slots = self.get_available_slots(doctor, start_date, end_date)
        context["doctor"] = doctor

        # generate table headers from days of week
        context["days_of_week"] = available_slots
        return context


class CheckoutAppointmentOrderView(LoginPatientRequiredMixin, View):
    @staticmethod
    def get(request, doctor_pk, start_date):
        doctor = get_object_or_404(Doctor, pk=doctor_pk)
        start_date = datetime.datetime.fromisoformat(start_date).strftime("%Y-%m-%d %H:%M")
        context = {"doctor": doctor, "start_date": start_date}
        return render(request, "appointments/checkout_appointment_order.html", context)

    @staticmethod
    def post(request: WSGIRequest, doctor_pk, start_date):
        doctor = get_object_or_404(Doctor, pk=doctor_pk)
        payment_method = request.POST.get("payment_method")
        order = Order(request)
        order.add(doctor_pk, start_date, doctor.fee)
        request.session.modified = True
        return redirect("appointments:payment-order", payment_method=payment_method)


class PaymentAppointmentOrderView(LoginPatientRequiredMixin, View):
    @staticmethod
    def get(request: WSGIRequest, payment_method):
        order = Order(request)
        price = order.get_price()
        if payment_method == PaymentMethod.WALLET.value:
            patient = request.user.patient
            if patient.wallet >= price:
                patient.wallet -= price
                patient.save()
                order.set_status(True)
                return redirect("appointments:booking-appointment")
            else:
                order.set_status(False)
                messages.warning(request, "Insufficient wallet balance.")
                return redirect("appointments:booking-appointment")
        else:
            response = send_request(
                request, price, f"Appointment Order", request.user.patient.phone_number, request.user.email
            )
            return redirect(response["url"])


class PaymentGatewayVerificationView(LoginPatientRequiredMixin, View):
    @staticmethod
    def get(request: WSGIRequest, *args, **kwargs):
        order = Order(request)
        authority = request.GET.get("Authority")
        status = request.GET.get("Status")
        if status == "OK":
            response = verify(order.get_price(), authority)
            if response["status"]:
                order.set_status(True)
                return redirect("appointments:booking-appointment")

        order.set_status(False)
        return redirect("appointments:booking-appointment")


class BookingAppointmentView(LoginPatientRequiredMixin, View):
    def get(self, request):
        order = Order(request)
        doctor = get_object_or_404(Doctor, pk=order.get_doctor_pk())
        start_datetime = timezone.datetime.fromisoformat(order.get_start_date())
        patient = self.request.user.patient
        if order.get_status():
            appointment = Appointment.objects.create(
                doctor=doctor,
                patient=patient,
                start_date=start_datetime,
            )
            # send the appointment to patient
            # send_mail(
            #     "Appointment Order Submitted",
            #     f"""
            #                     Hi Dear {request.user.get_full_name()},
            #                     Your appointment order has been submitted successfully.
            #                     Appointment Detail:
            #                     Doctor: Dr. {doctor.first_name} {doctor.last_name}
            #                     Appointment time start: {start_datetime}
            #                     office address: {doctor.address}
            #
            #                     GoodLuck for your from our team
            #                     """,
            #     None,
            #     [request.user.email],
            # )
            order.clear()
            messages.success(request, "Booking submitted successfully.")
            return render(request, "appointments/booking_status.html", {"appointment": appointment})
        else:
            order.clear()
            messages.warning(request, "Failed to book appointment. Please try again.")
            return redirect("appointments:show_weekly_doctor_availability", doctor_pk=doctor.pk)


class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = "appointments/detail.html"
