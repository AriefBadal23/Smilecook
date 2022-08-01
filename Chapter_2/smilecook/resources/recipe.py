from xml.dom import ValidationErr
from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.recipe import Recipe
from flask_jwt_extended import get_jwt_identity, jwt_required
from schemas.recipe import RecipeSchema

# Store a single recipe
recipe_schema = RecipeSchema()
# Store multiple recipes
recipe_list_schema = RecipeSchema(many=True)
# many – Should be set to True if obj is a collection so that the object will be serialized to a list. (JSON/dictionary)

class RecipeListResource(Resource):
    """ Getting all the public recipes back"""
    def get(self):
        recipes = Recipe.get_all_published()
        return recipe_list_schema.dump(recipes), HTTPStatus.OK

    @jwt_required()
    # The method can only be invoked after the user has logged in
    def post(self):
        """ Creates a new recipe """
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
        recipe.num_of_servings = data.get('num_of_servings') or recipe.num_of_servings
        recipe.cook_time = data.get('cook_time') or recipe.cook_time
        recipe.directions = data.get('directions') or recipe.directions
        recipe.save()
        return recipe_schema.dump(recipe), HTTPStatus.OK



    @jwt_required()
    def delete(self, recipe_id):
        """ with next() it returns the next item in an iterator;
         Checks if recipe.id is equal to the recipe_id argument if the condition is not True it will return None (end of iterable) """
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
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        recipe.is_publish = False
        recipe.save()
        return {}, HTTPStatus.NO_CONTENT
