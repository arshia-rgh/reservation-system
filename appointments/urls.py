from django.urls import path

from .views import ShowWeeklyDoctorAvailabilityView, BookingAppointmentView

app_name = "appointments"
urlpatterns = [
    path(
        "weekly/show/<int:doctor_pk>/",
        ShowWeeklyDoctorAvailabilityView.as_view(),
        name="show_weekly_doctor_availability",
    ),
    path(
        "bookings/<int:doctor_pk>/<str:start_time>/",
        BookingAppointmentView.as_view(),
        name="booking-appointment",
    ),
]
