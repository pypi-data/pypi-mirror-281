from flask import Blueprint,jsonify,request
from flask_apispec.views import MethodResource

from flask_apispec import doc, marshal_with, use_kwargs, FlaskApiSpec
from marshmallow import Schema, fields
from flask_restful import Api, Resource

main_bp_2 = Blueprint('main_v2', __name__)
api = Api(main_bp_2)


class UserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)


@doc(tags=[" main - v2"])
class UserAPI(MethodResource, Resource):
    @marshal_with(UserSchema(many=True))
    def get(self):
        users = [{'id': 1, 'username': 'user1', 'email': 'user1@example.com'}]  # Mock data
       
        return users

    @use_kwargs(UserSchema, location='json')
    @marshal_with(UserSchema(many=True))
    def post(self,**kwargs):
        user_data = kwargs  # 获取传入的 JSON 数据
        print("Received user data:", user_data)
        users = [{'id': 1, 'username': 'user1', 'email': 'user1@example.com'}]  # Mock data
        users.append(user_data)
        return users






def register_main_v2(docs):
    api.add_resource(UserAPI, '/main_v2')
    docs.register(UserAPI, blueprint="main_v2")
