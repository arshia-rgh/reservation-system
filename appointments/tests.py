from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from accounts.models import Patient
from doctors.models import Doctor, Schedule, Speciality
from .models import Appointment
from .views import ShowWeeklyDoctorAvailabilityView


class ShowWeeklyDoctorAvailabilityViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testemail@example.com", password="Aa12345678@")
        self.patient = baker.make(Patient, user=self.user)
        self.speciality = baker.make(Speciality)
        self.doctor = baker.make(Doctor)
        for i in range(1, 8):
            Schedule.objects.create(
                doctor=self.doctor,
                day_of_week=i,
                start_time="09:00",
                end_time="17:00",
            )
        self.client.force_login(self.user)

    def test_get_available_slots_with_no_appointments(self):
        start_date = timezone.now().date()
        end_date = start_date + timezone.timedelta(days=7)
        available_slots = ShowWeeklyDoctorAvailabilityView.get_available_slots(self.doctor, start_date, end_date)
        self.assertEqual(len(available_slots), 7)
        for day, slots in available_slots.items():
            self.assertEqual(len(slots), 24)  # 24 slots per day (4-hour slots)
            for slot, is_available in slots:
                self.assertTrue(is_available)  # All slots should be available since there are no appointments

    def test_get_available_slots_with_appointments(self):
        appointment = baker.make(
            Appointment,
            doctor=self.doctor,
            patient=self.patient,
            start_date=timezone.now() + timezone.timedelta(days=1, hours=10),
        )

        start_date = timezone.now().date()
        end_date = start_date + timezone.timedelta(days=7)
        available_slots = ShowWeeklyDoctorAvailabilityView.get_available_slots(self.doctor, start_date, end_date)

        self.assertEqual(len(available_slots), 7)
        for day, slots in available_slots.items():
            if day == appointment.start_date.strftime("%A %d"):
                self.assertEqual(len(slots), 24)
                for slot, is_available in slots:
                    if slot.hour == appointment.start_date.hour:
                        self.assertFalse(is_available)  # The slot for the appointment should be unavailable
                    else:
                        self.assertTrue(is_available)  # Other slots should be available
            else:
                self.assertEqual(len(slots), 24)
                for slot, is_available in slots:
                    self.assertTrue(
                        is_available
                    )  # All slots should be available since there are no appointments on other days

    def test_get_available_slots_with_non_existing_date_range(self):
        start_date = timezone.now().date() + timezone.timedelta(days=8)
        end_date = timezone.now().date() + timezone.timedelta(days=7)
        available_slots = ShowWeeklyDoctorAvailabilityView.get_available_slots(self.doctor, start_date, end_date)

        self.assertEqual(len(available_slots), 0)  # No slots should be available since the date range is non-existing

    def test_get_available_slots_with_overlapping_appointments(self):
        baker.make(
            Appointment,
            doctor=self.doctor,
            patient=self.patient,
            start_date=timezone.now() + timezone.timedelta(days=1, hours=10),
        )
        baker.make(
            Appointment,
            doctor=self.doctor,
            patient=self.patient,
            start_date=timezone.now() + timezone.timedelta(days=1, hours=11),
        )

        start_date = timezone.now().date()
        end_date = start_date + timezone.timedelta(days=7)
        available_slots = ShowWeeklyDoctorAvailabilityView.get_available_slots(self.doctor, start_date, end_date)

        self.assertEqual(len(available_slots), 7)
        for day, slots in available_slots.items():
            if day == timezone.now().date() + timezone.timedelta(days=1):
                self.assertEqual(len(slots), 24)
                for slot, is_available in slots:
                    if slot.hour == 10 or slot.hour == 11:
                        self.assertFalse(
                            is_available
                        )  # The slots for the overlapping appointments should be unavailable
                    else:
                        self.assertTrue(is_available)  # Other slots should be available
            else:
                self.assertEqual(len(slots), 24)
                for slot, is_available in slots:
                    self.assertTrue(
                        is_available
                    )  # All slots should be available since there are no appointments on other days
