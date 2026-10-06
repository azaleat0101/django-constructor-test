"""Конструктор тестов — интерактивный сценарий (ПР1)"""

from datetime import datetime

APP_NAME = "Конструктор тестов"
APP_VERSION = "0.1.0"


def get_test_info(title: str, description: str, questions_count: int) -> str:
    """Возвращает краткую информацию о тесте."""
    if questions_count <= 0:
        return f"Тест «{title}» пока не содержит вопросов."
    return (
        f"Тест: {title}\n"
        f"Описание: {description}\n"
        f"Количество вопросов: {questions_count}"
    )


def validate_title(title: str) -> str:
    """Проверяет корректность названия теста."""
    cleaned = title.strip()
    if len(cleaned) < 3:
        return "Ошибка: название теста слишком короткое (минимум 3 символа)."
    if len(cleaned) > 100:
        return "Ошибка: название теста слишком длинное (максимум 100 символов)."
    return f"Название «{cleaned}» принято."


def ask_question(number: int, text: str, options: str) -> str:
    """Выводит вопрос с вариантами и возвращает ответ пользователя."""
    print(f"Вопрос {number}: {text}")
    print(f"Варианты: {options}")
    answer = input("Ваш ответ: ")
    return answer


def check_answer(user_answer: str, correct_answer: str) -> bool:
    """Сравнивает ответ пользователя с правильным без учёта регистра."""
    normalized_user = user_answer.strip().lower()
    normalized_correct = correct_answer.strip().lower()
    return normalized_user == normalized_correct


def calculate_score(correct: int, total: int) -> str:
    """Считает процент правильных ответов и выставляет оценку."""
    if total <= 0:
        return "Невозможно вычислить результат: нет вопросов."
    percent = round(correct / total * 100, 1)
    if percent >= 90:
        grade = "Отлично"
    elif percent >= 75:
        grade = "Хорошо"
    elif percent >= 60:
        grade = "Удовлетворительно"
    else:
        grade = "Неудовлетворительно"
    return (
        f"Правильных ответов: {correct} из {total} "
        f"({percent}%). Оценка: {grade}."
    )


def main() -> None:
    print(f"=== {APP_NAME} v{APP_VERSION} ===")
    print(f"Запуск: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print()

    # 1. Информация о тесте
    title = "Основы Python"
    description = "Проверка базовых знаний языка Python"
    questions_count = 3
    print(get_test_info(title, description, questions_count))
    print(validate_title(title))
    print()

    # 2. Прохождение теста (три вопроса, без циклов — по требованию ПР1)
    correct_total = 0

    answer1 = ask_question(
        1,
        "Какой тип данных у значения 42?",
        "int / str / bool",
    )
    if check_answer(answer1, "int"):
        print("Верно!\n")
        correct_total = correct_total + 1
    else:
        print("Неверно. Правильный ответ: int\n")

    answer2 = ask_question(
        2,
        "Что выведет print(2 + 3 * 2)?",
        "7 / 10 / 12",
    )
    if check_answer(answer2, "10"):
        print("Верно!\n")
        correct_total = correct_total + 1
    else:
        print("Неверно. Правильный ответ: 10\n")

    answer3 = ask_question(
        3,
        "Какой оператор используется для ветвления?",
        "for / if / def",
    )
    if check_answer(answer3, "if"):
        print("Верно!\n")
        correct_total = correct_total + 1
    else:
        print("Неверно. Правильный ответ: if\n")

    # 3. Итог
    print(calculate_score(correct_total, questions_count))


if __name__ == "__main__":
    main()