from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade

api = Namespace("users", description="User operations")

user_input = api.model("UserInput", {
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})

# Update (PUT) - optional
user_update = api.model("UserUpdate", {
    "first_name": fields.String(required=False),
    "last_name": fields.String(required=False),
    "email": fields.String(required=False),
    "password": fields.String(required=False),
    "is_admin": fields.Boolean(required=False),
})

user_output = api.model("User", {
    "id": fields.String(readOnly=True),
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
    "is_admin": fields.Boolean,
    "created_at": fields.String,
    "updated_at": fields.String,
})

def serialize_user(u):
    return {
        "id": u.id,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "email": u.email,
        "is_admin": u.is_admin,
        "created_at": u.created_at.isoformat(),
        "updated_at": u.updated_at.isoformat(),
    }

@api.route("/")
class UserList(Resource):

    @api.marshal_list_with(user_output)
    def get(self):
        users = facade.user_repo.get_all()
        return [serialize_user(u) for u in users], 200

    @api.expect(user_input, validate=True)
    @jwt_required()
    def post(self):
        
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        if not is_admin:
            api.abort(403, "Admin privileges required")
            
        try:
            user = facade.create_user(request.json or {})
            return {
                "id": user.id,
                "message": "User registered successfully"
            }, 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route("/<string:user_id>")
class UserItem(Resource):

    @api.marshal_with(user_output)
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return serialize_user(user), 200

    @api.expect(user_update, validate=True)
    @api.marshal_with(user_output)
    @jwt_required()
    def put(self, user_id):
        
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        

        if not is_admin and str(current_user_id) != str(user_id):
            api.abort(403, "Unauthorized action")
            # return {"error": "Unauthorized action"}, 403 --- IGNORE ---

        data = request.json or {}
        
        if not is_admin and str(current_user_id) != str(user_id):
            api.abort(403, "Unauthorized action")

        if not is_admin and ("email" in data or "password" in data):
            api.abort(400, "You cannot modify email or password.")
        if is_admin and "email" in data:
            existing_user = facade.get_user_by_email(data["email"])
            if existing_user and str(existing_user.id) != str(user_id):
                api.abort(400, "Email already in use")
    
        try:
            user = facade.update_user(user_id, request.json or {})
            if not user:
                api.abort(404, "User not found")
            return serialize_user(user), 200
        except ValueError as e:
            api.abort(400, str(e))
