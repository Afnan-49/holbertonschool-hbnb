from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # Relationship: Reference to a User instance
        self.reviews = []   # Relationship: One-to-Many (A place has many reviews)
        self.amenities = [] # Relationship: Many-to-Many (A place has many amenities)

    def add_review(self, review):
        """Link a new review to this place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Link a new amenity to this place"""
        self.amenities.append(amenity)
