# app/persistence/repository.py
from abc import ABC, abstractmethod
from app import db

class Repository(ABC):
    """
    Abstract Base Class for the Repository pattern.
    Ensures all repository implementations follow the same interface.
    """
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class SQLAlchemyRepository(Repository):
    """
    SQLAlchemy-based implementation of the Repository pattern.
    Used for persistent storage in a relational database.
    """
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        """Adds a new object to the database session and commits."""
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        """Retrieves an object by its primary key ID."""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Retrieves all records for the specific model."""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Updates attributes of an existing object based on a dictionary."""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            db.session.commit()
        return obj

    def delete(self, obj_id):
        """Removes an object from the database."""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Finds the first record where a specific attribute matches a value."""
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
