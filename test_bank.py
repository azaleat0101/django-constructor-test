"""Функции работы с тестами и вопросами."""

from typing import Iterator


def get_test_info(title: str, description: str,
                  questions_count: int) -> str:
    """Краткая информация о тесте (сохранена из ПР1)."""
    if questions_count <= 0:
        return f"Тест «{title}» пока не содержит вопросов."
    return (
        f"Тест: {title}\n"
        f"Описание: {description}\n"
        f"Количество вопросов: {questions_count}"
    )


def validate_title(title: str) -> str:
    """Проверка названия теста (сохранена из ПР1)."""
    cleaned = title.strip()
    if len(cleaned) < 3:
        return "Ошибка: название слишком короткое (минимум 3 символа)."
    if len(cleaned) > 100:
        return "Ошибка: название слишком длинное (максимум 100 символов)."
    return f"Название «{cleaned}» принято."


def add_test(tests: dict[int, dict], title: str,
             description: str) -> int:
    """Добавить тест в словарь, вернуть его id."""
    if not title.strip():
        raise ValueError("Название теста не может быть пустым.")
    new_id = max(tests.keys(), default=0) + 1
    tests[new_id] = {
        "title": title.strip(),
        "description": description.strip(),
        "questions": [],
    }
    return new_id


def add_question(tests: dict[int, dict], test_id: int, text: str,
                 options: list[str], correct_answer: str) -> None:
    """Добавить вопрос в тест."""
    if test_id not in tests:
        raise KeyError(f"Тест с id={test_id} не найден.")
    if not text.strip():
        raise ValueError("Текст вопроса не может быть пустым.")
    if len(options) < 2:
        raise ValueError("Нужно минимум 2 варианта ответа.")
    if correct_answer not in options:
        raise ValueError("Правильный ответ должен входить в варианты.")
    tests[test_id]["questions"].append({
        "text": text.strip(),
        "options": options,
        "correct_answer": correct_answer.strip(),
    })


def find_tests(tests: dict[int, dict], query: str) -> list[dict]:
    """Найти тесты по подстроке в названии."""
    query_lower = query.strip().lower()
    return [
        {"id": test_id, **data}
        for test_id, data in tests.items()
        if query_lower in data["title"].lower()
    ]


def filter_tests_by_question_count(
    tests: dict[int, dict], min_questions: int
) -> Iterator[dict]:
    """Генератор тестов с числом вопросов >= min_questions."""
    for test_id, data in tests.items():
        if len(data["questions"]) >= min_questions:
            yield {"id": test_id, **data}


def sort_tests_by_title(tests: dict[int, dict]) -> list[dict]:
    """Вернуть тесты, отсортированные по названию (lambda)."""
    return sorted(
        ({"id": test_id, **data} for test_id, data in tests.items()),
        key=lambda item: item["title"].lower(),
    )
