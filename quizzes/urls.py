"""Маршруты приложения quizzes."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.quizzes, name="quizzes"),
    path("<int:test_id>/", views.quiz_detail, name="quiz_detail"),
]