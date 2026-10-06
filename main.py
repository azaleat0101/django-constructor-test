"""Конструктор тестов — точка входа и меню приложения."""

from attempts import cancel_attempt, check_answer, create_attempt
from storage import (
    ATTEMPTS_FILE, TESTS_FILE, load_data, load_tests, save_data,
)
from test_bank import (
    add_question, add_test, filter_tests_by_question_count,
    find_tests, sort_tests_by_title,
)
from utils import input_int, input_non_empty


def show_tests(tests: dict) -> None:
    """Вывести список тестов."""
    if not tests:
        print("Список тестов пуст.")
        return
    for test_id, data in tests.items():
        print(f"[{test_id}] {data['title']} — "
              f"вопросов: {len(data['questions'])}")


def show_attempts(attempts: list) -> None:
    """Вывести список попыток."""
    if not attempts:
        print("Попыток пока нет.")
        return
    for attempt in attempts:
        print(
            f"[{attempt['id']}] Тест {attempt['test_id']}, "
            f"{attempt['user_name']}, {attempt['date']}, "
            f"{attempt['percent']}% — {attempt['grade']}"
        )


def pass_test(tests: dict, attempts: list) -> None:
    """Провести пользователя по тесту."""
    test_id = input_int("ID теста: ")
    if test_id not in tests:
        print("Тест не найден.")
        return
    test = tests[test_id]
    if not test["questions"]:
        print("В тесте нет вопросов.")
        return
    user_name = input_non_empty("Ваше имя: ")
    correct = 0
    for number, question in enumerate(test["questions"], start=1):
        print(f"\nВопрос {number}: {question['text']}")
        print("Варианты: " + " / ".join(question["options"]))
        answer = input_non_empty("Ответ: ")
        if check_answer(answer, question["correct_answer"]):
            print("Верно!")
            correct += 1
        else:
            print(
                f"Неверно. Правильный ответ: "
                f"{question['correct_answer']}"
            )
    attempt = create_attempt(
        attempts, test_id, user_name, correct, len(test["questions"])
    )
    print(f"\nРезультат: {attempt['percent']}% — {attempt['grade']}")


def create_test(tests: dict) -> None:
    """Создать новый тест с вопросами."""
    title = input_non_empty("Название теста: ")
    description = input_non_empty("Описание: ")
    test_id = add_test(tests, title, description)
    print(f"Создан тест с id={test_id}")
    while input("Добавить вопрос? (y/n): ").strip().lower() == "y":
        text = input_non_empty("Текст вопроса: ")
        options = []
        for index in range(1, 4):
            options.append(input_non_empty(f"Вариант {index}: "))
        correct = input_non_empty("Правильный ответ: ")
        try:
            add_question(tests, test_id, text, options, correct)
            print("Вопрос добавлен.")
        except (ValueError, KeyError) as error:
            print(f"Ошибка: {error}")


def search_tests(tests: dict) -> None:
    """Найти тесты по подстроке."""
    query = input_non_empty("Поиск: ")
    results = find_tests(tests, query)
    if not results:
        print("Ничего не найдено.")
        return
    for item in results:
        print(f"[{item['id']}] {item['title']}")


def show_sorted(tests: dict) -> None:
    """Показать тесты, отсортированные по названию."""
    for item in sort_tests_by_title(tests):
        print(f"[{item['id']}] {item['title']}")


def show_filtered(tests: dict) -> None:
    """Показать тесты с 3 и более вопросами."""
    found = False
    for item in filter_tests_by_question_count(tests, 3):
        print(
            f"[{item['id']}] {item['title']} — "
            f"вопросов: {len(item['questions'])}"
        )
        found = True
    if not found:
        print("Нет тестов с 3 и более вопросами.")


def cancel_attempt_ui(attempts: list) -> None:
    """Отменить попытку по id."""
    attempt_id = input_int("ID попытки для отмены: ")
    if cancel_attempt(attempts, attempt_id):
        print("Попытка удалена.")
    else:
        print("Попытка с таким id не найдена.")


def menu() -> None:
    """Главное меню приложения."""
    tests = load_tests(TESTS_FILE)
    attempts = load_data(ATTEMPTS_FILE, [])

    actions = {
        "1": lambda: show_tests(tests),
        "2": lambda: show_attempts(attempts),
        "3": lambda: pass_test(tests, attempts),
        "4": lambda: create_test(tests),
        "5": lambda: search_tests(tests),
        "6": lambda: show_sorted(tests),
        "7": lambda: show_filtered(tests),
        "8": lambda: cancel_attempt_ui(attempts),
    }

    while True:
        print("\n=== Конструктор тестов ===")
        print("1. Показать тесты")
        print("2. Показать попытки")
        print("3. Пройти тест")
        print("4. Создать тест")
        print("5. Найти тест по названию")
        print("6. Сортировать тесты по названию")
        print("7. Показать тесты с 3+ вопросами")
        print("8. Отменить попытку")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "0":
            save_data(TESTS_FILE, tests)
            save_data(ATTEMPTS_FILE, attempts)
            print("Данные сохранены. До встречи!")
            return

        action = actions.get(choice)
        if action is None:
            print("Неизвестная команда.")
        else:
            try:
                action()
            except (ValueError, KeyError) as error:
                print(f"Ошибка: {error}")
            save_data(TESTS_FILE, tests)
            save_data(ATTEMPTS_FILE, attempts)


if __name__ == "__main__":
    menu()
