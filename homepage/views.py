"""View-функции главной страницы и общий каркас страниц."""

from django.http import HttpResponse


BOOTSTRAP = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)


def page(title: str, content: str) -> str:
    """Единый HTML-каркас всех страниц проекта."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Конструктор тестов</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/quizzes/">Тесты</a>
                <a class="nav-link" href="/attempts/">Попытки</a>
            </div>
        </div>
    </nav>
    <main class="container">
        {content}
    </main>
</body>
</html>"""


def index(request) -> HttpResponse:
    """Главная страница."""
    content = """
    <h1 class="display-4">Конструктор тестов</h1>
    <p class="lead">Приложение для создания и прохождения тестов.</p>
    <p>Основные разделы:</p>
    <a href="/quizzes/" class="btn btn-primary me-2">Тесты</a>
    <a href="/attempts/" class="btn btn-secondary">Попытки</a>
    """
    return HttpResponse(page("Конструктор тестов", content))