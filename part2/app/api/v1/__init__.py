from flask import Flask
from flask_restx import Api

api = Api(title="HBnB API", version="1.0", description="HBnB Part 2")

def create_app():
    app = Flask(__name__)
    api.init_app(app)

    from app.api.v1.users import ns as users_ns
    api.add_namespace(users_ns, path="/api/v1/users")

    return app