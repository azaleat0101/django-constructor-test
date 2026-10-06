"""Конструктор тестов — точка входа.

main.py организует взаимодействие объектов Test, User, Attempt
и не хранит данные предметной области в виде словарей.
"""

from models import Attempt, Question, Test, User
from models.attempts import cancel_attempt, create_attempt, show_attempts
from models.tests import (
    add_test,
    delete_question,
    delete_test,
    edit_question,          # ← добавили
    edit_test,
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


# ---------- Прохождение теста ----------


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


# ---------- Создание теста ----------


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


# ---------- Редактирование теста ----------


def edit_test_ui(tests: list[Test]) -> None:
    """Редактировать название и описание теста."""
    test_id = input_int("ID теста для редактирования: ")
    test = find_test_by_id(tests, test_id)
    if test is None:
        print("Тест не найден.")
        return

    print(f"Текущее название: {test.title}")
    print(f"Текущее описание: {test.description}")

    new_title = input(
        "Новое название (Enter — не менять): "
    ).strip()
    new_description = input(
        "Новое описание (Enter — не менять): "
    ).strip()

    try:
        edit_test(
            test,
            title=new_title if new_title else None,
            description=new_description if new_description else None,
        )
    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    print("Тест обновлён.")
    print(f"[{test.id}] {test}")


def delete_question_ui(tests: list[Test]) -> None:
    """Удалить вопрос из теста по индексу."""
    test_id = input_int("ID теста: ")
    test = find_test_by_id(tests, test_id)
    if test is None:
        print("Тест не найден.")
        return
    if test.questions_count == 0:
        print("В тесте нет вопросов.")
        return

    print(f"Вопросы теста «{test.title}»:")
    for index, question in enumerate(test.questions, start=0):
        print(f"  [{index}] {question}")

    index = input_int("Номер вопроса для удаления: ")
    if delete_question(test, index):
        print("Вопрос удалён.")
    else:
        print("Неверный номер вопроса.")


def delete_test_ui(
    tests: list[Test],
    attempts: list[Attempt],
) -> None:
    """Удалить тест (с подтверждением) и связанные попытки."""
    test_id = input_int("ID теста для удаления: ")
    test = find_test_by_id(tests, test_id)
    if test is None:
        print("Тест не найден.")
        return

    linked = sum(1 for a in attempts if a.test.id == test_id)
    print(f"Тест «{test.title}» содержит {test.questions_count} вопросов.")
    if linked:
        print(f"С ним связано попыток: {linked} — они тоже будут удалены.")

    confirm = input("Удалить? (y/n): ").strip().lower()
    if confirm != "y":
        print("Отменено.")
        return

    if delete_test(tests, test_id, attempts=attempts):
        print("Тест удалён.")
    else:
        print("Не удалось удалить тест.")


# ---------- Поиск и вывод ----------


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


# ---------- Сохранение ----------


def save_all(
    tests: list[Test],
    users: list[User],
    attempts: list[Attempt],
) -> None:
    save_tests(tests)
    save_users(users)
    save_attempts(attempts)


# ---------- Меню ----------


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
        "11": lambda: edit_test_ui(tests),
        "12": lambda: show_test_questions(tests),      
        "13": lambda: add_question_ui(tests),         
        "14": lambda: edit_question_ui(tests),        
        "15": lambda: delete_question_ui(tests),
        "16": lambda: delete_test_ui(tests, attempts),
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
        print("11. Редактировать тест")
        print("12. Показать вопросы теста")
        print("13. Добавить вопрос в тест")
        print("14. Редактировать вопрос")
        print("15. Удалить вопрос из теста")
        print("16. Удалить тест")
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

# ---------- Работа с вопросами теста ----------


def show_test_questions(tests: list[Test]) -> None:
    """Показать вопросы теста с номерами."""
    test_id = input_int("ID теста: ")
    test = find_test_by_id(tests, test_id)
    if test is None:
        print("Тест не найден.")
        return
    if test.questions_count == 0:
        print("В тесте нет вопросов.")
        return

    print(f"\nВопросы теста «{test.title}»:")
    for index, question in enumerate(test.questions):
        print(
            f"  [{index}] {question.text}\n"
            f"        варианты: {' / '.join(question.options)}\n"
            f"        правильный: {question.correct_answer}"
        )


def add_question_ui(tests: list[Test]) -> None:
    """Добавить вопрос в существующий тест."""
    test_id = input_int("ID теста: ")
    test = find_test_by_id(tests, test_id)
    if test is None:
        print("Тест не найден.")
        return

    text = input_non_empty("Текст вопроса: ")
    options = [input_non_empty(f"Вариант {i}: ") for i in range(1, 4)]
    correct = input_non_empty("Правильный ответ: ")
    try:
        test.add_question(Question(text, options, correct))
        print("Вопрос добавлен.")
        print(f"Теперь вопросов в тесте: {test.questions_count}")
    except ValueError as error:
        print(f"Ошибка: {error}")


def edit_question_ui(tests: list[Test]) -> None:
    """Редактировать текст, варианты и/или правильный ответ вопроса."""
    test_id = input_int("ID теста: ")
    test = find_test_by_id(tests, test_id)
    if test is None:
        print("Тест не найден.")
        return
    if test.questions_count == 0:
        print("В тесте нет вопросов.")
        return

    print(f"\nВопросы теста «{test.title}»:")
    for index, question in enumerate(test.questions):
        print(f"  [{index}] {question.text}")

    index = input_int("Номер вопроса для редактирования: ")
    if index < 0 or index >= test.questions_count:
        print("Неверный номер вопроса.")
        return

    question = test.questions[index]
    print(f"\nТекущий текст: {question.text}")
    print(f"Текущие варианты: {' / '.join(question.options)}")
    print(f"Текущий правильный ответ: {question.correct_answer}")

    new_text = input("Новый текст (Enter — не менять): ").strip()

    print("Новые варианты. Enter — оставить как есть.")
    print("Чтобы пропустить отдельный вариант, оставь поле пустым.")
    raw_options = [
        input(f"  Вариант {i} [{question.options[i - 1]}]: ").strip()
        for i in range(1, len(question.options) + 1)
    ]
    new_options = [
        raw if raw else current
        for raw, current in zip(raw_options, question.options)
    ]

    new_correct = input(
        f"Новый правильный ответ (Enter — не менять) "
        f"[{question.correct_answer}]: "
    ).strip()

    try:
        edit_question(
            test,
            index,
            text=new_text if new_text else None,
            options=new_options,
            correct_answer=new_correct if new_correct else None,
        )
        print("Вопрос обновлён.")
        print(f"[{index}] {test.questions[index]}")
    except ValueError as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    menu()