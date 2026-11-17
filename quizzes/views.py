"""View-функции приложения quizzes на Django ORM."""

from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from .models import Test


SORT_OPTIONS = {
    "title": "title",
    "-title": "-title",
    "questions": "question_count",
    "-questions": "-question_count",
}


def quizzes(request):
    """Список тестов: поиск, фильтр по числу вопросов, сортировка."""
    query = request.GET.get("q", "").strip()
    min_questions = request.GET.get("min_q", "").strip()
    sort = request.GET.get("sort", "title")

    queryset = Test.objects.annotate(question_count=Count("questions"))

    if query:
        queryset = queryset.filter(title__icontains=query)

    if min_questions:
        try:
            queryset = queryset.filter(question_count__gte=int(min_questions))
        except ValueError:
            min_questions = ""

    queryset = queryset.order_by(SORT_OPTIONS.get(sort, "title"))

    return render(
        request,
        "quizzes/quiz_list.html",
        {
            "tests": queryset,
            "query": query,
            "min_questions": min_questions,
            "sort": sort,
        },
    )


def quiz_detail(request, test_id):
    """Страница теста с вопросами. 404 при отсутствии."""
    test = get_object_or_404(Test, pk=test_id)
    questions = test.questions.all()
    return render(
        request,
        "quizzes/quiz_detail.html",
        {"test": test, "questions": questions},
    )