from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt  # Added from File-2
from app.services.facade import facade  # Using File-1's Singleton approach

api = Namespace("amenities", description="Amenity operations")

# --- Models from File-1 ---
place_in_amenity = api.model("PlaceInAmenity", {
    "id": fields.String,
    "title": fields.String,
})

amenity_input = api.model("AmenityInput", {
    "name": fields.String(required=True),
})

amenity_output = api.model("Amenity", {
    "id": fields.String(readOnly=True),
    "name": fields.String,
    "places": fields.List(fields.Nested(place_in_amenity)),
    "created_at": fields.String,
    "updated_at": fields.String,
})

def serialize_amenity(a):
    """Helper to ensure consistent output format"""
    return {
        "id": a.id,
        "name": a.name,
        "places": [{"id": p.id, "title": p.title} for p in (a.places or [])],
        "created_at": a.created_at.isoformat() if hasattr(a.created_at, 'isoformat') else a.created_at,
        "updated_at": a.updated_at.isoformat() if hasattr(a.updated_at, 'isoformat') else a.updated_at,        
    }

@api.route("/")
class AmenityList(Resource):

    @api.marshal_list_with(amenity_output)
    def get(self):
        """Retrieve all amenities (Public)"""
        amenities = facade.list_amenities()
        return [serialize_amenity(a) for a in amenities], 200

    @jwt_required()  # Added Security
    @api.expect(amenity_input, validate=True)
    @api.marshal_with(amenity_output, code=201)
    def post(self):
        """Add a new amenity (Admin Only)"""
        # Admin check from File-2
        token_claims = get_jwt()
        if not token_claims.get('is_admin'):
            api.abort(403, "Admin privileges required")

        try:
            amenity = facade.create_amenity(request.json or {})
            return serialize_amenity(amenity), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route("/<string:amenity_id>")
class AmenityItem(Resource):

    @api.marshal_with(amenity_output)
    def get(self, amenity_id):
        """Get amenity details (Public)"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return serialize_amenity(amenity), 200

    @jwt_required()  # Added Security
    @api.expect(amenity_input, validate=True)
    @api.marshal_with(amenity_output)
    def put(self, amenity_id):
        """Update an amenity (Admin Only)"""
        # Admin check from File-2
        token_claims = get_jwt()
        if not token_claims.get('is_admin'):
            api.abort(403, "Admin privileges required")

        try:
            # Note: request.json is used here to match File-1's style over api.payload
            amenity = facade.update_amenity(amenity_id, request.json or {})
            if not amenity:
                api.abort(404, "Amenity not found")
            return serialize_amenity(amenity), 200
        except ValueError as e:
            api.abort(400, str(e))
