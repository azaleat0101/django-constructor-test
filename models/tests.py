"""Класс Test и функции работы с коллекцией тестов."""

from typing import Iterator

from .questions import Question


class Test:
    """Тест, содержащий набор вопросов."""

    def __init__(
        self,
        test_id: int,
        title: str,
        description: str = "",
    ) -> None:
        if not self.validate_title(title):
            raise ValueError(
                "Название должно содержать от 3 до 100 символов."
            )
        self.id = test_id
        self.title = title.strip()
        self.description = description.strip()
        self.questions: list[Question] = []

    @staticmethod
    def validate_title(title: str) -> bool:
        """Проверить корректность названия (длина 3–100)."""
        cleaned = title.strip()
        return 3 <= len(cleaned) <= 100

    def add_question(self, question: Question) -> None:
        """Добавить вопрос в тест."""
        self.questions.append(question)

    @property
    def questions_count(self) -> int:
        """Количество вопросов в тесте."""
        return len(self.questions)

    def to_data(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "questions": [q.to_data() for q in self.questions],
        }

    @classmethod
    def from_data(cls, test_id: int, data: dict) -> "Test":
        test = cls(
            test_id=test_id,
            title=data["title"],
            description=data.get("description", ""),
        )
        for question_data in data.get("questions", []):
            test.add_question(Question.from_data(question_data))
        return test

    def __str__(self) -> str:
        return f"Тест «{self.title}», вопросов: {self.questions_count}"


# ------- Функции работы с коллекцией тестов (остаются функциями) -------


def add_test(
    tests: list[Test],
    title: str,
    description: str = "",
) -> Test:
    """Создать Test и добавить его в коллекцию."""
    new_id = max((t.id for t in tests), default=0) + 1
    test = Test(new_id, title, description)
    tests.append(test)
    return test


def find_test_by_id(tests: list[Test], test_id: int) -> Test | None:
    """Найти тест по идентификатору."""
    for test in tests:
        if test.id == test_id:
            return test
    return None


def find_tests(tests: list[Test], query: str) -> list[Test]:
    """Найти тесты по подстроке в названии."""
    q = query.strip().lower()
    return [t for t in tests if q in t.title.lower()]


def filter_tests_by_question_count(
    tests: list[Test],
    min_questions: int,
) -> Iterator[Test]:
    """Генератор тестов с числом вопросов >= min_questions."""
    for test in tests:
        if test.questions_count >= min_questions:
            yield test


def sort_tests_by_title(tests: list[Test]) -> list[Test]:
    """Вернуть тесты, отсортированные по названию."""
    return sorted(tests, key=lambda t: t.title.lower())


def show_tests(tests: list[Test]) -> None:
    """Вывести список тестов."""
    if not tests:
        print("Список тестов пуст.")
        return
    for test in tests:
        print(f"[{test.id}] {test}")