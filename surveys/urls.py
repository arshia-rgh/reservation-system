from django.urls import path

from .views import RateCommentCreateView

app_name = "surveys"
urlpatterns = [
    path("<int:doctor_pk>/rate/create/", RateCommentCreateView.as_view(), name="rate-create"),
    path("<int:doctor_pk>/comment/create/", RateCommentCreateView.as_view(), name="comment-create"),
]
