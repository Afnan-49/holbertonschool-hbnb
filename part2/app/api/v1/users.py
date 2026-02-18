from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

ns = Namespace("users", description="User operations")

user_input = ns.model("UserInput", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password"),
    "first_name": fields.String(required=False, description="First name"),
    "last_name": fields.String(required=False, description="Last name"),
})

user_update = ns.model("UserUpdate", {
    "email": fields.String(required=False),
    "password": fields.String(required=False),
    "first_name": fields.String(required=False),
    "last_name": fields.String(required=False),
})

user_output = ns.model("UserOutput", {
    "id": fields.String,
    "email": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String,
})

@ns.route("/")
class UsersCollection(Resource):
    # POST is usually provided in guide; included here for completeness
    @ns.expect(user_input, validate=True)
    @ns.marshal_with(user_output, code=201)
    def post(self):
        try:
            user = facade.create_user(ns.payload or {})
            return user.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))

    # ✅ TASK 2: Implement list users
    @ns.marshal_list_with(user_output, code=200)
    def get(self):
        users = facade.list_users()
        return [u.to_dict() for u in users], 200


@ns.route("/<string:user_id>")
class UserItem(Resource):
    # GET by ID is usually provided in guide; included here for completeness
    @ns.marshal_with(user_output, code=200)
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            ns.abort(404, "User not found")
        return user.to_dict(), 200

    # ✅ TASK 2: Implement update user (PUT)
    @ns.expect(user_update, validate=True)
    @ns.marshal_with(user_output, code=200)
    def put(self, user_id):
        try:
            user = facade.update_user(user_id, ns.payload or {})
            if not user:
                ns.abort(404, "User not found")
            return user.to_dict(), 200
        except ValueError as e:
            ns.abort(400, str(e))