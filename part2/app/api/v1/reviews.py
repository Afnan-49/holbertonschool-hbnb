from flask_restx import Namespace, Resource, fields

api = Namespace("reviews", description="Review operations")

review_model = api.model("Review", {
    "id": fields.String(readOnly=True),
    "text": fields.String(required=True),
    "rating": fields.Integer(required=True),
})


REVIEWS = []


@api.route("/")
class ReviewList(Resource):

    @api.marshal_list_with(review_model)
    def get(self):
        return REVIEWS

    @api.expect(review_model)
    @api.marshal_with(review_model, code=201)
    def post(self):
        review = api.payload
        review["id"] = str(len(REVIEWS) + 1)
        REVIEWS.append(review)
        return review, 201
