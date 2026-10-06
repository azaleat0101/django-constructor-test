"""View-функции для работы с попытками прохождения тестов."""

from django.http import HttpResponse

from homepage.views import page
from models.attempts import find_attempt_by_id
from storage import load_attempts, load_tests, load_users


def attempts(request) -> HttpResponse:
    """Список попыток."""
    tests = load_tests()
    users = load_users()
    attempts_list = load_attempts(tests, users)

    items = ""
    for attempt in attempts_list:
        badge = (
            "bg-success" if attempt.percent >= 60 else "bg-danger"
        )
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between">'
            f'<a href="/attempts/{attempt.id}/">'
            f'{attempt.user.name} — {attempt.test.title}</a>'
            f'<span class="badge {badge}">'
            f'{attempt.percent}% ({attempt.grade})</span>'
            f"</li>"
        )

    content = f"""
    <h1>Попытки</h1>
    <ul class="list-group">
        {items or '<li>Попыток пока нет.</li>'}
    </ul>
    """
    return HttpResponse(page("Конструктор тестов — попытки", content))


def attempt_detail(request, attempt_id: int) -> HttpResponse:
    """Страница одной попытки."""
    tests = load_tests()
    users = load_users()
    attempts_list = load_attempts(tests, users)
    attempt = find_attempt_by_id(attempts_list, attempt_id)

    if attempt is None:
        content = """
        <h1 class="text-danger">Попытка не найдена</h1>
        <a href="/attempts/" class="btn btn-outline-secondary">
            ← к списку попыток
        </a>
        """
        return HttpResponse(
            page("Попытка не найдена", content),
            status=404,
        )

    badge = "bg-success" if attempt.percent >= 60 else "bg-danger"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Попытка №{attempt.id}</h5>
            <p class="card-text">
                <strong>Пользователь:</strong> {attempt.user.name}
            </p>
            <p class="card-text">
                <strong>Тест:</strong> {attempt.test.title}
            </p>
            <p class="card-text">
                <strong>Дата:</strong> {attempt.date}
            </p>
            <p class="card-text">
                <strong>Правильных ответов:</strong>
                {attempt.correct} из {attempt.total}
            </p>
            <p class="card-text">
                <strong>Результат:</strong>
                <span class="badge {badge}">
                    {attempt.percent}% ({attempt.grade})
                </span>
            </p>
            <a href="/attempts/" class="btn btn-outline-secondary">
                ← к списку попыток
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Попытка №{attempt.id}", content))