## Веб-интерфейс (Django)

Проект дополнен веб-интерфейсом на Django 5.2.
Консольная версия (`main.py`) сохранена и продолжает работать.

### Технологии

- Python 3.10+
- Django 5.2 — веб-фреймворк
- Bootstrap 5.3 — оформление (CDN)
- pytest — тесты
- flake8 — качество кода

### Django-приложения

- `homepage` — главная страница и общий HTML-каркас (`page()`);
- `quizzes` — тесты и вопросы;
- `attempts` — попытки прохождения.

### Страницы

| URL | View | Назначение |
|---|---|---|
| `/` | `homepage.views.index` | главная, навигация |
| `/quizzes/` | `quizzes.views.quizzes` | список тестов |
| `/quizzes/<int:test_id>/` | `quizzes.views.quiz_detail` | тест с вопросами |
| `/attempts/` | `attempts.views.attempts` | список попыток |
| `/attempts/<int:attempt_id>/` | `attempts.views.attempt_detail` | одна попытка |

Если объект не найден — возвращается страница с кодом 404.

### Запуск веб-версии

    python manage.py migrate
    python manage.py runserver

Открыть: http://127.0.0.1:8000/

### Запуск консольной версии

    python main.py

### Что пока не реализовано в веб-интерфейсе

Создание, редактирование и удаление тестов/вопросов через
веб-формы появится в следующих работах — после перехода на
Django ORM и формы. Сейчас они доступны только в консольной версии.

## Структура проекта

- `manage.py`, `constructor/` — Django-проект;
- `homepage/`, `quizzes/`, `attempts/` — Django-приложения;
- `models/` — классы предметной области (ПР3);
- `storage.py` — загрузка/сохранение JSON;
- `main.py` — консольная версия;
- `utils.py` — ввод;
- `data/` — JSON-данные;
- `tests/` — pytest.