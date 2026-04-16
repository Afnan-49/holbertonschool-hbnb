from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize extensions globally
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize Extensions with App Context
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Initialize the Facade and store it in app config
    from app.services.facade import HBnBFacade
    facade = HBnBFacade()
    app.config["FACADE"] = facade

    # Setup API with documentation at the root
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/"
    )

    # Import Namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
        
    # Register Namespaces with standard /api/v1 prefix from File-2
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")

    # --- SEEDING THE ADMIN USER ---
    # We use an app context to ensure the facade can interact with the DB
    with app.app_context():
        try:
            # Check if admin exists before creating to avoid duplicate errors
            if not facade.get_user_by_email("admin@hbnb.com"):
                facade.create_user({
                    "first_name": "Admin",
                    "last_name": "HBnB",
                    "email": "admin@hbnb.com",
                    "password": "adminpassword123",
                    "is_admin": True
                })
        except Exception as e:
            app.logger.info(f"Admin seeding skipped or error: {e}")

    return app
