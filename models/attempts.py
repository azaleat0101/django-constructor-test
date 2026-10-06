"""Класс Attempt — попытка прохождения теста."""

from datetime import datetime

from .tests import Test, find_test_by_id
from .users import User, find_user_by_id


class Attempt:
    """Результат прохождения теста пользователем."""

    def __init__(
        self,
        attempt_id: int,
        test: Test,
        user: User,
        correct: int,
        total: int,
    ) -> None:
        if total <= 0:
            raise ValueError("Количество вопросов должно быть больше нуля.")
        self.id = attempt_id
        self.test = test
        self.user = user
        self.correct = correct
        self.total = total
        self.date = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.percent = round(correct / total * 100, 1)

    @property
    def grade(self) -> str:
        """Оценка по проценту правильных ответов."""
        if self.percent >= 90:
            return "Отлично"
        if self.percent >= 75:
            return "Хорошо"
        if self.percent >= 60:
            return "Удовлетворительно"
        return "Неудовлетворительно"

    def to_data(self) -> dict:
        """Преобразовать в словарь для JSON (хранятся id, не объекты)."""
        return {
            "id": self.id,
            "test_id": self.test.id,
            "user_id": self.user.id,
            "date": self.date,
            "correct": self.correct,
            "total": self.total,
            "percent": self.percent,
        }

    @classmethod
    def from_data(
        cls,
        data: dict,
        tests: list[Test],
        users: list[User],
    ) -> "Attempt | None":
        """Создать Attempt, восстановив связи с Test и User.

        Возвращает None, если связанные объекты не найдены.
        """
        test = find_test_by_id(tests, data["test_id"])
        user = find_user_by_id(users, data["user_id"])
        if test is None or user is None:
            return None
        attempt = cls(
            attempt_id=data["id"],
            test=test,
            user=user,
            correct=data["correct"],
            total=data["total"],
        )
        attempt.date = data.get("date", attempt.date)
        return attempt

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.user.name} — тест «{self.test.title}», "
            f"{self.percent}% ({self.grade}), {self.date}"
        )


def create_attempt(
    attempts: list[Attempt],
    test: Test,
    user: User,
    correct: int,
) -> Attempt:
    """Создать попытку и добавить в коллекцию."""
    new_id = max((a.id for a in attempts), default=0) + 1
    attempt = Attempt(new_id, test, user, correct, test.questions_count)
    attempts.append(attempt)
    return attempt


def cancel_attempt(attempts: list[Attempt], attempt_id: int) -> bool:
    """Удалить попытку по id. Вернуть True, если удалено."""
    for index, attempt in enumerate(attempts):
        if attempt.id == attempt_id:
            attempts.pop(index)
            return True
    return False


def show_attempts(attempts: list[Attempt]) -> None:
    if not attempts:
        print("Попыток пока нет.")
        return
    for attempt in attempts:
        print(attempt)

def find_attempt_by_id(
    attempts: list[Attempt],
    attempt_id: int,
) -> Attempt | None:
    """Найти попытку по идентификатору."""
    for attempt in attempts:
        if attempt.id == attempt_id:
            return attempt
    return None