from __future__ import annotations
# ADDED: InMemoryRepository for Amenities/Places, Amenity + Place models
from app.persistence.repository import InMemoryUserRepository, InMemoryRepository 
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

class HBnBFacade:
    def __init__(self) -> None:
        self.users = InMemoryUserRepository()
        # added: new repositories for entities
        self.amenities = InMemoryRepository() 
        self.places = InMemoryRepository()    


    # added: new Amenity management methods
    def create_amenity(self, data: dict) -> Amenity:
        amenity = Amenity(name=data.get("name"))
        self.amenities.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str):
        return self.amenities.get(amenity_id)

    def list_amenities(self):
        return self.amenities.list_all()

    # added: new Place management methods with relationship logic
    def create_place(self, data: dict) -> Place:
        # 1. Validate that the owner exists before creating the place
        owner = self.get_user(data.get("owner_id"))
        if not owner:
            raise ValueError("Owner not found")

        # 2. Initialize the Place object
        place = Place(
            title=data.get("title"),
            description=data.get("description"),
            price=data.get("price"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            owner=owner # Passing the actual User object, not just an ID
        )

        # 3. Fetch Amenity objects by their IDs and link them to the place
        amenity_ids = data.get("amenities", [])
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if amenity:
                place.add_amenity(amenity) # This uses the method we put in place.py

        self.places.add(place)
        return place

    def get_place(self, place_id: str):
        return self.places.get(place_id)

    def list_places(self):
        return self.places.list_all()

    def update_place(self, place_id: str, data: dict):
        place = self.places.get(place_id)
        if not place:
            return None
        
        # Uses the update method from BaseModel to handle the dictionary
        place.update(data) 
        return place

# single shared instance
facade = HBnBFacade()
