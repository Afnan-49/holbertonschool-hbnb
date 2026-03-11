from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity # From File-2
from app.services.facade import facade # Foundation from File-1

api = Namespace("users", description="User operations")

# --- Models from File-1 ---
user_input = api.model("UserInput", {
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})

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
    """File-1's ISO serialization logic"""
    return {
        "id": u.id,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "email": u.email,
        "is_admin": u.is_admin,
        "created_at": u.created_at.isoformat() if hasattr(u.created_at, 'isoformat') else u.created_at,
        "updated_at": u.updated_at.isoformat() if hasattr(u.updated_at, 'isoformat') else u.updated_at,
    }

@api.route("/")
class UserList(Resource):

    @api.marshal_list_with(user_output)
    def get(self):
        """Retrieve all users"""
        users = facade.user_repo.get_all()
        return [serialize_user(u) for u in users], 200

    @jwt_required() # Security from File-2
    @api.expect(user_input, validate=True)
    @api.marshal_with(user_output, code=201)
    def post(self):
        """Create a new user (Admin Only)"""
        token_claims = get_jwt()
        if not token_claims.get('is_admin'):
            api.abort(403, "Admin privileges required")

        user_data = request.json or {}
        
        # Email uniqueness check from File-2
        if facade.get_user_by_email(user_data.get('email')):
            api.abort(400, "Email already registered")

        try:
            user = facade.create_user(user_data)
            return serialize_user(user), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route("/<string:user_id>")
class UserItem(Resource):

    @api.marshal_with(user_output)
    def get(self, user_id):
        """Get user details"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return serialize_user(user), 200

    @jwt_required() # Security from File-2
    @api.expect(user_update, validate=True)
    @api.marshal_with(user_output)
    def put(self, user_id):
        """Update user information (Admin or Owner Only)"""
        token_claims = get_jwt()
        is_admin = token_claims.get('is_admin', False)
        current_user_id = get_jwt_identity()

        # Permission Check from File-2: Must be admin OR the user themselves
        if not is_admin and current_user_id != user_id:
            api.abort(403, "Admin privileges required or access denied")

        data = request.json or {}

        # Logic from File-2: Field restrictions for non-admins
        if not is_admin:
            if 'email' in data or 'password' in data or 'is_admin' in data:
                api.abort(400, "You cannot modify email, password, or admin status")
        
        # Email uniqueness check for Admins
        if is_admin and 'email' in data:
            existing_user = facade.get_user_by_email(data['email'])
            if existing_user and existing_user.id != user_id:
                api.abort(400, "Email already in use")

        try:
            user = facade.update_user(user_id, data)
            if not user:
                api.abort(404, "User not found")
            return serialize_user(user), 200
        except ValueError as e:
            api.abort(400, str(e))
