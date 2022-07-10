from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus

from models.recipe import Recipe, recipe_list


class RecipeListResource(Resource):
    """ Getting all the public recipes back"""
    def get(self):
        data = []
        for recipe in recipe_list:
            if recipe.is_publish is True:
                data.append(recipe.data)
        return {'data': data}, HTTPStatus.OK


    def post(self):
        """ Creates a new recipe """
        data = request.get_json()
        recipe = Recipe(name=data['name'],
                 description =data['description'],
                 num_of_servings=data['num_of_servings'],
                 cook_time=data['cook_time'],
                 directions=data['directions'])
        recipe_list.append(recipe)
        print(recipe_list)
        return recipe.data, HTTPStatus.CREATED


class RecipeResource(Resource):
    def get(self, recipe_id):
        """ Retrieves one recipe according to recipe_id """
        recipe = next((recipe for recipe in recipe_list if recipe_id == recipe_id and recipe.is_publish==True), None)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        return recipe.data, HTTPStatus.OK


    def put(self, recipe_id):
        """ Updates the attributes of the recipe """
        # Parses(process of converting) the incoming JSON request data and returns it
        # Takes the incoming JSON object and converts it to a Python object in this case a dictionary
        data = request.get_json()
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        recipe.name = data['name']
        recipe.description  = data['description']
        recipe.num_of_survings = data['num_of_servings']
        recipe.cook_time = data['cook_time']
        recipe.directions = data['directions']
        return recipe.data, HTTPStatus.OK

    def delete(self, recipe_id):
        """ with next() it returns the next item in an iterator;
         Checks if recipe.id is equal to the recipe_id argument if the condition is not True it will return None (end of iterable) """
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id),None)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        else:
            recipe_list.remove(recipe)
            return recipe_id



class RecipePublishResource(Resource):   
    """ Will update the publish status of the recipe """
    def put(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        recipe.is_publish = True
        return {}, HTTPStatus.NO_CONTENT
    
    def delete(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)
        if recipe is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        recipe.is_publish = False
