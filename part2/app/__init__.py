from flask import Flask
from flask_restx import Api

rest_api = Api(title="HBnB API", version="1.0", description="HBnB Application API")

def create_app():
    app = Flask(__name__)
    rest_api.init_app(app)

    # Import the Namespace from users.py
    from app.api.v1.users import ns as users_ns
    rest_api.add_namespace(users_ns, path="/api/v1/users")

    return app