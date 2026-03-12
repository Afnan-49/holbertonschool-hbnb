from __future__ import annotations
from app import db
from app.models.base_model import BaseModel
from app.models.associations import place_amenities

class Amenity(BaseModel):
    """
    Amenity Model: Represents features available at various places.
    Inherits ID and timestamps from BaseModel.
    """
    __tablename__ = "amenities"

    # Name is unique and indexed for fast lookup during validation/creation
    name = db.Column(db.String(128), nullable=False, unique=True, index=True)
    
    # Many-to-Many relationship with Place
    places = db.relationship(
        "Place",
        secondary=place_amenities,
        back_populates="amenities",
        lazy="subquery",
    )

    def validate(self) -> None:
        """
        Ensures the amenity name is provided and not just whitespace.
        """
        if not self.name or not self.name.strip():
            raise ValueError("Name is required")
