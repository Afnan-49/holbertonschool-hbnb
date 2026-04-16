from app import db

# Junction table to handle the many-to-many relationship
place_amenities = db.Table(
    "place_amenities",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"), primary_key=True),
)
