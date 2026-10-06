"""Маршруты приложения attempts."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.attempts, name="attempts"),
    path("<int:attempt_id>/", views.attempt_detail, name="attempt_detail"),
]