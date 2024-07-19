import secrets

from django.core.validators import RegexValidator
from django.db import models

from utils import BaseModelMixin


class Patient(BaseModelMixin):
    """
    This class represents a patient in the system.

    Attributes:
    user: The user associated with this patient.
    phone_number: The unique phone number of the patient.
    address: The address of the patient.
    birth_date: The birth date of the patient.
    wallet: The wallet balance of the patient.
    """

    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=13,
        unique=True,
        validators=[RegexValidator(r"^(09|\+989)\d{9}$", "Invalid Iranian phone number.")],
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    wallet = models.PositiveIntegerField(default=0)

    def __str__(self):
        """
        Returns the full name of the user associated with this patient.

        Returns:
        str: The full name of the user.
        """
        return self.user.get_full_name()


class OtpToken(BaseModelMixin):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    otp_expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()
