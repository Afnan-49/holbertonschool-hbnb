from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("places", description="Place operations")

place_model = api.model("Place", {
    "id": fields.String(readOnly=True),
    "title": fields.String(required=True),
    "price": fields.Float(required=True),
})


PLACES = []


@api.route("/")
class PlaceList(Resource):

    @api.marshal_list_with(place_model)
    def get(self):
        return PLACES

    @api.expect(place_model)
    @api.marshal_with(place_model, code=201)
    def post(self):
        place = api.payload
        place["id"] = str(len(PLACES) + 1)
        PLACES.append(place)
        return place, 201
