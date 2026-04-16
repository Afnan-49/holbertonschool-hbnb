from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity # From File-2
from app.services.facade import facade # Foundation from File-1

api = Namespace("places", description="Place operations")

# --- Models from File-1 ---
place_input = api.model("PlaceInput", {
    "title": fields.String(required=True),
    "description": fields.String(required=False),
    "price": fields.Float(required=True),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
    "owner_id": fields.String(required=True),
})

place_update = api.model("PlaceUpdate", {
    "title": fields.String(required=False),
    "description": fields.String(required=False),
    "price": fields.Float(required=False),
    "latitude": fields.Float(required=False),
    "longitude": fields.Float(required=False),
    "owner_id": fields.String(required=False),
})

review_in_place = api.model("ReviewInPlace", {
    "id": fields.String,
    "text": fields.String,
    "rating": fields.Integer,
    "user_id": fields.String,
})

place_output = api.model("PlaceOutput", {
    "id": fields.String(readOnly=True),
    "title": fields.String(required=True),
    "description": fields.String,
    "price": fields.Float(required=True),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
    "owner_id": fields.String(required=True),
    "amenities": fields.List(fields.Raw),
    "created_at": fields.String,
    "updated_at": fields.String,
})

def serialize_place(p):
    """File-1's precise serialization logic"""
    return {
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "price": p.price,
        "latitude": p.latitude,
        "longitude": p.longitude,
        "owner_id": p.owner_id,
        "amenities": [{"id": a.id, "name": a.name} for a in (p.amenities or [])],
        "created_at": p.created_at.isoformat() if hasattr(p.created_at, 'isoformat') else p.created_at,
        "updated_at": p.updated_at.isoformat() if hasattr(p.updated_at, 'isoformat') else p.updated_at,
    }

@api.route("/")
class PlaceList(Resource):

    @api.marshal_list_with(place_output)
    def get(self):
        """Retrieve all places (Public)"""
        places = facade.list_places()
        return [serialize_place(p) for p in places], 200

    @jwt_required()
    @api.expect(place_input, validate=True)
    @api.marshal_with(place_output, code=201)
    def post(self):
        """Create a new place (Protected)"""
        current_user_id = get_jwt_identity()
        place_data = request.json or {}
        
        # Security from File-2: Ensure owner_id matches the logged-in user
        place_data['owner_id'] = current_user_id 
        
        try:
            place = facade.create_place(place_data)
            return serialize_place(place), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route("/<string:place_id>")
class PlaceItem(Resource):

    @api.marshal_with(place_output)
    def get(self, place_id):
        """Get place details (Public)"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return serialize_place(place), 200

    @jwt_required()
    @api.expect(place_update, validate=True)
    @api.marshal_with(place_output)
    def put(self, place_id):
        """Update a place (Owner or Admin Only)"""
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        current_user_id = get_jwt_identity()

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        # Logic from File-2: Admin bypass or Owner check
        if not is_admin and place.owner_id != current_user_id:
            api.abort(403, "Unauthorized action")

        try:
            updated_place = facade.update_place(place_id, request.json or {})
            return serialize_place(updated_place), 200
        except ValueError as e:
            api.abort(400, str(e))

    @jwt_required()
    def delete(self, place_id):
        """Delete a place (Owner or Admin Only)"""
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        current_user_id = get_jwt_identity()

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        if not is_admin and place.owner_id != current_user_id:
            api.abort(403, "Unauthorized action")

        facade.delete_place(place_id)
        return {"message": "Place deleted successfully"}, 200
