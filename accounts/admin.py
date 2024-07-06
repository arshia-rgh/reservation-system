from django.contrib import admin

from accounts.models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """
    Custom admin model for the Patient model.

    Attributes:
    - list_display: Fields to display in the list view of the admin interface.
    - search_fields: Fields to search in the admin interface.
    """

    list_display = ("user", "phone_number", "address", "birth_date", "wallet")
    """
    Fields to display in the list view of the admin interface.

    Fields:
    - user: Link to the related User object.
    - phone_number: Phone number of the patient.
    - address: Address of the patient.
    - birth_date: Birth date of the patient.
    - wallet: Link to the related Wallet object.
    """

    search_fields = ("user__first_name", "user__last_name", "phone_number")
    """
    Fields to search in the admin interface.

    Fields:
    - user__first_name: First name of the related User object.
    - user__last_name: Last name of the related User object.
    - phone_number: Phone number of the patient.
    """
