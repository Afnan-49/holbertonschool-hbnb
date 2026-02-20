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
from app.models.place import Place

# ---------- Places ----------
def create_place(self, data: dict) -> Place:
    title = (data.get("title") or "").strip()
    description = (data.get("description") or "")
    price = data.get("price")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    owner_id = data.get("owner_id")
    amenity_ids = data.get("amenity_ids") or []

    owner = self.user_repo.get(owner_id)
    if not owner:
        raise ValueError("Owner not found")

    amenities = []
    for aid in amenity_ids:
        a = self.amenity_repo.get(aid)
        if not a:
            raise ValueError(f"Amenity not found: {aid}")
        amenities.append(a)

    place = Place(
        title=title,
        description=description,
        price=price,
        latitude=latitude,
        longitude=longitude,
        owner=owner,
        amenities=amenities,
    )
    place.validate()
    return self.place_repo.add(place)

def get_place(self, place_id: str):
    return self.place_repo.get(place_id)

def list_places(self):
    return self.place_repo.get_all()

def update_place(self, place_id: str, data: dict):
    place = self.place_repo.get(place_id)
    if not place:
        return None

    # allowed updates
    patch = {}
    if "title" in data:
        patch["title"] = (data.get("title") or "").strip()
    if "description" in data:
        patch["description"] = data.get("description") or ""
    if "price" in data:
        patch["price"] = data.get("price")
    if "latitude" in data:
        patch["latitude"] = data.get("latitude")
    if "longitude" in data:
        patch["longitude"] = data.get("longitude")

    # owner update (optional)
    if "owner_id" in data:
        new_owner = self.user_repo.get(data.get("owner_id"))
        if not new_owner:
            raise ValueError("Owner not found")
        patch["owner"] = new_owner

    place.update(patch)

    # amenities update (optional)
    if "amenity_ids" in data:
        amenity_ids = data.get("amenity_ids") or []
        new_amenities = []
        for aid in amenity_ids:
            a = self.amenity_repo.get(aid)
            if not a:
                raise ValueError(f"Amenity not found: {aid}")
            new_amenities.append(a)
        place.amenities = new_amenities
        place.save()  
    place.validate()
    return place
from app.models.review import Review

# ---------- Reviews ----------
def create_review(self, data: dict) -> Review:
    text = (data.get("text") or "").strip()
    rating = data.get("rating")
    user_id = data.get("user_id")
    place_id = data.get("place_id")

    user = self.user_repo.get(user_id)
    if not user:
        raise ValueError("User not found")

    place = self.place_repo.get(place_id)
    if not place:
        raise ValueError("Place not found")

    review = Review(text=text, rating=rating, user=user, place=place)
    review.validate()

    created = self.review_repo.add(review)

    # keep relationship on place (for showing reviews in place output)
    if not hasattr(place, "reviews") or place.reviews is None:
        place.reviews = []
    place.reviews.append(created)
    place.save()

    return created

def get_review(self, review_id: str):
    return self.review_repo.get(review_id)

def list_reviews(self):
    return self.review_repo.get_all()

def update_review(self, review_id: str, data: dict):
    review = self.review_repo.get(review_id)
    if not review:
        return None

    patch = {}
    if "text" in data:
        patch["text"] = (data.get("text") or "").strip()
    if "rating" in data:
        patch["rating"] = data.get("rating")

    review.update(patch)
    review.validate()
    return review

def delete_review(self, review_id: str) -> bool:
    review = self.review_repo.get(review_id)
    if not review:
        return False

    # remove from place.reviews if present
    place = review.place
    if place and hasattr(place, "reviews") and place.reviews:
        place.reviews = [r for r in place.reviews if r.id != review_id]
        place.save()

    return self.review_repo.delete(review_id) or True  # depending on your delete return

def list_reviews_by_place(self, place_id: str):
    place = self.place_repo.get(place_id)
    if not place:
        raise ValueError("Place not found")

    # If we store reviews on place:
    if hasattr(place, "reviews") and place.reviews is not None:
        return place.reviews


    return [r for r in self.review_repo.get_all() if r.place and r.place.id == place_id]


facade = HBnBFacade()
