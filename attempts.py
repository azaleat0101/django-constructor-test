"""Прохождение тестов и подсчёт результатов."""

from datetime import datetime


def check_answer(user_answer: str, correct_answer: str) -> bool:
    """Сравнить ответ без учёта регистра и пробелов."""
    return user_answer.strip().lower() == correct_answer.strip().lower()


def get_booking_status(is_available: bool) -> str:
    """Функция из ПР1 — статус (сохранена для преемственности)."""
    if is_available:
        return "Тест доступен для прохождения"
    return "Тест уже пройден"


def calculate_score(correct: int, total: int) -> dict:
    """Вычислить процент и оценку."""
    if total <= 0:
        raise ValueError("Количество вопросов должно быть больше нуля.")
    percent = round(correct / total * 100, 1)
    if percent >= 90:
        grade = "Отлично"
    elif percent >= 75:
        grade = "Хорошо"
    elif percent >= 60:
        grade = "Удовлетворительно"
    else:
        grade = "Неудовлетворительно"
    return {
        "correct": correct,
        "total": total,
        "percent": percent,
        "grade": grade,
    }


def create_attempt(attempts: list[dict], test_id: int, user_name: str,
                   correct: int, total: int) -> dict:
    """Создать запись о попытке прохождения."""
    result = calculate_score(correct, total)
    attempt = {
        "id": max((a["id"] for a in attempts), default=0) + 1,
        "test_id": test_id,
        "user_name": user_name.strip(),
        "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "correct": result["correct"],
        "total": result["total"],
        "percent": result["percent"],
        "grade": result["grade"],
    }
    attempts.append(attempt)
    return attempt


def cancel_attempt(attempts: list[dict], attempt_id: int) -> bool:
    """Удалить попытку по id. Вернуть True, если удалено."""
    for index, attempt in enumerate(attempts):
        if attempt["id"] == attempt_id:
            attempts.pop(index)
            return True
    return False
