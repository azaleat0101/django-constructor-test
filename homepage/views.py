"""View-функции главной страницы и статистики."""

from django.db.models import Avg, Count, Max, Min
from django.shortcuts import render

from attempts.models import Attempt, User
from quizzes.models import Test


def index(request):
    """Главная страница."""
    return render(request, "homepage/index.html")


def statistics(request):
    """Страница статистики по тестам, попыткам и пользователям."""
    attempts_stats = Attempt.objects.aggregate(
        count=Count("id"),
        avg_percent=Avg("percent"),
        best=Max("percent"),
        worst=Min("percent"),
    )

    tests_stats = Test.objects.annotate(
        attempts_count=Count("attempts"),
        avg_percent=Avg("attempts__percent"),
    ).order_by("-attempts_count", "title")

    users_stats = User.objects.annotate(
        attempts_count=Count("attempts"),
        avg_percent=Avg("attempts__percent"),
    ).order_by("-attempts_count", "name")

    return render(
        request,
        "homepage/statistics.html",
        {
            "tests_count": Test.objects.count(),
            "attempts_stats": attempts_stats,
            "tests_stats": tests_stats,
            "users_stats": users_stats,
        },
    )