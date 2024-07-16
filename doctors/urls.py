from django.urls import path

from .views import DoctorDetailView

app_name = "doctors"
urlpatterns = [
    path("details/<int:pk>/", DoctorDetailView.as_view(), name="detail"),
]
