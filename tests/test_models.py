"""Тесты классов предметной области и функций обработки.

Адаптировано из test_test_bank.py (ПР2) и части test_attempts.py.
Вместо словарей используются объекты Test, Question, User, Attempt.
"""

from models import Attempt, Question, Test, User
from models.attempts import (
    cancel_attempt,
    create_attempt,
)
from models.tests import (
    add_test,
    delete_question,
    delete_test,
    edit_question,          # ← добавили
    edit_test,
    filter_tests_by_question_count,
    find_test_by_id,
    find_tests,
    sort_tests_by_title,
)
from models.users import (
    add_user,
    find_user,
    find_user_by_id,
)


# ---------- Question ----------


def test_question_check_answer_ignores_case_and_spaces():
    question = Question("2+2?", ["3", "4"], "4")
    assert question.check_answer("4")
    assert question.check_answer("  4  ")
    assert question.check_answer(" 4 ")
    assert not question.check_answer("3")


def test_question_strips_text_and_correct():
    question = Question("  2+2?  ", ["3", "4"], "  4  ")
    assert question.text == "2+2?"
    assert question.correct_answer == "4"


def test_question_empty_text_raises():
    try:
        Question("   ", ["a", "b"], "a")
        assert False, "Ожидалось ValueError"
    except ValueError:
        assert True


def test_question_too_few_options_raises():
    try:
        Question("Q", ["only"], "only")
        assert False, "Ожидалось ValueError"
    except ValueError:
        assert True


def test_question_correct_not_in_options_raises():
    try:
        Question("Q", ["a", "b"], "c")
        assert False, "Ожидалось ValueError"
    except ValueError:
        assert True


def test_question_str():
    question = Question("2+2?", ["3", "4"], "4")
    assert "2+2?" in str(question)
    assert "3" in str(question)
    assert "4" in str(question)


# ---------- Test ----------


def test_test_creation():
    test = Test(1, "Основы Python", "Базовый тест")
    assert test.id == 1
    assert test.title == "Основы Python"
    assert test.description == "Базовый тест"
    assert test.questions_count == 0
    assert test.questions == []


def test_test_short_title_raises():
    try:
        Test(1, "ab")
        assert False, "Ожидалось ValueError"
    except ValueError:
        assert True


def test_test_long_title_raises():
    try:
        Test(1, "x" * 101)
        assert False, "Ожидалось ValueError"
    except ValueError:
        assert True


def test_validate_title_static():
    assert Test.validate_title("Хорошее название")
    assert not Test.validate_title("ab")
    assert not Test.validate_title("   ")
    assert not Test.validate_title("x" * 101)


def test_test_add_question():
    test = Test(1, "Тест")
    question = Question("Q1", ["a", "b"], "a")
    test.add_question(question)
    assert test.questions_count == 1
    assert test.questions[0] is question


def test_test_str():
    test = Test(1, "Основы Python")
    assert "Основы Python" in str(test)
    assert "0" in str(test)


# ---------- Функции обработки тестов ----------


def test_add_test_returns_object():
    tests: list[Test] = []
    test = add_test(tests, "Основы Python", "Базовый тест")
    assert test.id == 1
    assert test.title == "Основы Python"
    assert len(tests) == 1
    assert tests[0] is test


def test_add_test_generates_incremental_ids():
    tests: list[Test] = []
    t1 = add_test(tests, "Первый")
    t2 = add_test(tests, "Второй")
    assert t1.id == 1
    assert t2.id == 2


def test_add_test_invalid_title_raises():
    tests: list[Test] = []
    try:
        add_test(tests, "ab")
        assert False, "Ожидалось ValueError"
    except ValueError:
        assert True


def test_find_test_by_id():
    tests: list[Test] = []
    test = add_test(tests, "Основы Python")
    assert find_test_by_id(tests, test.id) is test
    assert find_test_by_id(tests, 999) is None


def test_find_tests_by_substring():
    tests: list[Test] = []
    add_test(tests, "Основы Python")
    add_test(tests, "Основы SQL")
    found = find_tests(tests, "python")
    assert len(found) == 1
    assert found[0].title == "Основы Python"


def test_find_tests_case_insensitive():
    tests: list[Test] = []
    add_test(tests, "PYTHON")
    assert len(find_tests(tests, "python")) == 1


def test_find_tests_empty_result():
    tests: list[Test] = []
    add_test(tests, "Основы Python")
    assert find_tests(tests, "java") == []


def test_sort_tests_by_title():
    tests: list[Test] = []
    add_test(tests, "Бета")
    add_test(tests, "Альфа")
    add_test(tests, "Гамма")
    sorted_tests = sort_tests_by_title(tests)
    assert [t.title for t in sorted_tests] == ["Альфа", "Бета", "Гамма"]


def test_filter_tests_by_question_count():
    tests: list[Test] = []
    small = add_test(tests, "Малый")
    big = add_test(tests, "Большой")
    for i in range(3):
        big.add_question(Question(f"Q{i}", ["a", "b"], "a"))
    assert small.questions_count == 0

    result = list(filter_tests_by_question_count(tests, 3))
    assert len(result) == 1
    assert result[0].title == "Большой"


def test_filter_tests_by_question_count_no_matches():
    tests: list[Test] = []
    add_test(tests, "Малый")
    assert list(filter_tests_by_question_count(tests, 3)) == []


# ---------- User ----------


def test_user_creation():
    user = User(1, "Иван")
    assert user.id == 1
    assert user.name == "Иван"


def test_user_strips_name():
    user = User(1, "  Иван  ")
    assert user.name == "Иван"


def test_user_empty_name_raises():
    try:
        User(1, "   ")
        assert False, "Ожидалось ValueError"
    except ValueError:
        assert True


def test_user_str():
    user = User(1, "Иван")
    assert "Иван" in str(user)
    assert "1" in str(user)


def test_add_user_returns_object():
    users: list[User] = []
    user = add_user(users, "Иван")
    assert user.id == 1
    assert users[0] is user


def test_add_user_incremental_ids():
    users: list[User] = []
    u1 = add_user(users, "Иван")
    u2 = add_user(users, "Мария")
    assert u1.id == 1
    assert u2.id == 2


def test_find_user_by_id():
    users: list[User] = []
    user = add_user(users, "Иван")
    assert find_user_by_id(users, user.id) is user
    assert find_user_by_id(users, 999) is None


def test_find_user_by_substring():
    users: list[User] = []
    add_user(users, "Иван Петров")
    add_user(users, "Мария Иванова")
    found = find_user(users, "иван")
    assert len(found) == 2


# ---------- Attempt ----------


def _make_test_with_questions(count: int = 3) -> Test:
    """Вспомогательная функция: тест с заданным числом вопросов."""
    test = Test(1, "Тест")
    for i in range(count):
        test.add_question(Question(f"Q{i}", ["a", "b"], "a"))
    return test


def test_attempt_creation_and_links():
    test = _make_test_with_questions(4)
    user = User(1, "Иван")
    attempts: list[Attempt] = []

    attempt = create_attempt(attempts, test, user, 4)

    assert attempt.id == 1
    assert attempt.test is test
    assert attempt.user is user
    assert attempt.correct == 4
    assert attempt.total == 4
    assert len(attempts) == 1


def test_attempt_grade_excellent():
    test = _make_test_with_questions(10)
    user = User(1, "Иван")
    attempts: list[Attempt] = []

    attempt = create_attempt(attempts, test, user, 9)
    assert attempt.percent == 90.0
    assert attempt.grade == "Отлично"


def test_attempt_grade_good():
    test = _make_test_with_questions(10)
    user = User(1, "Иван")
    attempts: list[Attempt] = []

    attempt = create_attempt(attempts, test, user, 8)
    assert attempt.percent == 80.0
    assert attempt.grade == "Хорошо"


def test_attempt_grade_satisfactory():
    test = _make_test_with_questions(10)
    user = User(1, "Иван")
    attempts: list[Attempt] = []

    attempt = create_attempt(attempts, test, user, 6)
    assert attempt.percent == 60.0
    assert attempt.grade == "Удовлетворительно"


def test_attempt_grade_unsatisfactory():
    test = _make_test_with_questions(10)
    user = User(1, "Иван")
    attempts: list[Attempt] = []

    attempt = create_attempt(attempts, test, user, 3)
    assert attempt.percent == 30.0
    assert attempt.grade == "Неудовлетворительно"


def test_attempt_zero_total_raises():
    test = Test(1, "Тест")
    user = User(1, "Иван")
    try:
        Attempt(1, test, user, 0, 0)
        assert False, "Ожидалось ValueError"
    except ValueError:
        assert True


def test_attempt_str():
    test = _make_test_with_questions(2)
    user = User(1, "Иван")
    attempts: list[Attempt] = []

    attempt = create_attempt(attempts, test, user, 2)
    text = str(attempt)
    assert "Иван" in text
    assert "Тест" in text
    assert "100.0" in text


def test_cancel_attempt_removes():
    test = _make_test_with_questions(1)
    user = User(1, "Иван")
    attempts: list[Attempt] = []

    attempt = create_attempt(attempts, test, user, 1)
    assert len(attempts) == 1
    assert cancel_attempt(attempts, attempt.id)
    assert attempts == []


def test_cancel_attempt_missing_returns_false():
    attempts: list[Attempt] = []
    assert not cancel_attempt(attempts, 99)

# ---------- Редактирование и удаление тестов ----------


def test_edit_test_title_and_description():
    tests: list[Test] = []
    test = add_test(tests, "Старое название", "Старое описание")
    edit_test(test, title="Новое название", description="Новое описание")
    assert test.title == "Новое название"
    assert test.description == "Новое описание"


def test_edit_test_only_title():
    tests: list[Test] = []
    test = add_test(tests, "Старое название", "Описание")
    edit_test(test, title="Новое название")
    assert test.title == "Новое название"
    assert test.description == "Описание"


def test_edit_test_only_description():
    tests: list[Test] = []
    test = add_test(tests, "Название", "Старое описание")
    edit_test(test, description="Новое описание")
    assert test.title == "Название"
    assert test.description == "Новое описание"


def test_edit_test_nothing_changes():
    tests: list[Test] = []
    test = add_test(tests, "Название", "Описание")
    edit_test(test)
    assert test.title == "Название"
    assert test.description == "Описание"


def test_edit_test_invalid_title_raises():
    tests: list[Test] = []
    test = add_test(tests, "Нормальное название")
    try:
        edit_test(test, title="ab")
        assert False, "Ожидалось ValueError"
    except ValueError:
        assert True
    assert test.title == "Нормальное название"


def test_test_update_directly():
    test = Test(1, "Старое", "Описание")
    test.update(title="Новое")
    assert test.title == "Новое"
    assert test.description == "Описание"


def test_delete_test():
    tests: list[Test] = []
    add_test(tests, "Тест 1")
    t2 = add_test(tests, "Тест 2")
    assert delete_test(tests, t2.id)
    assert len(tests) == 1
    assert tests[0].title == "Тест 1"


def test_delete_test_missing_returns_false():
    tests: list[Test] = []
    add_test(tests, "Тест 1")
    assert not delete_test(tests, 999)
    assert len(tests) == 1


def test_delete_test_cascades_attempts():
    tests: list[Test] = []
    test = add_test(tests, "Тест")
    test.add_question(Question("Q", ["a", "b"], "a"))
    user = User(1, "Иван")
    attempts: list[Attempt] = []
    create_attempt(attempts, test, user, 1)
    create_attempt(attempts, test, user, 0)
    assert len(attempts) == 2

    assert delete_test(tests, test.id, attempts=attempts)
    assert tests == []
    assert attempts == []


def test_delete_test_keeps_other_attempts():
    tests: list[Test] = []
    test_a = add_test(tests, "Тест A")
    test_b = add_test(tests, "Тест B")
    test_a.add_question(Question("Q", ["a", "b"], "a"))
    test_b.add_question(Question("Q", ["a", "b"], "a"))
    user = User(1, "Иван")
    attempts: list[Attempt] = []
    create_attempt(attempts, test_a, user, 1)
    create_attempt(attempts, test_b, user, 1)

    delete_test(tests, test_a.id, attempts=attempts)
    assert len(tests) == 1
    assert tests[0] is test_b
    assert len(attempts) == 1
    assert attempts[0].test is test_b


def test_delete_question():
    test = Test(1, "Тест")
    test.add_question(Question("Q1", ["a", "b"], "a"))
    test.add_question(Question("Q2", ["a", "b"], "a"))
    assert test.questions_count == 2
    assert delete_question(test, 0)
    assert test.questions_count == 1
    assert test.questions[0].text == "Q2"


def test_delete_question_invalid_index():
    test = Test(1, "Тест")
    test.add_question(Question("Q1", ["a", "b"], "a"))
    assert not delete_question(test, 5)
    assert not delete_question(test, -1)
    assert test.questions_count == 1

# ---------- Редактирование вопросов ----------


def test_question_update_text():
    question = Question("Старый?", ["a", "b"], "a")
    question.update(text="Новый?")
    assert question.text == "Новый?"
    assert question.options == ["a", "b"]
    assert question.correct_answer == "a"


def test_question_update_options():
    """Обновление вариантов, когда правильный ответ остаётся в списке."""
    question = Question("Q?", ["a", "b"], "a")
    question.update(options=["a", "b", "c"])
    assert question.options == ["a", "b", "c"]
    assert question.correct_answer == "a"


def test_question_update_options_removes_correct_raises():
    """Если правильного ответа нет в новых вариантах — ValueError."""
    question = Question("Q?", ["a", "b"], "a")
    try:
        question.update(options=["x", "y", "z"])
        assert False, "Ожидалось ValueError"
    except ValueError:
        assert True
    # состояние не изменилось
    assert question.options == ["a", "b"]
    assert question.correct_answer == "a"


def test_question_update_correct_answer():
    question = Question("Q?", ["a", "b"], "a")
    question.update(correct_answer="b")
    assert question.correct_answer == "b"


def test_question_update_all_fields():
    question = Question("Q?", ["a", "b"], "a")
    question.update(text="Новый?", options=["x", "y"], correct_answer="y")
    assert question.text == "Новый?"
    assert question.options == ["x", "y"]
    assert question.correct_answer == "y"


def test_question_update_empty_text_raises():
    question = Question("Q?", ["a", "b"], "a")
    try:
        question.update(text="   ")
        assert False, "Ожидалось ValueError"
    except ValueError:
        assert True


def test_question_update_wrong_correct_raises():
    question = Question("Q?", ["a", "b"], "a")
    try:
        question.update(correct_answer="c")
        assert False, "Ожидалось ValueError"
    except ValueError:
        assert True
    # состояние не изменилось
    assert question.correct_answer == "a"


def test_edit_question_function():
    test = Test(1, "Тест")
    test.add_question(Question("Q1", ["a", "b"], "a"))
    test.add_question(Question("Q2", ["c", "d"], "c"))

    edit_question(test, 1, text="Q2-new", correct_answer="d")
    assert test.questions[1].text == "Q2-new"
    assert test.questions[1].correct_answer == "d"
    assert test.questions[0].text == "Q1"


def test_edit_question_invalid_index():
    test = Test(1, "Тест")
    test.add_question(Question("Q1", ["a", "b"], "a"))
    try:
        edit_question(test, 5, text="X")
        assert False, "Ожидалось IndexError"
    except IndexError:
        assert True


def test_edit_question_keeps_other_fields():
    test = Test(1, "Тест")
    test.add_question(Question("Q1", ["a", "b"], "a"))
    edit_question(test, 0, text="Новый текст")
    assert test.questions[0].text == "Новый текст"
    assert test.questions[0].options == ["a", "b"]
    assert test.questions[0].correct_answer == "a"
