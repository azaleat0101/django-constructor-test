"""View-функции приложения attempts на Django ORM."""

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Attempt


SORT_OPTIONS = {
    "-date": "-date",
    "date": "date",
    "-percent": "-percent",
    "percent": "percent",
    "user": "user__name",
    "-user": "-user__name",
    "test": "test__title",
    "-test": "-test__title",
}


def attempts(request):
    """Список попыток: поиск, фильтр, сортировка, пагинация."""
    query = request.GET.get("q", "").strip()
    success = request.GET.get("success") == "1"
    hide_failed = request.GET.get("hide_failed") == "1"
    sort = request.GET.get("sort", "-date")

    queryset = Attempt.objects.select_related("user", "test")

    if query:
        queryset = queryset.filter(
            Q(user__name__icontains=query) | Q(test__title__icontains=query)
        )
    if success:
        queryset = queryset.filter(percent__gte=60)
    if hide_failed:
        queryset = queryset.exclude(percent__lt=60)

    queryset = queryset.order_by(SORT_OPTIONS.get(sort, "-date"))

    paginator = Paginator(queryset, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "attempts/attempt_list.html",
        {
            "page_obj": page_obj,
            "query": query,
            "success": success,
            "hide_failed": hide_failed,
            "sort": sort,
        },
    )


def attempt_detail(request, attempt_id):
    """Страница одной попытки. 404 при отсутствии."""
    attempt = get_object_or_404(
        Attempt.objects.select_related("user", "test"),
        pk=attempt_id,
    )
    return render(
        request,
        "attempts/attempt_detail.html",
        {"attempt": attempt},
    )