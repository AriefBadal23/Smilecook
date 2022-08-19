from xml.dom import ValidationErr
from flask import request
from flask_restful import Resource
from http import HTTPStatus
import os
from models.recipe import Recipe
from flask_jwt_extended import get_jwt_identity, jwt_required
from schemas.recipe import RecipeSchema
from extensions import image_set
from utils import save_image
from webargs import fields
from webargs.flaskparser import use_kwargs
from schemas.recipe import RecipeSchema, RecipePaginationSchema

# Store a single recipe
recipe_schema = RecipeSchema()
# Store multiple recipes
# many – Should be set to True if obj is a collection so that the object will be serialized to a list. (JSON/dictionary)
recipe_list_schema = RecipeSchema(many=True)
user_cover_schema = RecipeSchema(only=('recipe_cover_url',))
recipe_pagination_schema = RecipePaginationSchema()

class RecipeListResource(Resource):
    """ Getting all the public recipes back"""
    # Missing = default value when argument is missing
    @use_kwargs({'q':fields.Str(missing=''),
    'page': fields.Int(missing=1),
    'per_page':fields.Int(missing=20),
    'sort': fields.Str(missing='created_at'),
    'order': fields.Str(missing='desc')}, location='query')
    def get(self,q, page, per_page, sort, order,):
        if sort not in ['created_at', 'cook_time', 'num_of_servings', 'ingredients']:
            sort = 'created_at'
        if order not in ['asc', 'desc']:
            order = 'desc'
        paginated_recipes = Recipe.get_all_published(q, page, per_page, sort, order)
        return recipe_pagination_schema.dump(paginated_recipes), HTTPStatus.OK


    @jwt_required()
    def post(self):
        """ Creates a new recipe; only when a user has logged in """
        json_data = request.get_json()
        current_user = get_jwt_identity()
        try:
            data = recipe_schema.load(data=json_data)
        except ValidationErr as err:
            return {'message': "Validation Errors", 'errors': err}, HTTPStatus.BAD_REQUEST
        recipe = Recipe(**data)
        recipe.user_id = current_user
        recipe.save()
        return recipe_schema.dump(recipe), HTTPStatus.CREATED
    
    


class RecipeResource(Resource):
    @jwt_required(optional=True)
    def get(self, recipe_id):
        """ Retrieves one recipe according to recipe_id """
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if recipe.is_publish == False and recipe.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        return recipe_schema.dump(recipe), HTTPStatus.OK

    @jwt_required()
    def patch(self, recipe_id):
        """ Method to modify a particular part of the data of the db """
        json_data = request.get_json()
        # partial= ignore missing fields and not require any fields declared
        try:
            data = recipe_schema.load(data=json_data, partial=('name',))
        except ValidationErr as err:
            return {'message': "Validation Errors", 'errors': err}, HTTPStatus.BAD_REQUEST

        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        
        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message': 'Access not Allowed'}, HTTPStatus.FORBIDDEN

        recipe.name = data.get('name') or recipe.name
        recipe.description = data.get('description') or recipe.description
        recipe.ingredients = data.get('ingredients') or recipe.ingredients
        recipe.num_of_servings = data.get('num_of_servings') or recipe.num_of_servings
        recipe.cook_time = data.get('cook_time') or recipe.cook_time
        recipe.directions = data.get('directions') or recipe.directions
        recipe.save()
        return recipe_schema.dump(recipe), HTTPStatus.OK



    @jwt_required()
    def delete(self, recipe_id):
        """ Method to delete a particular recipe by using the recipe_id """
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        print(current_user)
        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
    
        recipe.delete()
        return {}, HTTPStatus.NO_CONTENT



class RecipePublishResource(Resource):   
    """ Will update the publish status of the recipe """
    @jwt_required()
    def put(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()
        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        recipe.is_publish = True
        recipe.save()
        return {}, HTTPStatus.NO_CONTENT
    
    @jwt_required()
    def delete(self, recipe_id):
        """ Unpublish the recipe from True to False """
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        recipe.is_publish = False
        recipe.save()
        return {}, HTTPStatus.NO_CONTENT


class RecipeCoverUploadResource(Resource):
    @jwt_required()
    def put(self, recipe_id):
        # The file that is selected by the client
        file = request.files.get('cover')

        # Check if the file exists or not and wheter the file extension is permitted
        if not file:
            return {'message': 'Not a valid image'}, HTTPStatus.BAD_REQUEST

        if not image_set.file_allowed(file, file.filename):
            return {'message':'File type not allowed'}, HTTPStatus.BAD_REQUEST

        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        # if the file is null or an empty value return a 404 error
        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        # if the currently logged user is not the same as the user that created the recipe
        # return a Access is not allowed message
        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        # Checks if the cover_image exists if so it will get the currently uploaded filename
        if recipe.cover_image:
            cover_path = image_set.path(folder='recipes', filename=recipe.cover_image)
            # if the filename already exists it will be removed
            if os.path.exists(cover_path):
                os.remove(cover_path)
        # Save the uploaded image in the folder
        filename = save_image(image=file, folder='recipes')
        recipe.cover_image = filename
        # save it in the db
        recipe.save()
        # return the cover_url of the recipe object
        return user_cover_schema.dump(recipe), HTTPStatus.OK

