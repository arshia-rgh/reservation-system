from django.core.validators import RegexValidator
from django.db import models

from utils import BaseModelMixin


class Speciality(BaseModelMixin):
    """
    Model representing a specialty in the medical system.

    Attributes:
    name: The name of the specialty.
    description: A brief description of the specialty.
    """
    name = models.CharField(max_length=255, unique=True, validators=[RegexValidator(r"^[a-zA-Z]+$", )])
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Speciality"
        verbose_name_plural = "Specialities"

    def __str__(self):
        return self.name


class Doctor(BaseModelMixin):
    """
    Model representing a doctor in the medical system.

    Attributes:
    first_name: The first name of the doctor.
    last_name: The last name of the doctor.
    specialty: The specialty of the doctor.
    phone_number: The phone number of the doctor.
    email: The email address of the doctor.
    address: The address of the doctor.
    fee: The fee of the doctor.
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, related_name='doctors')
    phone_number = models.CharField(
        max_length=13,
        unique=True,
        validators=[RegexValidator(r"^(09|\+989)\d{9}$", "Invalid Iranian phone number.")],
    )
    email = models.EmailField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    fee = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Schedule(BaseModelMixin):
    """
    Model representing a doctor's schedule in the medical system.

    Attributes:
    doctor: The doctor associated with the schedule.
    day_of_week: The day of the week for the schedule.
    start_time: The start time of the schedule.
    end_time: The end time of the schedule.
    """

    class DayOfWeek(models.IntegerChoices):
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5
        SATURDAY = 6
        SUNDAY = 7

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor.first_name} {self.doctor.last_name} - {self.get_day_of_week_display()}"
