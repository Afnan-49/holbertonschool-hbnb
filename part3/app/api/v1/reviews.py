from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity # From File-2
from app.services.facade import facade # Foundation from File-1

api = Namespace("reviews", description="Review operations")

# --- Models from File-1 ---
review_input = api.model("ReviewInput", {
    "text": fields.String(required=True),
    "rating": fields.Integer(required=True, description="1..5"),
    "user_id": fields.String(required=True),
    "place_id": fields.String(required=True),
})

review_update = api.model("ReviewUpdate", {
    "text": fields.String(required=False),
    "rating": fields.Integer(required=False, description="1..5"),
})

review_output = api.model("Review", {
    "id": fields.String(readOnly=True),
    "text": fields.String,
    "rating": fields.Integer,
    "user_id": fields.String,
    "place_id": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String,
})

def serialize_review(r):
    """File-1's serialization logic"""
    return {
        "id": r.id,
        "text": r.text,
        "rating": r.rating,
        "user_id": r.user_id,
        "place_id": r.place_id,
        "created_at": r.created_at.isoformat() if hasattr(r.created_at, 'isoformat') else r.created_at,
        "updated_at": r.updated_at.isoformat() if hasattr(r.updated_at, 'isoformat') else r.updated_at,
    }

@api.route("/")
class ReviewList(Resource):

    @api.marshal_list_with(review_output)
    def get(self):
        """Retrieve all reviews (Public)"""
        reviews = facade.list_reviews()
        return [serialize_review(r) for r in reviews], 200

    @jwt_required()
    @api.expect(review_input, validate=True)
    @api.marshal_with(review_output, code=201)
    def post(self):
        """Create a new review (Protected with Business Rules)"""
        current_user_id = get_jwt_identity()
        review_data = request.json or {}
        place_id = review_data.get('place_id')

        # Logic from File-2: Validate place and ownership
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        # Rule 1: Cannot review your own place
        if place.owner_id == current_user_id:
            api.abort(400, "You cannot review your own place")

        # Rule 2: One review per place per user
        existing_reviews = facade.list_reviews_by_place(place_id)
        if any(r.user_id == current_user_id for r in existing_reviews):
            api.abort(400, "You have already reviewed this place")

        # Force user_id to be the logged-in user
        review_data['user_id'] = current_user_id

        try:
            review = facade.create_review(review_data)
            return serialize_review(review), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route("/<string:review_id>")
class ReviewItem(Resource):

    @api.marshal_with(review_output)
    def get(self, review_id):
        """Get review details (Public)"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return serialize_review(review), 200

    @jwt_required()
    @api.expect(review_update, validate=True)
    @api.marshal_with(review_output)
    def put(self, review_id):
        """Update a review (Creator or Admin Only)"""
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        current_user_id = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")

        # Security from File-2: Admin bypass or Creator check
        if not is_admin and review.user_id != current_user_id:
            api.abort(403, "Unauthorized action")

        try:
            updated_review = facade.update_review(review_id, request.json or {})
            return serialize_review(updated_place), 200
        except ValueError as e:
            api.abort(400, str(e))

    @jwt_required()
    def delete(self, review_id):
        """Delete a review (Creator or Admin Only)"""
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        current_user_id = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")

        if not is_admin and review.user_id != current_user_id:
            api.abort(403, "Unauthorized action")

        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200

@api.route("/places/<string:place_id>/reviews")
class PlaceReviews(Resource):

    @api.marshal_list_with(review_output)
    def get(self, place_id):
        """List reviews for a specific place"""
        try:
            reviews = facade.list_reviews_by_place(place_id)
            return [serialize_review(r) for r in reviews], 200
        except ValueError as e:
            api.abort(404, str(e))
