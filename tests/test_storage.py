"""Тесты сериализации объектов в JSON-структуры и обратно.

Адаптировано из test_attempts.py (ПР2). Проверяется
преобразование объектов Test, Question, User, Attempt
через to_data/from_data, а также восстановление связей
Attempt → Test, User.
"""

from models import Attempt, Question, Test, User
from models.attempts import create_attempt


# ---------- Question ----------


def test_question_to_data():
    question = Question("2+2?", ["3", "4"], "4")
    data = question.to_data()
    assert data == {
        "text": "2+2?",
        "options": ["3", "4"],
        "correct_answer": "4",
    }


def test_question_from_data():
    data = {
        "text": "2+2?",
        "options": ["3", "4"],
        "correct_answer": "4",
    }
    question = Question.from_data(data)
    assert question.text == "2+2?"
    assert question.options == ["3", "4"]
    assert question.correct_answer == "4"


def test_question_round_trip():
    original = Question("2+2?", ["3", "4"], "4")
    restored = Question.from_data(original.to_data())
    assert restored.text == original.text
    assert restored.options == original.options
    assert restored.correct_answer == original.correct_answer


# ---------- Test ----------


def test_test_to_data():
    test = Test(1, "Основы Python", "Базовый тест")
    test.add_question(Question("Q1", ["a", "b"], "a"))
    data = test.to_data()
    assert data["title"] == "Основы Python"
    assert data["description"] == "Базовый тест"
    assert len(data["questions"]) == 1
    assert data["questions"][0]["text"] == "Q1"


def test_test_from_data():
    data = {
        "title": "Основы Python",
        "description": "Базовый тест",
        "questions": [
            {
                "text": "Q1",
                "options": ["a", "b"],
                "correct_answer": "a",
            },
        ],
    }
    test = Test.from_data(1, data)
    assert test.id == 1
    assert test.title == "Основы Python"
    assert test.description == "Базовый тест"
    assert test.questions_count == 1
    assert test.questions[0].correct_answer == "a"


def test_test_round_trip():
    original = Test(1, "Основы Python", "Описание")
    original.add_question(Question("Q1", ["a", "b"], "a"))
    original.add_question(Question("Q2", ["c", "d"], "c"))

    restored = Test.from_data(original.id, original.to_data())

    assert restored.id == original.id
    assert restored.title == original.title
    assert restored.description == original.description
    assert restored.questions_count == original.questions_count
    assert restored.questions[0].text == "Q1"
    assert restored.questions[1].correct_answer == "c"


def test_test_from_data_without_description():
    data = {"title": "Тест", "questions": []}
    test = Test.from_data(1, data)
    assert test.description == ""


# ---------- User ----------


def test_user_to_data():
    user = User(1, "Иван")
    assert user.to_data() == {"id": 1, "name": "Иван"}


def test_user_from_data():
    user = User.from_data({"id": 1, "name": "Иван"})
    assert user.id == 1
    assert user.name == "Иван"


def test_user_round_trip():
    original = User(42, "Мария")
    restored = User.from_data(original.to_data())
    assert restored.id == original.id
    assert restored.name == original.name


# ---------- Attempt ----------


def _make_attempt() -> tuple[Attempt, Test, User]:
    """Вспомогательная функция: подготовить Attempt с Test и User."""
    test = Test(1, "Тест")
    test.add_question(Question("Q1", ["a", "b"], "a"))
    test.add_question(Question("Q2", ["c", "d"], "c"))
    user = User(1, "Иван")
    attempts: list[Attempt] = []
    attempt = create_attempt(attempts, test, user, 2)
    return attempt, test, user


def test_attempt_to_data():
    attempt, test, user = _make_attempt()
    data = attempt.to_data()
    assert data["id"] == attempt.id
    assert data["test_id"] == test.id
    assert data["user_id"] == user.id
    assert data["correct"] == 2
    assert data["total"] == 2
    assert data["percent"] == 100.0
    assert "date" in data


def test_attempt_to_data_uses_ids_not_objects():
    """В JSON не должно быть ссылок на объекты — только id."""
    attempt, test, user = _make_attempt()
    data = attempt.to_data()
    assert data["test_id"] == test.id
    assert data["user_id"] == user.id
    assert "test" not in data
    assert "user" not in data


def test_attempt_from_data_restores_links():
    attempt, test, user = _make_attempt()
    data = attempt.to_data()
    restored = Attempt.from_data(data, [test], [user])
    assert restored is not None
    assert restored.test is test
    assert restored.user is user
    assert restored.percent == attempt.percent
    assert restored.date == attempt.date


def test_attempt_from_data_missing_test_returns_none():
    attempt, test, user = _make_attempt()
    data = attempt.to_data()
    data["test_id"] = 999
    assert Attempt.from_data(data, [test], [user]) is None


def test_attempt_from_data_missing_user_returns_none():
    attempt, test, user = _make_attempt()
    data = attempt.to_data()
    data["user_id"] = 999
    assert Attempt.from_data(data, [test], [user]) is None


def test_attempt_round_trip():
    original, test, user = _make_attempt()
    data = original.to_data()
    restored = Attempt.from_data(data, [test], [user])
    assert restored is not None
    assert restored.id == original.id
    assert restored.correct == original.correct
    assert restored.total == original.total
    assert restored.percent == original.percent
    assert restored.grade == original.grade