from flask import request
from flask_restful import Resource
from http import HTTPStatus
from utils import hash_password
from models.user import User


class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()
        username = json_data.get('username')
        email = json_data.get('email')
        non_hash_password = json_data.get('password')

        # Checks if username and email already exists if so throw a error message
        if User.get_by_username(username):
            return {'message':'username already used'}, HTTPStatus.BAD_REQUEST
        if User.get_by_email(email):
            return {'message':'email already used'}, HTTPStatus.BAD_REQUEST
        
        password = hash_password(non_hash_password)
        user = User(
            username=username,
            email = email,
            password = password
        )
        # saves to database
        user.save()
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        return data, HTTPStatus.CREATED


        