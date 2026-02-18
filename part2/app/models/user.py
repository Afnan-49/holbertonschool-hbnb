from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, email, password, first_name=None, last_name=None, is_admin=False):
        super().__init__()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.places = []

    @property
    def first_name(self):
        return getattr(self, "_first_name", None)

    @first_name.setter
    def first_name(self, value):
        if value is None or value == "":
            self._first_name = None
            return
        if len(value) > 50:
            raise ValueError("First name must be under 50 characters")
        self._first_name = value

    @property
    def last_name(self):
        return getattr(self, "_last_name", None)

    @last_name.setter
    def last_name(self, value):
        if value is None or value == "":
            self._last_name = None
            return
        if len(value) > 50:
            raise ValueError("Last name must be under 50 characters")
        self._last_name = value

    def validate(self):
        # basic validations used by facade
        if not self.email or not self.email.strip():
            raise ValueError("Email is required")

        if not self.password:
            raise ValueError("Password is required")

        if len(self.password) < 6:
            raise ValueError("Password must be at least 6 characters")

        # first_name/last_name validation handled by setters above

    def to_dict(self):
        """
        Return safe dict for API output.
        IMPORTANT: do NOT expose password.
        """
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }