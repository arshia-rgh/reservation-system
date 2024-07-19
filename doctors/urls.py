from django.urls import path

from .views import DoctorDetailView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView, ScheduleCreateView, ScheduleUpdateView

app_name = "doctors"
urlpatterns = [
    path("details/<int:pk>/", DoctorDetailView.as_view(), name="detail"),
    path("create/", DoctorCreateView.as_view(), name="create"),
    path("delete/<int:pk>/", DoctorDeleteView.as_view(), name="delete"),
    path("update/<int:pk>/", DoctorUpdateView.as_view(), name="update"),
    path("schedule/<int:pk>/", ScheduleCreateView.as_view(), name="schedule-create"),
    path("schedule/<int:pk>/", ScheduleUpdateView.as_view(), name="schedule-update"),
]
