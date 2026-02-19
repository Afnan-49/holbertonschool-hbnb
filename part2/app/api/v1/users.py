from flask_restx import Namespace, Resource, fields

api = Namespace("users", description="User operations")

user_model = api.model("User", {
    "id": fields.String(readOnly=True),
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
})


USERS = []


@api.route("/")
class UserList(Resource):

    @api.marshal_list_with(user_model)
    def get(self):
        return USERS

    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        user = api.payload
        user["id"] = str(len(USERS) + 1)
        USERS.append(user)
        return user, 201
