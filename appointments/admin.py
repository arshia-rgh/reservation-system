from django.contrib import admin

from appointments.models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Custom admin model for the Appointment model.

    Attributes:
    - list_display: Fields to display in the change list page of the admin.
    - list_filter: Fields to filter the change list page of the admin.
    - search_fields: Fields to search in the change list page of the admin.
    """

    list_display = ("doctor", "patient", "start_date", "attended")
    """
    Fields to display in the change list page of the admin.

    Returns:
    - tuple: A tuple of field names.
    """

    list_filter = ("created_at", "updated_at", "attended")
    """
    Fields to filter the change list page of the admin.

    Returns:
    - tuple: A tuple of field names.
    """

    search_fields = (
        "doctor__user__first_name",
        "doctor__user__last_name",
        "patient__user__first_name",
        "patient__user__last_name",
        "start_date",
        "attended",
    )
    """
    Fields to search in the change list page of the admin.

    Returns:
    - tuple: A tuple of field names.
    """
