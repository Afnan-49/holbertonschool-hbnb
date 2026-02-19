from flask_restx import Namespace, Resource, fields
from flask import current_app

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model("Amenity", {
    "id": fields.String(readOnly=True),
    "name": fields.String(required=True),
})


AMENITIES = []


@api.route("/")
class AmenityList(Resource):

    @api.marshal_list_with(amenity_model)
    def get(self):
        return AMENITIES

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        amenity = api.payload
        amenity["id"] = str(len(AMENITIES) + 1)
        AMENITIES.append(amenity)
        return amenity, 201
