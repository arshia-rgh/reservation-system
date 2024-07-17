from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView

from accounts.mixins import LoginPatientRequiredMixin
from appointments.models import Appointment
from doctors.models import Schedule, Doctor


class ShowWeeklyDoctorAvailabilityView(LoginPatientRequiredMixin, TemplateView):
    template_name = "appointments/show_weekly_doctor_availability.html"

    @staticmethod
    def get_current_week():
        current_date = timezone.now()

        start_date = current_date - timezone.timedelta(days=(current_date.weekday() or 7) - 1)
        end_date = start_date + timezone.timedelta(days=7)
        return start_date, end_date

    @staticmethod
    def get_available_slots(doctor, start_date, end_date):
        def get_daily_slots(date):
            day_of_week = date.weekday()
            availabilities = Schedule.objects.filter(doctor=doctor, day_of_week=day_of_week)

            available_slots = []
            slot_duration = timezone.timedelta(minutes=20)

            for availability in availabilities:
                start_time = timezone.make_aware(timezone.datetime.combine(date, availability.start_time))
                end_time = timezone.make_aware(timezone.datetime.combine(date, availability.end_time))

                current_time = start_time
                while current_time + slot_duration <= end_time:
                    slot_end = current_time + slot_duration
                    if not Appointment.objects.filter(Q(start_date__range=(current_time, slot_end))).exists():
                        available_slots.append((current_time, True))
                    else:
                        available_slots.append((current_time, False))
                    current_time += slot_duration

            return available_slots

        # Generate all dates within the range
        delta = end_date - start_date
        all_available_slots = {}

        for i in range(1, delta.days + 1):
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
