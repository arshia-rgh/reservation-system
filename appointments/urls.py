from django.urls import path


from .views import (
    AppointmentDetailView,
    ShowWeeklyDoctorAvailabilityView,
    BookingAppointmentView,
    CheckoutAppointmentOrderView,
    PaymentAppointmentOrderView,
    PaymentGatewayVerificationView,
)

app_name = "appointments"
urlpatterns = [
    path("details/<int:pk>/", AppointmentDetailView.as_view(), name= "detail"),
    path(
        "weekly/show/<int:doctor_pk>/",
        ShowWeeklyDoctorAvailabilityView.as_view(),
        name="show_weekly_doctor_availability",
    ),
    path("payment/verify/", PaymentGatewayVerificationView.as_view(), name="payment-verify"),
    path(
        "payment/<str:payment_method>/",
        PaymentAppointmentOrderView.as_view(),
        name="payment-order",
    ),
    path(
        "checkout/<int:doctor_pk>/<str:start_date>/",
        CheckoutAppointmentOrderView.as_view(),
        name="checkout-appointment-order",
    ),
    path(
        "bookings/",
        BookingAppointmentView.as_view(),
        name="booking-appointment",
    ),
]
