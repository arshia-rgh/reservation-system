from django.contrib import admin

from doctors.models import Speciality, Doctor, Schedule


@admin.register(Speciality)
class SpecialtyAdmin(admin.ModelAdmin):
    """
    Custom admin model for the Specialty model.

    Attributes:
    - list_display: Fields to display in the list view of the admin interface.
    - list_filter: Fields to filter the list view of the admin interface.
    - search_fields: Fields to search in the admin interface.

    Methods:
    - None (This class inherits from django.contrib.admin.ModelAdmin, so it doesn't have any additional methods)
    """

    list_display = ("name", "description")
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "description")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """
    Custom admin model for the Doctor model.

    Attributes:
    - list_display: Fields to display in the list view of the admin interface.
    - list_filter: Fields to filter the list view of the admin interface.
    - search_fields: Fields to search in the admin interface.
    """

    list_display = ("first_name", "last_name", "speciality", "phone_number", "address", "fee")
    list_filter = ("speciality",)
    search_fields = ("first_name", "last_name", "speciality__name", "phone_number", "address", "fee")


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """
    Custom admin model for the Schedule model.

    Attributes:
    - list_display: Fields to display in the list view of the admin interface.
    - list_filter: Fields to filter the list view of the admin interface.
    - search_fields: Fields to search in the admin interface.
    """

    list_display = ("doctor", "day_of_week", "start_time", "end_time")
    list_filter = ("day_of_week",)
    search_fields = (
        "doctor__first_name",
        "doctor__last_name",
        "doctor__specialty__name",
        "day_of_week",
        "start_time",
        "end_time",
    )
