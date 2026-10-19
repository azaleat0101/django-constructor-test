"""Маршруты приложения attempts."""

from django.urls import path

from . import views

app_name = "attempts"

urlpatterns = [
    path("", views.attempts, name="list"),
    path("<int:attempt_id>/", views.attempt_detail, name="detail"),
]
