from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Avg
from django.urls import reverse

from utils import BaseModelMixin


class Speciality(BaseModelMixin):
    """
    Model representing a specialty in the medical system.

    Attributes:
    name: The name of the specialty.
    description: A brief description of the specialty.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[RegexValidator(r"^[a-zA-Z]+$", "Specialty name must contain only letters.")],
    )
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
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, related_name="doctors")
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

    def get_absolute_url(self):
        """
        Returns the absolute URL of the doctor's detail page.

        Parameters:
        self (Doctor): The instance of the Doctor model.

        Returns:
        str: The absolute URL of the doctor's detail page.

        This method uses Django's reverse function to generate the URL for the
        'detail' view of the 'doctors' app, passing the primary key (pk) of the
        doctor as an argument. The generated URL is returned as a string.
        """
        return reverse("doctors:detail", args=[self.pk])

    @property
    def rate(self):
        """
        Returns the average rating of the doctor.

        Returns:
        float: The average rating of the doctor.
        """
        average_rating = self.rates.aggregate(avg=Avg("score"))["avg"]
        return average_rating if average_rating is not None else "N/A"


class Schedule(BaseModelMixin):
    """
    Model representing a doctor's schedule in the medical system.

    Attributes:
    doctor: The Doctor object associated with the schedule.
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

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="schedules")
    day_of_week = models.IntegerField(choices=DayOfWeek.choices, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ("day_of_week",)

    def __str__(self):
        return f"{self.doctor.first_name} {self.doctor.last_name} - {self.get_day_of_week_display()}"
