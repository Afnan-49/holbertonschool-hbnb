from flask import Flask
from flask_restx import Api

api = Api(title="HBnB API", version="1.0", description="HBnB Part 2")

def create_app():
    app = Flask(__name__)
    api.init_app(app)

    from app.api.v1.users import ns as users_ns
    from app.api.v1.places import ns as places_ns
    from app.api.v1.amenities import ns as amenities_ns
    from app.api.v1.reviews import ns as reviews_ns
    
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")

    return app