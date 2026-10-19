"""View-функции для работы с тестами."""

from django.shortcuts import render

from models.tests import find_test_by_id
from storage import load_tests


def quizzes(request):
    """Список тестов."""
    tests = load_tests()
    context = {
        "tests": tests,
    }
    return render(request, "quizzes/quiz_list.html", context)


def quiz_detail(request, test_id):
    """Страница одного теста со списком вопросов."""
    tests = load_tests()
    test = find_test_by_id(tests, test_id)
    context = {
        "test": test,
    }
    return render(
        request,
        "quizzes/quiz_detail.html",
        context,
        status=404 if test is None else 200,
    )