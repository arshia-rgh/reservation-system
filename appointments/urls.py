from django.urls import path

from .views import AppointmentDetailView

app_name="appointments"
urlpatterns =[
    path("details/<int:pk>/", AppointmentDetailView.as_view(), name= "detail"),

]
