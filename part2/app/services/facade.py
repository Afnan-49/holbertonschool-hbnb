from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ---------- Users ----------
    def create_user(self, user_data: Dict[str, Any]) -> User:
        user = User(
            email=user_data.get("email"),
            password=user_data.get("password"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
        )
        user.validate()

        # unique email
        existing = self.user_repo.find_by("email", user.email)
        if existing:
            raise ValueError("Email already exists")

        return self.user_repo.add(user)

    def get_user(self, user_id: str) -> Optional[User]:
        return self.user_repo.get(user_id)

    def list_users(self) -> List[User]:
        return self.user_repo.list_all()

    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Optional[User]:
        user = self.user_repo.get(user_id)
        if not user:
            return None

        if "first_name" in user_data:
            user.first_name = (user_data.get("first_name") or "").strip()
        if "last_name" in user_data:
            user.last_name = (user_data.get("last_name") or "").strip()

        user.validate()
        user.save()
        return user
    
    from app.models.amenity import Amenity

# ---------- Amenities ----------
def create_amenity(self, data: dict) -> Amenity:
    name = (data.get("name") or "").strip()
    amenity = Amenity(name=name)
    amenity.validate()

    if self.amenity_repo.get_by_attribute("name", amenity.name):
        raise ValueError("Amenity name already exists")

    return self.amenity_repo.add(amenity)

def get_amenity(self, amenity_id: str):
    return self.amenity_repo.get(amenity_id)

def list_amenities(self):
    return self.amenity_repo.get_all()

def update_amenity(self, amenity_id: str, data: dict):
    amenity = self.amenity_repo.get(amenity_id)
    if not amenity:
        return None

    if "name" in data:
        amenity.update({"name": (data.get("name") or "").strip()})

    amenity.validate()
    return amenity


facade = HBnBFacade()
