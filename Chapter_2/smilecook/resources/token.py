from http import HTTPStatus
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (create_access_token,
create_refresh_token, get_jwt_identity, jwt_required, get_jwt)
from utils import check_password
from models.user import User

black_list = set()


class TokenResource(Resource):
    """ Generates a access token and refresh token if the user has passed his email and password """
    def post(self):
        json_data = request.get_json()
        email = json_data.get('email')
        password = json_data.get('password')
        user = User.get_by_email(email=email)  
        if not user or not check_password(password, user.password):
            return {'message':'email or password is incorrect'}, HTTPStatus.UNAUTHORIZED

        if user.is_active is False:
            return {'message': 'The user account is not activated yet'}, HTTPStatus.FORBIDDEN

        # if password check passes create a access and refresh token en return HTTPstatus OK
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return {'access_token': access_token,
                'refresh_token': refresh_token}, HTTPStatus.OK


class RefreshResource(Resource):
    # Make the endpoint protected so it requires a refresh token
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()     # generate a access token for the user
        access_token = create_access_token(identity=current_user, fresh=False)
        return {'token':access_token}, HTTPStatus.OK



class RevokeResource(Resource):
    @jwt_required()
    def post(self):
        """ Method to revoke the passed in JWT token """
        jti = get_jwt()['jti']
        black_list.add(jti)
        return {'message': 'Succesfully logged out'}, HTTPStatus.OK