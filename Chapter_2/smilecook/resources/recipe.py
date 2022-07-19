from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus
from models.recipe import Recipe
from flask_jwt_extended import get_jwt_identity, jwt_required


class RecipeListResource(Resource):
    """ Getting all the public recipes back"""
    def get(self):
        recipes = Recipe.get_all_published()
        data = []
        for recipe in recipes:
                data.append(recipe.data)
        return {'data': data}, HTTPStatus.OK

    @jwt_required()
    # The method can only be invoked after the user has logged in
    def post(self):
        """ Creates a new recipe """
        json_data = request.get_json()
        current_user = get_jwt_identity()
        recipe = Recipe(name=json_data['name'],
                 description =json_data['description'],
                 num_of_servings=json_data['num_of_servings'],
                 cook_time=json_data['cook_time'],
                 directions=json_data['directions'],
                 user_id = current_user)
        recipe.save()
        return recipe.data(), HTTPStatus.CREATED


class RecipeResource(Resource):
    @jwt_required(optional=True)
    def get(self, recipe_id):
        """ Retrieves one recipe according to recipe_id """
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        print(current_user)
        if recipe.is_publish == False and recipe.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        return recipe.data, HTTPStatus.OK

    @jwt_required()
    def put(self, recipe_id):
        """ Updates the attributes of the recipe """
        # Parses(process of converting) the incoming JSON request data and returns it
        # Takes the incoming JSON object and converts it to a Python object in this case a dictionary (.get_json())
        json_data = request.get_json()
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        print(current_user)
        if current_user != recipe.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        recipe.name = json_data['name']
        recipe.description = json_data['description']
        recipe.num_of_servings = json_data['num_of_servings']
        recipe.cook_time = json_data['cook_time']
        recipe.directions  = json_data['directions ']
        recipe.save()
        return recipe.data, HTTPStatus.OK


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
        else:
            recipe.delete()
            return recipe_id



class RecipePublishResource(Resource):   
    """ Will update the publish status of the recipe """
    def put(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        recipe.is_publish = True
        return {}, HTTPStatus.NO_CONTENT
    
    def delete(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        recipe.is_publish = False
        return {}, HTTPStatus.NO_CONTENT
