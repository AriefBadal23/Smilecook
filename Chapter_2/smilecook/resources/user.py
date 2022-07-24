from flask import request
from flask_restful import Resource
from http import HTTPStatus
from schemas.user import UserSchema
from utils import hash_password
from models.user import User
from schemas.user import UserSchema
from flask_jwt_extended import get_jwt_identity, jwt_required

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email',))


class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()
        data, errors = user_schema.load(data=json_data)
        if errors:
            return {'message': 'Validation errors', 'errors':errors}, HTTPStatus.BAD_REQUEST
  
        # Checks if username and email already exists if so throw a error message
        if User.get_by_username(data.get('username')):
            return {'message':'username already used'}, HTTPStatus.BAD_REQUEST
        
        if User.get_by_email(data.get('email')):
            return {'message':'email already used'}, HTTPStatus.BAD_REQUEST        
        
        user = User(**data)
        # saves to database
        user.save()
        
        return user_schema.dump(user).data, HTTPStatus.CREATED

class UserResource(Resource):
    @jwt_required(optional=True)
    def get(self, username):
        user = User.get_by_username(username=username)
        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND
        current_user= get_jwt_identity()
        if current_user == user.id:
            data = user_schema.dump(user).data
        else:
            data = user_public_schema.dump(user).data
        return data, HTTPStatus.OK
         
class MeResource(Resource):
    @jwt_required()
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())
        
        return user_schema.dump(user).data, HTTPStatus.OK
