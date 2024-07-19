from django.db import models
from django.urls import reverse

from accounts.models import Patient
from doctors.models import Doctor
from utils import BaseModelMixin


class Appointment(BaseModelMixin):
    """
    Represents an appointment between a patient and a doctor.

    Attributes:
    doctor (Doctor): The doctor associated with the appointment.
    patient (Patient): The patient associated with the appointment.
    start_date (DateTimeField): The start date and time of the appointment.
    attended (BooleanField): Indicates whether the appointment has been attended.
    """

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    start_date = models.DateTimeField(null=False, blank=False)
    attended = models.BooleanField(default=False)


    def get_absolute_url(self):
        return reverse("appointments:detail", args=[self.pk])
