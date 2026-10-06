"""Класс User и функции работы с коллекцией пользователей."""


class User:
    """Пользователь, проходящий тесты."""

    def __init__(self, user_id: int, name: str) -> None:
        cleaned = name.strip()
        if not cleaned:
            raise ValueError("Имя пользователя не может быть пустым.")
        self.id = user_id
        self.name = cleaned

    def to_data(self) -> dict:
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_data(cls, data: dict) -> "User":
        return cls(user_id=data["id"], name=data["name"])

    def __str__(self) -> str:
        return f"Пользователь #{self.id}: {self.name}"


def add_user(users: list[User], name: str) -> User:
    """Создать User и добавить в коллекцию."""
    new_id = max((u.id for u in users), default=0) + 1
    user = User(new_id, name)
    users.append(user)
    return user


def find_user_by_id(users: list[User], user_id: int) -> User | None:
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_user(users: list[User], query: str) -> list[User]:
    q = query.strip().lower()
    return [u for u in users if q in u.name.lower()]


def show_users(users: list[User]) -> None:
    if not users:
        print("Пользователей пока нет.")
        return
    for user in users:
        print(user)