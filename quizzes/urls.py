"""Маршруты приложения quizzes."""

from django.urls import path

from . import views

app_name = "quizzes"

urlpatterns = [
    path("", views.quizzes, name="list"),
    path("<int:test_id>/", views.quiz_detail, name="detail"),
]