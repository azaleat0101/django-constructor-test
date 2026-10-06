"""View-функции для работы с тестами."""

from django.http import HttpResponse

from homepage.views import page
from models.tests import find_test_by_id
from storage import load_tests


def quizzes(request) -> HttpResponse:
    """Список тестов."""
    tests = load_tests()
    items = ""
    for test in tests:
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between">'
            f'<a href="/quizzes/{test.id}/">{test.title}</a>'
            f'<span class="badge bg-primary">'
            f'{test.questions_count} вопросов</span>'
            f"</li>"
        )
    content = f"""
    <h1>Тесты</h1>
    <ul class="list-group">{items or "<li>Тестов пока нет.</li>"}</ul>
    """
    return HttpResponse(page("Конструктор тестов — тесты", content))


def quiz_detail(request, test_id: int) -> HttpResponse:
    """Страница одного теста со списком вопросов."""
    tests = load_tests()
    test = find_test_by_id(tests, test_id)
    if test is None:
        content = """
        <h1 class="text-danger">Тест не найден</h1>
        <a href="/quizzes/" class="btn btn-outline-secondary">
            ← к списку тестов
        </a>
        """
        return HttpResponse(
            page("Тест не найден", content),
            status=404,
        )

    questions_html = ""
    for number, question in enumerate(test.questions, start=1):
        options = "".join(
            f'<li class="list-group-item">{opt}</li>'
            for opt in question.options
        )
        questions_html += f"""
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="card-title">
                    Вопрос {number}: {question.text}
                </h5>
                <ul class="list-group list-group-flush">{options}</ul>
                <p class="card-text mt-2">
                    <strong>Правильный ответ:</strong>
                    {question.correct_answer}
                </p>
            </div>
        </div>
        """

    content = f"""
    <div class="card mb-3">
        <div class="card-body">
            <h5 class="card-title">{test.title}</h5>
            <p class="card-text">{test.description}</p>
            <span class="badge bg-primary">
                Вопросов: {test.questions_count}
            </span>
        </div>
    </div>
    {questions_html or '<p class="text-muted">Вопросов пока нет.</p>'}
    <a href="/quizzes/" class="btn btn-outline-secondary">
        ← к списку тестов
    </a>
    """
    return HttpResponse(page(test.title, content))