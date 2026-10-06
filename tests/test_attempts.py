"""Тесты функций прохождения и подсчёта результатов."""

from attempts import (
    calculate_score, cancel_attempt, check_answer, create_attempt,
)


def test_check_answer_ignores_case_and_spaces():
    assert check_answer("  INT  ", "int")
    assert not check_answer("str", "int")


def test_calculate_score_grades():
    result = calculate_score(9, 10)
    assert result["percent"] == 90.0
    assert result["grade"] == "Отлично"


def test_calculate_score_zero_total_raises():
    try:
        calculate_score(0, 0)
        assert False, "Ожидалось ValueError"
    except ValueError:
        assert True


def test_create_attempt_appends():
    attempts = []
    attempt = create_attempt(attempts, 1, "Иван", 2, 3)
    assert len(attempts) == 1
    assert attempt["user_name"] == "Иван"
    assert attempt["percent"] > 0


def test_cancel_attempt_removes():
    attempts = [{"id": 1, "test_id": 1}]
    assert cancel_attempt(attempts, 1)
    assert attempts == []


def test_cancel_attempt_missing_returns_false():
    attempts = []
    assert not cancel_attempt(attempts, 99)
