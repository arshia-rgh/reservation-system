from django.urls import path

from home.views import IndexHomePageView

app_name = "home"
urlpatterns = [
    path("", IndexHomePageView.as_view(), name="index"),
]
