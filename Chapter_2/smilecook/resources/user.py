from xml.dom import ValidationErr
from flask import render_template, request, url_for
from flask_restful import Resource
from http import HTTPStatus
from schemas.user import UserSchema
from utils import hash_password, generate_token, verify_token
from models.user import User
from schemas.user import UserSchema
from flask_jwt_extended import get_jwt_identity, jwt_required
from webargs import fields
from webargs.flaskparser import use_kwargs
from models.recipe import Recipe
from schemas.recipe import RecipeSchema
from mailgun import MailgunApi
import os
from dotenv import load_dotenv

mailgun=MailgunApi(domain= os.getenv('DOMAIN'),
                    api_key=os.getenv('API_KEY'))

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email',))
                                # many=True; show multiple recipes
recipe_list_schema = RecipeSchema(many=True)

def config():
    load_dotenv()



class UserActivateResource(Resource):
    def get(self, token):
        # Verifies the token which will be used to activate the account and checks if it is not expired (default=30 min) 
        # If the token is valid and not expired the user email will be returned and the account activation can proceed.
        email = verify_token(token, salt='activate')
        user = User.get_by_email(email=email)
        if email is False:
            return {'message': 'Invalid token or token expired'}, HTTPStatus.BAD_REQUEST
        if not user:
            return {'message': 'User not found'}, HTTPStatus. NOT_FOUND
        # Updates the is_activate attribute of the object from False --> True
        user.is_active = True
        # Save the changes in the database
        user.save()
        return {}, HTTPStatus.NO_CONTENT

class UserRecipeListResource(Resource):
    @jwt_required(optional=True) # endpoint can be accessed without logging in
    @use_kwargs({'visibility': fields.String(missing='public')},location='query') # Recieve the parameter of visibility (public is default value if not passed) 
    def get(self, username, visibility):
        """ Method to retrieve recipes that are created by a specic username """
        user = User.get_by_username(username = username)
        if user is None:
            return {'message':'User not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility='public'
        recipes = Recipe.get_all_by_user(user_id=user.id, visibility=visibility)
        return recipe_list_schema.dump(recipes), HTTPStatus.OK

class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            data = user_schema.load(data=json_data)

        except ValidationErr as err:
            return {'message': 'Validation errors', 'errors':err}, HTTPStatus.BAD_REQUEST

        # Checks if username and email already exists if so throw a error message
        if User.get_by_username(data.get('username')):
            return {'message':'username already used'}, HTTPStatus.BAD_REQUEST
        
        if User.get_by_email(data.get('email')):
            return {'message':'email already used'}, HTTPStatus.BAD_REQUEST        

        user = User(**data)
        # saves to database
        user.save()
        token = generate_token(user.email, salt='activate')
        subject = 'Please confirm your registration.'
        username = user.username.title()
        link = url_for('useractivateresource', token=token, _external=True)
        # text = f'Hi thanks for using SmileCook! \n Please confirm your registration by clicking on the link: {link}'

        mailgun.send_email(to=user.email,
                            subject=subject,
                            # text=text,
                            html=render_template('email.html', link=link, username=username))

        
        return user_schema.dump(user), HTTPStatus.CREATED

class UserResource(Resource):
    @jwt_required(optional=True)
    def get(self, username):
        user = User.get_by_username(username=username)
        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND
        current_user= get_jwt_identity()
        if current_user == user.id:
            data = user_schema.dump(user)
        else:
            data = user_public_schema.dump(user)
        return data, HTTPStatus.OK
         
class MeResource(Resource):
    @jwt_required()
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())
        return user_schema.dump(user), HTTPStatus.OK

