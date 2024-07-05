from django.contrib import admin

from appointments.models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("doctor", "patient", "start_date", "attended")
    list_filter = ("created_at", "updated_at", "attended")
    search_fields = (
        "doctor__user__first_name",
        "doctor__user__last_name",
        "patient__user__first_name",
        "patient__user__last_name",
        "start_date",
        "attended",
    )
