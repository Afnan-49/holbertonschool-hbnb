from __future__ import annotations
from app.persistence.repository import InMemoryUserRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self) -> None:
        self.users = InMemoryUserRepository()

    def create_user(self, data: dict) -> User:
        user = User(
            email=(data.get("email") or "").strip(),
            password=(data.get("password") or ""),
            first_name=(data.get("first_name") or "").strip(),
            last_name=(data.get("last_name") or "").strip(),
        )
        user.validate()

        if self.users.find_by_email(user.email):
            raise ValueError("Email already exists")

        self.users.add(user)
        return user

    def get_user(self, user_id: str):
        return self.users.get(user_id)

    def list_users(self):
        return self.users.list_all()

    def update_user(self, user_id: str, data: dict):
        user = self.users.get(user_id)
        if not user:
            return None

        # Only allow updating these fields (typical for black-box tests)
        if "email" in data:
            new_email = (data.get("email") or "").strip()
            if not new_email:
                raise ValueError("Invalid email")
            existing = self.users.find_by_email(new_email)
            if existing and existing.id != user_id:
                raise ValueError("Email already exists")
            user.email = new_email

        if "first_name" in data:
            user.first_name = (data.get("first_name") or "").strip()

        if "last_name" in data:
            user.last_name = (data.get("last_name") or "").strip()

        # Password update (IF your task allows it). If not allowed, delete this block.
        if "password" in data and data.get("password") is not None:
            pw = data.get("password")
            if pw and len(pw) >= 6:
                user.password = pw
            else:
                raise ValueError("Password must be at least 6 characters")

        user.touch()
        self.users.update(user)
        return user

# single shared instance
facade = HBnBFacade()