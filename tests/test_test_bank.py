"""Тесты функций работы с тестами."""

from test_bank import (
    add_question, add_test, filter_tests_by_question_count,
    find_tests, sort_tests_by_title, validate_title,
)


def test_add_test_returns_id():
    tests = {}
    test_id = add_test(tests, "Основы Python", "Базовый тест")
    assert test_id == 1
    assert tests[test_id]["title"] == "Основы Python"


def test_add_test_empty_title_raises():
    tests = {}
    try:
        add_test(tests, "   ", "Описание")
        assert False, "Ожидалось ValueError"
    except ValueError:
        assert True


def test_validate_title_short():
    assert "Ошибка" in validate_title("ab")


def test_add_question_appends():
    tests = {}
    test_id = add_test(tests, "Тест", "Описание")
    add_question(tests, test_id, "2+2?", ["3", "4", "5"], "4")
    assert len(tests[test_id]["questions"]) == 1


def test_add_question_wrong_correct_raises():
    tests = {}
    test_id = add_test(tests, "Тест", "")
    try:
        add_question(tests, test_id, "2+2?", ["3", "4"], "5")
        assert False, "Ожидалось ValueError"
    except ValueError:
        assert True


def test_find_tests_by_substring():
    tests = {}
    add_test(tests, "Основы Python", "")
    add_test(tests, "Основы SQL", "")
    found = find_tests(tests, "python")
    assert len(found) == 1
    assert found[0]["title"] == "Основы Python"


def test_sort_tests_by_title():
    tests = {}
    add_test(tests, "Бета", "")
    add_test(tests, "Альфа", "")
    sorted_tests = sort_tests_by_title(tests)
    assert sorted_tests[0]["title"] == "Альфа"


def test_filter_tests_by_question_count():
    tests = {}
    add_test(tests, "Малый", "")
    big_id = add_test(tests, "Большой", "")
    add_question(tests, big_id, "Q1", ["a", "b"], "a")
    add_question(tests, big_id, "Q2", ["a", "b"], "a")
    add_question(tests, big_id, "Q3", ["a", "b"], "a")
    result = list(filter_tests_by_question_count(tests, 3))
    assert len(result) == 1
    assert result[0]["id"] == big_id
