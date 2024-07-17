from django.urls import path

from .views import ShowWeeklyDoctorAvailabilityView

app_name = "appointments"
urlpatterns = [
    path(
        "weekly/show/<int:doctor_pk>/",
        ShowWeeklyDoctorAvailabilityView.as_view(),
        name="show_weekly_doctor_availability",
    ),

]
