from flask import Blueprint
from flask_apispec.views import MethodResource

from flask_apispec import doc, marshal_with, use_kwargs, FlaskApiSpec
from marshmallow import Schema, fields,validate,ValidationError
from flask_restful import Api, Resource

main_bp_1 = Blueprint('main_v1', __name__)
api = Api(main_bp_1)


class UserSchema(Schema):
    id = fields.Str(dump_only=True,missing=1)
    username = fields.Str()
    email = fields.Str(required=True)
    device_id = fields.Str( description="The ID of the device.",validate=validate.OneOf(["1---", "3", "5"]))

class UserOutPut(Schema):
    message = fields.Str(required=True)


@doc(tags=[" main - v1"])
class UserAPI(MethodResource, Resource):
    @marshal_with(UserSchema(many=True))
    def get(self):
        users = [{'id': 1, 'username': 'user1', 'email': 'user1@example.com'}]  # Mock data
        return users

    @use_kwargs(UserSchema, location='json')
    @marshal_with(UserSchema(many=True))
    def post(self, **kwargs):
        users = [
            {"id": 1, "username": "user1", "email": "user1@example.com"},
            {"id": 2, "username": "user2", "email": "user2@example.com"},
        ]
        return users




def register_main_v1(docs):
    api.add_resource(UserAPI, '/main_v1')
    docs.register(UserAPI, blueprint="main_v1")
