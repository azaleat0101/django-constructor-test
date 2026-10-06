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

    def update(self, title: str | None = None,
               description: str | None = None) -> None:
        """Обновить название и/или описание теста.

        Параметр None означает «не менять».
        """
        if title is not None:
            if not self.validate_title(title):
                raise ValueError(
                    "Название должно содержать от 3 до 100 символов."
                )
            self.title = title.strip()
        if description is not None:
            self.description = description.strip()

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


# ------- Функции работы с коллекцией тестов -------


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


def edit_test(
    test: Test,
    title: str | None = None,
    description: str | None = None,
) -> None:
    """Отредактировать тест.

    Параметр None означает «не менять соответствующее поле».
    """
    test.update(title=title, description=description)


def delete_test(
    tests: list[Test],
    test_id: int,
    attempts: list | None = None,
) -> bool:
    """Удалить тест по id.

    Если передан список attempts, связанные попытки тоже удаляются,
    чтобы не осталось «висячих» ссылок.
    """
    test = find_test_by_id(tests, test_id)
    if test is None:
        return False
    if attempts is not None:
        attempts[:] = [a for a in attempts if a.test.id != test_id]
    tests.remove(test)
    return True


def delete_question(test: Test, index: int) -> bool:
    """Удалить вопрос по индексу (начиная с 0)."""
    if index < 0 or index >= test.questions_count:
        return False
    test.questions.pop(index)
    return True

def edit_question(
    test: Test,
    index: int,
    text: str | None = None,
    options: list[str] | None = None,
    correct_answer: str | None = None,
) -> None:
    """Отредактировать вопрос по индексу.

    Параметр None означает «не менять соответствующее поле».
    Бросает IndexError, если индекс вне диапазона.
    """
    if index < 0 or index >= test.questions_count:
        raise IndexError("Вопроса с таким номером нет.")
    test.questions[index].update(
        text=text,
        options=options,
        correct_answer=correct_answer,
    )