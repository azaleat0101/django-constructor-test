"""View-функции для работы с попытками."""

from django.shortcuts import render

from models.attempts import find_attempt_by_id
from storage import load_attempts, load_tests, load_users


def attempts(request):
    """Список попыток."""
    tests = load_tests()
    users = load_users()
    attempts_list = load_attempts(tests, users)
    context = {
        "attempts": attempts_list,
    }
    return render(request, "attempts/attempt_list.html", context)


def attempt_detail(request, attempt_id):
    """Страница одной попытки."""
    tests = load_tests()
    users = load_users()
    attempts_list = load_attempts(tests, users)
    attempt = find_attempt_by_id(attempts_list, attempt_id)
    context = {
        "attempt": attempt,
    }
    return render(
        request,
        "attempts/attempt_detail.html",
        context,
        status=404 if attempt is None else 200,
    )