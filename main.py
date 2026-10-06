"""Конструктор тестов — точка входа.

main.py организует взаимодействие объектов Test, User, Attempt
и не хранит данные предметной области в виде словарей.
"""

from models import Attempt, Question, Test, User
from models.attempts import cancel_attempt, create_attempt, show_attempts
from models.tests import (
    add_test,
    filter_tests_by_question_count,
    find_test_by_id,
    find_tests,
    show_tests,
    sort_tests_by_title,
)
from models.users import add_user, find_user, show_users
from storage import (
    load_attempts,
    load_tests,
    load_users,
    save_attempts,
    save_tests,
    save_users,
)
from utils import input_int, input_non_empty


def pass_test(
    tests: list[Test],
    users: list[User],
    attempts: list[Attempt],
) -> None:
    """Пройти тест: создать Attempt и связать с Test и User."""
    test_id = input_int("ID теста: ")
    test = find_test_by_id(tests, test_id)
    if test is None:
        print("Тест не найден.")
        return
    if test.questions_count == 0:
        print("В тесте нет вопросов.")
        return

    name = input_non_empty("Ваше имя: ")
    user = next((u for u in users if u.name == name), None)
    if user is None:
        user = add_user(users, name)

    correct = 0
    for number, question in enumerate(test.questions, start=1):
        print(f"\nВопрос {number}: {question.text}")
        print("Варианты: " + " / ".join(question.options))
        answer = input_non_empty("Ответ: ")
        if question.check_answer(answer):
            print("Верно!")
            correct += 1
        else:
            print(f"Неверно. Правильный ответ: {question.correct_answer}")

    attempt = create_attempt(attempts, test, user, correct)
    print(f"\nРезультат: {attempt}")


def create_test(tests: list[Test]) -> None:
    """Создать тест с вопросами."""
    title = input_non_empty("Название теста: ")
    description = input_non_empty("Описание: ")
    try:
        test = add_test(tests, title, description)
    except ValueError as error:
        print(f"Ошибка: {error}")
        return
    print(f"Создан тест [{test.id}] «{test.title}»")

    while input("Добавить вопрос? (y/n): ").strip().lower() == "y":
        text = input_non_empty("Текст вопроса: ")
        options = [input_non_empty(f"Вариант {i}: ") for i in range(1, 4)]
        correct = input_non_empty("Правильный ответ: ")
        try:
            test.add_question(Question(text, options, correct))
            print("Вопрос добавлен.")
        except ValueError as error:
            print(f"Ошибка: {error}")


def search_tests(tests: list[Test]) -> None:
    query = input_non_empty("Поиск: ")
    results = find_tests(tests, query)
    if not results:
        print("Ничего не найдено.")
        return
    for test in results:
        print(f"[{test.id}] {test.title}")


def show_sorted(tests: list[Test]) -> None:
    for test in sort_tests_by_title(tests):
        print(f"[{test.id}] {test.title}")


def show_filtered(tests: list[Test]) -> None:
    found = False
    for test in filter_tests_by_question_count(tests, 3):
        print(f"[{test.id}] {test.title} — вопросов: {test.questions_count}")
        found = True
    if not found:
        print("Нет тестов с 3+ вопросами.")


def search_users(users: list[User]) -> None:
    query = input_non_empty("Имя для поиска: ")
    results = find_user(users, query)
    if not results:
        print("Пользователи не найдены.")
        return
    for user in results:
        print(user)


def cancel_attempt_ui(attempts: list[Attempt]) -> None:
    attempt_id = input_int("ID попытки для удаления: ")
    if cancel_attempt(attempts, attempt_id):
        print("Попытка удалена.")
    else:
        print("Попытка с таким id не найдена.")


def save_all(
    tests: list[Test],
    users: list[User],
    attempts: list[Attempt],
) -> None:
    save_tests(tests)
    save_users(users)
    save_attempts(attempts)


def menu() -> None:
    """Главное меню приложения."""
    tests = load_tests()
    users = load_users()
    attempts = load_attempts(tests, users)

    actions = {
        "1": lambda: show_tests(tests),
        "2": lambda: show_users(users),
        "3": lambda: show_attempts(attempts),
        "4": lambda: pass_test(tests, users, attempts),
        "5": lambda: create_test(tests),
        "6": lambda: search_tests(tests),
        "7": lambda: show_sorted(tests),
        "8": lambda: show_filtered(tests),
        "9": lambda: search_users(users),
        "10": lambda: cancel_attempt_ui(attempts),
    }

    while True:
        print("\n=== Конструктор тестов ===")
        print("1. Показать тесты")
        print("2. Показать пользователей")
        print("3. Показать попытки")
        print("4. Пройти тест")
        print("5. Создать тест")
        print("6. Найти тест по названию")
        print("7. Сортировать тесты по названию")
        print("8. Показать тесты с 3+ вопросами")
        print("9. Найти пользователя")
        print("10. Удалить попытку")
        print("0. Выход")
        choice = input("Действие: ").strip()

        if choice == "0":
            save_all(tests, users, attempts)
            print("Данные сохранены.")
            return

        action = actions.get(choice)
        if action is None:
            print("Неизвестная команда.")
        else:
            try:
                action()
            except (ValueError, KeyError) as error:
                print(f"Ошибка: {error}")
            save_all(tests, users, attempts)


if __name__ == "__main__":
    menu()