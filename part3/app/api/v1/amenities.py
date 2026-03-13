from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import get_jwt, jwt_required

from app.services.facade import facade  # facade instance (Singleton)

api = Namespace("amenities", description="Amenity operations")
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

})

def serialize_amenity(a):
    return {
        "id": a.id,
        "name": a.name,
        "places": [{"id": p.id, "title": p.title} for p in (a.places or [])],
    }

@api.route("/")
class AmenityList(Resource):

    @api.marshal_list_with(amenity_output)
    def get(self):
        amenities = facade.list_amenities()
        return [serialize_amenity(a) for a in amenities], 200

    @api.expect(amenity_input, validate=True)
    @api.marshal_with(amenity_output, code=201)
    @jwt_required()
    def post(self):
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        
        if not is_admin:
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
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return serialize_amenity(amenity), 200

    @api.expect(amenity_input, validate=True)
    @api.marshal_with(amenity_output)
    @jwt_required()
    def put(self, amenity_id):
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        if not is_admin:
            api.abort(403, "Admin privileges required")
            
        try:
            amenity = facade.update_amenity(amenity_id, request.json or {})
            if not amenity:
                api.abort(404, "Amenity not found")
            return serialize_amenity(amenity), 200
        except ValueError as e:
            api.abort(400, str(e))
