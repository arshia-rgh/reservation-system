from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from accounts.models import Patient
from doctors.models import Doctor
from utils import BaseModelMixin


class Comment(BaseModelMixin):
    """
    Model representing a comment made by a patient on a doctor's profile.

    Attributes:
    doctor: the doctor whom the comment is for.
    patient: The patient who made the comment.
    title: The title of the comment.
    content: The content of the comment.
    """

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="comments")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="comments")
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        """
        Returns a string representation of the comment.

        Returns:
        str: The title of the comment.
        """
        return self.title


class Rate(BaseModelMixin):
    """
    Model representing a rating given by a patient to a doctor.

    Attributes:
    doctor: The doctor to whom the rating is given.
    patient: The patient who gave the rating.
    score: The score given by the patient.
    """

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="rates")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="rates")
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        """
        Returns a string representation of the rating.

        Returns:
        str: A string combining the doctor's name and the score.
        """
        return f"{self.doctor} - {self.score}"
