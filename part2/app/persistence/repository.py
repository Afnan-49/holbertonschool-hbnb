from __future__ import annotations
from typing import Dict, List, Optional

class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users: Dict[str, object] = {}

    def add(self, user) -> object:
        self._users[user.id] = user
        return user

    def get(self, user_id: str):
        return self._users.get(user_id)

    def list_all(self) -> List[object]:
        return list(self._users.values())

    def update(self, user) -> object:
        self._users[user.id] = user
        return user

    def find_by_email(self, email: str):
        for u in self._users.values():
            if getattr(u, "email", None) == email:
                return u
        return None